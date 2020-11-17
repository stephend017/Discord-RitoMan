from setuptools import setup


with open("README.md", "r") as file:
    readme = file.read()


setup(
    name="discord_ritoman",
    version="0.0.1",
    description="A python module",
    long_description=readme,
    author="myname",
    author_email="myemail",
    packages=["discord_ritoman"],
    package_data={"": ["*.json", "*.pgsql"]},
)
