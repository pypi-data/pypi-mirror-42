# Sink

Arch Linux AUR installer for the lazy.  Probably still a little buggy.  Please report any issues in
the GitHub issue tracker.

    usage: sink [-h] [-i] [-d DIR] [-y] [--debug] PKGNAME [PKGNAME ...]

    Download and install packages from AUR

    positional arguments:
      PKGNAME            Packages to install from AUR

    optional arguments:
      -h, --help         show this help message and exit
      -i, --install      Install the package, don't just download and unpack
      -d DIR, --dir DIR  Use this directory to build
      -y, --noconfirm    Do not confirm before installing packages, and do not review PKGBUILDs  NOT RECOMMENDED
      --debug            Show debug messages
  