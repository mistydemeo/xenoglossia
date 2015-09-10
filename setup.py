from setuptools import setup

setup(
    name="xenoglossia",
    description="Robust(?) string manipulation language",
    author="Misty De Meo",
    author_email="mistydemeo@gmail.com",
    license="kindest",
    version="0.2",
    packages=["xenoglossia"],
    entry_points={"console_scripts": ["xg = xenoglossia.main:main"]},
    install_requires=["pyparsing>=2,<3", "six>=1,<3"],
)
