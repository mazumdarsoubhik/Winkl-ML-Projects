import pandas as pd
import numpy as np
from collections import Counter
import nltk
import psycopg2
from nltk.corpus import stopwords
import re
from itertools import chain 
import math
import time
import logging 
import requests
import json
print("Imported all packages.")
print("Loading GoogleNews...")
from gensim import models
