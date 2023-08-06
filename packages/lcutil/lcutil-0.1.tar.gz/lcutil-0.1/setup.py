from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


# https://pypi.org/pypi?%3Aaction=list_classifiers
setup(name='lcutil',
      version='0.1',
      description='General useful utility functions for Python projects.',
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
      ],
      keywords='utility functions devel',
      url='http://github.com/lcordier/lcutil/',
      author='Louis Cordier',
      author_email='lcordier@gmail.com',
      license='MIT',
      packages=['lcutil'],
      install_requires=[
      #    'markdown',
      ],
      # test_suite='nose.collector',
      # tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': [
              'find_between=lcutil.find_between:main',
              'imap_tool=lcutil.imap_tool:main',
          ],
      },
      include_package_data=True,
      zip_safe=False)
