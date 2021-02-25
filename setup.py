from setuptools import setup


with open("README.md", "r") as file:
    readme = file.read()


setup(
    name="discord_ritoman",
    version="1.0.0",
    description="An application that utilizes the discord API & Riot API to send progress updates and standout performances to a discord server",
    long_description=readme,
    author="Stephen Davis",
    author_email="stephenedavis17@gmail.com",
    packages=["discord_ritoman"],
    package_data={"": ["*.json", "*.pgsql"]},
)
