import re
import setuptools
import sys

with open("README.md", "r") as fd:
    long_description = fd.read()

prereqs = ['bombfuse', 'kthread']

if re.search(r'win(32|64)', sys.platform) is not None:
    try:
        import win32api
    except ImportError:
        prereqs.append('pypiwin32')
    
setuptools.setup(
    name="amncore",
    version="0.2.2",
    author="The Munshi Group",
    author_email="support@munshigroup.com",
    description="AmmuNation Framework core modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/munshigroup/amncore",
    packages=setuptools.find_packages(),
    install_requires = prereqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
