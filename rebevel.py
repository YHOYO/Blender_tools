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
 "name": "Re-bevel",  
 "author": "Diego Quevedo ( http://doshape.com/ )",  
 "version": (1, 0),  
 "blender": (2, 7 , 3),  
 "location": "View3D > EditMode > ToolShelf",  
 "description": "allow create the faces as Bevel vertex",  
 "warning": "",  
 "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Modeling/ReBevel",  
 "tracker_url": "",  
 "category": "Doshape"} 

import bpy
import bmesh
import mathutils
import math

def arco(self, bm, C, u, v, divisiones):
    '''
    crea los vertices (puntos) de un arco centrado en C, con cordenadas iniciales de los puntos u  v
    Devuelve una lista  con los puntos creados
    
    nota. aunque slerp crea los puntos de manera adecuada, es necesario recalcular la distancia de los puntos
    
    para que se creen todas las caras de u a v, el rango debe ser el total de divisiones + 1
    
    
    '''
    a = u-C
    b= v-C
        
    da = calcularLargos(bm, C, u)
    db = calcularLargos(bm, C, v)
    l= []    
    
    for k in range(0, divisiones+1, 1):          
        try:
            p = a.slerp(b,k/divisiones) 
        except:
            self.report({'ERROR'}, "Opposite Vectors Unsupported")
            return {'CANCEL'}
        p = p+C     
        
        p= puntoColinear(C,p, da)        
       # dc = calcularLargos(bm, C, p)     
  
        v3 = bm.verts.new(p)
        v3.select = True   
        
        l.append(v3)
    
    return l


def puntoColinear(v1,v2, distancia):
    
    '''
    Devuelve las coordenadas de un nuevo punto colinear a otros dos a una distancia particular del v1
    '''
    
    '''
        puntos colineares
        https://math.stackexchange.com/questions/175896/finding-a-point-along-a-line-a-certain-distance-away-from-another-point
        en un circulo v1 es el punto central
    '''
    v= v2-v1  
    magnitud = math.sqrt(v.x**2+v.y**2+v.z**2)    
    
    if magnitud == 0:
        magnitud = 0.000000001;
    u = v/magnitud
    p=  v1 + distancia*u       
    return p
    
def calcularLargos(bm, vertice1, vertice2):
    
    '''
    Devuelve la distancia que existe entre dos vertices
    '''
    v1 = vertice1
    v2 = vertice2

    #print(v1)
    #print(v2)

    #dv1v2 = math.sqrt(math.fabs((((((v2.co.x)-(v1.co.x))**2))+((((v2.co.y)-(v1.co.y))**2))+((((v2.co.z)-(v1.co.z))**2)))))
    dv1v2 = math.sqrt(math.fabs((((((v2[0])-(v1[0]))**2))+((((v2[1])-(v1[1]))**2))+((((v2[2])-(v1[2]))**2)))))
   # print(dv1v2)
    return (dv1v2)

def vertice_en_interseccion(bm,radio, v1, v2, normal, punto):
    
        '''
        calcula las coordenadas de intersección de dos circulos coplanares
        como pueden ser dos puntos diferentes, entonces dependiendo la opción punto que llegue, devuelve las coordenadas del nuevo punto que es intersección de ambos circulos
        '''
        #mat = obj.matrix_world
        #pn1=bm.verts.new((0,0,0))
        r0 = radio
        r1 = radio
        
        v1 = v1.co
        v2 = v2.co
        distancia =  calcularLargos(bm, v1, v2)
        
        dx = v2.x-v1.x
        dy = v2.y-v1.y
        dz = v2.z-v1.z
        
        #d= round(math.sqrt(dx**2 + dy**2+dz**2),5)
        d= distancia
        
        if d>r0+r1:
            print("no se intersectan, circulos separados")
        elif d< math.fabs(r1-r0):
            print("no se intersectar, un circulo dentro de otro")
        elif d == 0  and r0 == r1:
            print("circulos coincidentes con infinitas soluciones")
        else:
            a=(r0**2-r1**2+d**2)/(2*d)
            b=(r1**2-r0**2+d**2)/(2*d)
            h= math.sqrt(r0**2-a**2)
            #print("distancia a ",a, "\ndistancia b ",b, "\naltura ", h)
            #print(a+b)    
            

            magnitude = math.sqrt((v2-v1)[0]**2 + (v2-v1)[1]**2+ (v2-v1)[2]**2)
            v = (v2-v1)/magnitude 
            
            cn = mathutils.Vector(normal)
            w = cn.cross(v)
            #print("x"*20)
           
            #print("unite vector1 : ",v, "\nCentro normal",cn, "\nunite vector2 : ",w, "\nmult1: ",(a*v), "\nmult2 ",(h*w))
            
            
            if punto == 1:
                p3 = v1+ (a*v) + (h*w)
            else:
                p3= v1+ (a*v) - (h*w)

            #pn1.co = p3
            #pn1.select=True
        
        return p3

        

def plano_perpendicular(bm, verts, normal):
    '''
    crea un plano perpendicular a los puntos dados
    teniendo en cuenta la normal entregada
    
    devuelve la normal del nuevo plano
    '''
    lv = []    
    #print(da)
    #mat = obj.matrix_world
    vn =(verts[0] + (verts[1]-verts[0])/2)
    
    da = calcularLargos(bm, verts[0], vn)
    lv.append(vn)
    
    for ve in verts:
                
        lv.append(ve)
        p2 = ve + normal   
        p = puntoColinear(ve,p2, da)       
        lv.append(p)
        #bm.verts.new(p)               

        p2 = ve - normal  
        p = puntoColinear(ve,p2, da)      
        lv.append(p)
        #bm.verts.new(p)
        
    n = mathutils.geometry.normal(lv)
    return n


################################################################################
######  ReBevel##########################################  
################################################################################ 

class ReBevelOperator(bpy.types.Operator):
    "Re bevel "
    bl_idname = 'mesh.rebevel'
    bl_label = 'Rebevel operator'
    bl_description  = "allow create the bevel in other point"
    bl_options = {'REGISTER', 'UNDO'}
    

    
    
    
    opciones = bpy.props.EnumProperty(items=[("a", "a", "a", "",1),
                                            ("b", "b", "b", "",2),
                                            ("c", "c", "c", "",3)],
                                      name= "Direction",
                                      description="", 
                                      default="a", 
                                      options={'ANIMATABLE'}  
                                      )
    
    ops_vert = bpy.props.EnumProperty(items=[("p1-p1", "p1-p1", "p1-p1", "",1),
                                            ("p2-p2", "p2-p2", "p2-p2", "",2),
                                            ("p1-p2", "p1-p2", "p1-p2", "",3),
                                            ("p2-p1", "p2-p1", "p2-p1", "",4)],
                                      name= "vertices options",
                                      description="", 
                                      default="p1-p1", 
                                      options={'ANIMATABLE'}  
                                      )
    sections = bpy.props.IntProperty(name="Sections", 
                                       description="", 
                                       default=2, 
                                       min=1, 
                                       max=2**31-1, 
                                       soft_min=-2**31, 
                                       soft_max=2**31-1, 
                                       step=1, 
                                       
                                       )
    invert = bpy.props.BoolProperty(
                                    name="Invert Faces Union",
                                    description="Invert Faces Union",
                                    default = False) 
    def main(self, context, opciones, ops_vert, sections, invert):
        print("*"*50)
        
        obj = bpy.context.object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        pto1 = pto2 = 0
        #escoger los 4 vertices
        vtx = [v for v in bm.verts if (v.select==True and not v.hide)]
        
        if(len(vtx)==4):
            v1 = vtx[0]
            v2 = vtx[1]
            v3 = vtx[2]
            v4 = vtx[3]
            if(opciones == "a"):
                v1 = vtx[0]
                v2 = vtx[1]
                v3 = vtx[2]
                v4 = vtx[3]
            elif(opciones == "b"):
                v1 = vtx[0]
                v2 = vtx[3]
                v3 = vtx[2]
                v4 = vtx[1]    
            elif(opciones == "c"):
                v1 = vtx[0]
                v2 = vtx[2]
                v3 = vtx[1]
                v4 = vtx[3]  
            else:
                print("no es una opcion valida")    
            
            if ops_vert == "p1-p1":
                pto1 = pto2 = 1
            elif ops_vert == "p2-p2":
                pto1 = pto2 = 2   
            elif ops_vert == "p1-p2":
                pto1 = 1
                pto2 = 2
            elif ops_vert == "p2-p1":
                pto1 = 2
                pto2 = 1
            else:
                print("no es una opcion valida")
                
            #seleccion de los 4 vertices
            #v1,v2,v3,v4= [v for v in bm.verts if (v.select==True and not v.hide)]

            #calculo de normales y axis perpendiculares
            vertices = [v1.co,v2.co,v3.co,v4.co]
            n= mathutils.geometry.normal(vertices)

            axis1= plano_perpendicular(bm, [v1.co, v2.co], n)
            axis2= plano_perpendicular(bm, [v3.co, v4.co], n)

            #calculo de radios primero entre puntos y luego para triangulo rectangulo
            radio_circulo1 = calcularLargos(bm,v1.co, v2.co)
            radio_circulo2 = calcularLargos(bm, v3.co, v4.co)

            radio1 = (1/math.sqrt(2))*radio_circulo1
            radio2 = (1/math.sqrt(2))*radio_circulo2

            v5= vertice_en_interseccion(bm,radio1, v1, v2, axis1, pto1)
            v6=vertice_en_interseccion(bm,radio2, v3, v4, axis2, pto2)

            #crear arcos, primero puntos y luego caras
            arco1 = arco(self,bm, v5,v1.co,v2.co, sections)
            arco2 = arco(self, bm, v6,v3.co,v4.co, sections)


            contador = len(arco1)-1
            contador2 = len(arco1)
            while contador>0:
                if invert:
                    bm.faces.new((arco1[contador],arco1[contador-1],arco2[contador],arco2[contador-1]))
                else:
                    bm.faces.new((arco1[contador],arco1[contador-1],arco2[contador2-contador],arco2[contador2-contador-1]))
                
                contador -=1

            #se recalculan las normales
            bpy.ops.mesh.normals_make_consistent(inside=True)
            #eliminar dobles
            bpy.ops.mesh.remove_doubles()

        bmesh.update_edit_mesh(me, True)        

        
           
    
    
    @classmethod
    def poll(self, context):
        obj = context.active_object
        return all([obj is not None, obj.type == 'MESH', obj.mode == 'EDIT'])

    def execute(self, context):
        
        self.main(context,  self.opciones, self.ops_vert, self.sections, self.invert)

        return {'FINISHED'}
    
                 
    

class ReBevelOperatorPanel(bpy.types.Panel):
	#bl_category = "Bisector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    #bl_context = "editmode"
    bl_label = " Rebevel"
    @classmethod
    def poll(cls, context):
        return (context.mode == 'EDIT_MESH')
    
    def draw(self, context):
        layout = self.layout
 
        row = layout.row(align=True)
        row.operator(ReBevelOperator.bl_idname) #Reecreate a bevel
        
    

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
