# Module 1 - Create a Blockchain

# To be installed:
# Flask==1.1.2
# Postman HTTP Client

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Part 1 - Building a Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []

# Part 2 - Mining our Blockchain
