from distutils.core import setup
import setuptools

console_scripts = """
"""

setup(
  name = 'kintsugi',
  packages = ['kintsugi'],
  version = '0.0.1',
  description = '',
  long_description = '',
  author = '',
  license = '',
  package_data={},
  url = 'https://github.com/alvations/kintsugi',
  keywords = [],
  classifiers = [],
  install_requires = ['six', 'click', 'joblib', 'tqdm'],
)
