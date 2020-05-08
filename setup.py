
from setuptools import setup
from setuptools import find_packages

setup(
    # TODO add inform
    name='pip_services_benchmark',
    version='0.0.0',
    url='https://github.com/banalna/pip-benchmark-python',
    # license='',
    description='Basic portable abstractions for Pip.Services in Python',
    # author='',
    # author_email='',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'psutil', 'pytest', 'pip-services3-commons'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
