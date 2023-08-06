from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(name='pyfidelimax',
      long_description=long_description,
      long_description_content_type='text/markdown',
      version='1.0.1',
      description='fidelimax.com.br integration',
      url='https://gitlab.com/yk2kus/pyfidelimax',
      author='Yogesh Kushwaha',
      author_email='info@tkopen.com',
      license='MIT',
      packages=['pyfidelimax'],
      install_requires=['requests'],
      zip_safe=False)
