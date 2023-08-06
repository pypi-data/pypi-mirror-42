from setuptools import setup, find_packages

long_description = """tcapy is a transaction cost analysis library"""

setup(name='tcapy',
      version='0.1.0',
      description='tcapy is a transaction cost analysis library',
      author='Saeed Amen',
      author_email='saeed@cuemacro.com',
      long_description=long_description,
      license='Apache 2.0',
      keywords=['tca'],
      url='https://github.com/cuemacro/tcapy',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[],
      zip_safe=False)
