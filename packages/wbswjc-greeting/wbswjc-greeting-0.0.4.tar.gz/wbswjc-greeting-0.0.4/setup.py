import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wbswjc-greeting",
    version="0.0.4",
    author="wbswjc",
    author_email="me@wujunchao.com",
    description="Just say hi!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wbswjc/python-greeting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
