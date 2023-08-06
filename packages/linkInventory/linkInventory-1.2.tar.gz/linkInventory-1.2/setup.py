from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='linkInventory',
      version='1.02',
      description='WAN link inventory management ',
      long_description=readme(),
      url='https://github.com/microservice-tsp-billing/linkInventory',
      author='Bhujay Kumar Bhatta',
      author_email='bhujay.bhatta@yahoo.com',
      license='Apache Software License',
      packages=find_packages(),
#       package_data={
#         # If any package contains *.txt or *.rst files, include them:
#         '': ['*.txt', '*.rst', '*.yml'],
#         # And include any *.msg files found in the 'hello' package, too:
#         #'hello': ['*.msg'],
#     },
      include_package_data=True,
      install_requires=[
          'requests==2.20.1',
          'configparser==3.5.0',
          'PyJWT==1.7.0',
          'PyYAML==3.13',
          'cryptography==2.3.1',
          'six==1.11.0',
          'Flask==1.0.2',
          'Flask-Testing==0.7.1',      
          'konfig==1.1',
          'tokenleaderclient==0.9',
          'pyOpenSSL==19.0.0',
          'mssql-cli==0.15.0',
          'pyodbc==4.0.26',
          'SQLAlchemy==1.2.18',
          'sqlparse==0.2.4',
          'urllib3==1.24.1',
          
      ],
      entry_points = {
        'console_scripts': ['encrypt-pwd=linkInventory.configs.config_cli:main',
                            'linv-start=linkInventory.app_run:main'],
        },
      test_suite='nose.collector',
      tests_require=['nose'],

      zip_safe=False)
