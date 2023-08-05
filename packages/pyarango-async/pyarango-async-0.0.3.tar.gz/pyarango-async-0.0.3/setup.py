import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyarango-async",
    version="0.0.3",
    author="MJR",
    author_email="rafiei_mohamad@ymail.com",
    description="A simple arango driver for python async codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JRafiei/pyarango-async",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp',
        'async_timeout',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
