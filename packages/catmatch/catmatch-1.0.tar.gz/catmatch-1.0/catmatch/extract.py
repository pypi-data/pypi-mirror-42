'''

catmatch project 
-------------------
File: extract.py

This file contains the code
who extracts headers from catalog

@author: R. THOMAS
@year: 2018
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

#### Python Libraries
import numpy
import sys


def header(inputfile):
    '''
    This function looks inside the
    catalog and extract the header.
    (see function fake header)
    Parameters:
    -----------
    imputfile   str, path to the input file

    Return:
    -------
    Headers     list of string, one string for each column
    '''
    ####extract number of column
    A = numpy.genfromtxt(inputfile, dtype='str').T
    Nc = len(A)  ###--> number of column

    ####read the first line of the raw file
    with open(inputfile, 'r') as F:
        ###[1:-1]--> this remove '#' and the '\n' at the end
        firstLine = F.readline()[1:-1]
     
    ###count the number of element in the first line
    Nh = len(firstLine.split())
    ##check if they are equal:
    if Nh == Nc:
        #if yes we take the splitted header
        header = firstLine.split()
    else:
        print('Number of header column in %s dif from number of columns: Nc = %s and Nh = %s'\
                %(inputfile, Nc, Nh))
        sys.exit()
    return header

def column(name_col, columns, cat):
    '''
    This function extract the column corresponding to the name
    given in argument
    Parameters:
    -----------
    name_col    str, name of the column to plt
    column      list of str, with columns name
    cat         str, catalog to open
    Return:
    -------

    '''
    ###we find the index of the column in the catalog
    index_in_cat = numpy.where(name_col == numpy.array(columns) )[0][0]

    ##we load the catalog
    cat = numpy.genfromtxt(cat, dtype='str').T

    return cat[index_in_cat]


