import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='sugarcrm-cloud-python',
      version='0.1.0',
      description='API wrapper for SugarCRM cloud written in Python',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      url='https://github.com/GearPlug/sugarcrm-cloud-python',
      author='Miguel Ferrer',
      author_email='ingferrermiguel@gmail.com',
      license='MIT',
      packages=['sugarcrm_cloud'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
