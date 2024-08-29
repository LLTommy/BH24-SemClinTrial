from setuptools import setup, find_packages

setup(
    name='clinical-trials-rdf-converter',
    version='0.1.0',
    description='A tool to convert clinical trial data to RDF format',
    author='Thomas Liener',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/clinical-trials-rdf-converter',
    packages=find_packages(),
    install_requires=[
        'requests',
        'rdflib',
    ],
    entry_points={
        'console_scripts': [
            'ct-rdf=ct_rdf.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
