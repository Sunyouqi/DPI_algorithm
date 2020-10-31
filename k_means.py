from sklearn.datasets import load_breast_cancer
import numpy as np
import math
import sys


class K_means_algo:
    def __init__(self, database):
        self.data = database
        
        
    def init_random(self, k):
        min_val = np.amin(self.data)
        max_val = np.amax(self.data)
        column_number = len(self.data[0]) if len(self.data) else 0
        #random_k = np.random.uniform(low = min_val, high = max_val, size = (k, column_number))
        random_k = np.random.randint(low = 0 ,high = len(self.data)-1, size = k)
        result = []
        for i in random_k:
            result.append(self.data[i])
        
        return result
        
    def euclidean_distance(self, instance_1, instance_2):
        distance = 0
        for i in range(len(instance_1)):
            distance += (instance_1[i] - instance_2[i]) ** 2
        return math.sqrt(distance)
        
    
    def k_means(self, k):
        column_number = len(self.data[0]) if len(self.data) else 0
        total_instance = len(self.data)
        #initialization with random cluster centroids
        cluster_centroids = self.init_random(k)
        self.labels_ = np.zeros(total_instance)
        
        
        while True:
            #assign each point to a cluster centroid
            assignment_matrix = [[] for i in range(k)]
            
            for i in range(total_instance):
                assignment , min_distance = -1, sys.float_info.max
                for j in range(k):
                    cur_distance = self.euclidean_distance( cluster_centroids[j], self.data[i] )
                    if cur_distance < min_distance:
                        min_distance , assignment = cur_distance , j
                self.labels_[i] = assignment
                assignment_matrix[assignment].append(self.data[i].tolist())
            
                
            new_centroids = [[0 for i in range(column_number)] for j in range(k)]
            
            for i in range(len(assignment_matrix)):
                for j in range(column_number):
                    if len(assignment_matrix[i]):
                        for a in range(len(assignment_matrix[i])):
                            new_centroids[i][j] += (assignment_matrix[i][a][j])
                        new_centroids[i][j] /= len(assignment_matrix[i])
            
            new_centroids = np.array(new_centroids)
            
            if (new_centroids == cluster_centroids).all():
                self.assignment_matrix = assignment_matrix
                break;
            
            cluster_centroids = new_centroids
            
        self.cluster_centroids = cluster_centroids
        
        return self
            
    def calc_distortion(self):
        total_instance = len(self.data)
        assigned_centroid = [[]] * total_instance
        
        for i in range(total_instance):
            assigned_centroid[i] = list(self.cluster_centroids[int(self.labels_[i])])
            
        assigned_centroid = np.array(assigned_centroid)
        distortion = np.sum((self.data - assigned_centroid) ** 2) / total_instance
        return distortion
            
            

