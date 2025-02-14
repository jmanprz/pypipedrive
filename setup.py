from setuptools import setup
from setuptools._distutils.dep_util import newer

setup(
    author="Gildas Tone",
    author_email="jm@magicalpotion.io",
    name="pypipedrive",
    version="1.0.0",
    package_data={
        "pypipedrive": ["py.typed"],
    },
)