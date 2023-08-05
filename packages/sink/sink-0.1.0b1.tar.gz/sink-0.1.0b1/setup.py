""" setuptools installation configuration """
import setuptools
import sink

setuptools.setup(
    name='sink',
    version=sink.__version__,
    description='Arch Linux AUR installer for the lazy',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',
    author=sink.__author__,
    author_email=sink.__email__,
    url='http://github.com/mikeshultz/sink',
    packages=['sink'],
    data_files=['README.md'],
    install_requires=[
        'coloredlogs>=10.0',
        'requests>=2.20.0',
        'semantic-version>=2.6.0'
    ],
    extras_require={
        'dev': ['wheel>=0.32.3', 'twine>=1.12.1'],
    },
    license=sink.__license__,
    zip_safe=False,
    keywords='archlinux aur installer',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],
    entry_points={
        'console_scripts': ['sink=sink.cli:main'],
    }
)
