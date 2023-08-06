import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thewhitetools",
    version="0.0.1",
    author="Enrique Blanco Carmona",
    author_email="enblacar1996@gmail.com",
    description="A collection of functions and classes that come in handy for bioinformaticians.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enblacar/thewhitetools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
