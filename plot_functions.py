#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: plot_pymaid.py
Date: May 19th, 2022
Author: Auguste de Pennart
Description:
    plots a 2D representation of the neuron(s) of interest

List of functions:
    print_to_output:
        creates an output file of figure
    json_parse:
        parses json file
    colour_parser:
        associate each object to be coloured with correct colour
    colour_neuron:
        associate colour to neuron
    neuron_by_annotation:
        finds neurons on catmaid database by annotation
    neuron_by_name:
        finds neurons on catmaid database by name
    volume_build:
        finds volumes on catmaid database
    angle_build:
        change to desired figure perspective
    figure_build:
        create figure

List of "non standard modules"
    pymaid
        searching for data on catmaid database
    matplotlib.pyplot as plt
        plotting
    navis
        creating 2d plot data to be plotted with matplotlib
    matplotlib.colors
        allows for conversion between different colour naming types
    json
        reads json files

Procedure:
    NA

Usage:
    python plot_pymaid.py

known error:
 """

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # fix it so it displays name of file here
    print('using plot_functions.py as main script')


# functions
# ----------------------------------------------------------------------------------------

# print_to_output
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# outputfile:
# name of output file
# use:
# when outputfile specified creates an output file of figure
# return:
# no return
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def print_to_output(outputfile=None):
    import matplotlib.pyplot as plt
    try:
        plt.savefig(f'{outputfile}.pdf', transparent=True)
    except TypeError:
        pass


# json_parse
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# jsonfile:
# user-inputted json file
# user_colour:
# boolean, whether user-specified colours are used or not
# use:
# parses json file
# return:
# neuron_col_dict:
# dictionary of objects and colours
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def json_parse(jsonfile=None, user_colour=None):
    import json
    import matplotlib.colors
    # variables
    neur_col_dict = {}
    jsonfile = open(jsonfile, 'r')
    json_dict = json.load(jsonfile)
    # print(json_dict)
    jsonfile.close()
    if user_colour:
        for item in json_dict:
            if user_colour:
                for key, value in item.items():
                    # print(key, value)
                    if key == 'skeleton_id':
                        neuron = value
                    if key == 'color':
                        RGB = matplotlib.colors.to_rgba(value, item['opacity'])
                        # print((RGB))
                        temp_neur_col_dict = colour_parser(RGB, neuron)
                        neur_col_dict = {**neur_col_dict, **temp_neur_col_dict}
    elif not user_colour:
        neur_col_dict = []
        for item in json_dict:
            for key, value in item.items():
                # print(key, value)
                if key == 'skeleton_id':
                    neur_col_dict.append(value)
    print(neur_col_dict)
    return neur_col_dict


# colour_parser
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# colour_choice:
# user-inputted colours
# num_check:
# user-inputted object to be coloured
# use:
# associate each object to be coloured with correct colour
# return:
# neuron_col_dict:
# dictionary of objects and colours
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def colour_parser(colour_choice=None, num_check=None):
    import re
    # variables
    neur_col_dict = {}
    colour_list = []
    # for standard input
    if isinstance(colour_choice, list):
        for colour in colour_choice:
            match = re.findall('\d[\.]\d*|[\d]', colour)
            match = [float(x) for x in match]
            num_tup = tuple(match)
            colour_list.append(num_tup)
    # for json
    elif isinstance(colour_choice, tuple):
        num_check = [num_check]
        colour_list = [colour_choice]
    print(colour_list, num_check)
    if not colour_choice == None:
        try:
            if len(num_check) == len(colour_list):
                for number in range(0, len(num_check)):  # ensures same number of colours to objects to be coloured
                    neur_col_dict[num_check[number]] = colour_list[number]
            elif len(num_check) != len(colour_list):
                print("same number of neurons/volumes and colours needed")
                exit()
        except TypeError:
            print('colour but no neuron/volume provided, try again')
            exit()
    elif colour_choice == None:
        neur_col_dict = num_check
    # print(neur_col_dict)
    return neur_col_dict


# colour_neuron
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# neuron_data:
# user-inputted neuron(s)
# colour:
# user-inputted colour(s)
# use:
# associate colour to neuron
# return:
# cmap:
# dictionary of neurons to colours
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def colour_neuron(neuron_data=None, colour=None):
    # variables
    cmap = {}
    var_type = str(type(neuron_data.id))
    # print(var_type)
    # print(colour)
    if var_type == "<class 'numpy.ndarray'>":
        for neuron in range(0, len(neuron_data.id)):
            cmap[neuron_data[neuron].id] = colour,
    elif not var_type == "<class 'numpy.ndarray'>":
        cmap[neuron_data.id] = colour,
    # print(cmap)
    return cmap


# neuron_by_annotation
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# annotation:
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
    import pymaid
    # variables
    cmap = {}
    nl = pymaid.CatmaidNeuronList(None)
    # for user-input colour(s)
    if isinstance(annotation, dict):
        for annot, colour in annotation.items():
            skids = pymaid.get_skids_by_annotation(f'/{annot}')  # retrieve skeleton id(s)
            # print(skids)
            tempnl = pymaid.get_neurons(skids)  # retrieve neuron(s)
            # print(tempnl.id)
            tempcmap = colour_neuron(tempnl, colour)
            nl += tempnl
            cmap = {**cmap, **tempcmap}
        # print(cmap)
    # for default colour(s)
    elif isinstance(annotation, list):
        for annot in annotation:
            skids = pymaid.get_skids_by_annotation(f'/{annot}')  # retrieve skeleton id(s)
            nl += pymaid.get_neurons(skids)  # retrieve neuron(s)

        # print(nl)
    return nl, cmap


# neuron_by_name
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# neuron_data:
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
    import pymaid
    # variables
    cmap = {}
    nl = pymaid.CatmaidNeuronList(None)
    # for user-input colour(s)
    if isinstance(neuron_data, dict):
        for neuron, colour in neuron_data.items():
            # print(neuron,colour)
            # for standard input
            if not isinstance(neuron, int):
                tempnl = pymaid.get_neurons(f'/{neuron}')  # retrieve neuron(s)
                # print(tempnl.id)
            # for json
            elif isinstance(neuron, int):
                neuron = [neuron]
                tempnl = pymaid.get_neurons(neuron)  # retrieve neuron(s)
            tempcmap = colour_neuron(tempnl, colour)
            nl += tempnl
            cmap = {**cmap, **tempcmap}
        # print(cmap)
    # for default colour(s)
    elif isinstance(neuron_data, list):
        for neuron in neuron_data:
            # print(neuron)
            # for standard input
            if not isinstance(neuron, int):
                nl += pymaid.get_neurons(f'/{neuron}')  # retrieve neuron(s)
            # for json
            elif isinstance(neuron, int):
                neuron = [neuron]
                nl += pymaid.get_neurons(neuron)  # retrieve neuron(s)
    # print(nl)
    return nl, cmap


# volume_build
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# volume_data:
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
    # variables
    vol_list = []
    # for user-input volume colour(s)
    if isinstance(volume_data, dict):
        for volume, colour in volume_data.items():
            # print(volume, colour)
            vol = pymaid.get_volume(volume)  # retrieve volume
            if colour:
                vol.color = colour
                vol_list.append(vol)
    # for default volume colour(s)
    elif isinstance(volume_data, list):
        for volume in volume_data:
            vol = pymaid.get_volume(volume)  # retrieve volume
            vol_list.append(vol)
    # print(vol_list)
    return vol_list


# angle_build
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# axis:
# ax variable from plot2d
# perspective_list:
# list of figure distance, azimuth and elevation
# use:
# change to desired figure perspective
# return:
# axis:
# ax with new figure perspective
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def angle_build(axis=None, perspective_list=None):
    perspective_list = [int(x) for x in perspective_list]
    # adjust for negative angles
    if perspective_list[1] < 0:
        perspective_list[1] = 360 + perspective_list[1]
    if perspective_list[2] < 0:
        perspective_list[2] = 360 + perspective_list[2]
    axis.dist = perspective_list[0]  # zoom
    for angle in range(0, 360, perspective_list[1]):  # adjust azimuth
        axis.azim = angle
    for angle in range(0, 360, perspective_list[2]):  # adjust elevation
        axis.elev = angle
    return axis


# figure_build
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# neuron_data:
# neurons from catmaid database
# colour:
# associated user-inputted neuron colour
# volume:
# volume data from catmaid database
# perspective:
# list of figure distance, azimuth and elevation
# show_plot:
# boolean, whether plot is displayed or not
# use:
# create figure
# return:
# no return
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def figure_build(neuron_data=None, colour=None, volume=None, perspective=None, show_plot=None, outputfile=None):
    import matplotlib.pyplot as plt
    import navis
    if not perspective:
        perspective = [7, -90, 360]
    if volume:
        if colour:
            fig, ax = navis.plot2d([neuron_data, volume], color=colour, method='3d_complex')  # setup figure
            ax = angle_build(ax, perspective)
        elif not colour:
            fig, ax = navis.plot2d([neuron_data, volume], method='3d_complex')  # setup figure
            ax = angle_build(ax, perspective)
    elif not volume:
        if colour:
            fig, ax = navis.plot2d(neuron_data, color=colour, method='3d_complex')  # setup figure
            ax = angle_build(ax, perspective)
        elif not colour:
            fig, ax = navis.plot2d(neuron_data, method='3d_complex')  # setup figure
            ax = angle_build(ax, perspective)
    # print(ax)
    print_to_output(outputfile)
    if show_plot:
        plt.show()  # plot figure
