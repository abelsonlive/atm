from setuptools import setup, find_packages

setup(
    name = 'atm',
    version = '0.0.8',
    description = "",
    long_description = "",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    keywords = 'Scraping, Caching, Requests',
    author = 'Brian Abelson',
    author_email = 'brianabelson@gmail.com',
    url = 'http://github.com/abelsonlive/atm',
    license = 'MIT',
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages = [],
    include_package_data = False,
    zip_safe = False,
    install_requires = [
        "boto",
        "requests"
    ],
    tests_require = []
)