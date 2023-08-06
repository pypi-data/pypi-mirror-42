import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyLidar2",
    python_requires="<=2.7.15",
    version="1.1",
    author="Lakshman mallidi",
    author_email="lakshman.mallidi@gmail.com",
    description="Library for Lidar. Currently supports YdLidar from http://www.ydlidar.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lakshmanmallidi/YdLidar.git",
    packages=['PyLidar2'],
    install_requires=[
        'pyserial',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
   
