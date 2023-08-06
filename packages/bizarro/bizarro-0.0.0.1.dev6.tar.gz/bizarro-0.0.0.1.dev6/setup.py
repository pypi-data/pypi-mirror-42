from setuptools import setup

install_requires = [
    'zathura',
    'phonenumbers'
]

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='bizarro',  # alternative name docket
      packages=['bizarro', 'bizarro.utility', 'bizarro.template', 'bizarro..buttons'],
      version='0.0.0.1.dev6',
      description='',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ibtehaz-shawon/bizarro',
      author='Ibtehaz Shawon',
      author_email='ibtehaz.92@gmail.com',
      license='MIT',
      install_requires=[
          install_requires
      ],
      entry_points={
          'console_scripts': [
              'bizarro = bizarro.__init__:create_app'
          ]
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
