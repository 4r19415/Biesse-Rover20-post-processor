import os, math
import struct


from itertools import chain



#class for a 3d point
class Point3D:
    def __init__(self,p):
        self.point_size=0.5
        self.x=p[0]
        self.y=p[1]
        self.z=p[2]
        self.a=0
        self.b=0
        if(len(p)>=5):
            self.a=p[3]
            self.b=p[4]

    def __add__(self,other):
        return  Point3D((self.x+other.x, self.y+other.y, self.z+other.z,
                         self.a+other.a, self.b+other.b))
    
    def __neg__(self):
        return Point3D( (-self.x, -self.y, -self.z, -self.a, -self.b) )
    
    def __sub__(self,other):
        return self + (-other)
    
    def __str__(self):
        if ((self.a == 0) & (self.b == 0)):
            return "< %f %f %f >" % (self.x,self.y,self.z)
        else:
            return "< %f %f %f %f %f >" % (self.x,self.y,self.z,self.a,self.b)

    def norm(self):
        return math.sqrt( self.x*self.x+ self.y*self.y+ self.z*self.z)
    
    def scale(self,v):
        self.x*=v; self.y*=v; self.z*=v; self.a*=v; self.b*=v

    def __mul__(self, other):
        if(type(other) == int or type(other) == float):
            return Point3D((other*self.x,other*self.y,other*self.z,other*self.a,other*self.b))
        else:
            print("Point3D x " + str(type(other)) + " not suported")

    def normalize(self):
        self.scale(1/self.norm())
    
    def offset(self, p):
        self.x+=p.x
        self.y+=p.y
        self.z+=p.z
    
    def rotate(self, M):
        tempPt = M*self
        self.x,self.y,self.z = tempPt.x, tempPt.y, tempPt.z