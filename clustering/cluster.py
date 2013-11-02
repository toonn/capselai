import zlib # =gzip, 1to9
import bz2 # 1to9

# The following algorithms were designed for speed not compression ratio
import snappy
import lz4 # compress and compressHC

class cluster:
    """A cluster always has two members, those can be clusters or strings."""
    def __init__(self, member1, member2, ncd):
        self.member1 = member1
        self.member2 = member2
        self.ncd = ncd

def ncd(C, string1, string2):
    """Calculate the normalized compression distance between string1 and
    string2 using the compressor C"""
    x = len(C(string1))
    y = len(C(string2))
    xy = len(C(string1 + string2))
    return (xy - min(x,y))/float(max(x,y))
    
def single_linkage(C, cluster1, cluster2):
    pass

def complete_linkage(C, cluster1, cluster2):
    pass

def avg_linkage(C, cluster1, cluster2):
    pass
