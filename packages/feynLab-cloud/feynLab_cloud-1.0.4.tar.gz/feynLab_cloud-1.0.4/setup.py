import setuptools
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feynLab_cloud",
    version="1.0.4",
    author="FeynLab Technology, Inc.",
    author_email="social@feynlab.io",
    description="Python Library for FeynLab Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.feynlab.io/feynlab-cloud/supported-devices/raspberry-pi",
    packages= setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
