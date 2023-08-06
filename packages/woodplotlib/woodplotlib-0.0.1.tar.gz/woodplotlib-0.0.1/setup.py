import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="woodplotlib",
    version="0.0.1",
    author="David Roundy",
    author_email="daveroundy@gmail.com",
    description="A package for creating woodworking designs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daveroundy/woodplotlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
