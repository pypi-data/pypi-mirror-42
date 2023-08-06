import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pulathisi",
    version="0.0.8",
    author="Dewmal Nilanka",
    author_email="dewmal@egreen.io",
    description="Brain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dewmal/pybrain",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)