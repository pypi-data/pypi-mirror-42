import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rescue-api",
    version="1.0.0",
    author="Matthew Jorgensen",
    author_email="matthew@jrgnsn.net",
    description="A Python wrapper for the RescueTime API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.sr.ht/~mjorgensen/spark",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)