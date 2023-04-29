"""
Setup script for pkg package.
"""

from setuptools import setup

setup(name='open_alex',
      version='0.0.1',
      
      description='bibtex and ris utilities',
      maintainer='saroj',
      maintainer_email='ssathish@andrew.cmu.edu',
      license='MIT',
      packages=['openalex'],
      scripts=[],
      entry_points={
        "console_scripts": ["cite = openalex.cmdline:cite"]},
      long_description='''to get citations bibtex/ris''')
