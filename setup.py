﻿# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README-pypi.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

extras = {
    "artagger": ["artagger"],
    "deepcut": ["deepcut", "keras", "tensorflow"],
    "icu": ["pyicu"],
    "ipa": ["epitran"],
    "ml": ["fastai==1.0.22", "keras", "numpy", "torch"],
    "ner": ["sklearn_crfsuite"],
    "thai2fit": ["gensim", "numpy","emoji"],
    "thai2rom": ["keras", "numpy"],
    "full": [
        "artagger",
        "deepcut",
        "epitran",
        "fastai==0.7.0",
        "gensim",
        "keras",
        "numpy",
        "pyicu",
        "sklearn_crfsuite",
        "tensorflow",
        "torch",
    ],
}

setup(
    name="pythainlp",
    version="2.0",
    description="Thai Natural Language Processing library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="PyThaiNLP",
    author_email="wannaphong@kkumail.com",
    url="https://github.com/PyThaiNLP/pythainlp",
    packages=find_packages(),
    test_suite="tests",
    python_requires=">=3.6",
    package_data={
        "pythainlp.corpus": [
            "corpus_license.md",
            "countries_th.txt",
            "negations_th.txt",
            "orchid_pos_th.json",
            "orchid_pt_tagger.dill",
            "stopwords_th.txt",
            "syllables_th.txt",
            "tha-wn.db",
            "thailand_provinces_th.csv",
            "thailand_provinces_th.txt",
            "ud_thai_pud_pt_tagger.dill",
            "ud_thai_pud_unigram_tagger.dill",
            "unigram_tagger.dill",
            "words_th.txt",
            "words_th_frozen_201810.txt",
            "tnc_freq.txt"
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords="pythainlp",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Thai",
        "Topic :: Text Processing :: Linguistic",
    ],
    scripts=['bin/pythainlp']
)

# TODO: Check extras and decide to download additional data, like model files
