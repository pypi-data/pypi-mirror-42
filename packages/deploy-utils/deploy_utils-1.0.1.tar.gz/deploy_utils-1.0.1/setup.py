import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    README = f.read()
 
setup(
    name='deploy_utils',
    version='1.0.1',
    description='Utilities for deploying projects to EC2',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/evansiroky/deploy_utils',
    author='Evan Siroky',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    keywords='AWS Fabric deployment',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.9.101',
        'fabric>=1.10.1,<2',
        'django-fab-deploy>=0.7.5'
    ],
    entry_points={
        'console_scripts': [
            'launch_amazon_linux=deploy_utils.example_script:amazon_linux_test_battery',
            'launch_centos6=deploy_utils.example_script:centos6_test_battery'
        ]
    },
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True
)
