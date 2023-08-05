from distutils.util import convert_path
from distutils import log
from distutils.errors import DistutilsError, DistutilsOptionError
import os
import glob
import io

if "__PEX_UNVENDORED__" in __import__("os").environ:
  from setuptools.extern import six  # vendor:skip
else:
  from pex.third_party.setuptools.extern import six


if "__PEX_UNVENDORED__" in __import__("os").environ:
  from pkg_resources import Distribution, PathMetadata, normalize_path  # vendor:skip
else:
  from pex.third_party.pkg_resources import Distribution, PathMetadata, normalize_path

if "__PEX_UNVENDORED__" in __import__("os").environ:
  from setuptools.command.easy_install import easy_install  # vendor:skip
else:
  from pex.third_party.setuptools.command.easy_install import easy_install

if "__PEX_UNVENDORED__" in __import__("os").environ:
  from setuptools import namespaces  # vendor:skip
else:
  from pex.third_party.setuptools import namespaces

if "__PEX_UNVENDORED__" in __import__("os").environ:
  import setuptools  # vendor:skip
else:
  import pex.third_party.setuptools as setuptools


__metaclass__ = type


class develop(namespaces.DevelopInstaller, easy_install):
    """Set up package for development"""

    description = "install package in 'development mode'"

    user_options = easy_install.user_options + [
        ("uninstall", "u", "Uninstall this source package"),
        ("egg-path=", None, "Set the path to be used in the .egg-link file"),
    ]

    boolean_options = easy_install.boolean_options + ['uninstall']

    command_consumes_arguments = False  # override base

    def run(self):
        if self.uninstall:
            self.multi_version = True
            self.uninstall_link()
            self.uninstall_namespaces()
        else:
            self.install_for_development()
        self.warn_deprecated_options()

    def initialize_options(self):
        self.uninstall = None
        self.egg_path = None
        easy_install.initialize_options(self)
        self.setup_path = None
        self.always_copy_from = '.'  # always copy eggs installed in curdir

    def finalize_options(self):
        ei = self.get_finalized_command("egg_info")
        if ei.broken_egg_info:
            template = "Please rename %r to %r before using 'develop'"
            args = ei.egg_info, ei.broken_egg_info
            raise DistutilsError(template % args)
        self.args = [ei.egg_name]

        easy_install.finalize_options(self)
        self.expand_basedirs()
        self.expand_dirs()
        # pick up setup-dir .egg files only: no .egg-info
        self.package_index.scan(glob.glob('*.egg'))

        egg_link_fn = ei.egg_name + '.egg-link'
        self.egg_link = os.path.join(self.install_dir, egg_link_fn)
        self.egg_base = ei.egg_base
        if self.egg_path is None:
            self.egg_path = os.path.abspath(ei.egg_base)

        target = normalize_path(self.egg_base)
        egg_path = normalize_path(os.path.join(self.install_dir,
                                               self.egg_path))
        if egg_path != target:
            raise DistutilsOptionError(
                "--egg-path must be a relative path from the install"
                " directory to " + target
            )

        # Make a distribution for the package's source
        self.dist = Distribution(
            target,
            PathMetadata(target, os.path.abspath(ei.egg_info)),
            project_name=ei.egg_name
        )

        self.setup_path = self._resolve_setup_path(
            self.egg_base,
            self.install_dir,
            self.egg_path,
        )

    @staticmethod
    def _resolve_setup_path(egg_base, install_dir, egg_path):
        """
        Generate a path from egg_base back to '.' where the
        setup script resides and ensure that path points to the
        setup path from $install_dir/$egg_path.
        """
        path_to_setup = egg_base.replace(os.sep, '/').rstrip('/')
        if path_to_setup != os.curdir:
            path_to_setup = '../' * (path_to_setup.count('/') + 1)
        resolved = normalize_path(
            os.path.join(install_dir, egg_path, path_to_setup)
        )
        if resolved != normalize_path(os.curdir):
            raise DistutilsOptionError(
                "Can't get a consistent path to setup script from"
                " installation directory", resolved, normalize_path(os.curdir))
        return path_to_setup

    def install_for_development(self):
        if six.PY3 and getattr(self.distribution, 'use_2to3', False):
            # If we run 2to3 we can not do this inplace:

            # Ensure metadata is up-to-date
            self.reinitialize_command('build_py', inplace=0)
            self.run_command('build_py')
            bpy_cmd = self.get_finalized_command("build_py")
            build_path = normalize_path(bpy_cmd.build_lib)

            # Build extensions
            self.reinitialize_command('egg_info', egg_base=build_path)
            self.run_command('egg_info')

            self.reinitialize_command('build_ext', inplace=0)
            self.run_command('build_ext')

            # Fixup egg-link and easy-install.pth
            ei_cmd = self.get_finalized_command("egg_info")
            self.egg_path = build_path
            self.dist.location = build_path
            # XXX
            self.dist._provider = PathMetadata(build_path, ei_cmd.egg_info)
        else:
            # Without 2to3 inplace works fine:
            self.run_command('egg_info')

            # Build extensions in-place
            self.reinitialize_command('build_ext', inplace=1)
            self.run_command('build_ext')

        self.install_site_py()  # ensure that target dir is site-safe
        if setuptools.bootstrap_install_from:
            self.easy_install(setuptools.bootstrap_install_from)
            setuptools.bootstrap_install_from = None

        self.install_namespaces()

        # create an .egg-link in the installation dir, pointing to our egg
        log.info("Creating %s (link to %s)", self.egg_link, self.egg_base)
        if not self.dry_run:
            with open(self.egg_link, "w") as f:
                f.write(self.egg_path + "\n" + self.setup_path)
        # postprocess the installed distro, fixing up .pth, installing scripts,
        # and handling requirements
        self.process_distribution(None, self.dist, not self.no_deps)

    def uninstall_link(self):
        if os.path.exists(self.egg_link):
            log.info("Removing %s (link to %s)", self.egg_link, self.egg_base)
            egg_link_file = open(self.egg_link)
            contents = [line.rstrip() for line in egg_link_file]
            egg_link_file.close()
            if contents not in ([self.egg_path],
                                [self.egg_path, self.setup_path]):
                log.warn("Link points to %s: uninstall aborted", contents)
                return
            if not self.dry_run:
                os.unlink(self.egg_link)
        if not self.dry_run:
            self.update_pth(self.dist)  # remove any .pth link to us
        if self.distribution.scripts:
            # XXX should also check for entry point scripts!
            log.warn("Note: you must uninstall or replace scripts manually!")

    def install_egg_scripts(self, dist):
        if dist is not self.dist:
            # Installing a dependency, so fall back to normal behavior
            return easy_install.install_egg_scripts(self, dist)

        # create wrapper scripts in the script dir, pointing to dist.scripts

        # new-style...
        self.install_wrapper_scripts(dist)

        # ...and old-style
        for script_name in self.distribution.scripts or []:
            script_path = os.path.abspath(convert_path(script_name))
            script_name = os.path.basename(script_path)
            with io.open(script_path) as strm:
                script_text = strm.read()
            self.install_script(dist, script_name, script_text, script_path)

    def install_wrapper_scripts(self, dist):
        dist = VersionlessRequirement(dist)
        return easy_install.install_wrapper_scripts(self, dist)


class VersionlessRequirement:
    """
    Adapt a pkg_resources.Distribution to simply return the project
    name as the 'requirement' so that scripts will work across
    multiple versions.

    >>> dist = Distribution(project_name='foo', version='1.0')
    >>> str(dist.as_requirement())
    'foo==1.0'
    >>> adapted_dist = VersionlessRequirement(dist)
    >>> str(adapted_dist.as_requirement())
    'foo'
    """

    def __init__(self, dist):
        self.__dist = dist

    def __getattr__(self, name):
        return getattr(self.__dist, name)

    def as_requirement(self):
        return self.project_name
