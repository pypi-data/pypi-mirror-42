import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cta_transit_tracker",
    version="0.0.1",
    author="Carter Halamka",
    description="An asyncronous wrapper over the Chicago Transit Authority Bus Tracker and Train Tracker APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chalamka/cta_transit_tracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)