from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pgbar',
    version='0.3',
    packages=['pgbar'],
    url='https://gitlab.com/sajeeshen/python-terminal-progress',
    license='',
    author='Sajeesh E Namboothiri',
    author_email='sajeeshe@gmail.com',
    description='Terminal Progress Bar',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
