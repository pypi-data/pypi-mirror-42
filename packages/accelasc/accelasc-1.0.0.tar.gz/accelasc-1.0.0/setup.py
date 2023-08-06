import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='accelasc',
    version='1.0.0',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='implementation of accel_asc algorithm for integer partitions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/accelasc.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
