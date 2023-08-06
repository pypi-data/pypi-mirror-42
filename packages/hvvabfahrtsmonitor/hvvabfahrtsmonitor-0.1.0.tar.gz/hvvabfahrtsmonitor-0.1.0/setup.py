import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hvvabfahrtsmonitor",
    version="0.1.0",
    author="Manuel Catu",
    author_email="m.cantu.reinhard@gmail.com",
    description="Do requests to the hvv abfahrtsmonitor and get parsed data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcantureinhard/hvvabfahrtsmonitor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
