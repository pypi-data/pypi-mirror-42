import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basictable",
    version="1.0.1",
    author="Rich Kelley",
    author_email="rk5devmail@gmail.com",
    description="A small library to print structured data tables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rich5/basictable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

