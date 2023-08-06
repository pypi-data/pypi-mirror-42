import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doc_trans",
    version="0.0.2",
    author="sergey-sy",
    author_email="maiyashik@gmail.com",
    description="Translate documentation from Python objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sergey-sy/doc_trans",
    scripts=["bin/doc_trans"],
    keywords=["documentation",
              "translate documentation",
              "yandex translator"],
    packages=setuptools.find_packages(),
    install_requires=['y_trans'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
