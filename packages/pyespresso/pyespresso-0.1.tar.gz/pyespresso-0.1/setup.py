from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='pyespresso',
      version='0.1',
      description='Py. ESPRESSO',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/j-faria/pyespresso',
      author='João Faria',
      author_email='joao.faria@astro.up.pt',
      license='GPL-3.0',
      packages=['pyespresso'],
      zip_safe=False)
