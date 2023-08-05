from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lofo-importance',
    version='0.1.0',
    author="Ahmet Erdem",
    author_email="ahmeterd4@gmail.com",
    description="Leave One Feature Out Importance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['lofo'],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
