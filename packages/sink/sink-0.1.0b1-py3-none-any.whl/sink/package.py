""" Package object and related """
import re
import semantic_version
from .const import PKGBUILD_DEP_W_VERSION

# pylint: disable=too-few-public-methods
class Package:
    """ Package object that handles all the weirdness

        ref: https://wiki.archlinux.org/index.php/PKGBUILD#depends
    """
    def __init__(self, pkgname):
        self.raw = pkgname
        self.spec = None
        self.pkgname = self._parse_pkgname(pkgname)

    def __repr__(self):
        return self.raw

    def _parse_pkgname(self, pkgname):
        """ Parse the given package name """

        # Not allowed in PKGBUILD
        assert not ('>' in pkgname and '<' in pkgname), "PKGBUILD dep format is invalid for {}".format(pkgname)

        parsed = re.match(PKGBUILD_DEP_W_VERSION, pkgname)

        # Assume it's just a package name if it doesn't parse out
        if not parsed or not parsed.group(2):
            self.pkgname = pkgname
        else:
            self.pkgname = parsed.group(1)
            # Set the version spec if we need to
            self.spec = semantic_version.Spec(parsed.group(2))

        return self.pkgname


def pkgname_to_package(pkgname):
    """ Convert a plain pkgname string to a Package object """
    if isinstance(pkgname, Package):
        return pkgname
    return Package(pkgname)
