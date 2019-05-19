from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="opulent-pandas",
    version="0.0.4",
    description="A package to validate the schema of a pandas dataframe",
    author="Daniel van der Ende",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["opulent_pandas"],
    install_requires=["pandas==0.23.4"],
    extras_require={"test": ["pytest==4.0.2"], "lint": ["flake8==3.5.0"]},
)
