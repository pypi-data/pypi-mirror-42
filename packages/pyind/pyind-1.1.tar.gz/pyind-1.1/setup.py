import setuptools


setuptools.setup(
    name="pyind",
    version="1.1",
    author="chankane",
    author_email="brawnychocolate@gmail.com",
    description="A genetic algorithm library in Python3",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chankane/pyind",
    keywords="pyind genetic ga GA",
    install_requires=['numpy'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
