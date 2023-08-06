from setuptools import setup
 
setup(
     name='sf_object_tools',    # This is the name of your PyPI-package.
     version='0.1',                          # Update the version number for new releases
     author='Dan Aronson',
     author_email='dan@openfiber.net',
     description='Open source project for processing object updates from salesforce',
     py_modules=['sf_update'],
     install_requires=['boto3'],
     url='https://github.com/openfibernet/sf_object_updates'
     )
