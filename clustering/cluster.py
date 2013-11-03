import zlib # =gzip, 1to9
import bz2 # 1to9

# The following algorithms were designed for speed not compression ratio
import snappy
import lz4 # compress and compressHC

class cluster:
    """A cluster contains members, those can be clusters or strings."""
    def __init__(self, *members):
        self.members = members

    def __iter__(self):
        for member in self.members:
            try: #if
                member.quacks()
                #then
                for m in member:
                    yield m
            except AttributeError:
                yield member

    def quacks(self):
        pass

normalised_compression_distances = {}
def ncd(C, string1, string2):
    """Calculate the normalized compression distance between string1 and
    string2 using the compressor C"""
    pair = tuple([string1, string2].sort())
    try:
        ncd = normalised_compression_distances[pair]
    except TypeError:
        x = len(C(string1))
        y = len(C(string2))
        xy = len(C(string1 + string2))
        ncd = (xy - min(x,y))/float(max(x,y))
        normalised_compression_distances[pair] = ncd
    return ncd
    
def single_linkage(distances, cluster1, cluster2):
    """Calculates the distance between two clusters using single linkage.

    distances is a dictionary of (str,str/str,cluster/cluster,cluster) tuples.
    It is updated with the calculated distance.

    """
    pair = tuple([cluster1,cluster2].sort())
    try:
        distance = distances[pair]
    except KeyError:
        min_distance_pair = ()
        min_distance = float('inf')
        for endnode1 in cluster1:
            for endnode2 in cluster2:
                current_pair = tuple([endnode1,endnode2].sort())
                if distances[current_pair] <= min_distance:
                    min_distance = distances[current_pair]
                    min_distance_pair = current_pair
        distances[min_distance_pair] = min_distance
    return min_distance


def complete_linkage(distances, cluster1, cluster2):
    pass

def avg_linkage(distances, cluster1, cluster2):
    pass
