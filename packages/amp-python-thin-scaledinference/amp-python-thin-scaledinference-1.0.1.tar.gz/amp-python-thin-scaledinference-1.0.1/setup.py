import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amp-python-thin-scaledinference",
    version="1.0.1",
    author="Scaled Inference",
    author_email="dev.opera@scaledinference.com",
    description="Amp Python Thin Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScaledInference/amp-python-thin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
