# Research Project A

## Introduction

This short research project was completed at the [Sakai Laboratory](http://sakailab.com/) over the winter semester (October 2019 ~ January 2020) and served as an introduction into information retrieval. My initial task was to create a search engine using the ClueWeb12 Disk B corpus but eventually I have also experimented with offline evaluation testing using [Anserini](https://github.com/castorini/anserini). Over the semester I have learnt much about search algorithms, evaluation of search systems and statistical testing.

The files contained here are various scripts that I have used during the experiment, as well as a simple search engine.

## Contents

### Index

The corpus I have used is the ClueWeb12 Disk B corpus which contains about 52 million web pages. Indexing was done with Anserini-0.6.0. The actual corpus and Anserini are not included in this repository.

### Search Engine

The `app/` directory contains a flask web application that acts as a interface for the Anserini search engine. Python 3.6.7 was used during this experiment.

### Evaluation Testing

The `scripts/` directory contains shell scripts that perform indexing and evaluation. The topics and qrels used are from the TREC 2013 Web Track  and TREC 2014 Web Track, and evaluation was performed using `trec_eval` and `gdeval.pl` (available from Anserini).

The `stats/` directory contains python scripts and notebooks that:
- Performs a grid search over parameters for BM25, BM25+RM3 and BM25PRF.
- Performs a randomized Tukey HSD test comparing 5 systems.
- Contains an implementation of randomized Tukey HSD test (in python).
