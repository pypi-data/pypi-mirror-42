from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="event-gateway-sdk",
    version="1.1.0",
    author="Johann BICH",
    author_email="johannbich@gmail.com",
    description="Event Gateway Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kalote/event-gateway-sdk",
    packages=find_packages(exclude=('tests')),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
