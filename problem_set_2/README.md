# Problem Set 2 - Luis Chan

## Exercise 1: Spelling Correction Using a Bloom Filter 

This project implements a **Bloom Filter** from scratch to identify words with single-character typos, simulating a basic spelling correction system. The goal is to explore the trade-offs between Bloom filter size and the number of hash functions, balancing false positives and accurate suggestions.

## Background

A **Bloom Filter** is a probabilistic data structure that efficiently tests whether an element is part of a set. While it may return false positives, it never returns false negatives. This project uses three hash functions (`sha256`, `blake2b`, and `sha3_256`) to simulate spelling correction through the identification of potential words based on single-character typos.

The project explores how Bloom filters, commonly used in fields like bioinformatics for sequence alignment, can be applied to spelling correction.

## Setup

1. **Download Word List**: 
   The project uses a list of English words, which can be downloaded from the following repository:
   - [Words List](https://github.com/dwyl/english-words/blob/master/words.txt)
   
2. **Read the Words**: 
   The list of words can be read line by line using the following snippet:
   ```python
   with open('words.txt') as f:
       for line in f:
           word = line.strip()
           # Process the word here

