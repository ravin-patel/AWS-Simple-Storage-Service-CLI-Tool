from setuptools import setup

setup(
    name='s3cli',
    version='0.1.0',
    packages=['s3cli'],
    install_requires=['boto3>=1.9.201',
                      'botocore>=1.12.201', 'moto', 'pytest'],
    entry_points={
        'console_scripts': [
            's3cli = pycli.__main__:main'
        ]
    })
