import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="castyllo",
    version="0.0.1dev",
    author="Brian Kiefer",
    auther_email="bkief22@gmail.com",
    description="A testing package for Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkief/castyllo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)