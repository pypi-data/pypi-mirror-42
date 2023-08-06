#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Emerging Technologies Team Core Library for General Helper Functions
    
    Contains general helper based functions classes such as Enums and Exceptions
"""

__author__ = "Kevin Thomas Bradley"
__copyright__ = "Copyright 2019, United Nations OICT PSGD ETT"
__credits__ = ["Kevin Bradley", "Yihan Bao", "Praneeth Nooli"]
__date__ = "11 February 2019"
__version__ = "0.1"
__maintainer__ = "Kevin Thomas Bradley"
__email__ = "bradleyk@un.org"
__status__ = "Development"

import pandas as pd             # DataFrame management
import logging                  # Error Handling
import numpy as np              # Mathematical calcs
import pickle                   # Used for loading models
import sklearn                  # Used for model generation via pickle
from enum import Enum           # Used for custom Enums
from yihan_constants import Encoding  # Used to identify character encoding

# Base Error class
class Error(Exception):
    """ETT Base class for other custom exceptions"""
    pass

# Custom Error Class
class InvalidLabelsToModelsError(Error):
   """The number of labels does not match the number of expected corresponding models"""
   pass

# Wrapper Class 
class Helper:

    ## TODO some form of verification to check filename is not null or empty-DONE
    # This function is used to load a CSV file based on the 
    # filename and return this output.
    # @param filename The source file, as an string.
    # @return A DataFrame of the CSV file data.
    # @see OSError
    # @see Exception
    """
    @staticmethod
    def load_csv(filename):
        try:
            return pd.read_csv(filename, encoding = Encoding.LATIN_1.value)
        except OSError as ose:
            print('Handle this by TODO: LOGGING it as an OSError somewhere ' + str(ose)) # TODO use some form of logging
        except Exception as e:
            print('Handle this by TODO: LOGGING it as a general exception somewhere' + str(e)) # TODO use some form of logging
    """
    @staticmethod
    def load_csv(filename):
        try:
            return pd.read_csv(filename, encoding="Latin-1")
        except OSError:
            logging.error("OSError occurred", exc_info=True)
        except Exception:
            logging.error("Exception occurred", exc_info=True)
       
    
