import setuptools

setuptools.setup(
    name='busho',
    version='1.0',
    author='Czw_96',
    author_email='459749926@qq.com',
    description='Multi-host deployment.',
    url='https://github.com/Czw96/propor',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'paramiko',
    ]
)
