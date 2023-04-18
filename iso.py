from Utils3D import *

def panDef(filename,point):
    msg = ""
    msg += "\n\t" + "NOME=\"" + filename + "\"\x00" 
    msg += "\n\t" + "LPX=%d\x00" % (10000 * point.x)
    msg += "\n\t" + "LPY=%d\x00" % (10000 * point.y)
    msg += "\n\t" + "LPZ=%d\x00" % (10000 * point.z)
    msg += "\n\t" + "CNFT=\"1\"\x00"
    msg += "\n\t" + "XSOSP=26350000\x00"
    msg += "\n\t" + "STRET=0\x00"
    msg += "\n\t" + "FILABAT=1\x00"
    msg += "\n\t" + "CNFTP=\"1\"\x00"

    return msg

def bpsymDef(point):
    msg = ""
    msg += "\n\t" + "BPSYM\x00" 
    msg += "\n\t\tSYMBOL=\"X\" VALUE =\"%.4f\"\x00" % point.x
    msg += "\n\t\tSYMBOL=\"Y\" VALUE =\"%.4f\"\x00" % point.y
    msg += "\n\t\tSYMBOL=\"Z\" VALUE =\"%.4f\"\x00" % point.z

    msg += "\n\t\tSYMBOL=\"d1\" VALUE =\"%.4f\"\x00" % 90
    msg += "\n\t\tSYMBOL=\"d2\" VALUE =\"%.4f\"\x00" % 90
    msg += "\n\t\tSYMBOL=\"a\" VALUE =\"%d\"\x00" % 500
    msg += "\n\t\tSYMBOL=\"b\" VALUE =\"%d\"\x00" % 300
    msg += "\n\t\tSYMBOL=\"r\" VALUE =\"%d\"\x00" % 50

    msg += "\n\t" + "END\x00" 


    return msg

def symDef(point):
    msg = ""

    msg += "\n\tSYMBOL=\"X\"\x00\n\tVALUE =\"%.4f\"\x00" % point.x
    msg += "\n\tSYMBOL=\"Y\"\x00\n\tVALUE =\"%.4f\"\x00" % point.y
    msg += "\n\tSYMBOL=\"Z\"\x00\n\tVALUE =\"%.4f\"\x00" % point.z

    return msg

def profDef(index, macro, vi, va, vr, prf, mut, vsorv, ing, out, radius = 20):
    msg = "\nPROF\x00"
    msg += "\n\tTIPO=12 INDMACRO=%d\x00"%macro
    msg += "\n\t\x00IND=%d \x00IND=-1\x00 " % index
    msg += "\n\t\x00"
    msg += "\n\tAR=0 IF=0 AF=0 SF=133333 PF=0\x00"
    msg += "\n\tNC=0 DC=0 PC=0 VC=0 \x00"
    msg += "\n\tGIUST=0 OX=0 SOX=\"0.00\" OY=0 SOY=\"0.00\"\x00"
    msg += "\n\tDTECH\x00"
    msg += "\n\tPIANO=3 VI=%d VA=%d VR=%d " %(vi, va, vr)
    msg +=      "PRF=%d NOMUT=\"%d\" NS=0 PAS=0\x00" %(prf, mut)
    msg += "\n\tCOMP=0 VER=1	DELTA=0 SOVRA=0 VSOVR=%d " % (vsorv)
    msg +=      "ING=%d OUT=%d SCAS=0 RAC=1 AT=50 RIU=%d\x00" % (ing, out, 10000*radius)

    msg += "\n\tEND\x00"
    return msg

def spaces(x):
    if(x == 0):
        return"0 "
    msg = ""
    if(abs(x)<100):
        msg += " "
    if(abs(x)<10):
        msg += " "
    msg += "%.6f " % x
    return msg

def gseg(pointA,pointB):
    msg = ""
    msg += "GSEG\x00 COL=28 " 
    msg += "X1="+ spaces(pointA.x) 
    msg += "Y1="+ spaces(pointA.y) 
    msg += "X2="+ spaces(pointB.x) 
    msg += "Y2="+ spaces(pointB.y) 
    msg += "ZI="+ spaces(pointA.z) 
    msg += "ZF="+ spaces(pointB.z) 

    msg += "  NUM=0 SOL=0 END\x00"
    return msg

def garc(pointA,pointB,centreOffset,sens):
    msg = ""
    msg += "GARC\x00 COL=28 " 

    centre = pointA + centreOffset
    radius = centreOffset.norm()

    msg += "XC="+ spaces(centre.x) 
    msg += "YC="+ spaces(centre.y) 
    msg += "R="+ spaces(radius) 
    msg += "S="+ str(sens) + " "
    
    msg += "X1="+ spaces(pointA.x) 
    msg += "Y1="+ spaces(pointA.y) 
    msg += "X2="+ spaces(pointB.x) 
    msg += "Y2="+ spaces(pointB.y) 
    msg += "ZI="+ spaces(pointA.z) 
    msg += "ZF="+ spaces(pointB.z) 

    msg += "  NUM=10 SOL=0 END\x00"
    return msg

def percageDroit(index,point, outil, feed, depth):
    msg = ""
    msg += "\nFV "
    msg += "\n\tIND=%d " % index
    msg += "\n\tSP=1 "
    msg += "\n\tSX=\"%.2f\" "%point.x
    msg += "\n\tX=%d "%(point.x*10000)
    msg += "\n\tSY=\"%.2f\" "%point.y
    msg += "\n\tY=%d "%(point.y*10000)
    msg += "\n\tSZ=\"%.2f\" "% 0 #point.z
    msg += "\n\tZ=%d "% 0 #(point.z*10000)
    msg += "\n\tDIAM=0 "
    msg += "\n\tTIPO=0 "
    msg += "\n\tTF=0 " 
    msg += "\n\tSRIP=\"1\" "
    msg += "\n\tRIP=1 "
    msg += "\n\tSSTEPX=\"0.00\" "
    msg += "\n\tSTEPX=0 "
    msg += "\n\tSSTEPY=\"0.00\" "
    msg += "\n\tSTEPY=0 "
    msg += "\n\tSANG=\"0.00\" "
    msg += "\n\tANG=0 "
    msg += "\n\tCAL= %d, 0, "%outil
    msg += "\n\tDTECH "
    msg += "\n\tPIANO=3 VI=0 VA=0	VR=%d PRF=%d NOMUT=\"%d\" NS=0 PAS=0 "%(feed,-10000*depth,outil)
    msg += "\n\tEND "

    msg += "\nEND "
    return msg

# x=1 -x=3 y=2 -y=4
# outil x+ = 11 13
# outil x- = 12 14
# outil y+ = 15
# outil y- = 16
def percageChamp(index,point, outil, feed, haut):
    msg = ""
    msg += "\nFO "
    msg += "\n\tIND=%d " % index
    msg += "\n\tSP=1 "
    if   ((outil == 11) or (outil == 13)):
        msg += "\n\tLATO=%d " % 1
    elif ((outil == 12) or (outil == 14)):
        msg += "\n\tLATO=%d " % 3
    elif (outil == 15):
        msg += "\n\tLATO=%d " % 2
    elif (outil == 16):
        msg += "\n\tLATO=%d " % 4
    else:
        print("utilisation d'un percage à champ avec l'outil n°%d non reconnu" % outil )
        exit(1)
    msg += "\n\tSX=\"%.2f\" "%point.x
    msg += " X=%d "%(point.x*10000)
    msg += "\n\tSY=\"%.2f\" "%point.y
    msg += " Y=%d "%(point.y*10000)
    msg += "\n\tSZ=\"%.2f\" "%haut
    msg += " Z=%d "%(10000*haut)
    msg += "\n\tDIAM=0 "
    msg += "\n\tTIPO=0 "
    msg += "\n\tSRIP=\"1\" "
    msg += "\n\tRIP=1 "
    msg += "\n\tSSTEPX=\"0.00\" "
    msg += "\n\tSTEPX=0 "
    msg += "\n\tSSTEPY=\"0.00\" "
    msg += "\n\tSTEPY=0 "
    msg += "\n\tCAL= %d, 0, "%outil
    msg += "\n\tDTECH "
    msg += "\n\tPIANO=3 VI=0 VA=0	VR=%d PRF=%d NOMUT=\"%d\" NS=0 PAS=0 "%(feed, -point.z*10000, outil)
    msg += "\n\tEND "

    msg += "\nEND "
    return msg

