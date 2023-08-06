from distutils.core import setup

setup(
  name = 'ui-translator',
  packages = ['ui-translator'],
  version = '0.5',
  license='MIT',
  description = 'Python module used for translating Qt .ui files between languages using Google Translate',
  author = 'Bogdan Caleta Ivkovic',
  author_email = 'bogdan.caleta@gmail.com',
  url = 'https://github.com/Raptr3x/qt-ui-translator',
  download_url = 'https://github.com/Raptr3x/qt-ui-translator/archive/v_05.tar.gz',
  keywords = ['ui', 'ui translator', 'translate'],
  install_requires=['ptranslator'],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
  entry_points={
          'console_scripts': [
              'uitranslate = ui-translator.ui_translator:main'
          ]
  },
)