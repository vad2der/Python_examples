'''
Algorithmic Thinking Project 3:
Closest pairs and clustering algorithms
four functions:
slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)
where cluster_list is a list of clusters in the plane
'''

import math
import alg_cluster
import user41_QUCWvLQtmY_25 as viz
import urllib2
import codeskulptor

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair_backup(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    
    pairs = []
    closest_pairs = []
    temp_tuple = (float('inf'), -1, -1)
    for ind_u, dummy_cluster_u in enumerate(cluster_list):
        for ind_v, dummy_cluster_v in enumerate(cluster_list):
            if ind_u < ind_v:
                pair_uv = pair_distance(cluster_list, ind_u, ind_v)
                pairs.append(pair_uv)
                if pair_uv[0] < temp_tuple[0]:
                    temp_tuple = pair_uv
    for pair in pairs:
        if pair[0] == temp_tuple[0]:
            closest_pairs.append(pair)
    
    return eval(tuple(set(closest_pairs))[0])


def slow_closest_pair(cluster_list):
    """
    Takes a list of Cluster objects and returns a closest pair where the pair
    is represented by the tuple (dist, idx1, idx2) with idx1 < idx2 where dist
    is the distance between the closest pair cluster_list[idx1] and
    cluster_list[idx2]. This function should implement the brute-force closest
    pair method described in SlowClosestPair from Homework 3.
    """
    closest_pair = (float('inf'), -1, -1)
    cluster_list_len = len(cluster_list)
    for idx_1 in range(cluster_list_len):
        for idx_2 in range(cluster_list_len):
            if idx_1 != idx_2:
                cluster1, cluster2 = cluster_list[idx_1], cluster_list[idx_2]
                cluster_dist = cluster1.distance(cluster2)
                if cluster_dist < closest_pair[0]:
                    closest_pair = (cluster_dist, idx_1, idx_2)
    return closest_pair


def fast_closest_pair(cluster_list):
    """
    Takes a list of Cluster objects and returns a closest pair where the pair
    is represented by the tuple (dist, idx1, idx2) with idx1 < idx2 where dist
    is the distance between the closest pair cluster_list[idx1] and
    cluster_list[idx2]. This function should implement the divide-and-conquer
    closest pair method described FastClosestPair from Homework 3.
    """
    cluster_list_len = len(cluster_list)
    if cluster_list_len <= 3:
        closest_pair = slow_closest_pair(cluster_list)
    else:
        split = cluster_list_len / 2
        left_list = cluster_list[:split]
        right_list = cluster_list[split:]
        closest_left = fast_closest_pair(left_list)
        closest_right = fast_closest_pair(right_list)
        min_halves = min(closest_left, (closest_right[0], closest_right[1] + split, closest_right[2] + split))
        mid = 0.5 * (cluster_list[split - 1].horiz_center() + cluster_list[split].horiz_center())
        min_cross = closest_pair_strip(cluster_list, mid, min_halves[0])
        closest_pair = min(min_halves, min_cross)
    return closest_pair

    
def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Takes a list of Cluster objects and two floats horiz_center and half_width.
    horiz_center specifies the horizontal position of the center line for a
    vertical strip. half_width specifies the maximal distance of any point in
    the strip from the center line. This function should implement the helper
    function described in ClosestPairStrip from Homework 3 and return a tuple
    corresponding to the closest pair of clusters that lie in the specified
    strip. (Again the return pair of indices should be in ascending order.)
    As one important coding note, you will need to sort a list of clusters by
    the horizontal (as well as vertical) positions of the cluster centers. This
    operation can be done in a single line of Python using the sort method for
    lists by providing a key argument of the form:
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    """
    index_list = [idx for idx in range(len(cluster_list)) \
                  if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width]
    index_list.sort(key=lambda idx0: cluster_list[idx0].vert_center())
    strip_len = len(index_list)
    closest_pair = (float('inf'), -1, -1)
    for idx1 in range(strip_len - 1):
        for idx2 in range(idx1 + 1, min(idx1 + 4, strip_len)):
            point1 = index_list[idx1]
            point2 = index_list[idx2]
            current_dist = (cluster_list[point1].distance(cluster_list[point2]), min(point1, point2), max(point1, point2))
            closest_pair = min(closest_pair, current_dist)
    return closest_pair



def hierarchical_clustering(cluster_list, num_clusters):
    """
    Takes a list of Cluster objects and applies hierarchical clustering as
    described in the pseudo-code HierarchicalClustering from Homework 3 to this
    list of clusters. This clustering process should proceed until num_clusters
    clusters remain. The function then returns this list of clusters.
    """
    list_len = len(cluster_list)
    while list_len > num_clusters:
        cluster_list.sort(key=lambda cluster: cluster.horiz_center())
        closest_pair = fast_closest_pair(cluster_list)
        cluster_list[closest_pair[1]].merge_clusters(
            cluster_list[closest_pair[2]])
        cluster_list.pop(closest_pair[2])
        list_len -= 1
    return cluster_list


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    def center_distance(cluster_center, center_point):
        """
        input: cluster_center(type = tuple)
               center_point(type = tuple)
        output: distance between the two points
        """

        return math.sqrt((cluster_center[1] - center_point[1]) ** 2 + (cluster_center[0] - center_point[0]) ** 2)
        
    # initialize k-means clusters to be initial clusters with largest populations
    pop_and_index = [(cluster_list[idx].total_population(), idx) for idx in range(0, len(cluster_list))]
    pop_and_index.sort()
    pop_order = [pop_and_index[idx][1] for idx in range(0, len(pop_and_index))]
    centers = [(cluster_list[idx].horiz_center(), cluster_list[idx].vert_center()) for idx in pop_order[:-(num_clusters+1):-1]]
    
    for dummy_ind in range(0, num_iterations):
        kmeans_clusters = []
        
        for idx in range(0, num_clusters):
            kmeans_clusters.append(alg_cluster.Cluster(set([]), centers[idx][0], centers[idx][1], 0, 0.0))
        
        for cluster in cluster_list:
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            dists = [center_distance(cluster_center, center) for center in centers]
            kmeans_clusters[dists.index(min(dists))].merge_clusters(cluster)
        
        centers = [(k_cluster.horiz_center(), k_cluster.vert_center()) for k_cluster in kmeans_clusters]
    
    return kmeans_clusters


def compute_distortions(cluster_list, data_table):
    """
    Takes a list of clusters and uses cluster_error to compute its distortion.
    """
    return sum([cluster.cluster_error(data_table) for cluster in cluster_list])

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]
def run():
    DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
    DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
    DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
    DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
    DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

    data_table = load_data_table(DATA_3108_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    codeskulptor.set_timeout(200)
    
    cluster_list = hierarchical_clustering(singleton_list, 15)
    print "Displaying", len(cluster_list), "hierarchical clusters"

    #cluster_list = kmeans_clustering(singleton_list, 15, 5)	
    #print "Displaying", len(cluster_list), "k-means clusters"

    
    viz.plot_it(data_table, cluster_list)
      
def create_cluster_list(url):
    data_table = viz.load_data_table(url)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    return singleton_list, data_table

#run()