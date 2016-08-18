import os
import sys
import shutil
import logging
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


class SampleFile:
	"""
		Small class to store the file to copy and the user input for how many to copy
	"""
	def __init__(self,filename, totalCopies=TOTAL_COPIES,catCopies=CAT_COPIES):
		self.fileName = filename
		self.totalCopies =totalCopies
		self.catCopies = catCopies
		logging.info("[%s]: Created SampleFile with" % (self.__class__.__name__,self.fileName,self.totalCopies,self.catCopies))


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
		logging.info("\n[%s]: Entering %s" % (self.__class__.__name__, sys._getframe(  ).f_code.co_name))
		logging.info("[%s]: using %s" % (self.__class__.__name__, self.SampleFile))

		filename = os.path.basename(self.SampleFile).split('.')
		self.shortName = filename[0]
		self.extension = filename[1]
		self.path = os.path.dirname(os.path.abspath(self.SampleFile))

		if (not self.path == None) and (not self.extension == None) and (not self.shortName == None):
			logging.info("[%s]: Exiting %s with True" % (self.__class__.__name__, sys._getframe(  ).f_code.co_name))
			return True
		else:
			logging.info("[%s]: Exiting %s with True" % (self.__class__.__name__, sys._getframe(  ).f_code.co_name))
			return False

	def generateSamples(self):
		logging.info("\n[%s]: Entering %s" % (self.__class__.__name__, sys._getframe(  ).f_code.co_name))
		if self.getShortName():
			samplepath = os.path.join(self.path, "Samples")

			if os.path.exists(samplepath):
				shutil.rmtree(samplepath)

			try:
				os.mkdir(samplepath)
			except Exception as msg:
				print "Can't make dir because %s"%msg

			for type in REP_TYPES:
				for i in range(self.catcopies):
					copyname = os.path.join(samplepath, (type + "-" + str(i) + "." + self.extension))
					shutil.copy(self.SampleFile,copyname)

		logging.info("[%s]: Exiting %s"%(self.__class__.__name__, sys._getframe(  ).f_code.co_name))

def main():
	samplename = None
	totalcopies = TOTAL_COPIES
	catcopies = CAT_COPIES
	success = True
	args = sys.argv[1:]

	logging.info("\n[%s]: Entering %s with args: " % (os.path.basename(__file__),sys._getframe(  ).f_code.co_name,args))

	if "-f" not in args:
		print "*ERROR* A target sample must be supplied:\n-f c:\\xyz\\myfile.exe"
		logging.info("[%s]: Exiting %s due to no -f flag\n" % (os.path.basename(__file__), sys._getframe(  ).f_code.co_name,))
		exit()

	for arg in range(0,len(args)):
		if args[arg] == "-f":
			if (not arg == len(args)-1) and (os.path.isfile(args[arg+1])):
				if samplename == None:
					samplename = args[arg+1]
					success = success and True
					print "Using sample file %s"%samplename
					logging.info("[%s]: Using sample file %s" % (os.path.basename(__file__),samplename))
				else:
					print "*ERROR* Please only enter one parameter for sample file\n"
					logging.info("[%s]: More than one file provided, please check" % (os.path.basename(__file__)))
					success = success and False
			else:
				print "*ERROR* Please make sure the filename is valid\n"
				logging.info("[%s]: Exiting %s due to invalid filename %s" % (os.path.basename(__file__),args[arg+1]))
				logging.info("[%s]: ***EXIT***"%(os.path.basename(__file__)))
				exit()
			pass
		if args[arg] == "-t":
			#print "T value is %s and the mod is %d"%(args[arg+1],(int(args[arg+1])%5))
			if (not arg == len(args)-1) and ((int(args[arg+1])%5) == 0):
				totalcopies = int(args[arg+1])
				catcopies = totalcopies/5
				success = success and True
				print "Found new total copies, using %d\n" % totalcopies
				logging.info("[%s]: Found totalcopies override: %d" % (os.path.basename(__file__),totalcopies))
			else:
				print "*ERROR* Please make sure you enter a valid total number.\ni.e, must be divisible by 5\n"
				logging.info("[%s]: TotalCopies override for %d failed, ensure it is divisible by 5" % (os.path.basename(__file__),totalcopies))

	if success:
		print "\nsuccess!"
		print samplename
		print totalcopies
		print catcopies
		logging.info("[%s]: Success! With sample: %s, totalcopies: %d, catcopies: %d" % (os.path.basename(__file__),samplename,totalcopies,catcopies))

		sf = SampleFile(samplename,totalcopies,catcopies)
		SampleGenerator(sf).generateSamples()


if __name__ == "__main__":
	main()