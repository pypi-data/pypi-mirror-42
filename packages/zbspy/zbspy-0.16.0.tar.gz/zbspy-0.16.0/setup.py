import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zbspy",
    version="0.16.0",
    author="James Hitchcock",
    author_email="james@0bsnetwork.com",
    description="Python Library for Interacting with the 0bsnetwork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0bsnetwork/ZbsPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)