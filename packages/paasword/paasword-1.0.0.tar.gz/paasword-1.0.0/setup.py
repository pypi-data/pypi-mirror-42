import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paasword",
    version="1.0.0",
    author="Gilad Soffer",
    author_email="paasword.cto@gmail.com",
    description="Paas-Word authentication for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.paas-word.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)