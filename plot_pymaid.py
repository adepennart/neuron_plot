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
    1. Takes project id and either json file or, via standard input, neuron(s) of interest
    2. logs into Catmaid account
    3. plots neurons in 2D with optional print to output file

Usage:
    python plot_pymaid.py [-h] [-v] -i PROJECT_ID
                      (-j JSON | -n NEURON [NEURON ...]) [-a]
                      [-V VOLUME [VOLUME ...]] [-c COLOUR [COLOUR ...]]
                      [-C VOLUME_COLOUR [VOLUME_COLOUR ...]]
                      [-p PERSPECTIVE PERSPECTIVE PERSPECTIVE] [-o OUTPUT]

known error:
    9. need some threshold, so not to break computer
    10. make regex and non regex option, currently standard input is regex and json is not regex
    11. create an error if no comma found for colours, if i want before the program does
    13. can put type=int and default=### in argparse
    14. better naming for search term used for neurons
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
import matplotlib.colors
import json

#argparse
# ----------------------------------------------------------------------------------------
#program description
usage='plots a 2D representation of the neurons of interest'
parser=argparse.ArgumentParser(description=usage)#create an argument parser
reqgroup= parser.add_argument_group(title='required arguments')
exgroup = parser.add_argument_group(title='one or the other')
group = exgroup.add_mutually_exclusive_group(required=True)
optgroup= parser.add_argument_group(title='optional arguments with project id')
#creates the argument for program version
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 1.0')
#make sure number
reqgroup.add_argument('-i', '--project_id',
                    metavar='PROJECT_ID',
                    dest='project_id',
                    required=True,
                    help='user-specified project id (ie. lamarcki_OV)')

#this needs to be updated
group.add_argument('-j', '--json',
                    metavar='JSON',
                    dest='json',
                    help='user-specified catmaid json file')
#this needs to be updated
group.add_argument('-n', '--neuron',
                    metavar='NEURON',
                    dest='neuron',
                    nargs='+',
                    help='user-specified Neuron(s) of interest. REGEX accepted. ')
#this needs to be updated
optgroup.add_argument('-a', '--annotation',
                    dest='annotation',
                    action = 'store_true',
                    help='If looking through annotations and not neuron name, please select. REGEX accepted.')
#this needs to be updated
optgroup.add_argument('-V', '--volume',
                    metavar='VOLUME',
                    dest='volume',
                    nargs='+',
                    help='user-specified Volume(s) of interest')
#this needs to be updated
optgroup.add_argument('-c', '--colour',
                    metavar='COLOUR',
                    dest='colour',
                    nargs='+',
                    help='User-specified neuron colours, currently only RGBA argument accepted (ie. 0,1,0,.1)')
#this needs to be updated
optgroup.add_argument('-C', '--volume_colour',
                    metavar='VOLUME_COLOUR',
                    dest='volume_colour',
                    nargs='+',
                    help='User-specified volume colours, currently only RGBA argument accepted (ie. 0,1,0,.1)')
#this needs to be updated
optgroup.add_argument('-p', '--perspective',
                    metavar='PERSPECTIVE',
                    dest='perspective',
                    nargs=3,
                    help='User-specified perspective for plot, default is 7, -90, 0 for camera distance, vertical rotational angle and horizontal rotational angle (ie. 6 87 73)')
#creates the optinal argument for output file name
parser.add_argument('-o', '--output',
                    metavar='OUTPUT',
                    dest='outputfile',
                    help='optional plot output file')
args=parser.parse_args()#parses command line

#functions
# ----------------------------------------------------------------------------------------

# print_to_output
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #outputfile:
        # name of output file
# use:
    # when outputfile specified creates an output file of figure
# return:
    # no return
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_to_output(outputfile=None):
    try:
        plt.savefig(f'{outputfile}.pdf', transparent=True)
    except TypeError:
        pass

# colour_parser
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #colour_choice:
        # user-inputted colours
    #num_check:
        # user-inputted object to be coloured
# use:
    # associate each object to be coloured with correct colour
# return:
    # neuron_col_dict:
        # dictionary of objects and colours
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def colour_parser(colour_choice=None, num_check=None):
    # variables
    neur_col_dict = {}
    colour_list = []
    # for standard input
    if not isinstance(colour_choice, tuple):
        for colour in colour_choice:
            match = re.findall('\d[\.]\d*|[\d]', colour)
            match = [float(x) for x in match]
            num_tup = tuple(match)
            colour_list.append(num_tup)
    # for json
    elif isinstance(colour_choice, tuple):
        num_check = [num_check]
        colour_list = [colour_choice]
    # print(colour_list, num_check)
    for number in range(0, len(num_check)): #ensures same number of colours to objects to be coloured
        if len(num_check) != len(colour_list):
            print("same number of neurons and colours needed")
            exit()
        elif len(num_check) == len(colour_list):
            neur_col_dict[num_check[number]] = colour_list[number]
    # print(neur_col_dict)
    return neur_col_dict

# colour_neuron
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #neuron_data:
        # user-inputted neuron(s)
    #colour:
        # user-inputted colour(s)
# use:
    # associate colour to neuron
# return:
    # cmap:
        # dictionary of neurons to colours
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def colour_neuron(neuron_data=None,colour=None):
    #variables
    cmap = {}
    var_type=str(type(neuron_data.id))
    # print(var_type)
    # print(colour)
    if var_type == "<class 'numpy.ndarray'>":
        for neuron in range(0,len(neuron_data.id)):
            cmap[neuron_data[neuron].id]= colour,
    elif not var_type == "<class 'numpy.ndarray'>":
        cmap[neuron_data.id] = colour,
    # print(cmap)
    return cmap

# neuron_by_annotation
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #annotation:
        # dictionary of neurons by annotation and associated colours
        # or
        # list of neurons by annotation
# use:
    # finds neurons on catmaid database by annotation
# return:
    # nl:
        # neurons from catmaid database
    # cmap:
        # associated user-inputted neuron colour (if applicable)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def neuron_by_annotation(annotation=None):
    #variables
    cmap = {}
    nl = pymaid.CatmaidNeuronList(None)
    #for user-input colour(s)
    if isinstance(annotation,dict):
        for annot, colour in annotation.items():
            skids = pymaid.get_skids_by_annotation(f'/{annot}') # retrieve skeleton id(s)
            # print(skids)
            tempnl = pymaid.get_neurons(skids) # retrieve neuron(s)
            # print(tempnl.id)
            tempcmap=colour_neuron(tempnl,colour)
            nl += tempnl
            cmap= {**cmap,**tempcmap}
        # print(cmap)
    #for default colour(s)
    elif isinstance(annotation,list):
        for annot in annotation:
            skids = pymaid.get_skids_by_annotation(f'/{annot}') # retrieve skeleton id(s)
            nl += pymaid.get_neurons(skids) # retrieve neuron(s)

        # print(nl)
    return nl, cmap

# neuron_by_name
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #neuron_data:
        # dictionary of neurons by name and associated colours
        # or
        # list of neurons by name
# use:
    # finds neurons on catmaid database by name
# return:
    # nl:
        # neurons from catmaid database
    # cmap:
        # associated user-inputted neuron colour (if applicable)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def neuron_by_name(neuron_data=None):
    #variables
    cmap = {}
    nl = pymaid.CatmaidNeuronList(None)
    #for user-input colour(s)
    if isinstance(neuron_data, dict):
        for neuron, colour in neuron_data.items():
            # print(neuron,colour)
            #for standard input
            if not isinstance(neuron, int):
                tempnl = pymaid.get_neurons(f'/{neuron}') # retrieve neuron(s)

                # print(tempnl.id)
            #for json
            elif isinstance(neuron, int):
                neuron = [neuron]
                tempnl = pymaid.get_neurons(neuron) # retrieve neuron(s)
            tempcmap = colour_neuron(tempnl, colour)
            nl += tempnl
            cmap = {**cmap, **tempcmap}
        # print(cmap)
    #for default colour(s)
    elif isinstance(neuron_data, list):
        for neuron in neuron_data:
            # print(neuron)
            nl += pymaid.get_neurons(f'/{neuron}') # retrieve neuron(s)
    # print(nl)
    return nl, cmap

# volume_build
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #volume_data:
        # dictionary of volumes and associated colours
        # or
        # list of volumes
# use:
    # finds volumes on catmaid database
# return:
    # vol_list:
        # volume data from catmaid database
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def volume_build(volume_data=None):
    #variables
    vol_list=[]
    #for user-input volume colour(s)
    if isinstance(volume_data, dict):
        for volume, colour in volume_data.items():
            # print(volume, colour)
            vol = pymaid.get_volume(volume) # retrieve volume
            if colour:
                vol.color = colour
                vol_list.append(vol)
    #for default volume colour(s)
    elif isinstance(volume_data, list):
        for volume in volume_data:
            vol = pymaid.get_volume(volume) # retrieve volume
            vol_list.append(vol)
    # print(vol_list)
    return vol_list

# angle_build
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #axis:
        # ax variable from plot2d
    #perspective_list:
        # list of figure distance, azimuth and elevation
# use:
    # change to desired figure perspective
# return:
    # axis:
        # ax with new figure perspective
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def angle_build(axis=None, perspective_list=None):
    perspective_list = [int(x) for x in perspective_list]
    #adjust for negative angles
    if perspective_list[1] < 0:
        perspective_list[1]= 360 + perspective_list[1]
    if perspective_list[2] < 0:
        perspective_list[2] = 360 + perspective_list[2]
    axis.dist = perspective_list[0]  # zoom
    for angle in range(0, 360, perspective_list[1]): # adjust azimuth
        axis.azim = angle
    for angle in range(0, 360, perspective_list[2]): #adjust elevation
        axis.elev = angle
    return axis

# figure_build
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #neuron_data:
        # neurons from catmaid database
        # and
        # associated user-inputted neuron colour (if applicable)
    #volume:
        # volume data from catmaid database
    #perspective:
        # list of figure distance, azimuth and elevation
# use:
    # create figure
# return:
    # no return
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def figure_build(neuron_data=None,volume=None, perspective=None):
    if not perspective:
        perspective=[7,-90,360]
    if volume:
        if neuron_data[1]:
            fig, ax = navis.plot2d([neuron_data[0], volume], color=neuron_data[1], method='3d_complex') #setup figure
            ax = angle_build(ax, perspective)
        elif not neuron_data[1]:
            fig, ax = navis.plot2d([neuron_data[0], volume], method='3d_complex') #setup figure
            ax = angle_build(ax, perspective)
    elif not volume:
        if neuron_data[1]:
            fig, ax = navis.plot2d(neuron_data[0], color=neuron_data[1], method='3d_complex') #setup figure
            ax = angle_build(ax, perspective)
        elif not neuron_data[1]:
            fig, ax = navis.plot2d(neuron_data[0], method='3d_complex') #setup figure
            ax = angle_build(ax, perspective)
    # print(ax)
    print_to_output(args.outputfile)
    plt.show() #plot figure

# main code
# --------------------------------------------------------------------------------------
rm = pymaid.connect_catmaid(project_id=args.project_id)#open Catmaid to project id

if args.json:
    neur_col_dict={}
    inputted = open(args.json, 'r')
    json_file = json.load(inputted)
    # print(json_file)
    inputted.close()
    for item in json_file:
        for key, value in item.items():
            # print(key, value)
            if key == 'skeleton_id':
                neuron=value
            if key == 'color':
                RGB=matplotlib.colors.to_rgba(value,item['opacity'])
                # print((RGB))
                temp_neur_col_dict=colour_parser(RGB,neuron)
                neur_col_dict = {**neur_col_dict, **temp_neur_col_dict}
    nl_cmap=neuron_by_name(neur_col_dict)

#is this needed?
if args.colour:
    neur_col_dict=colour_parser(args.colour, args.neuron)

if not args.json:
    if args.annotation:
        if neur_col_dict:
            nl_cmap=neuron_by_annotation(neur_col_dict)
        elif not neur_col_dict:
            nl_cmap = neuron_by_annotation(args.neuron)
    elif not args.annotation:
        if neur_col_dict:
            nl_cmap=neuron_by_name(neur_col_dict)
        elif not neur_col_dict:
            nl_cmap = neuron_by_name(args.neuron)

if args.volume:
    if args.volume_colour:
        vol_colour_dict=colour_parser(args.volume_colour, args.volume)
        volume=volume_build(vol_colour_dict)
    elif not args.volume_colour:
        volume = volume_build(args.volume)
    figure_build(nl_cmap,volume,args.perspective)
elif not args.volume:
    figure_build(nl_cmap,perspective=args.perspective)
