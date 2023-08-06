import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aimlufotech",
    version="0.0.2",
    author="Ufotech",
    author_email="juanpestana96@gmail.com",
    description="AIML Package with special functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ufotech/aiml-ufotech.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
