# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('using test_pymaid.py as main script')

import pymaid
import pandas

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
