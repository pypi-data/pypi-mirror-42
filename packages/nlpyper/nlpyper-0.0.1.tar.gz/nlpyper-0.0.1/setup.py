import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlpyper",
    version="0.0.1",
    author="Zuhaitz Beloki",
    author_email="zbeloki@gmail.com",
    description="A tiny framework to create NLP pipelines in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zbeloki/nlpyper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
