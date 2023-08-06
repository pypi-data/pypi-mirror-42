import pypandoc
import os

templates_setup_cfg = """[metadata]
name = 
author =
author-email = 
summary = 
license = MIT
description-file =
    README.rst
home-page = http://
requires-python = >= 3.4
classifier =
    Development Status :: 4 - Beta
    Environment :: Console
    Environment :: OpenStack
    Intended Audience :: Developers
    Intended Audience :: Information Technology
    License :: OSI Approved :: Apache Software License
    Operating System :: OS Independent
    Programming Language :: Python

[files]
packages = 

[entry_points]
console_scripts =
    pbr = pbr.cmd:main

"""

templates_setup_py = """import setuptools

setuptools.setup(setup_requires=['pbr'],pbr=True)
"""


class PBRTool:
    def __init__(self, path='.'):
        self.path = path

    def _create_setup_cfg(self):

        with open(os.path.join(self.path, 'setup.cfg'), 'w') as f:
            f.write(templates_setup_cfg)

        return os.path.join(self.path, 'setup.cfg')

    def _create_setup_py(self):

        with open(os.path.join(self.path, 'setup.py'), 'w') as f:
            f.write(templates_setup_py)

        return os.path.join(self.path, 'setup.py')

    def mkpbr(self):
        self._create_setup_cfg()
        self._create_setup_py()

    def md2rst(self):
        output = pypandoc.convert_file(
            os.path.join(self.path, 'README.md'), 'rst')
        with open(os.path.join(self.path, 'README.rst'), 'w') as f:
            f.write(output)
