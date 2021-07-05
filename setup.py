from setuptools import setup, find_packages

import imp

version = imp.load_source('abletonparsing.version', 'abletonparsing/version.py')

setup(
    name='abletonparsing',
    version=version.version,
    description='Python module for parsing Ableton Live ASD clip files containing warp markers.',
    author='David Braun',
    author_email='braun@ccrma.stanford.edu',
    url='http://github.com/dbraun/abletonparsing',
    download_url='http://github.com/dbraun/abletonparsing/releases',
    packages=find_packages(),
    long_description="""Python module for parsing Ableton Live ASD clip files containing warp markers.""",
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
    install_requires=[],
    extras_require={
        'docs': ['numpydoc'],
        'tests': [
            'pytest',
            'pyrubberband',
            'librosa',
            'soundfile'
        ]
    },
    test_require=[
        'pytest',
        'pyrubberband',
        'librosa',
        'soundfile'
        ]
)
