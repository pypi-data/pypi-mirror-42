import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.read().splitlines()

all_deps = ["r2c-lib==0.0.2"] + install_requires

setuptools.setup(
    name="r2c-cli",
    version="0.0.3",
    author="R2C",
    author_email="hello@ret2.co",
    description="A CLI for R2C",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ret2.co",
    install_requires=all_deps,
    packages=["r2c", "r2c.cli"],
    include_package_data=True,
    license="Proprietary",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    scripts=["bin/r2c", "bin/r2c.cmd"],
)
