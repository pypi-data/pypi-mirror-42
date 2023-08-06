import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepoc",
    version="0.0.2",
    author="Tu Vu",
    author_email="tvu@ebi.ac.uk",
    description="A machine learning tool to classify complex datasets based on ontologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/biomodels/deepoc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)