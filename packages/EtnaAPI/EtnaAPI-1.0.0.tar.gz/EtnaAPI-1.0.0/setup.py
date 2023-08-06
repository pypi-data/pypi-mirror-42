import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "EtnaAPI",
    version = "1.0.0",
    author = "Clément Doumergue",
    author_email = "doumer_c@etna-alternance.net",
    description = "Python wrapper to make calls to the Etna's API",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/etna-alternance/EtnaAPI",
    packages = setuptools.find_packages(),
    install_requires = [
        "requests",
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
