# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:23:36 2019

@author: daukes
"""

import yaml
import numpy
import matplotlib.pyplot as plt
import os
import shapely.geometry as sg
from foldable_robotics.layer import Layer
import foldable_robotics.layer

class obj(object):
    pass

def objectify(var):
    if isinstance(var,dict):
        new_var = obj()
        for key,value in var.items():
            setattr(new_var,key,objectify(value))
        return new_var
    elif isinstance(var,list):
        new_var = [objectify(item) for item in var]
        return new_var
    else: 
        return var    
        
class Component(object):
    pass

class Face(object):
    pass

def create_loops(filename):
#    plt.figure()
    with open(filename) as f:
        data1 = yaml.load(f)
    data = objectify(data1)
    global_transform = numpy.array(data.transform)
    components = []
    for component in data.components:
        new_component = Component()
        local_transform = numpy.array(component.transform)
        T = local_transform.dot(global_transform)
        faces = []
        for face in component.faces:
            new_face = Face()
            loops = []
            for loop in face.loops:
                loop = numpy.array(loop)
                loop_a = numpy.hstack([loop,numpy.ones((len(loop),1))])
                loop_t = loop_a.dot(T)
                loop_out = loop_t[:,:2].tolist()
                loops.append(loop_out)
#                plt.fill(loop_t[:,0],loop_t[:,1])
            new_face.loops = loops
            faces.append(new_face)
        new_component.faces = faces
        components.append(new_component)
    return components

def component_to_layer(component):
    faces = []
    for face in component.faces:
        loops = []
        for loop in face.loops:
            loops.append(Layer(sg.Polygon(loop)))
        if not not loops:
            face_new = loops.pop(0)            
            for item in loops:
                face_new^=item
            faces.append(face_new)
    if not not faces:
        component_new = faces.pop(0)
        for item in faces:
            component_new|=item
        return component_new
            
def get_joints(*component_layers,round_digits):
    segments = []
    for layer in component_layers:
        segments.extend(layer.get_segments())
    
    segments = [tuple(sorted(item)) for item in segments]
    segment_array = numpy.array(segments)
    segment_array = segment_array.round(round_digits)
    segments2 = [(tuple(a),tuple(b)) for a,b in segment_array.tolist()]    
    segments3 = list(set(segments2))
    
    ii = [segments3.index(item) for item in segments2]
    jj = list(set(ii))
    kk = [ii.count(item) for item in jj]
    ll = [segments3[aa] for aa,bb in zip(jj,kk) if bb>1]

    mm = []
    for item in ll:
        mm.append(segments2.index(item))
        
    nn = [segments[ii] for ii in mm]
    
    return nn

def length(segment):
    segment = numpy.array(segment)
    v = segment[1]-segment[0]
    l=((v**2).sum())**.5
    return l
                
if __name__=='__main__':
    user_path = os.path.abspath(os.path.expanduser('~'))
    folder = os.path.join(user_path,'class_foldable_robotics/cad/spherical_example')
    filename = os.path.normpath(os.path.join(folder,'input.yaml'))
    components = create_loops(filename)
    layers = [component_to_layer(item) for item in components]
    layer2 = Layer()
    for item in layers:
        layer2 |= item>>1e-3
    layer2.plot(new=True)
#    
    round_digits = 2
    
    segments = get_joints(*layers,round_digits=round_digits)
    lengths = [length(item) for item in segments]
    max_length = max(lengths)
    valid_segments = [item for item,l in zip(segments,lengths) if l>max_length/1000]
    
    linestrings = [sg.LineString(item) for item in valid_segments]
    joints = Layer(*linestrings)
    joints.plot()
#    for segment in segments:
#        segment = numpy.array(segment)
#        plt.plot(segment[:,0],segment[:,1])

#    layer2.export_dxf('bodies')
#    joints.export_dxf('joints')
    
    
    import ezdxf
    dwg = ezdxf.new('R2010')
    msp = dwg.modelspace()

    import foldable_robotics.dxf

    dxf_layer_body = dwg.layers.new(name='body', dxfattribs={'color': foldable_robotics.dxf.to_index[0xff0000]})    
    dxf_layer_joints= dwg.layers.new(name='joints', dxfattribs={'color': foldable_robotics.dxf.to_index[0x0000ff]})    

    for path in layer2.get_paths():
        msp.add_lwpolyline(path,dxfattribs={'layer': 'body'})
    for path in joints.get_paths():
        msp.add_lwpolyline(path,dxfattribs={'layer': 'joints'})

    full_output = os.path.join(user_path,'desktop','design.dxf')
    dwg.saveas(full_output)            
    
#    msp.add_line((0, 0), (10, 0), dxfattribs={'layer': 'Lines'})
#    
#    
##        loops = self.exteriors()+self.interiors()
#        for geom in self.geoms:
#            if isinstance(geom,sg.Polygon):
#                exterior = list(geom.exterior.coords)
#                interiors = [list(interior.coords) for interior in geom.interiors]
#                loops = [exterior]+interiors
#
#            elif isinstance(geom,sg.LineString):
#                line = list(geom.coords)
#                loops = [line]
#            
#            for loop in loops:
#                msp.add_lwpolyline(loop)
#        dwg.saveas(name+'.dxf')    