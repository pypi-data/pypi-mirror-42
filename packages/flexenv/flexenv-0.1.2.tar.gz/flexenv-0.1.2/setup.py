import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flexenv",
    version="0.1.2",
    author="Jimmy He",
    author_email="jimmy.xrail@me.com",
    description="an environ-compatible tool for reading config as envvars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WaggleNet/flexenv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyyaml'
    ]
)
