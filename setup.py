import sys
from setuptools import setup

is_win = sys.platform.startswith('win')

install_requires = ["aiofiles", "pystache", "pyyaml"]
if is_win:
    install_requires += ["colorama"]


setup(
    name="pybase16-builder",
    version="0.2.8",
    description="A base16 colorscheme builder for Python",
    long_description=open("README.rst").read(),
    url="https://github.com/InspectorMustache/pybase16-builder",
    packages=["pybase16_builder"],
    author="Pu Anlai",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Other/Nonlisted Topic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="base16",
    install_requires=install_requires,
    python_requires=">=3.5",
    entry_points={"console_scripts": ["pybase16 = pybase16_builder.cli:run"]},
)
