from codecs import open as codecs_open
from setuptools import setup, find_packages
import os

with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()

install_requires = ['click']
tests_require = ['pytest','pytest-cov','pytest-console-scripts','pytest-mock']
extras_require = {}
setup_requires=['pytest-runner']

entry_points={
 'console_scripts': [
   'jvstats=jvstats.console:cli'
 ]
}

datadir = os.path.join('data')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

setup(name='jvstats',
      packages=find_packages(),
      package_data={
        "jvstats": []
      },
      data_files = datafiles,
      version='0.1.4',
      python_requires='>=3.5',
      description=u"",
      classifiers=[],
      keywords='',
      author=u"Jaime Viloria",
      long_description=long_description,
      author_email='jaime.viloria@gmail.com',
      license='MIT',
      include_package_data=True,
      zip_safe=False,
      setup_requires=setup_requires,
      install_requires=install_requires,
      extras_require=extras_require,
      tests_require=tests_require,
      entry_points=entry_points
      )

