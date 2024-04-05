""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
Note, this is NOT a correct DTLearner; Replace with your own implementation.  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import warnings  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np


class DTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self._leaf_size = leaf_size
        self._verbose = verbose

    def author(self):
        return "szhou401"  # replace tb34 with your Georgia Tech username

    def add_evidence(self, data_x, data_y):
        self.tree = self._build_tree(data_x, data_y)
        if self._verbose:
            print("Printing DTLearner tree...")
            print(self.tree)

    def query(self, points):
        result = []
        for p in points:
            result.append(self._get_query_result(p))
        return np.asanyarray(result)

    def _get_query_result(self, point):
        # Start at the root node (node 0)
        node = 0

        # Function to check if the current node is a leaf
        def is_leaf(n):
            return np.isnan(self.tree[n][0])

        # Determine which child node to move to
        def next_node(n, split_val):
            if split_val <= self.tree[n][1]:
                return n + int(self.tree[n][2])
            else:
                return n + int(self.tree[n][3])

        # Traverse the tree until a leaf node is found
        while not is_leaf(node):
            feature_idx = int(self.tree[node][0])
            node = next_node(node, point[feature_idx])

        return self.tree[node][1]

    def _build_tree(self, data_x, data_y):
        num_data_points = data_x.shape[0]

        # Base cases for leaf nodes
        if num_data_points <= self._leaf_size or np.all(np.isclose(data_y, data_y[0])):
            return np.array([np.nan, np.mean(data_y), np.nan, np.nan])

        # Find the best feature to split on
        best_feature_index = self._get_best_feature_index(data_x, data_y)

        # Split data based on the median of the best feature
        split_val = np.median(data_x[:, best_feature_index])
        left_check = data_x[:, best_feature_index] <= split_val
        right_check = ~left_check
        # Edge case: if all data points go to one branch after split
        if np.all(left_check) or np.all(right_check):
            return np.array([np.nan, np.mean(data_y), np.nan, np.nan])
        # Recursive tree building for left and right branches
        left_tree = self._build_tree(data_x[left_check], data_y[left_check])
        right_tree = self._build_tree(data_x[right_check], data_y[right_check])

        # Determine root node's structure
        if left_tree.ndim == 1:
            root = [best_feature_index, split_val, 1, 2]
        else:
            root = [best_feature_index, split_val, 1, left_tree.shape[0] + 1]

        return np.vstack((root, left_tree, right_tree))

    def _get_best_feature_index(self, data_x, data_y):
        num_features = data_x.shape[1]
        best_correlation = -1
        best_feature_index = 0

        for feature_idx in range(num_features):
            feature_values = data_x[:, feature_idx]
            std_dev = np.std(feature_values)

            if std_dev > 0:
                correlation = abs(np.corrcoef(feature_values, data_y)[0, 1])
            else:
                correlation = 0

            if correlation > best_correlation:
                best_correlation = correlation
                best_feature_index = feature_idx

        return best_feature_index


