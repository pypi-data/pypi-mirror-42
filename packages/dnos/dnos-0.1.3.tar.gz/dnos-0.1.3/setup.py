import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dnos",
    version="0.1.3",
    author="Adib Rastegarnia",
    author_email="adib.rastegarnia@gmail.com",
    description="Protobuf models for DNOS application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dnosproject/dnos-core-grpc-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
