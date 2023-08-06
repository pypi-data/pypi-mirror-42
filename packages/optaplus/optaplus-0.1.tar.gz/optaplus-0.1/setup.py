from setuptools import setup

setup(name='optaplus',
      version='0.1',
      description='Optaplus package is a range of functions ' 
      'to act as helping hands for people working with Opta and Tracab data.',
      url='http://github.com/tylerjrichards',
      author='Joe Mulberry, Tyler Richards',
      author_email='tylerjrichards@gmail.com',
      license='MIT',
      packages=['optaplus'],
      install_requires=[
          'elementpath',
          'pandas',
          'numpy',
      ],
      zip_safe=False)
