from distutils.core import setup

setup(
  name = 'hyperlite',
  packages = ['hyperlite'],
  version = '0.1',
  license='MIT',
  description = 'An official hyperlite database client or shell to interact with hyperlite database.',
  author = 'Anongrp',
  author_email = 'developeranikesh@gmail.com',
  url = 'https://github.com/anongrp/hyperlite-client',
  download_url = 'https://github.com/anongrp/hyperlite-client/archive/0.1.tar.gz',
  keywords = ['hyperlite', 'hyperlitedb', 'hypershell', 'hyperlite-client'],
  install_requires=[ ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ],
)