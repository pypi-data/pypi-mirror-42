""" Various defs of things like constants and exceptions """
from datetime import datetime
from pathlib import Path

# URL Templates
AUR_TMPL_URL = "https://aur.archlinux.org/packages/{}/"
AUR_PKGBUILD_URL = "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h={}"
SNAPSHOT_TMPL_URL = "https://aur.archlinux.org/cgit/aur.git/snapshot/{}.tar.gz"

# Paths
TMP_DIR = Path("/tmp/.sink-{}".format(datetime.now().isoformat().replace(':', '').replace('.', '')))
BUILD_DIR = TMP_DIR.joinpath("build")

WARNING_BANNER = [
    "========================THIS IS A DANGEROUS ACTION========================",
    "AUR Packages are user-generated and can not be trusted. It's also a good",
    "idea to make sure your system is up to date first as some packages may be",
    "looking for the most up to date libraries when building."
    "",
    "Are you sure you want to proceed? [y,N]",
]

# Exit codes
EXIT_OK = 0
EXIT_CANCELLED = 2
EXIT_ERROR = 3

# Regex for yo butts
PKGBUILD_DEPS_REGEX = r'depends\=\(([\w\d\s\-\>\<\=\.\n\'\"]+)\)'
PKGBUILD_MAKEDEPS_REGEX = r'makedepends\=\(([\w\d\s\-\>\<\=\.\n\'\"]+)\)'
PKGBUILD_DEP_W_VERSION = r'^([\w\d\-]+)([\>\<\=\d\-\.]*)$'

# Possible useful answers to a yes/no prompt
ANSWERS_POSITIVE = ['y', 'ye', 'yes']
ANSWERS_NEGATIVE = ['n', 'no', 'negatory']

# Exceptions
class SinkException(Exception): pass # pylint: disable=missing-docstring,multiple-statements
class PackageNotFound(SinkException): pass # pylint: disable=missing-docstring,multiple-statements
