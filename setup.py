from setuptools import setup, find_packages

import imp

version = imp.load_source('abletonparsing.version', 'abletonparsing/version.py')

setup(
    name='abletonparsing',
    version=version.version,
    description='Python module to wrap rubberband',
    author='David Braun',
    author_email='braun@ccrma.stanford.edu',
    url='http://github.com/dbraun/abletonparsing',
    download_url='http://github.com/bmcfee/abletonparsing/releases',
    packages=find_packages(),
    long_description="""A python module to parse Ableton ASD files.""",
    classifiers=[
        "License :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='audio music sound',
    license='MIT',
    install_requires=[
        'librosa>=0.8.0',
    ],
    extras_require={
        'docs': ['numpydoc'],
        # 'tests': [
        #     'pytest',
        #     'pytest-cov',
        #     'contextlib2',
        # ]
    },
    # test_require=[
    #     'pytest',
    #     'pytest-cov',
    #     'contextlib2',
    # ]
)
