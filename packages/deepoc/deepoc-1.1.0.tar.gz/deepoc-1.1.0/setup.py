import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepoc",
    version="1.1.0",
    author="Tu Vu",
    author_email="tvu@ebi.ac.uk",
    description="A machine learning tool to classify complex datasets based on ontologies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/biomodels/deepoc",
    packages=setuptools.find_packages(),
    install_requires=[
        "tensorflow",
        "obonet",
        "networkx"
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
