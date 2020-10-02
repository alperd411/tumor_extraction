import pydicom as dicom
import numpy as np
import os
from glob import glob

path = './ct/'


# ds = dicom.dcmread(path)
# print(ds.dir())

l = glob('./{path}/*.dcm')
for l in l:
    ds= dicom.dcmread(l)
    name = (str(ds.SOPInstanceUID))
    os.rename(l , name)

# x = (ds.data_element("SOPInstanceUID"))
# name = (str(ds.SOPInstanceUID))
# os.rename()