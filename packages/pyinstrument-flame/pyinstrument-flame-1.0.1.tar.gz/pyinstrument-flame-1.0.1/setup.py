from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='pyinstrument-flame',
    version='1.0.1',
    description='An interactive SVG Flame Chart Renderer for pyinstrument.',
    long_description=long_description,
    author='Christian Stuart',
    author_email='me@cjstuart.nl',
    packages=['pyinstrument_flame'],
    package_data={
        'pyinstrument_flame': ['pyinstrument_flame/vendor/*.pl']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent ",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Testing",
        "Environment :: Web Environment"
    ],
)

