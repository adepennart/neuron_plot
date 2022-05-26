#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: plot_pymaid.py
Date: May 19th, 2022
Author: Auguste de Pennart
Description:
    plots a 2D representation of the neuron(s) of interest

List of functions:
    No user defined functions are used in the program.

List of "non standard modules"
    plot_functions:
        a module containing all functions to create 2d plot of neurons

Procedure:
    1. Takes project id and either json file or, via standard input, neuron(s) of interest
    2. logs into Catmaid account
    3. plots neurons in 2D with optional print to output file

Usage:
    python plot_pymaid.py [-h] [-v] -i PROJECT_ID
                      (-j JSON | -n NEURON [NEURON ...]) [-J] [-a]
                      [-c COLOUR [COLOUR ...]] [-V VOLUME [VOLUME ...]]
                      [-C VOLUME_COLOUR [VOLUME_COLOUR ...]]
                      [-p PERSPECTIVE PERSPECTIVE PERSPECTIVE] [-o OUTPUT]
                      [-s]

known error:
    1. no threshold on how many neurons can be looked up, error shown by pymaid code
    2. no option for regex and non regex, currently standard input is regex and json is not regex
    3. accepts only RGB colour option, if not provided error shown by pymaid code
    4. some variable names could be clearer (ie. neur_col_dict)
    5. error shown by pymaid code when annotation argument used for json file
    6. does not currently accept more than 1 json file
    7. add neuron connections, thickness and transparency
    8. currently overwrites files
    9. all functions with two outputs, should be assigned two different variables
 """

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #fix it so it displays name of file here
    print('using plot_pymaid.py as main script')

# import modules
# ----------------------------------------------------------------------------------------
# import re  # module for using regex
import argparse #module for terminal use
import pymaid
# import pandas
# import matplotlib.pyplot as plt
# import navis
# import matplotlib.colors
# import json
# import sys
# print(sys.path)

# import os
# import sys
# import inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)

from  plot_functions import *


#argparse
# ----------------------------------------------------------------------------------------
#program description
usage='plots a 2D representation of the catmaid neurons of interest'
parser=argparse.ArgumentParser(description=usage)#create an argument parser
reqgroup= parser.add_argument_group(title='required arguments')
exgroup = parser.add_argument_group(title='one or the other')
group = exgroup.add_mutually_exclusive_group(required=True)
optgroup= parser.add_argument_group(title='optional arguments')
opt_j_group= parser.add_argument_group(title='optional arguments with json')
opt_n_group= parser.add_argument_group(title='optional arguments with neuron')

#creates the argument for program version
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 1.1')
#creates the argument where project_id will be inputted
reqgroup.add_argument('-i', '--project_id',
                    metavar='PROJECT_ID',
                    dest='project_id',
                    required=True,
                    help='user-specified project id (ie. lamarcki_OV)')
#creates the argument where the json file will be inputted
group.add_argument('-j', '--json',
                    metavar='JSON',
                    dest='json',
                    help='user-specified catmaid json file')
#creates the argument where the neuron(s) be inputted
group.add_argument('-n', '--neuron',
                    metavar='NEURON',
                    dest='neuron',
                    nargs='+',
                    help='user-specified Neuron(s) of interest. REGEX accepted.')
#creates the argument whether or not user_specified colour will be used for json files
opt_j_group.add_argument('-J', '--json_colour',
                    dest='json_colour',
                    action='store_false',
                    default='store_True',
                    help='option to not use user-specified colours')
#creates the argument where to search for neurons by annotation and not by name
opt_n_group.add_argument('-a', '--annotation',
                    dest='annotation',
                    action = 'store_true',
                    help='If looking through annotations and not neuron name, please select. REGEX accepted.')
#creates the argument where colour can be inputted for -neuron
opt_n_group.add_argument('-c', '--colour',
                    metavar='COLOUR',
                    dest='colour',
                    nargs='+',
                    help='User-specified neuron colours, currently only RGBA argument accepted (ie. 0,1,0,.1)')
#creates the argument where volume will be inputted
optgroup.add_argument('-V', '--volume',
                    metavar='VOLUME',
                    dest='volume',
                    nargs='+',
                    help='user-specified Volume(s) of interest')
#creates the argument where volume colour will be inputted
optgroup.add_argument('-C', '--volume_colour',
                    metavar='VOLUME_COLOUR',
                    dest='volume_colour',
                    nargs='+',
                    help='User-specified volume colours, currently only RGBA argument accepted (ie. 0,1,0,.1)')
#creates the argument where the plot perspective will be inputted
optgroup.add_argument('-p', '--perspective',
                    metavar='PERSPECTIVE',
                    dest='perspective',
                    nargs=3,
                    help='User-specified perspective for plot, default is 7, -90, 0 for camera distance, vertical rotational angle and horizontal rotational angle (ie. 6 87 73)')
#creates the argument where the output file name will be inputted
parser.add_argument('-o', '--output',
                    metavar='OUTPUT',
                    dest='outputfile',
                    help='optional plot output file')
#creates the argument whether to show or not the plot
parser.add_argument('-s', '--no_show',
                    dest='no_show',
                    action='store_false',
                    default='store_True',
                    help='option to not show plot')
args=parser.parse_args()#parses command line

# variables
# --------------------------------------------------------------------------------------
neur_col_dict={}
volume=None
# main code
# --------------------------------------------------------------------------------------
rm = pymaid.connect_catmaid(project_id=args.project_id)#open Catmaid to project id

if args.json:
    neur_col_dict=json_parse(args.json,args.json_colour)
elif args.neuron:
    neur_col_dict = colour_parser(args.colour, args.neuron)
if args.annotation:
    nl, cmap=neuron_by_annotation(neur_col_dict)
elif not args.annotation:
    nl, cmap=neuron_by_name(neur_col_dict)
vol_colour_dict = colour_parser(args.volume_colour, args.volume)
volume = volume_build(vol_colour_dict)
figure_build(nl, cmap, volume, args.perspective, args.no_show)
