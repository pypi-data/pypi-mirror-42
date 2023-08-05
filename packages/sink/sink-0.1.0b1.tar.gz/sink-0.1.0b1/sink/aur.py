""" Functions to interact with the AUR """
import sys
import re
from pathlib import Path
from subprocess import check_call, CalledProcessError

import requests

from .const import (
    BUILD_DIR,
    SNAPSHOT_TMPL_URL,
    AUR_PKGBUILD_URL,
    PKGBUILD_DEPS_REGEX,
    PKGBUILD_MAKEDEPS_REGEX,
    EXIT_OK,
    EXIT_ERROR,
    PackageNotFound,
    SinkException,
    ANSWERS_POSITIVE,
    ANSWERS_NEGATIVE,
)
from .package import pkgname_to_package
from .arch import (
    get_installed_packages,
    check_official_repository,
    install_official_package,
    pkgbuild_arrstr_to_list,
)
from .logger import get_logger

log = get_logger('aur') # pylint: disable=invalid-name

def prompt_yes_no(msg):
    """ Prompt a user for a yes/no question """
    while True:
        inp = input(msg).lower()
        if inp in ANSWERS_POSITIVE:
            return True
        elif inp in ANSWERS_NEGATIVE:
            return False

def unpack_snapshot(sfile, pkgname):
    """ Unpack the snapshot """

    cmd = [
        'tar',
        '-xzf',
        str(sfile.resolve()),
        '-C',
        str(BUILD_DIR.resolve())
    ]
    
    log.debug("Running: {}".format(' '.join(cmd)))

    check_call(cmd)

    return BUILD_DIR.joinpath(pkgname)

def makepkg(pkgdir, noconfirm=False):
    """ Run makepkg """

    log.debug("Building package in {}".format(pkgdir))

    cmd = ['makepkg']
    if noconfirm:
        cmd.append('--noconfirm')

    log.debug("Running: {}".format(' '.join(cmd)))

    return check_call(cmd, cwd=pkgdir)

def makepkg_install(pkgdir, noconfirm=False):
    """ Run makepkg """

    log.info("Installing package from {}".format(pkgdir))

    cmd = ['makepkg', '-i']
    if noconfirm:
        cmd.append('--noconfirm')

    log.debug("Running: {}".format(' '.join(cmd)))

    return check_call(cmd, cwd=pkgdir)

def download(pkgname):
    """ Download an AUR snapshot for pkgname """

    log.info("Downloading {}...".format(SNAPSHOT_TMPL_URL.format(pkgname)))

    download_dest = BUILD_DIR.joinpath("{}.tar.gz".format(pkgname))
    cmd = [
        'curl',
        '-s',
        '--output',
        str(download_dest),
        SNAPSHOT_TMPL_URL.format(pkgname),
    ]

    log.debug("Running: {}".format(' '.join(cmd)))

    check_call(cmd)
    return download_dest

def fetch_pkgbuild(pkgname, dep_of=None):
    """ Retreive a PKGBUILD for a specific package """

    resp = requests.get(AUR_PKGBUILD_URL.format(pkgname))
    if resp.status_code == 404:
        msg = "Package {} does not exist"
        if dep_of is not None:
            msg += " (dependency of {})"
            msg = msg.format(pkgname, dep_of)
        else:
            msg = msg.format(pkgname)
        raise PackageNotFound(msg)
    elif resp.status_code != 200:
        raise SinkException("Unknown error from AUR.  Received code {}".format(resp.code))
    else:
        assert resp.status_code == 200

    return resp.content.decode('utf-8')

def fetch_deps(pkgname, dep_of=None):
    """ Get the deps from a pkgbuild """
    pkgbuild = fetch_pkgbuild(pkgname, dep_of)

    deps = []
    make_deps = []
    deps_match = re.search(PKGBUILD_DEPS_REGEX, pkgbuild)
    makedeps_match = re.search(PKGBUILD_MAKEDEPS_REGEX, pkgbuild)

    if not deps_match and not makedeps_match:
        log.debug("Unable to find either depends or makedepends in PKGBUILD")
    else:
        if deps_match:
            deps = pkgbuild_arrstr_to_list(deps_match.group(1))
        if makedeps_match:
            make_deps = pkgbuild_arrstr_to_list(makedeps_match.group(1))
        if len(deps) + len(make_deps) > 0:
            deps = sorted(list(set(deps + make_deps)))

    if len(deps) > 0:
        map(pkgname_to_package, deps)

    return deps

def confirm_pkgbuild(pkgdir):
    """ Display a PKGBUILD from a given dir for the user to review """

    CONFIRM_SUFFIX = '.confirm'
    pkgbuild = pkgdir.joinpath('PKGBUILD')

    if not pkgbuild.is_file():
        raise Exception("PKGBUILD missing")

    # Load PKGBUILD into vim
    try:
        check_call(['vim', '{}'.format(pkgbuild)])
    except CalledProcessError:
        log.debug("vim exited non-zero.")
        return False

    if prompt_yes_no("Continue building PKGBUILD? [y/n] "):
        return True

    return False

def install(pkgname, dep_of=None, skip_install=False, builddir=BUILD_DIR, noconfirm=False):
    """ Install a package from AUR """

    installed = []

    pkg = pkgname_to_package(pkgname)
    if not isinstance(builddir, Path):
        builddir = Path(builddir)

    log.debug("Preparing to install {}...".format(pkgname))

    # Make sure this package isn't already installed
    installed_packages = get_installed_packages()
    if pkg.pkgname in installed_packages:
        log.info("{} already installed.".format(pkgname))
        return [pkg.pkgname]

    # Check the official repos
    has_official_package = check_official_repository(pkg.pkgname)

    # Install the official package, or pretend if skipped
    if has_official_package:
        if skip_install:
            return [pkg.pkgname]
        try:
            return install_official_package(pkg.raw, noconfirm=noconfirm)
        except CalledProcessError:
            log.exception("Error installing package {} from official repository.".format(pkg.pkgname))
            sys.exit(EXIT_ERROR)

    # Dependencies first!
    deps = fetch_deps(pkg.pkgname, dep_of)
    if len(deps) > 0:
        for d in deps:
            installed.extend(install(d,
                                     dep_of=pkg.pkgname,
                                     skip_install=skip_install,
                                     noconfirm=noconfirm))

    # Make sure the temporary directory exists
    builddir.mkdir(mode=0o700, parents=True, exist_ok=True)

    # Download the PKGBUILD
    dest_file = None
    try:
        dest_file = download(pkg.pkgname)
    except CalledProcessError:
        log.exception("Error downloading snapshot for {}".format(pkg.pkgname))
        sys.exit(EXIT_ERROR)

    if not dest_file or not dest_file.exists():
        log.error("Unexpected file missing for {}".format(pkg.pkgname))
        sys.exit(EXIT_ERROR)

    # Extract
    dest_dir = None
    try:
        dest_dir = unpack_snapshot(dest_file, pkg.pkgname)
    except CalledProcessError:
        log.exception("Error extracting snapshot {}".format(dest_file))
        sys.exit(EXIT_ERROR)

    if not dest_dir or not dest_dir.exists():
        log.error("Extracted package missing for {}".format(pkg.pkgname))
        sys.exit(EXIT_ERROR)

    # Confirm the PKGBUILD with the user
    if not noconfirm:
        user_confirmed = confirm_pkgbuild(dest_dir)
        if not user_confirmed:
            log.warn("User declined PKGBUILD for {}".format(pkg.pkgname))
            sys.exit(EXIT_OK)

    # Build
    try:
        makepkg(dest_dir, noconfirm=noconfirm)
    except CalledProcessError:
        log.exception("Error building package {}".format(pkg.pkgname))
        sys.exit(EXIT_ERROR)

    # Install
    if not skip_install:
        try:
            makepkg_install(dest_dir, noconfirm=noconfirm)
        except CalledProcessError:
            log.exception("Error installing {}".format(pkg.pkgname))
            sys.exit(EXIT_ERROR)

    installed.append(pkg.pkgname)

    return installed
