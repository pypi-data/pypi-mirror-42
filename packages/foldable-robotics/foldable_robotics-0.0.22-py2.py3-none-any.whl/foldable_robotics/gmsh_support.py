# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 15:03:43 2019

@author: danaukes
"""

import subprocess
import numpy        
import matplotlib.pyplot as plt
import shapely
import shapely.geometry as sg
from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import meshio
import idealab_tools.plot_tris
import numpy
import os

class GmshObject(object):
    ii = 0
    
    def assign_id(self):    
        type(self).ii+=1
        self.id = type(self).ii
    pass

class Point(GmshObject):

    def __init__(self,x,y,z,p):
        self.x = x
        self.y = y
        self.z = z
        self.p = p
        self.assign_id()
    
    def comp(self):
        return self.x,self.y,self.z,self.p

    def string(self):
        my_string = '//+\nPoint({0:d}) = {5}{1:.3f},{2:.3f},{3:.3f},{4:.3f}{6};\n'.format(self.id,self.x,self.y,self.z,self.p,'{','}')
        return my_string

class Line(GmshObject):

    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.assign_id()

    def string(self):
        my_string = '//+\nLine({0:d}) = {{{1:d},{2:d}}};\n'.format(self.id,self.p1.id,self.p2.id)
        return my_string

class Loop(GmshObject):
    
    def __init__(self,*lines):
        self.lines = lines
        self.assign_id()
    
    def string(self):
        a = ['{0:d}'.format(line.id) for line in self.lines]
        b = ','.join(a)
        my_string = '//+\nLine Loop({0:d}) = {{{1}}};\n'.format(self.id,b)
        return my_string

class Surface(GmshObject):

    def __init__(self,loop):
        self.loop = loop
        self.assign_id()

    def string(self):
        my_string = '//+\nPlane Surface({0:d}) = '.format(self.id)+'{'+'{0:d}'.format(self.loop.id)+'};\n'
        return my_string

class Extrude(GmshObject):

    def __init__(self,surface,t):
        self.surface = surface
        self.t = t
        self.assign_id()
    def string(self):
        my_string = '//+\nExtrude {'+'0,0,{0:.3f}'.format(self.t)+'} {\n  Surface{'+'{0:d}'.format(self.surface.id)+'};\n}\n'
        return my_string
    def extruded_points(self):
        tuples = [line.p1.comp() for line in self.surface.loop.lines]
        tuples = [(x,y,z+self.t,p) for x,y,z,p in tuples]
        return tuples

class Coherence(GmshObject):

    def __init__(self,l1_volumes,l2_volumes):
        self.l1_volumes = l1_volumes
        self.l2_volumes = l2_volumes
        self.assign_id()
    def string(self):
        a=['Volume{{{0}}}'.format(item.id) for item in self.l1_volumes]
        aa = '; '.join(a)

        b=['Volume{{{0}}}'.format(item.id) for item in self.l2_volumes]
        bb = '; '.join(b)
        my_string = '''//+
r()=BooleanFragments{{ {0}; Delete; }}{{ {1}; Delete; }};
// Printf("resulting geometries: ", r());
// Printf("size of r: ",#r());
'''.format(aa,bb)
        return my_string


class GeoFile(object):
    template = '''
    SetFactory("OpenCASCADE");
    Geometry.LineNumbers = 0;
    Geometry.SurfaceNumbers = 0;
    '''
    def __init__(self):
        self.points = []
        self.lines = []
        self.loops = []
        self.surfaces = []
        self.extrusions= []
        self.layer_coherence = []
        
    def string(self):
        b = ''.join([point.string() for point in self.points])
        c = ''.join([line.string() for line in self.lines])
        d = ''.join([loop.string() for loop in self.loops])
        e = ''.join([surface.string() for surface in self.surfaces])
        f = ''.join([extrusion.string() for extrusion in self.extrusions])
        g = ''.join([item.string() for item in self.layer_coherence])
        return self.template+b+c+d+e+f+g
    
    def point_tuples(self):
        return [item.comp() for item in self.points]

    def make_mesh(self,delete_files=True):
        with open('output.geo','w') as f:
            f.writelines(self.string())
        
        string = 'gmsh output.geo -3 -format msh'
        p = subprocess.Popen(string)
        p.wait()
        mesh_file = 'output.msh'
        data = meshio.read(mesh_file)
        if delete_files:
            os.remove('output.msh')
            os.remove('output.geo')
        return data


def laminate_to_geo(lam):
    z=0
    t = 1
    geofile = GeoFile()
    extrusions_by_layer = []
    
    for layer in lam:
        extrusions = []
        for geo in layer.geoms:
            if isinstance(geo,sg.Polygon):
                xy = list(geo.exterior.coords)
                xyzp = [(coord[0],coord[1],z,1) for coord in xy]
                points = [Point(*item) for item in xyzp]
                lines = [Line(ii,jj) for ii,jj in zip(points[:-1],points[1:])]
    #            lines.append(Line(points[-1],points[0]))
                loop = Loop(*[line for line in lines])
                surface = Surface(loop)
                extrusion = Extrude(surface,t)
    
                extrusions.append(extrusion)
    
                geofile.points.extend(points)
                geofile.lines.extend(lines)
                geofile.loops.append(loop)
                geofile.surfaces.append(surface)
                geofile.extrusions.append(extrusion)
    
        extrusions_by_layer.append(extrusions)
        z+=t
   
    for ext1,ext2 in zip(extrusions_by_layer[:-1],extrusions_by_layer[1:]):
        geofile.layer_coherence.append(Coherence(ext1,ext2))

    return geofile

if __name__=='__main__':
    tri = sg.Polygon([(0,0),(1,0),(1,1)])
    tri

    circle = sg.Point(0,0).buffer(.5)
    circle

    square = sg.box(-1,-1,-.25,1)


    lam = Laminate(Layer(circle),Layer(tri,square))
    lam = lam.simplify(.001)
    lam.plot(new=True)

        
    geofile = laminate_to_geo(lam)
    data = geofile.make_mesh()

                
    #print(geofile.string())


    quads = data.cells['tetra']
    tris = data.cells['triangle']
    points = data.points
    face_colors = numpy.array([(1,0,0,.5) for item in tris])
    idealab_tools.plot_tris.plot_tris(points,tris,face_colors=face_colors,drawEdges=True, edgeColor = (0,0,0,1))