# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='genfiles',
    version='0.0.17',
    url='https://github.com/tuaplicacionpropia/genfiles',
    download_url='https://github.com/tuaplicacionpropia/genfiles/archive/master.zip',
    author=u'tuaplicacionpropia.com',
    author_email='tuaplicacionpropia@gmail.com',
    description='Python library for generate files with jinja and hjson.',
    long_description='Python library for generate files with jinja and hjson.',
    keywords='jinja, hjson, files, generate',
    classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2.7',
      'Intended Audience :: Developers',
      'Topic :: Multimedia :: Graphics',
    ],
    scripts=[
      'bin/gf_generate.cmd', 'bin/gf_generate'
    ],
    packages=find_packages(exclude=['tests']),
    package_data={},
    #package_data={'': ['license.txt']},
    #package_data={'templates': ['*.txt', '*.hjson']}
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
    install_requires=[
        'hjson>=2.0.2',
    ],
)

