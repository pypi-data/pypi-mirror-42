# Sink

Arch Linux AUR installer for the lazy.  You probably shouldn't use this.  AUR 
packages are horribly insecure and each `PKGBUILD` should be individually 
reviewed.

    usage: sink [-h] [-i] [-d DIR] [-y] [--debug] PKGNAME [PKGNAME ...]

    Download and install packages from AUR

    positional arguments:
      PKGNAME            Packages to install from AUR

    optional arguments:
      -h, --help         show this help message and exit
      -i, --install      Install the package, don't just download and unpack
      -d DIR, --dir DIR  Use this directory to build
      -y, --noconfirm    Do not confirm before installing packages.
      --debug            Show debug messages
  