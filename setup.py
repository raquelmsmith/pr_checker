from setuptools import find_packages, setup

setup(
    name='pr-checker',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'pr-checker=pr_checker.cli:main',
        ],
    },
    author='Raquel M Smith',
    author_email='your.email@example.com',
    description='A simple CLI tool to check PR statuses on GitHub',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/raquelmsmith',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)