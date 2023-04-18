import sys
sys.tracebacklimit = 0
#import glob
#print(glob.glob("A:\\*.PAN"))

from Utils3D import *
from iso import *
from GCode import *
import shutil


class IsoGen:
    def __init__(self, filename, panneau):

        self.isPathing = False

        self.file = open(filename,'w')
        msg = ""

        msg += "\nPROFILI REL3\x00"

        msg += "\nB_PAN\x00"
        msg += panDef(filename.split('\\')[-1],panneau)+"\x00"

        msg += "\nB_SYM\x00"
        msg += symDef(panneau)
        msg += "\nE_SYM\x00"

        msg += "\nE_PANNELLO\x00"

        msg += "\nB_FORO\x00"
        msg += "\nE_FORI\x00"

        msg += "\nB_AS\x00"
        self.file.write(msg)

        self.profDefs = []
        self.paths = []

    def write(self, msg):
        self.file.write(msg)

    def end(self):
        for profdef in self.profDefs:
            self.file.write(profdef)
        self.file.write( "\nE_AS\x00" ) 
        for path in self.paths:
            self.file.write(path)

        self.file.close()





def main():
    args = sys.argv[1:]

    

    panFile = args[1]
    ncFile  = args[0]

    infile = open(ncFile)
    line = infile.readline()
    while(line):
        line = infile.readline()
        data = line.split()
        if data[0] == "G0":
            if data[1][0] == "Z":
                safeZ = float(data[1][1:])
                print( "épaisseur panneau = " + str(safeZ))
                break

    x = 0
    while (x==0):
        print("Longueur panneau ? : ")
        msg = input( "" ).replace(",",".")
        try:
            float(msg) 
            x = float(msg) 
        except:
            print(" T'es pas un trés doué toi, essaie encore ... ")
    


    #panneau = Point3D((534,406,25))
    panneau = Point3D((x,400,safeZ))
    writer = IsoGen(panFile,panneau)

    reader = GcodeReader(writer)
    reader.panneau = panneau

    reader.readfile(ncFile)

    while not reader.doLine():
        pass

    writer.end()

    print("\n\n\n\n")

    try:
        shutil.copyfile(panFile, "A:\\" + panFile.split('\\')[-1])
    except:
        raise Exception("T'as oublié la disquette abruti !") from None
        exit(1)



if __name__ == '__main__':
    main()