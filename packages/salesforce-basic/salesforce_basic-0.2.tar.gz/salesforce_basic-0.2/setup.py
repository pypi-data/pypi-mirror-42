from setuptools import setup
 
setup(
     name='salesforce_basic',    # This is the name of your PyPI-package.
     version='0.2',                          # Update the version number for new releases
     author='Dan Aronson',
     author_email='dan@openfiber.net',
     description='Basic class for talking to salesforce, refreshes the access token if needed',
     py_modules=['salesforce_basic'],
     install_requires=['boto3'],
     url='https://github.com/openfibernet/salesforce_basic'
     )
