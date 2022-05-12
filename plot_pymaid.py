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
    4. options of colour, azimuth and elevation angles
    6. configuration file json
        https://stackoverflow.com/questions/11154946/require-either-of-two-arguments-using-argparse
    9. need some threshold, so not to break computer
    10. make regex and non regex option
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
req_arg.add_argument('-i', '--project_id',
                    metavar='PROJECT_ID',
                    dest='project_id',
                    required=True,
                    help='user-specified project id (ie. lamarcki_OV)')
#
#this needs to be updated
req_arg.add_argument('-n', '--neuron',
                    metavar='NEURON',
                    dest='neuron',
                    nargs='+',
                    required=True,
                    help='user-specified Neuron(s) of interest. REGEX accepted. ')
#this needs to be updated
parser.add_argument('-s', '--volume',
                    metavar='VOLUME',
                    dest='volume',
                    nargs='+',
                    help='user-specified Volume(s) of interest')
#this needs to be updated
parser.add_argument('-a', '--annotation',
                    dest='annotation',
                    action = 'store_true',
                    help='If looking through annotations and not neuron name, please select. REGEX accepted.')
#this needs to be updated
parser.add_argument('-c', '--colour',
                    metavar='COLOUR',
                    dest='colour',
                    nargs='+',
                    help='User-specified neuron colours, currently only RGBA argument accepted (ie. 0,1,0,.1)')
#this needs to be updated
parser.add_argument('-f', '--volume_colour',
                    metavar='VOLUME_COLOUR',
                    dest='volume_colour',
                    nargs='+',
                    help='User-specified volume colours, currently only RGBA argument accepted (ie. 0,1,0)')
#this needs to be updated
parser.add_argument('-p', '--perspective',
                    metavar='PERSPECTIVE',
                    dest='perspective',
                    nargs=3,
                    help='User-specified perspective for plot, default is 7, -90, 0 for camera distance, vertical rotational angle and horizontal rotational angle (ie. 6 87 73)')

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
#obselete
def print_to_output(outputfile=None):
    try:
        plt.savefig(f'{outputfile}.pdf', transparent=True)
    except TypeError:
        pass

#make dictionary of neuron type and colour
#create neurons
#crreate dictionary of neuron id and associated colour

def neuron_by_annotation(annotation=None):
    # print(nl)
    cmap = {}
    nl = pymaid.CatmaidNeuronList(None)
    if isinstance(annotation,dict):
        for key, value in annotation.items():
            skids = pymaid.get_skids_by_annotation(f'/{key}')
            # print(skids)
            tempnl = pymaid.get_neurons(skids)
            # print(tempnl.id)
            #going to make a nested forloop, sorry
            # print(value)
            tempcmap=colour_neuron(tempnl,value)
            nl += tempnl
            cmap= {**cmap,**tempcmap}
        # print(cmap)
    elif isinstance(annotation,list):
        for annot in annotation:
            skids = pymaid.get_skids_by_annotation(f'/{annot}')
            nl += pymaid.get_neurons(skids)
        # print(nl)
    return nl, cmap

#regex
def neuron_by_name(neuron_list=None):
    cmap = {}
    nl = pymaid.CatmaidNeuronList(None)
    if isinstance(neuron_list, dict):
        nl = pymaid.CatmaidNeuronList(None)
        for key, value in neuron_list.items():
            #regex inserted
            tempnl = pymaid.get_neurons(f'/{key}')
            # print(tempnl.id)
            # going to make a nested forloop, sorry
            # print(value)
            tempcmap = colour_neuron(tempnl, value)
            nl += tempnl
            cmap = {**cmap, **tempcmap}
        # print(cmap)
    elif isinstance(neuron_list, list):
        for neuron in neuron_list:
            # print(neuron)
            nl += pymaid.get_neurons(f'/{neuron}')
    # print(nl)
    return nl, cmap

def volume_build(volume_col_dict=None):
    vol_list=[]
    if isinstance(volume_col_dict, dict):
        for key, value in volume_col_dict.items():
            # print(key, value)
            # Retrieve volume
            vol = pymaid.get_volume(key)
            if value:
                vol.color = value
                vol_list.append(vol)
    elif isinstance(volume_col_dict, list):
        for volume in volume_col_dict:
            vol = pymaid.get_volume(volume)
            vol_list.append(vol)
    # print(vol_list)
    return vol_list

def colour_neuron(neuron_list=None,colour=None):
    cmap = {}
    var_type=str(type(neuron_list.id))
    # print(neuron_list)
    # print(var_type)
    # print(colour)
    # colour=int(colour)
    if var_type == "<class 'numpy.ndarray'>":
        for neuron in range(0,len(neuron_list.id)):
            # cmap[neuron_list[neuron].id]= colour,
            cmap[neuron_list[neuron].id]= colour,
    elif not var_type == "<class 'numpy.ndarray'>":
        cmap[neuron_list.id] = colour,
    return cmap

def colour_parser(colour_choice=None, num_check=None):
    type_col_dict = {}
    num_list = []
    # colour_list=args.colour
    colour_list = []
    #is if statement this redundant
    # if colour_choice:
    for colour in colour_choice:
        # print(colour)
        match = re.findall('\.\d|\d', colour)
        # print(match)
        match=[float(x) for x in match]
        print(match)
        num_tup = tuple(match)
        # print(num_tup)
        colour_list.append(num_tup)
        num_list = []
    # print(colour_list)
    for number in range(0,len(num_check)):
        if len(num_check) != len(colour_list):
            print("same number of neurons and colours needed")
            exit()
        elif len(num_check) == len(colour_list):
            type_col_dict[num_check[number]]=colour_list[number]
    # elif not colour_choice:
    #     for number in range(0, len(num_check)):
    #         type_col_dict[num_check[number]] = 0
    # print(type_col_dict)
    return type_col_dict

def angle_build(axis=None, perspective_list=None):
    perspective_list = [int(x) for x in perspective_list]
    # zoom
    axis.dist = perspective_list[0]
    # adjust perspective
    for angle in range(0, 360, perspective_list[1]):
        axis.azim = angle
    for angle in range(0, 360, perspective_list[2]):
        axis.elev = angle
    return axis

def figure_build(neuron_list=None,volume=None, perspective=None):
    if not perspective:
        perspective=[7,-90,360]
    if volume:
        if neuron_list[1]:
            # print([neuron_list[0], volume],)
            fig, ax = navis.plot2d([neuron_list[0], volume], color=neuron_list[1], method='3d_complex')
            #angle don't work
            #doesn\t work with multiple volumes
            ax = angle_build(ax, perspective)
        elif not neuron_list[1]:
            fig, ax = navis.plot2d([neuron_list[0], volume], method='3d_complex')
            ax = angle_build(ax, perspective)
    elif not volume:
        if neuron_list[1]:
            fig, ax = navis.plot2d(neuron_list[0], color=neuron_list[1], method='3d_complex')
            ax = angle_build(ax, perspective)
        elif not neuron_list[1]:
            fig, ax = navis.plot2d(neuron_list[0], method='3d_complex')
            ax = angle_build(ax, perspective)
    print_to_output(args.outputfile)
    plt.show()

#variables
# ----------------------------------------------------------------------------------------
type_col_dict={}
num_list=[]

# main code
# --------------------------------------------------------------------------------------

#is this needed?
if args.colour:
    type_col_dict=colour_parser(args.colour, args.neuron)

rm = pymaid.connect_catmaid(project_id=args.project_id)

#might not need to
#specify by colour
if args.annotation:
    if type_col_dict:
        nl_cmap=neuron_by_annotation(type_col_dict)
    elif not type_col_dict:
        nl_cmap = neuron_by_annotation(args.neuron)
elif not args.annotation:
    if type_col_dict:
        nl_cmap=neuron_by_name(type_col_dict)
    elif not type_col_dict:
        nl_cmap = neuron_by_name(args.neuron)

if args.volume:
    #no if statement needed, even when no args.volume_colour provided
    if args.volume_colour:
        vol_colour_dict=colour_parser(args.volume_colour, args.volume)
        # print(colour_list)
        volume=volume_build(vol_colour_dict)
    elif not args.volume_colour:
        volume = volume_build(args.volume)
    figure_build(nl_cmap,volume,args.perspective)
elif not args.volume:
    figure_build(nl_cmap,perspective=args.perspective)
