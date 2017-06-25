'''
BEGIN GPL LICENSE BLOCK

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

END GPL LICENCE BLOCK
'''

bl_info = {  
 "name": "markers_list",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 3),  
 "blender": (2, 7 , 3),  
 "location": "View3D",  
 "description": "show markers list ",  
 "warning": "",  
 "wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Animation/Markers_list",  
 "tracker_url": "",  
 "category": "Mesh"} 

import bpy
import bmesh
import mathutils
import math
import sys

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

list= [] 

    
def frame_to_time(frame_number, fps):
    raw_time = (frame_number - 1) / fps
    return round(raw_time, 3)

def draw(self, context):
    for a in list:
        self.layout.label(a)
        
def markers_list_config(scene, context):
    items = [("-1", "","")]

    if 1>0 :
             #print(context.scene.text)
        scena = bpy.context.scene
        fps = scena.render.fps
        fps_base = scena.render.fps_base
        
        
        
        for k, v in scena.timeline_markers.items():
            frame = v.frame
            frame_time = frame_to_time(frame, fps)
            #print(frame, frame_time, v.name)
            #imprimir = "Marker: "+ str(v.name) + " Frame:" + str(frame) +  " Frame Time: " + str(frame_time)
            imprimir = (v.name)
            
            list.append(str(imprimir))
            

        list.sort(key = str.lower) 
        
        
        for i in list:
            for k, v in scena.timeline_markers.items():
                if i ==  v.name:
                    if len(bpy.context.scene.text)== 0:
                        items.append((str(v.frame),str(v.name),""))
                    elif len(bpy.context.scene.text)== 1 and (str(bpy.context.scene.text) == " "):
                        items.append((str(v.frame),str(v.name),"")) 
                    elif len(bpy.context.scene.text)== 1 and (str(bpy.context.scene.text) != " "):
                        if str(bpy.context.scene.text.capitalize()) in str(i.capitalize()):
                            marcador = (str(v.frame),str(v.name),"")
                            if marcador not in items:
                                items.append(marcador)
                    else: 
                        entrada = bpy.context.scene.text.split(" ")
                        nombres = i.split(" ")
                        
                        contador = 0
                                               
                        for a in entrada: 
                            for b in nombres:
                                
                                if str(a.capitalize()) in b.capitalize():
                                    contador +=1
                                print (a, " ", b)
                                print (contador)
                                if contador >= len(entrada):
                                    marcador = (str(v.frame),str(v.name),"")
                                    if marcador not in items:
                                        items.append(marcador)
                            
                    
                
          
        contador = 0
        for b in bpy.data.texts:
            if b.name == "marker's list":
                contador += 1
                bpy.data.texts["marker's list"].clear()
                
        if contador == 0:
            bpy.data.texts.new(name="marker's list")
        
        for a in list:
            #print(a)
            bpy.data.texts["marker's list"].write(a)
            bpy.data.texts["marker's list"].write("\n")
            
        #bpy.context.window_manager.popup_menu(draw, title="Markers list", icon='INFO')
        
        while len(list) !=0:
            list.remove(list[0])
            
           
    
        

    return items

def set_frame(self, context):

    bpy.context.scene.frame_set(int(bpy.context.scene.markers.markers_list))
    return None
  
class menu_enum(PropertyGroup):
    
    markers_list = EnumProperty(
        attr="mark_list",
        name="Marker's List", 
        description="",
        items=markers_list_config,
        #default="-1",
        options={'ANIMATABLE'},
        update=set_frame, 
        get=None, 
        set=None)
        
    
    
class ShowMarkersOperatorPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Show Markers list"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)
    
    def draw(self, context):
        
        layout = self.layout 
        scene = context.scene
        
        
        #row = layout.row(align=True)
        
        #row.operator(ShowMarkersOperator.bl_idname) 
        
        layout = self.layout
        col = layout.column()
        col.prop(scene.markers, "markers_list", text="")
        
        col.prop(context.scene, "text", text="")



    

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.markers = PointerProperty(type=menu_enum)

    bpy.types.Scene.text = bpy.props.StringProperty(name="Find Marker",
                                    description="",
                                    default="", 
                                    #maxlen=0,
                                    options={'ANIMATABLE'},
                                    subtype='NONE',
                                    update=None, 
                                    get=None, 
                                    set=None)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.markers
    del bpy.types.Scene.text


if __name__ == "__main__":
    register()