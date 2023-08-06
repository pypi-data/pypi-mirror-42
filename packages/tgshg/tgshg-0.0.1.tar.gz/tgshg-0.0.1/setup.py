import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tgshg",
    version="0.0.1",
    author="tgshg",
    author_email="tgshgworld@gmail.com",
    description="A test small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tgshg/salmo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)