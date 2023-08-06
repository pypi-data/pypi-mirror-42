from setuptools import setup, find_packages

setup(
    name='okra',
    version='0.9dev4',
    packages=["okra", "okra/protobuf"],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'google-cloud-storage==1.14.0',
        'protobuf==3.6.1',
        'sqlalchemy==1.2.17',
        'redis==3.2.0',
    ],
    scripts=['bin/okra'],
    setup_requires=['pytest-runner'],
    test_requires=[
        'pytest',
    ],
    test_suite='pytest',
    zip_safe=False
)
