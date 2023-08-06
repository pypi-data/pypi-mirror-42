import os
from setuptools import setup, find_packages

reqs = []

def get_version():
	return open('VERSION.txt').read().strip()

def long_description():
	return open('README.md').read().strip()

def package_data():
    file_set = []
    for root, dirs, files in os.walk('ephemera'):
        for f in files:
            if '.git' in f.split(os.path.normpath(os.path.join(root, f))):
                # Prevent the repo from being added.
                continue
            file_name = os.path.relpath(os.path.join(root, f), 'ephemera')
            file_set.append(file_name)
    return file_set

setup(name='Ephemera',
      version=get_version(),
      description='Ephemera Networking Toolkit',
      long_description=long_description(),
      long_description_content_type='text/markdown',
      keywords='ephemera, networking, proxy, privacy, anonymity',
      author='Ryan Rock',
      author_email='r@ryanrock.co',
      url='http://www.ephemera.net',
      license='The MIT License',
      provides=['ephemera'],
      packages=find_packages(),
      package_data={'': package_data()},
      classifiers=['Programming Language :: Python :: 3',
                   'Development Status :: 1 - Planning',
                   'License :: OSI Approved :: MIT License',
                   ],
)
