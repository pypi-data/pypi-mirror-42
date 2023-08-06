import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="szgo",
    version="0.0.29",
    author="Chenpingling",
    author_email="chenpingling@protonmail.com",
    description="Computer Go Board Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twoutlook/szgo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
