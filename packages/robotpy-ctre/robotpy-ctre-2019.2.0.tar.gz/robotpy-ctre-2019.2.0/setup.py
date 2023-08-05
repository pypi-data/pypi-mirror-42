#
# Much of this copied from https://github.com/pybind/python_example.git
#

import os
from os.path import dirname, exists, join
from setuptools import find_packages, setup, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.sdist import sdist
import shutil
import subprocess
import sys
import setuptools

ctre_lib_version = "5.13.0"

setup_dir = dirname(__file__)
git_dir = join(setup_dir, ".git")
base_package = "ctre"
version_file = join(setup_dir, base_package, "version.py")

# Automatically generate a version.py based on the git version
if exists(git_dir):
    p = subprocess.Popen(
        ["git", "describe", "--tags", "--long", "--dirty=-dirty"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = p.communicate()
    # Make sure the git version has at least one tag
    if err:
        print("Error: You need to create a tag for this repo to use the builder")
        sys.exit(1)

    # Convert git version to PEP440 compliant version
    # - Older versions of pip choke on local identifiers, so we can't include the git commit
    v, commits, local = out.decode("utf-8").rstrip().split("-", 2)
    if commits != "0" or "-dirty" in local:
        v = "%s.post0.dev%s" % (v, commits)

    # Create the version.py file
    with open(version_file, "w") as fp:
        fp.write("# Autogenerated by setup.py\n__version__ = '{0}'".format(v))
        fp.write("\n__ctre_version__ = '%s'" % ctre_lib_version)

if exists(version_file):
    with open(join(setup_dir, base_package, "version.py"), "r") as fp:
        exec(fp.read(), globals())
else:
    __version__ = "master"

with open(join(setup_dir, "README.rst"), "r") as readme_file:
    long_description = readme_file.read()


#
# pybind-specific compilation stuff
#


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
        f.write("int main (int argc, char **argv) { return 0; }")
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.

    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, "-std=c++14"):
        return "-std=c++14"
    elif has_flag(compiler, "-std=c++11"):
        return "-std=c++11"
    else:
        raise RuntimeError(
            "Unsupported compiler -- at least C++11 support " "is needed!"
        )


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""

    c_opts = {"msvc": ["/EHsc"], "unix": []}

    if sys.platform == "darwin":
        c_opts["unix"] += ["-stdlib=libc++", "-mmacosx-version-min=10.7"]

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == "unix":
            opts.append('-DVERSION_INFO="%s"' % ctre_lib_version)
            opts.append("-s")  # strip
            opts.append("-g0")  # remove debug symbols
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, "-fvisibility=hidden"):
                opts.append("-fvisibility=hidden")
        elif ct == "msvc":
            opts.append('/DVERSION_INFO=\\"%s\\"' % ctre_lib_version)
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


install_requires = ["wpilib>=2019.0.0,<2020.0.0"]


class Downloader:
    """
        Utility object to allow lazily retrieving needed artifacts on demand,
        instead of distributing several extra MB with the pypi build.
    """

    def __init__(self):
        self._halsrc = None
        self._ctresrc = None

        self._ctre_devdir = os.environ.get("RPY_CTRE_DEVDIR")
        if self._ctre_devdir:
            # development use only -- preextracted files so it doesn't have
            # to download it over and over again
            # -> if the directory doesn't exist, it will download the current
            #    files to that directory

            self._halsrc = join(self._ctre_devdir, "hal")
            self._ctresrc = join(self._ctre_devdir, "ctre")

    # copy/paste from hal_impl.distutils
    def _download(self, url):
        import atexit
        import posixpath
        from urllib.request import urlretrieve, urlcleanup
        import sys

        print("Downloading", posixpath.basename(url))

        def _reporthook(count, blocksize, totalsize):
            percent = int(count * blocksize * 100 / totalsize)
            sys.stdout.write("\r%02d%%" % percent)
            sys.stdout.flush()

        filename, _ = urlretrieve(url, reporthook=_reporthook)
        atexit.register(urlcleanup)
        return filename

    def _download_and_extract_zip(self, url, to=None):
        import atexit
        import shutil
        import tempfile
        import zipfile

        if to is None:
            # generate temporary directory
            tod = tempfile.TemporaryDirectory()
            to = tod.name
            atexit.register(tod.cleanup)

        zip_fname = self._download(url)
        with zipfile.ZipFile(zip_fname) as z:
            if isinstance(to, str):
                z.extractall(to)
                return to
            else:
                for src, dst in to.items():
                    with z.open(src, "r") as zfp:
                        with open(dst, "wb") as fp:
                            shutil.copyfileobj(zfp, fp)

    @property
    def halsrc(self):
        if not self._halsrc or not exists(self._halsrc):
            import hal_impl.distutils

            self._halsrc = hal_impl.distutils.extract_hal_libs(to=self._halsrc)
        return self._halsrc

    @property
    def ctresrc(self):
        if not self._ctresrc or not exists(self._ctresrc):
            # Download and extract three libs
            base = "http://devsite.ctr-electronics.com/maven/release/com/ctre/phoenix/"
            dirs = [
                "cci/%(version)s/cci-%(version)s-headers.zip",
                "cci/%(version)s/cci-%(version)s-linuxathenastatic.zip",
                "core/%(version)s/core-%(version)s-headers.zip",
            ]

            if self._ctre_devdir:
                dirs.append("api-java/%(version)s/api-java-%(version)s-sources.jar")

            for l in dirs:
                url = base + (l % dict(version=ctre_lib_version))
                self._ctresrc = self._download_and_extract_zip(url, to=self._ctresrc)

        return self._ctresrc


get = Downloader()

_travis_build = os.environ.get("TRAVIS_BUILD")

# Detect roboRIO.. not foolproof, but good enough
if exists("/etc/natinst/share/scs_imagemetadata.ini") or _travis_build:

    # Don't try to link when testing on travis, as it will fail
    # -> We can still catch compile errors, which is good enough I suspect
    if _travis_build:
        libraries = None
    else:
        libraries = ["wpiHal", "CTRE_PhoenixCCI"]

    ext_modules = [
        Extension(
            "ctre._impl.ctre_roborio",
            ["ctre/_impl/ctre_roborio.cpp"],
            include_dirs=[
                # Path to pybind11 headers
                get_pybind_include(),
                get_pybind_include(user=True),
                get.ctresrc,
            ],
            libraries=libraries,
            library_dirs=[
                join(get.halsrc, "linux", "athena", "shared"),
                join(get.ctresrc, "linux", "athena", "static"),
            ],
            language="c++",
        )
    ]

    # This doesn't actually work, as it needs to be installed before setup.py is ran
    # ... but we specify it
    # install_requires = ['pybind11>=1.7']
    install_requires.append("robotpy-hal-roborio>=2019.0.0,<2020.0.0")
    cmdclass = {"build_ext": BuildExt}
else:
    install_requires.append("robotpy-hal-sim>=2019.0.0,<2020.0.0")
    ext_modules = None
    cmdclass = {}

#
# Autogenerating the required CTRE files is something that
# is done at sdist time. This means if you are testing builds,
# you have to run 'setup.py sdist build'.
#
# The advantage of doing it this way is that the autogen files
# are distributed with the pypi package, so simulation users
# don't have to install anything special to build this
#


class SDist(sdist):
    def run(self):
        from header2whatever import batch_convert
        import CppHeaderParser

        CppHeaderParser.ignoreSymbols.append("CCIEXPORT")

        # Do this before deleting the autogen directory, as it may fail
        ctresrc = get.ctresrc

        config_path = join(setup_dir, "gen", "gen.yml")
        outdir = join(setup_dir, "ctre", "_impl", "autogen")

        shutil.rmtree(outdir, ignore_errors=True)

        batch_convert(config_path, outdir, ctresrc)

        with open(join(outdir, "__init__.py"), "w"):
            pass

        super().run()


cmdclass["sdist"] = SDist

if os.environ.get("READTHEDOCS", None) == "True":
    sys.argv.insert(1, "sdist")

setup(
    name="robotpy-ctre",
    version=__version__,
    author="Dustin Spicuzza",
    author_email="dustin@virtualroadside.com",
    url="https://github.com/robotpy/robotpy-ctre",
    description="RobotPy bindings for CTRE third party libraries",
    long_description=long_description,
    packages=find_packages(),
    ext_modules=ext_modules,
    install_requires=install_requires,
    cmdclass=cmdclass,
    zip_safe=False,
    entry_points={
        "robotpylib": ["info = ctre._impl.info:Info"],
        "robotpysim": ["ctre = ctre._impl.sim_ui:CtreUI"],
    },
)
