from setuptools import setup, find_packages

# Import __version__ variable from version.py
version = {}
with open("pynextgen/version.py") as fp:
    exec(fp.read(), version)

# Adding list of requirements
with open("requirements.txt", "r") as f:
    requirements = f.read().split()

with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name="pynextgen",
    version=f"{version['__version__']}",
    author="Etienne Kornobis",
    author_email="ekornobis@gmail.com",
    description="[UNSTABLE] A package of custom tools to tackle bioinformatic projects.",
    long_description=readme,
    url="http://pypi.org/project/pynextgen/",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "divergent_transcription=pynextgen.scripts.divergent_transcription:main",
            "clean_featurecounts=pynextgen.scripts.clean_featurecounts:main",
        ]
    },
    classifiers=["Programming Language :: Python :: 3"],
)
