#!/bin/env python
""" Download and install packages from AUR """
import sys
import argparse
from .logger import get_logger, set_debug_logging
from .const import (
    WARNING_BANNER,
    BUILD_DIR,
    EXIT_CANCELLED,
)
from .package import pkgname_to_package
from .aur import install

log = get_logger('cli') # pylint: disable=invalid-name

def main():
    """ CLI entry point function """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pkgname', metavar='PKGNAME', type=str, nargs='+',
                        help='Packages to install from AUR')
    parser.add_argument('-i', '--install', action='store_true', default=False,
                        help="Install the package, don't just download and unpack")
    parser.add_argument('-d', '--dir', type=str, default=None,
                        help="Use this directory to build")
    parser.add_argument('-y', '--noconfirm', action='store_true', default=False,
                        help="Do not confirm before installing packages, and do not review PKGBUILDs. NOT RECOMMENDED")
    parser.add_argument('--debug', action='store_true', default=False,
                        help="Show debug messages")

    args = parser.parse_args()

    if args.debug:
        set_debug_logging()

    if args.install and not args.noconfirm:

        for ln in WARNING_BANNER:
            print(ln)

        confirm = input().lower()

        if confirm != 'y':
            log.warning("User cancelled", file=sys.stderr)
            sys.exit(EXIT_CANCELLED)

    builddir = args.dir or BUILD_DIR
    for pkg in args.pkgname:
        installed = install(pkgname_to_package(pkg),
                            skip_install=(not args.install),
                            builddir=builddir,
                            noconfirm=args.noconfirm)

    log.info("Sucsessfully installed/built these pakcages: {}".format(' '.join(installed)))

if __name__ == '__main__':
    main()
