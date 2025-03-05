import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nftqcd/lgt",
    version="0.1.2",
    author="Sam Foreman",
    author_email="saforem2@gmail.com",
    description=(
        "A package containing a collection of"
        " utilities for Lattice Gauge Theory"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nftqcd/lgt",
    project_urls={
        "Bug Tracker": "https://github.com/nftqcd/lgt/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
