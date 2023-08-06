from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='koffisortwork',
      version='0.1',
      description='The koffisortwork algorithm',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='sort elelments in different ways',
      url='http://gitlab.propulsion-home.ch/koffi-fiadjigbe/week3/day4',
      author='koffi fiadjigbe',
      author_email='koffifiadjigbe@gmail.com',
      license='MIT',
      packages=['koffisortwork'],
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
)
