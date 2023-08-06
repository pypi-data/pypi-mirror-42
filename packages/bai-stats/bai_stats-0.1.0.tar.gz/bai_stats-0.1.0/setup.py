import setuptools



with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bai_stats",
    version="0.1.0",
    author="Sudhir Aithal",
    author_email="aithalsudhir@gmail.com",
    description="Package for statistical analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

