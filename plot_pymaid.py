#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: plot_pymaid.py
Date: May 9th, 2022
Author: Auguste de Pennart
Description:
    plots a 2D representation of the neurons of interest

List of functions:
    No user defined functions are used in the program.

List of "non standard modules"
    No "non standard modules" are used in the program.

Procedure:
    1. logs into catmaid account
    2. asks for project id (ie. lamarcki_OV)
    3. shows neurons and prints to output file


    1. for loop through taxonomy database and pull out aves taxonomy ids
    2. for loop through uniport database and pull out bird species ids
    3. for loop through the blast output file and find the genes with the best match is a bird gene
    4. for loop through fna file to find scaffold for matching bird id
    5. for loop through genome file and remove scaffolds that contain bird genes
Usage:
    python3 plot_pymaid.py
known error:
    1. make finding neuron default, but if annotation and neuron not found, error, have to make i find list or not
    1. should put user input for neuron
    2. should check both name of neurons and annotations
    3. should put user input for volume
    4. options of colour, azimuth and elevation angles
    3. perhaps option of saving
    5. set get annotation and name pf neuron as regex
 """

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #fix it so it displays name of file here
    print('using plot_pymaid.py as main script')

# import modules
# ----------------------------------------------------------------------------------------
import re  # module for using regex
import argparse #module for terminal use
import pymaid
import pandas
import matplotlib.pyplot as plt
import navis

#argparse
# ----------------------------------------------------------------------------------------
#program description
usage='plots a 2D representation of the neurons of interest'
parser=argparse.ArgumentParser(description=usage)#create an argument parser
req_arg= parser.add_argument_group(title="required arguments")
#creates the argument for program version
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 1.0')
#make sure number
#
req_arg.add_argument('-p', '--project_id',
                    metavar='PROJECT_ID',
                    dest='project_id',
                    required=True,
                    help='user-specified project id (ie. lamarcki_OV)')
#
#this needs to be updated
req_arg.add_argument('-n', '--NEURON',
                    metavar='NEURON',
                    dest='neuron',
                    nargs='+',
                    required=True,
                    help='user-specified Neuron(s) of interest')
#this needs to be updated
req_arg.add_argument('-a', '--ANNOTATION',
                    dest='annotation',
                    action = 'store_true',
                    help='If looking through annotations and not neuron name, please select')
#creates the optinal argument for output file name
parser.add_argument('-o', '--output',
                    metavar='OUTPUT',
                    dest='outputfile',
                    help='optional genome assembled outputfile')
args=parser.parse_args()#parses command line

#functions
# ----------------------------------------------------------------------------------------

# print_to_output
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # genone_id_dict:
        # a dictionary of each species and a list of all genome ids
    #outputfile:
        # name of output file
# use:
    # when outputfile specified creates an output file of all species and the genome ids
# return:
    # no return
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_to_output(outputfile=None):
    try:
        plt.savefig(f'{outputfile}.pdf', transparent=True)
    except TypeError:
        pass

def neuron_by_annotation(annotation=None):
    skids = pymaid.get_skids_by_annotation(annotation)
    # print(skids)
    nl = pymaid.get_neurons(skids)
    # print(nl)
    return nl

#regex
def neuron_by_name(neuron=None):
    nl = pymaid.get_neurons(neuron)
    # nl = pymaid.get_neurons(/EPG*)
    # print(nl)
    return nl

def colour_neuron(neuron_list=None,colour=None):
    cmap = {}
    var_type=str(type(neuron_list.id))
    print(neuron_list)
    print(var_type)
    if var_type == "<class 'numpy.ndarray'>":
        for neuron in range(0,len(neuron_list.id)):
            cmap[neuron_list[neuron].id]= colour,
    elif not var_type == "<class 'numpy.ndarray'>":
        cmap[neuron_list.id] = colour,
    return cmap


#variables
# ----------------------------------------------------------------------------------------
cmap ={}

# main code
# --------------------------------------------------------------------------------------
rm = pymaid.connect_catmaid(project_id=args.project_id)

print(args.neuron)

#specify by colour
if args.annotation:
    nl=neuron_by_annotation(args.neuron)
elif not args.annotation:
    nl = neuron_by_name(args.neuron)

cmap=colour_neuron(nl,(0,0,1))

#if getting by neuron name
# nl = pymaid.get_neurons(/EPG*)

# # Retrieve volume
# vol = pymaid.get_volume(['EB','PB'])
#
# # Set color and alpha
# print(vol)
# # vol.color = (0, 1, 0, .1)
# for key,value in vol.items():
#     value.color = (0, 1, 0, .1)
# # vol[1].color = (0, 1, 0, .1)
# print(vol['EB'])
# # print(vol.items(0))

# # Plot
# fig, ax = navis.plot2d([nl ,vol['EB'],vol['PB']], method='3d_complex')
# ax.dist = 6
# plt.show()

#plot using matplot
fig, ax = navis.plot2d(nl, color=cmap, method ='3d_complex')
#zoom
ax.dist = 6
#adjust perspective
for angle in range (0, 360, -87):
    ax.azim= angle

for angle in range (0, 360, -73):
    ax.elev= angle

print_to_output(args.outputfile)
plt.show()



