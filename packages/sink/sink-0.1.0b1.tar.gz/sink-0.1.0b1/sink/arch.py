""" Functions for Arch Linux functionality """
from subprocess import check_call, check_output, CalledProcessError
from .logger import get_logger

log = get_logger('arch') # pylint: disable=invalid-name

def pkgbuild_arrstr_to_list(s):
    """ Remove any redundant whitespace, quotes, and return a list """
    s = s.replace("'", '')
    s = s.replace('"', '')
    s = s.replace('\t', ' ')
    s = s.replace('\n', ' ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.split(' ')

def get_installed_packages():
    """ Leverage pacman to get installed packages """

    package_strings = check_output([
        'pacman',
        '-Q',
    ],
                                   universal_newlines=True)

    installed = []
    for pkg in package_strings.split('\n'):
        installed.append(pkg.split(' ')[0])
    return installed

def check_official_repository(pkgname):
    """ Check for an official package """
    log.info("checking the official repository for {}".format(pkgname))
    try:
        cmd = [
            'pacman',
            '-Ssq',
            '^{}$'.format(pkgname),
        ]
        log.debug("Running: {}".format(' '.join(cmd)))
        check_call(cmd)
        return True
    except CalledProcessError:
        return False

def install_official_package(pkgname, noconfirm=False):
    """ Use pacman to install a package from the official repos """

    cmd = [
        'sudo',
        'pacman',
        '-S',
    ]

    if noconfirm:
        cmd.append('--noconfirm')

    cmd.append(pkgname)

    log.debug("Running: {}".format(' '.join(cmd)))

    check_call(cmd)

    return [pkgname]
