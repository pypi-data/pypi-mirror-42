#!/usr/bin/env python

from distutils.core import setup

setup(
    name="embeddingvectorizer",
    version="0.01",
    description="Sklearn vectorizers using word embedding model",
    author="Wouter van Atteveldt",
    author_email="wouter@vanatteveldt.com",
    packages=["embeddingvectorizer"],
    include_package_data=True,
    zip_safe=False,
    keywords = ["API", "text"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Text Processing",
    ],
    install_requires=[
        "scikit-learn"
    ],
    extras_require={
        'dev': [
            'nose',
            'ipython',
            'jupyter'
        ]
    }
)
