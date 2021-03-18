# HTTP logs stream analyzing tool

## Overview

Implematation of logs stream analyzing tool to define exact hour where most of the users experienced server errors. It uses asyncio simple client-server model to retrieve messages from different sources and process in single place. For calculating cardinality of unique users during hour HyperLogLog++ algorithm used. 

## Requirements

 - Python 3.8+
 - Poetry dependencies manager

## Usage
Install dependencies and configure settings (optional)

    cd src
    poetry install
    cp .env.example .env
To start log server:

    poetry shell
    python main.py
To start log producing client(s):

    poetry shell
    log_record_generators/fake_log_generator_v1.sh | python pipeline.py
    
   To run tests:
   
    poetry shell
    python -m unittest discover -v
    
Server will output current hour value with maximum of unique users experienced server errors on each received message. Example:

    Total messages: 9406 - Current hour with max value of server errors experienced for unique users is: 10

### TODO

 - enhance message processing and cardinality estimation performance (suggestion: add threads/other paralleling)
 - enhance client-server stability
 - increase code coverage
 - rework output frequency (reduce spamming)
