import zlib # =gzip, 1to9
import bz2 # 1to9

# The following algorithms were designed for speed not compression ratio
#import snappy
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

def ncd(C, string1, string2, normalised_compression_distances={}):
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
        min_distance = distances[pair]
    except KeyError:
        min_distance = float('inf')
        for endnode1 in cluster1:
            for endnode2 in cluster2:
                current_pair = tuple([endnode1,endnode2].sort())
                if distances[current_pair] <= min_distance:
                    min_distance = distances[current_pair]
        distances[pair] = min_distance
    return min_distance


def complete_linkage(distances, cluster1, cluster2):
    """Calculates the distance between two clusters using complete linkage.

    distances is a dictionary of (str,str/str,cluster/cluster,cluster) tuples.
    It is updated with the calculated distance.

    """
    pair = tuple([cluster1,cluster2].sort())
    try:
        max_distance = distances[pair]
    except KeyError:
        max_distance = float('-inf')
        for endnode1 in cluster1:
            for endnode2 in cluster2:
                current_pair = tuple([endnode1,endnode2].sort())
                # This would be more efficient if iterating over a cluster
                # would iterate over subclusters instead of endnodes.
                if distances[current_pair] >= max_distance:
                    max_distance = distances[current_pair]
        distances[pair] = max_distance
    return max_distance

def avg_linkage(distances, cluster1, cluster2):
    """Calculates the distance between two clusters using average linkage.

    distances is a dictionary of (str,str/str,cluster/cluster,cluster) tuples.
    It is updated with the calculated distance.

    """
    pair = tuple([cluster1,cluster2].sort())
    try:
        avg_distance = distances[pair]
    except KeyError:
        avg_distance = 0
        nb_vals = 0
        for endnode1 in cluster1:
            for endnode2 in cluster2:
                current_pair = tuple([endnode1,endnode2].sort())
                avg_distance += distances[current_pair]
                nb_vals += 1
        avg_distance /= nb_vals
        distances[pair] = avg_distance
    return avg_distance

def link(linkage_metric, clusters, distances):
    while(len(clusters) > 1):
        next_cluster_pair = ()
        min_distance = float('inf')
        for pair in itertools.combinations(clusters, r=2):
            dist = linkage_metric(distances, pair[0], pair[1])
            if dist < min_distance:
                min_distance = dist
                next_cluster_pair = pair
        clusters.remove(next_cluster_pair[0])
        clusters.remove(next_cluster_pair[1])
        next_cluster = cluster(next_cluster_pair[0], next_cluster_pair[1])
        clusters.append(next_cluster)

def strings_to_clusters_distances(C, strings):
    distances = {}
    for pair in itertools.combinations(strings, r=2):
        ncd(C, pair[0], pair[1], distances)
    clusters = [cluster(s) for s in strings]
    return clusters, distances
