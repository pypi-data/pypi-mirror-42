from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='sorting_algorithms',
      version='0.1',
      description='Sorting Functions',
      test_suite='nose.collector',
      tests_require=['nose'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='bubble insertion quick selection',
      url='https://gitlab.propulsion-home.ch/vidal-rosas/week3/day4',
      author='Vidal Rosas',
      author_email='pepitoperez@hotmail.com',
      license='MIT',
      packages=['sorting_algorithms'],
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)