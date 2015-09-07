from setuptools import setup

setup(
    name="xenoglossia",
    version="0.1",
    packages=["xenoglossia"],
    entry_points={"console_scripts": ["xg = xenoglossia.main:main"]},
)
