import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="serflag",
    version="0.0.1",
    author="Pavel Borisov",
    author_email="pzinin@gmaill.com",
    description="Serializes flags to lists of strings with special values for ALL and NONE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pashazz/serflag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
)