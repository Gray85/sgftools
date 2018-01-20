from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name="sgftools",
    version="0.1",
    description="A library for manipulating sgf files",
    url="https://github.com/Gray85/sgftools",
    author="Korolyov Sergey",
    author_email="korolyovs@mail.ru",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Board Games',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',

    ],
    keywords="go game baduk weiqi kifu",
    packages=["sgftools"],
    py_modules=["kifugen"],
    install_requires=["FPDF >=1.7.2", "pyparsing >=2.0.7", "svgwrite"]
)
