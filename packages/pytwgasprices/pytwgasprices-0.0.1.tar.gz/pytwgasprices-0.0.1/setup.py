import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytwgasprices",
    version="0.0.1",
    author="Serge45",
    author_email="Serge45497@gmail.com",
    description="A simple package to fetch the latest Taiwan gas prices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Serge45/pytwgasprices",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'bs4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)