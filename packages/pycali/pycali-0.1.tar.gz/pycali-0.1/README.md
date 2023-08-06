# CaLi

[![Build Status](https://travis-ci.com/benjimor/CaLi.svg?branch=master)](https://travis-ci.com/benjimor/CaLi)

A python package that defines a partial order over licenses

# Introduction

CaLi is a lattice-based model for license orderings. This repository contains a python package that implements this model.


Our code uses the ODRL CaLi ordering ⟨A, DL, C<sub>L</sub>, C<sub>→</sub>⟩ such that:
* A is the set of 72 actions of ODRL (e.g., cc:Distribution, cc:ShareAlike),
* DL is the deontic lattice `Undefined <= Permissions <= Duty <= Prohibition` (actions can be either permitted, obliged, prohibited or not specified; in this deontic lattice, the undefined status is the least restrictive and the prohibited one the most restrictive),
* C<sub>L</sub> and
* C<sub>→</sub> are sets of constraints.

[CaLi online demonstrator](http://cali.priloo.univ-nantes.fr/) Is an exemple of license compliant search engine using CaLi model.

# Installation

Installation in a `virtualenv` is recommended.

Assuming you already have `python 3` and `pip` installed

```bash
pip install pycali
```

this will automatically install [rdflib](https://github.com/RDFLib/rdflib) used to manipulate RDF.

# Getting started

This section shows how to create a CaLi ordering with ease.

## Load a vocabulary

```python

```

## Load a deontic lattice

## Define constraints

## Load licenses

## Instanciate a CaLi Ordering

### Browse the CaLi Ordering