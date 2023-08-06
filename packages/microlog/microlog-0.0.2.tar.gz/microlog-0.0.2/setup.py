import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="microlog",
    version="0.0.2",
    author="Brian Sacash",
    description="A simple and lightweight logging library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsacash/microlog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
