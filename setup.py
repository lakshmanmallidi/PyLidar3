import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyLidar3",
    python_requires=">=3.4",
    version="1.6",
    author="Lakshman mallidi",
    author_email="lakshman.mallidi@gmail.com",
    description="Library for Lidar. Currently supports YdLidar(X4,G4) from http://www.ydlidar.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lakshmanmallidi/PyLidar3",
    packages=['PyLidar3'],
    install_requires=[
        'pyserial',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
   
