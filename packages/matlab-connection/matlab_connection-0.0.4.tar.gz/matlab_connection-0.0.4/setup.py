import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matlab_connection",
    url="https://github.com/pckosek/matlab_connection",
    version="0.0.4",
    description="Package to streamline reading from and writing data to MATLAB from python",
    long_description=long_description,
    long_description_content_type="text/markdown",    
    author="Paul Kosek",    
    author_email="pckosek@fcps.edu",
    
    packages=setuptools.find_packages(),
    package_data={'matlab_connection': ['./mfiles/*.m']},
    include_package_data=True,
    
    # Dependent packages (distributions)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
    keywords='MATLAB, python' 

)