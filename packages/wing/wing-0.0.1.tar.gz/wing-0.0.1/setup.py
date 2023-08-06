import setuptools

with open("README.md", "r") as fh: 
    long_description = fh.read()

setuptools.setup(
    name="wing",
    version="0.0.1",
    author="Tom Roth", 
    author_email="tom.roth@live.com.au", 
    description="Data science utils to help you wing it", 
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/puzzler10/wing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

