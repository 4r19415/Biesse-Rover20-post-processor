from Utils3D import *
from iso import *

G0FEED = 7300
FLAGFEED = 42

class GcodeReader():
    def __init__(self, out):
        self.out = out
        self.buff = []
        self.line = 0
        self.tool = 0
        self.feed = 0
        self.rotSpeed = 0
        self.prevPos = Point3D((0,0,0,0,0))
        self.newPos = Point3D((0,0,0,0,0))
        self.index = 1
        self.opIndex = -1
        self.panneau = Point3D((0,0,0))
        self.needNewOp = True
        self.NextOpEntry = 0
        self.firstMove = True
        self.g1Feed = 0
        self.rotationCenter = Point3D((0,0,0))

    def readfile(self, filename):
        fp=open(filename,'rb')
        self.buff = fp.readlines()
        fp.close()
        self.points = []
        x,y,z,a,b, = 0,0,0,0,0

    def offset(self, p):
        for pt in self.points:
            pt.offset(p)
    
    def rotate(self, M):
        for pt in self.points:
            pt.rotate(M)       

    def readParams(self, words):
        for word in words:
            if word[0] == "G":
                moveType = int(word[1:])
            elif word[0] == "S":
                prevRot = self.rotSpeed
                if(word[1:].isdigit()):
                    self.rotSpeed = int(word[1:])
                if(not(prevRot == self.rotSpeed)):
                    self.needNewOp = True

            elif word[0] == "F":           
                prevfeed = self.g1Feed
                
                temp = float(str(word[1:]))
                if (temp == FLAGFEED):
                    self.NextOpEntry = moveType
                else:
                    self.g1Feed = temp
                if(not(prevfeed == self.g1Feed)):
                    self.needNewOp = True

        for i in range(len(words)-1):
            if words[i+1][0] == "X":
                self.newPos.x = float(words[i+1][1:])
            elif words[i+1][0] == "Y":
                self.newPos.y = float(words[i+1][1:])
            elif words[i+1][0] == "Z":
                prevZ = self.newPos.z
                self.newPos.z = float(words[i+1][1:])
                if(not(prevZ == self.newPos.z)):
                    self.needNewOp = True
            elif words[i+1][0] == "I":
                self.rotationCenter.x = float(words[i+1][1:])
            elif words[i+1][0] == "J":
                self.rotationCenter.y = float(words[i+1][1:])
            elif words[i+1][0] == "K":
                self.rotationCenter.z = float(words[i+1][1:])
            elif words[i+1][0] == "R":
                self.prcHeight = float(words[i+1][1:])
            elif words[i+1][0] == "T":
                prevTool = self.tool
                self.tool = float(words[i+1][1:])
                if(not(prevTool == self.tool)):
                    self.needNewOp = True

            else:
                pass
                #print("not understood: G + " + str(words[i+1][0]) +" "+ str(words[i+1][1:]))

    def newOpGen(self):
        self.needNewOp = False
        self.firstMove = True
        if(self.opIndex >= 0):
            self.out.paths[self.opIndex] += bpsymDef(self.panneau)
            self.out.paths[self.opIndex] += "\nEPGR\x00"
        self.opIndex += 1
        if self.NextOpEntry == 0:
            self.out.profDefs.append(profDef(self.index + self.opIndex-1,
                                        1,             #macro
                                        self.feed,      #vi
                                        self.feed,      #va
                                        self.rotSpeed,  #vr
                                        -self.newPos.z*10000,         #prf
                                        self.tool,      #mut
                                        self.feed,      #vsorv
                                        2,              #ing
                                        2))             #out
        elif self.NextOpEntry == 2:
            self.out.profDefs.append(profDef(self.index + self.opIndex-1,
                                        44,             #macro
                                        self.feed,      #vi
                                        self.feed,      #va
                                        self.rotSpeed,  #vr
                                        -self.newPos.z*10000,         #prf
                                        self.tool,      #mut
                                        self.feed,      #vsorv
                                        4,              #ing
                                        2,              #out
                                        self.rotationCenter.norm())) #radius
            self.NextOpEntry = 0
        elif self.NextOpEntry == 3:
            self.out.profDefs.append(profDef(self.index + self.opIndex-1,
                                        44,             #macro
                                        self.feed,      #vi
                                        self.feed,      #va
                                        self.rotSpeed,  #vr
                                        -self.newPos.z*10000,         #prf
                                        self.tool,      #mut
                                        self.feed,      #vsorv
                                        5,              #ing
                                        2,               #out
                                        self.rotationCenter.norm())) #radius
            self.NextOpEntry = 0
        else:
            raise Exception("wrong usage of newOpGen with entry = " + str(entry)) from None
        self.out.paths.append("\nBPGR\x00")
        self.out.paths[self.opIndex] += "\n\tGPRO TY=10 PI=-1 PF=-1 NO=\"BOX_02\" NPR=0 XI=%.6f YI=%.6f "% (self.prevPos.x,self.prevPos.y) 
        self.out.paths[self.opIndex] += "XF=%.6f YF=%.6f END\x00" % (self.prevPos.x,self.prevPos.y) 
        self.out.paths[self.opIndex] += "\n\tGINP COL=0 NUM=%d MIR=0 P=0 RAY=1000000000 ROT=0 END\x00" %(self.opIndex)
        self.out.paths[self.opIndex] += "\n\tGDIR COL=6 X1=%.6f Y1=%.6f X2=%.6f Y2=%.6f END\x00"%(self.prevPos.x,self.prevPos.y,self.newPos.x,self.newPos.y)


    def doLine(self): 
        if self.line < len(self.buff):         
            words=self.buff[self.line].decode('UTF-8').split()
                        
            if len(words)>0:
                #print(words)
                self.readParams(words)

                if words[0]=='G0' :
                    pass

                elif words[0]=='G1' :
                    self.feed = self.g1Feed

                    if ((len(self.buff) > self.line+1) and (len(self.buff[self.line+1].decode('UTF-8').split()) > 0)):
                        if (not(self.buff[self.line+1].decode('UTF-8').split()[0] == 'G98')):

                            if( (not self.firstMove)  and
                                ((abs(self.newPos.x - self.prevPos.x ) + abs(self.newPos.y - self.prevPos.y )) > 0 ) ):
                                                              
                                if(self.needNewOp):
                                    #print("should not be call: " + str(words))
                                    #print(str(self.newPos) + "->" + str(self.prevPos))
                                    self.newOpGen()
                                                                
                                self.out.paths[self.opIndex] += "\n\t" + gseg(self.prevPos,self.newPos)
                            
                            self.firstMove = False
                          
                elif words[0]=='G2':
                    if (self.NextOpEntry == 2):
                        self.newOpGen()
                    elif(self.needNewOp):
                        self.newOpGen()
                    else: 
                        self.out.paths[self.opIndex] += "\n\t" + garc(self.prevPos,self.newPos,self.rotationCenter,2)
                    self.firstMove = False

                elif words[0]=='G3':
                    if (self.NextOpEntry == 3):
                        self.newOpGen()
                    elif(self.needNewOp):
                        self.newOpGen()
                    else:
                        self.out.paths[self.opIndex] += "\n\t" + garc(self.prevPos,self.newPos,self.rotationCenter,1)
                    self.firstMove = False

                elif words[0]=='G4':
                    self.out.profDefs[-1] = self.out.profDefs[-1][:-5]
                    self.out.profDefs[-1] += "\tEND\nSOSP \n\tTIPO=1 \nEND"
                elif words[0]=='G5':
                    self.out.profDefs[-1] = self.out.profDefs[-1][:-5]
                    self.out.profDefs[-1] += "\tEND\nSOSP \n\tTIPO=2 \nEND"
                elif words[0]=='G81':
                    self.readParams(words)
                    #print("Drill at "+ str(self.feed) +" mm/min at " + str(self.newPos))

                    if (self.tool in [11,12,13,14,15,16]):
                        self.out.write(percageChamp(self.index,
                                                self.newPos,
                                                self.tool,
                                                self.feed,
                                                self.prcHeight  ))
                    else:
                        self.out.write(percageDroit(self.index,
                                                    self.newPos,
                                                    self.tool,
                                                    self.feed,
                                                    self.newPos.z ))
                    self.index += 1
                
                else:
                    pass # TODO re put that
                    #print("Gcode not understood: " + str(words))
                
                self.prevPos = Point3D((self.newPos.x,
                                            self.newPos.y,
                                            self.newPos.z,
                                            self.newPos.a,
                                            self.newPos.b))
            self.line += 1 
            return 0
        else:
            if(self.opIndex>=0):
                self.out.paths[self.opIndex] += bpsymDef(self.panneau)
                self.out.paths[self.opIndex] += "\nEPGR "
            return 1


def main():
    reader = GcodeReader(0)
    reader.readfile("prc+ctr.nc")
    while not reader.doLine():
        pass



if __name__ == '__main__':
    main()