import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyApiManager",
    version="0.0.6",
    author="Brian Pierre-Emmanuel & BESEVIC Ivan",
    author_email="pebrian@outlook.fr",
    description="This is a usefull api manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pebbrian/PyApiManager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'requests',
    ],
)
