import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiinterface",
    version="0.0.1",
    author="oguzhan",
    author_email="oguzhan_687@hotmail.com",
    description="makine öğrenimi denemesi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oguz687/netinterface",
    packages=setuptools.find_packages(),
    scripts=["yapayzekacore.py","otom.py","otomasyondb.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)