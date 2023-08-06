import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cjdropshipping",
    version="0.0.1",
    author="liuvae",
    author_email="liuvae820@gmail.com",
    description="api for cjdropshipping-python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuvae820/cjdropshipping-python3.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)