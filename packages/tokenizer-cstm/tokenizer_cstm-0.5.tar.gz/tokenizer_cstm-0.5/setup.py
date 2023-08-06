
import setuptools
from distutils.core import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()


setup(name='tokenizer_cstm',
      version='0.5',
      description='fining sentences from raw text and tokenizing',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Andrin Pelican',
      author_email='andrin.pelican@bluewin.ch',
      packages=['tokenizer_cstm'],
     )
