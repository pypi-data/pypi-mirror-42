import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='racrypt',
    version='0.1',
    author="Rasmart team",
    author_email="rasmarutil@gmail.com",
    description="use c-code crypto in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rasmartguy/racrypt",
    #Update
    packages=['racrypt'],
    package_data={'racrypt': [
        'libra_lib.dylib',
        'libra_lib.so',
        'ra_lib.dll',
    ]},

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)