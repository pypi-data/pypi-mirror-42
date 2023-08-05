import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dccli",
    version="0.0.1",
    author="YL & SW",
    author_email="deepcluster.io@gmail.com",
    description="cli for manage job in DeepCluster.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['test', ]),
    entry_points={
        'console_scripts': [
            'dccli=dccli.cli:main',
        ],
    },
    install_requires=[
        'pyyaml',
        'boto3',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)