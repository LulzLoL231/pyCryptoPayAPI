# -*- coding: utf-8 -*-
#
#  pyCryptoPayAPI - Lib setup file.
#  Created by LulzLoL231 at 11/09/22
#
import re
from setuptools import setup


init_data = open('CryptoPayAPI/__init__.py').read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, init_data, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError(
        'Unable to find version string in "CryptoPayAPI/__init__.py"')


def long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(extras_require={"dev": ["attrs==22.1.0; python_version >= '3.5'", 'autopep8==1.7.0', 'cached-property==1.5.2', 'cerberus==1.3.4', "certifi==2022.6.15.1; python_version >= '3.6'", "chardet==5.0.0; python_full_version >= '3.6.0'", "charset-normalizer==2.1.1; python_full_version >= '3.6.0'", "colorama==0.4.5; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'distlib==0.3.6', 'flake8==5.0.4', "idna==3.3; python_version >= '3.5'", 'iniconfig==1.1.1', "mccabe==0.7.0; python_full_version >= '3.6.0'", 'mypy==0.971', 'mypy-extensions==0.4.3', 'orderedmultidict==1.0.1', "packaging==20.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "pep517==0.13.0; python_full_version >= '3.6.0'", "pip==22.2.2; python_version >= '3.7'", "pip-shims==0.7.3; python_full_version >= '3.6.0'", 'pipenv-setup==3.2.0', 'pipfile==0.0.2', "platformdirs==2.5.2; python_version >= '3.7'", "plette[validation]==0.3.0; python_version >= '3.7'", "pluggy==1.0.0; python_full_version >= '3.6.0'", "py==1.11.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "pycodestyle==2.9.1; python_full_version >= '3.6.0'", "pyflakes==2.5.0; python_full_version >= '3.6.0'", "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'pytest==7.1.3', 'pytest-asyncio==0.19.0', "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "requests==2.28.1; python_version >= '3.7' and python_version < '4'", "requirementslib==1.6.9; python_version >= '3.7'", "setuptools==65.3.0; python_version >= '3.7'", "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", "tomli==2.0.1; python_version >= '3.7'", "tomlkit==0.11.4; python_version < '4' and python_full_version >= '3.6.0'", "typing-extensions==4.3.0; python_version >= '3.7'", "urllib3==1.26.12; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4, 3.5' and python_version < '4'", "vistir==0.6.1; python_version not in '3.0, 3.1, 3.2, 3.3' and python_version >= '3.7'", "wheel==0.37.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", ]},
      name='pyCryptoPayAPI',
      version=verstr,
      long_description=long_description(),
      long_description_content_type='text/markdown',
      description='Python API wrapper for Crypto Pay API',
      author='Maxim Mosin',
      author_email='max@mosin.pw',
      license='MIT License, see LICENSE file',
      keywords=['cryptopay', 'crypto'],
      url='https://github.com/LulzLoL231/pyCryptoPayAPI',
      download_url='https://github.com/LulzLoL231/pyCryptoPayAPI/archive/master.zip',
      packages=['CryptoPayAPI'],
      install_requires=["anyio==3.6.1; python_full_version >= '3.6.2'", "certifi==2022.6.15.1; python_version >= '3.6'", "h11==0.12.0; python_version >= '3.6'", "httpcore==0.15.0; python_version >= '3.7'", 'httpx==0.23.0', "idna==3.3; python_version >= '3.5'", 'pydantic==1.10.2', 'rfc3986[idna2008]==1.5.0', "sniffio==1.3.0; python_version >= '3.7'", "typing-extensions==4.3.0; python_version >= '3.7'"
                        ],
      setup_requires=['wheel'],
      classifiers=[
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Environment :: Console',
    'Development Status :: 4 - Beta',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10'
    'Programming Language :: Python :: 3 :: Only',
]
)
