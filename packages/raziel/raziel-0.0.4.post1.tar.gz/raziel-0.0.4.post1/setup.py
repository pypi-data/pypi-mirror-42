import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raziel",
    version="0.0.4-1",
    author="Janos Borst",
    author_email="borst@informatik.uni-leipzig.de",
    url="https://git.informatik.uni-leipzig.de/mai13ivw/raziel",
    description="A Data Transformation helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(), #['ptagger','ptagger.plugins'],#
    install_requires = ["allennlp", "flair", "numpy", "keras", "tqdm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
