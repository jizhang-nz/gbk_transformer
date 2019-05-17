# GBK transformer
Transformation of a Genbank file into a FASTA file and a feature table.

## Introduction

GBK_converter.py is a python script to transfrom a Genbank file into a FASTA file and a feature table.

## Motivation

To transform a GenBank file (.gbk, .gb or .gbff) into a FASTA sequence file (.fna, .fas, .fasta), and all the features into a table that can be easily manipulate with programs like EXCEL.

## Prerequisites

This program was written with Python 3.

No extra Python module or other program is needed to run the program.

## Usage
If you have Python 3 installed in your system, you could put the program with your GenBank files, and run the program with command like:

    python gbk_converter.py -i input.gbff

The program would then output two files: 

    input.fna
    input.xls
