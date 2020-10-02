import operator
import os
import warnings
import vtk
import numpy as np
import pydicom
from dicom_contour.contour import coord2pixels, get_contour_dict, plot2dcontour, fill_contour
from vtk.util import numpy_support
import pyvista as py
import sys
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from glob import glob
import pydicom as dicom

name = 'patientname'
username = os.getlogin()
print(username)
path = filedialog.askdirectory()
print(path)

#rename dicom files
#
# l = glob('./{path}/*.dcm')
# for l in l:
#     ds= dicom.dcmread(l)
#     name = (str(ds.SOPInstanceUID))
#     os.rename(l , name)


def get_contour_file(path):
    """
    Get contour file from a given path by searching for ROIContourSequence

    Inputs:
            path (str): path of the the directory that has DICOM files in it, e.g. folder of a single patient
    Return:
        contour_file (str): name of the file with the contour
    """
    # handle `/` missing
    if path[-1] != '/': path += '/'
    # get .dcm contour file
    fpaths = [path + f for f in os.listdir(path)]
    n = 0
    for fpath in fpaths:
        f = pydicom.read_file(fpath)
        if 'ROIContourSequence' in dir(f):
            contour_file = fpath.split('/')[-1]
            n += 1
    if n > 1: warnings.warn("There are multiple files, returning the last one!")
    return contour_file


contour_file = get_contour_file(path)


def cfile2pixels(file, path, ROIContourSeq=0):
    """
    Given a contour file and path of related images return pixel arrays for contours
    and their corresponding images.
    Inputs
        file: filename of contour
        path: path that has contour and image files
        ROIContourSeq: tells which sequence of contouring to use default 0 (RTV)
    Return
        contour_iamge_arrays: A list which have pairs of img_arr and contour_arr for a given contour file
    """
    # handle `/` missing
    if path[-1] != '/': path += '/'
    f = pydicom.read_file(path + file)
    # index 0 means that we are getting RTV information
    RTV = f.ROIContourSequence[ROIContourSeq]
    # get contour datasets in a list
    contours = [contour for contour in RTV.ContourSequence]
    img_contour_arrays = [coord2pixels(cdata, path) for cdata in contours]
    return img_contour_arrays


contour_arrays = cfile2pixels(file=contour_file, path=path, ROIContourSeq=0)


# print(contour_arrays[0])

def slice_order(path):
    """
    Takes path of directory that has the DICOM images and returns
    a ordered list that has ordered filenames
    Inputs
        path: path that has .dcm images
    Returns
        ordered_slices: ordered tuples of filename and z-position
    """
    # handle `/` missing
    if path[-1] != '/': path += '/'
    slices = []
    for s in os.listdir(path):
        try:
            f = pydicom.read_file(path + '/' + s)
            f.pixel_array  # to ensure not to read contour file
            slices.append(f)
        except:
            continue

    slice_dict = {s.SOPInstanceUID: s.ImagePositionPatient[-1] for s in slices}
    ordered_slices = sorted(slice_dict.items(), key=operator.itemgetter(1))
    return ordered_slices


ordered_slices = slice_order(path)
#print(ordered_slices[:1])

print('*******************************')

contour_dict = get_contour_dict(contour_file, path, 0)

def get_data(path, index):
    """
    Generate image array and contour array
    Inputs:
        path (str): path of the the directory that has DICOM files in it
        contour_dict (dict): dictionary created by get_contour_dict
        index (int): index of the desired ROISequence
    Returns:
        images and contours np.arrays
    """
    images = []
    contours = []
    # handle `/` missing
    if path[-1] != '/': path += '/'
    # get contour file
    contour_file = get_contour_file(path)
    # get slice orders
    ordered_slices = slice_order(path)
    # get contour dict
    contour_dict = get_contour_dict(contour_file, path, index)

    for k, v in ordered_slices:
        # get data from contour dict
        if k in contour_dict:
            images.append(contour_dict[k][0])
            contours.append(contour_dict[k][1])
        # get data from dicom.read_file
        else:
            img_arr = pydicom.read_file(path + k + '').pixel_array
            contour_arr = np.zeros_like(img_arr)
            images.append(img_arr)
            contours.append(contour_arr)

    return np.array(images), np.array(contours)


images, contours_3d = get_data(path, index=0)
print('************---------------------****************')

x_coord = contours_3d[:,0]
y_coord = contours_3d[:,1]
z_coord = contours_3d[:,2]
print(x_coord.shape)
print(y_coord.shape)
print(z_coord.shape)
z,x,y = contours_3d.nonzero()


points = np.c_[z, x, y]
print(points.shape)
foo = py.PolyData(points)
# foo.save('./poly.ply')
print(type(foo))


nodes = points

point_cloud = py.PolyData(nodes)
point_cloud.plot(render_points_as_spheres=True, point_size=10)

meshko = point_cloud.triangulate().delaunay_3d()
meshko.plot()
meshko.save(f'C:\\Users\\{username}\\Desktop\\{name}.vtk')

m = meshko.extract_surface()
m.plot()
print(type(meshko))

def writeSTL(p):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(p)

    surface_filter = vtk.vtkDataSetSurfaceFilter()
    surface_filter.SetInputConnection(reader.GetOutputPort())

    triangle_filter = vtk.vtkTriangleFilter()
    triangle_filter.SetInputConnection(surface_filter.GetOutputPort())

    writer = vtk.vtkSTLWriter()
    writer.SetFileName(f'C:\\Users\\{username}\\Desktop\\{name}.stl')
    writer.SetInputConnection(triangle_filter.GetOutputPort())
    writer.Write()

writeSTL(f'C:\\Users\\{username}\\Desktop\\{name}.vtk')


param1 = f'C:\\Users\\{username}\\Desktop\\{name}.vtk'
param2 = f'C:\\Users\\{username}\\Desktop\\{name}.stl'
param3 =f'C:\\Users\\{username}\\Desktop\\TBALL-CUBE-{name}.stl'
###### CALL .BAT FILE WITH ARGUMENTS########
