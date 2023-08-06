"""Setup"""
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requires = list(f.read().splitlines())

setup(name='commodity_tool',
      version='0.5dev',
      long_description=readme,
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: MacOS X',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 3.7',
                   'Topic :: Scientific/Engineering :: Information Analysis'],
       url='https://github.com/johnnymac0515/Commodity-Project',
       author='John Macnamara',
       author_email= 'john.macnamara.dev@gmail.com',
       license=license,
       packages=find_packages(),
       install_requires=requires,
       include_package_data=True,
       entry_points= {
           'console_scripts': ['commodity_tool=commodity_project_ir.command_line:main']
                    }
       
        )
       