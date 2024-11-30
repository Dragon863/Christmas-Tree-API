from setuptools import setup, find_packages

setup(
    name="runshawtree",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "pygame",
    ],
    author="Daniel Benge",
    author_email="hi@danieldb.uk",
    description="A simulator for LED displays",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Runshaw-Hack-Club/Christmas-Tree",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
