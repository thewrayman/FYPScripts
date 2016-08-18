from collections import namedtuple



REP_TYPES = ('KnownClean','ProbablyClean','Unknown','ProbablyDirty','KnownDirty')

class ReputationValues:
	NO_REPUTATION = {'NoRep': 0}
	KNOWN_CLEAN = {'KnownClean': 1}
	PROBABLY_CLEAN = {'ProbablyClean': 2}
	UNKNOWN = {'Unknown': 3}
	PROBABLY_DIRTY = {'ProbablyDirty': 4}
	KNOWN_DIRTY = {'KnownDirty': 5}

class FileTypes:
	PE_FILE = 0
	DLL_FILE = 1
	TXT_FILE = 2
	OTHER = 3

class FileExtensions:
	PE_FILE = 0
	DLL_FILE = 1
	TXT_FILE = 2
	OTHER = 3

class PacketType:
	TCP = 0x06
	UDP = 0X11
	ICMP = 0x01
