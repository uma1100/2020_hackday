import hid
import re

VENDOR_ID = 0x057E
L_PRODUCT_ID = 0x2006
R_PRODUCT_ID = 0x2007

for device in hid.enumerate(0, 0):
    str = ''
    for k, v in device.items():
        str += '{} : {} \n'.format(k, v)
    if 'Joy-Con' in str :
        print (str)
        print ('')