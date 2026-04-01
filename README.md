# Security and Privacy: Performance Benchmarking of Cryptographic Mechanisms

## Overview
This project is Assignment #1 for the Security and Privacy. It provides Python implementations to measure and benchmark the execution times of cryptographic mechanisms based on AES, RSA, and SHA256 when processing files of different sizes.

## Group Members
1. Aly Mohamed Saad Filho - 202401045
2. Amanda Lucas - 202400455
3. Silvia Baciu Pinto - 202405988

## Features and Cryptographic Mechanisms
This repository implements performance benchmarking for the following tasks:
* **AES Cryptography:** Encrypts and decrypts files using AES in Counter (CTR) Mode with a 256-bit key. 
* **RSA Cryptography:** Implements the RSA function and its inverse using a 2048-bit key. It uses a secure encryption scheme defined as:
    $Enc(m;r)=(RSA(r),H(0,r)\oplus m_{0},...,H(n,r)\oplus m_{n})$.
    Here, $r$ is uniform, $H$ is a SHA-256 hash function producing outputs of size $l$, and $n$ is the number of blocks calculated as $\lceil|m|/l\rceil$.
* **SHA-256 Hashing:** Measures the time for SHA-256 hash generation, and it's inverse, for the generated file sizes.

## Performance Measurement Methodology
* **Scope:** The benchmarking exclusively measures the time of the cryptographic operations/algorithms; it excludes the time required for file generation.
* **Padding:** If padding is used, note that it may affect the results, especially for smaller file sizes like the one with 8 bits.
* **Statistical Significance:** The code relies on multiple runs to produce statistically significant results (e.g., standard deviation or confidence intervals). It accounts for running a fixed algorithm over the same file multiple times, as well as over multiple randomly generated files of fixed sizes.

## Experimental Setup

* **OS:** Windows 11.
* **CPU:** 13th Gen Intel(R)Core(TM) i7-13620H
* **RAM:** 32GB - 5200 MT/s
* **Python Version:** 3.13.12

## Libraries Used (requirements.txt)

* **cryptography** == 46.0.6
* **matplotlib** == 3.10.8
* **numpy** == 2.4.4
* **pandas** == 3.0.2
* **seaborn** == 0.13.2

## How to Run
*First, install the libraries needed.*
```bash
pip install -r requirements.txt
```
*Then run the following program to generate the files.*
```bash
python gen_files.py
```
*with the files properly generated, just choose which method of encryption and decryption you want to use:*
```bash
python AES_ctr.py
```
*or*
```bash
python rsa_custom.py
```
*for better visualization of the results, run the assigment1.py with your code editor.*
