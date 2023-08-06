import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getIOU",
    version="0.0.1",
    author="Ben Jafek",
    author_email="jafek91@gmail.com",
    description="This package computes the IOU between boxes for a variety of different bounding box formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jafekb/getIOU",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)