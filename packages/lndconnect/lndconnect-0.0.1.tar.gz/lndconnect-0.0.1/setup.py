import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lndconnect",
    version="0.0.1",
    author="Otto Suess",
    author_email="ottosuess@protonmail.com",
    description="Parsing and creating lndconnect links",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LN-Zap/py_lndconnect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
