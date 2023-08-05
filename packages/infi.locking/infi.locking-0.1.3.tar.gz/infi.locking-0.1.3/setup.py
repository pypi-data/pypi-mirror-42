
SETUP_INFO = dict(
    name = 'infi.locking',
    version = '0.1.3',
    author = 'Arnon Yaari',
    author_email = 'arnony@infinidat.com',

    url = 'https://git.infinidat.com/host-opensource/infi.locking',
    license = 'PSF',
    description = """infi.locking module""",
    long_description = """infi.locking is a modlue used to manage lock files in the Linux enviroment""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'setuptools',
'infi.pyutils',
'lockfile'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

