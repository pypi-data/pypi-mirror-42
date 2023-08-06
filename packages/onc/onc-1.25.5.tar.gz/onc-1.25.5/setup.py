import setuptools

buildVersion = "1.25.5"

print('setup.py has build version: ' + buildVersion + '. Make sure this is the version you want to upload.')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onc",
    version=buildVersion,
    author="Ryan Ross, Allan Rempel, Dany Cabrera",
    author_email="dcabrera@uvic.ca",
    description="Ocean 2.0 API Python Client Library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
	url='https://wiki.oceannetworks.ca/display/O2A/Python+Client+Library',
    packages=setuptools.find_packages(),
	install_requires=['requests', 'python-dateutil', 'numpy', 'puremagic'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)