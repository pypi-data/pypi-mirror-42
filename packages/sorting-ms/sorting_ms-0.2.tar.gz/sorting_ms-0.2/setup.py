from setuptools import setup

setup(name='sorting_ms',
      version='0.2',
      description='some simple sorting functions',
      long_description='Exercise to create a python package that has some simple sorting functions included',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='sorting function marita salz',
      url='https://gitlab.propulsion-home.ch/marita-salz/week-3/day-4',
      author='Marita Salz',
      author_email='marita.salz@hispeed.ch',
      license='MIT',
      packages=['sorting_ms'],
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
 )

