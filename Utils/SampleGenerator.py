__author__ = 'emmet'
import os
import sys#
import shutil
"""
    This script will take a file, eg. samplefile.exe and create a host of sample files from it.
    Default generation is 100 samples varying from:
    KnownClean
    KnownDirty
    Unknown
    ProbablyDirty
    ProbablyClean

    Default will product 20 of each from the samplefile by copying it and giving a name related to the reptation type

    These can used to simulate discovering a file of a certain reputation
"""
TOTAL_COPIES = 100
CAT_COPIES = 20

CWD = os.getcwd()

REP_TYPES = ['KnownClean','ProbablyClean','Unknown','ProbablyDirty','KnownDirty']


class SampleFile():
    """
        Small class to store the file to copy and the user input for how many to copy
    """
    def __init__(self,filename, totalCopies=TOTAL_COPIES,catCopies=CAT_COPIES):
        self.fileName = filename
        self.totalCopies =totalCopies
        self.catCopies = catCopies


class SampleGenerator:
    """
        Class which carries out generation functionality.
        Takes in a SampleFile object from which it gets file info and copy info
    """
    def __init__(self,SampleFile):
        self.SampleFile = SampleFile.fileName
        self.catcopies = SampleFile.catCopies
        self.path = None
        self.shortName = None
        self.extension = None

    def getShortName(self):
        #print "samplefile: %s"%self.SampleFile
        filename = os.path.basename(self.SampleFile).split('.')
        #print "filename: %s"%filename
        self.shortName = filename[0]
        self.extension = filename[1]
        self.path = os.path.dirname(os.path.abspath(self.SampleFile))
        if (not self.path == None) and (not self.extension == None) and (not self.shortName == None):
            return True
        else:
            return False

    def generateSamples(self):
        if self.getShortName():
            samplepath = os.path.join(self.path,"Samples")

            if os.path.exists(samplepath):
                shutil.rmtree(samplepath)
            try:
                os.mkdir(os.path.join(self.path,"Samples"))
            except Exception as msg:
                print "Can't make dir because %s"%msg

            for type in REP_TYPES:
                for i in range(self.catcopies):
                    copyname = os.path.join(samplepath,(type+"-"+ str(i) +"."+self.extension))
                    shutil.copy(self.SampleFile,copyname)

def main():
    samplename = None
    totalcopies = TOTAL_COPIES
    catcopies = CAT_COPIES
    success = True
    args = sys.argv[1:]
    if not "-f" in args:
        print "*ERROR* A target sample must be supplied:\n-f c:\\xyz\\myfile.exe"
        exit()
    for arg in range(0,len(args)):
        if args[arg] == "-f":
            if (not arg == len(args)-1) and (os.path.isfile(args[arg+1])):
                if samplename == None:
                    samplename = args[arg+1]
                    success = success and True
                    print "Using sample file %s"%samplename
                else:
                    print "*ERROR* Please only enter one parameter for sample file\n"
                    success = success and False
            else:
                print "*ERROR* Please make sure the filename is valid\n"
                exit()
            pass
        if args[arg] == "-t":
            #print "T value is %s and the mod is %d"%(args[arg+1],(int(args[arg+1])%5))
            if (not arg == len(args)-1) and ((int(args[arg+1])%5) == 0):
                totalcopies = int(args[arg+1])
                catcopies = totalcopies/5
                success = success and True
                print "Found new total copies, using %d\n"%totalcopies
            else:
                print "*ERROR* Please make sure you enter a valid total number.\ni.e, must be divisible by 5\n"

    if success:
        print "success!"
        print samplename
        print totalcopies
        print catcopies

        sf = SampleFile(samplename,totalcopies,catcopies)
        SampleGenerator(sf).generateSamples()


if __name__ == "__main__":
    main()