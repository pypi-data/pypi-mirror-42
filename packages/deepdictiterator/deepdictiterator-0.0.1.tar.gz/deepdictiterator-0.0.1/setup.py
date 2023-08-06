import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepdictiterator",
    version="0.0.1",
    author="Pavel Borisov",
    author_email="pzinin@gmail.com",
    description="Iterates through deep dictionaries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pashazz/deepdictiterator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
)