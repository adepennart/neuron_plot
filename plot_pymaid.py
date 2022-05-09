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
    1. should put user input for neuron
    2. should check both name of neurons and annotations
    3. should put user input for volume
    4. options of colour, azimuth and elevation angles
    3. perhaps option of saving
 """

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #fix it so it displays name of file here
    print('using plot_pymaid.py as main script')

import sys
from pathlib import Path
import pymaid
import pandas
import matplotlib.pyplot as plt
import navis

# allows for different file names to be adjusted easily for user
outputfile = 'neuron_fig1.png'

# uses the files specified by user
if len(sys.argv) == 1:
   outputfile = outputfile

# exits script if unexpected arguments in commandline.
else:
    try:
        raise ArithmeticError
    except:
        print("wrong number of arguments, try again")
        exit()

try:
    while 1:
        user=input('Would you like to use the lamarckii_OV stack as default(y/n)?\n')
        user=user.upper()
        if user.upper() == 'N' or user.upper() == 'NO':
            PROJECT_ID=input("type project_id of interest\n")
            break
        elif user.upper() == 'Y' or user.upper() == 'YES':
            PROJECT_ID =11
            break
except KeyError:
    print('not a string')
    exit()

#variables
cmap ={}


rm = pymaid.connect_catmaid(project_id=PROJECT_ID)


skids = pymaid.get_skids_by_annotation(['EPG','PEN'])
print(skids)

nl = pymaid.get_neurons(skids)
# print(nl)
for neuron in range(0,4):
    cmap[nl[neuron].id]= (0,0,1),
cmap[nl[4].id]= (1,0,0)
print(cmap)

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

plt.savefig('figure_1.pdf', transparent=True)
plt.show()

# output = open(outputfile, 'w')
# print(plt, file=output)
# output.close()
