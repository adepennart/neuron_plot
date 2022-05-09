# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('using test_pymaid.py as main script')

import pymaid
import pandas
import matplotlib.pyplot as plt
import navis

try:
    while 1:
        user=input('Would you like to use the megalopta_OV stack as default(y/n)?\n')
        user=user.upper()
        if user.upper() == 'N' or user.upper() == 'NO':
            PROJECT_ID=input("type project_id of interest\n")
            break
        elif user.upper() == 'Y' or user.upper() == 'YES':
            PROJECT_ID =8
            break
except KeyError:
    print('not a string')
    exit()


rm = pymaid.connect_catmaid(project_id=PROJECT_ID)


skids = pymaid.get_skids_by_annotation(['AugusteTODO'])
print(skids)

nl = pymaid.get_neurons(skids)

# fig, ax = nl.plot2d()
# plt.show()

# Retrieve volume
# vol = pymaid.get_volume(['EB'])
vol = pymaid.get_volume(['EB','PB'])

# Set color and alpha
print(vol)
# vol.color = (0, 1, 0, .1)
for key,value in vol.items():
    value.color = (0, 1, 0, .1)
# vol[1].color = (0, 1, 0, .1)
print(vol['EB'])
# print(vol.items(0))

# Plot
fig, ax = navis.plot2d([nl ,vol['EB'],vol['PB']], method='3d_complex')
ax.dist = 6
plt.show()



fig, ax = navis.plot2d(nl[0], method='3d_complex')

# for i in range(0, 360, 10):
#    # Change rotation
#    ax.azim = i
#    # Save each incremental rotation as frame
#    plt.savefig('frame_{0}.png'.format(i), dpi=200)
#

#catmaid tutotiral
#https://pymaid.readthedocs.io/en/latest/source/intro.html

#fly brain catmaid tutorial
#https://www.virtualflybrain.org/docs/tutorials/3_pymaid/