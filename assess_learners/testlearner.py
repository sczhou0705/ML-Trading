""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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
"""

import BagLearner as bl
import DTLearner as dt
import math
import matplotlib.pyplot as plt
import numpy as np
import RTLearner as rt
import util


def main():
    np.random.seed(0)
    e1_q1_overfitting_leaf_size_chart()
    e2_q1_overfitting_leaf_size_bagging_chart()
    e3_f1_mae_comparison_dt_and_rt_chart()  # Mean Absolute Error comparison
    e3_f2_r_squared_comparison_dt_and_rt_chart()  # R-squared comparison


def e1_q1_overfitting_leaf_size_chart():
    trainX, trainY, testX, testY = create_train_and_test_datasets(read_file('Istanbul.csv'))
    leaf_sizes = range(1, 51, 2)  # Leaf size range from 1 to 50 with step 2
    out_of_sample = []
    in_sample = []

    for leaf_size in leaf_sizes:
        learner = dt.DTLearner(leaf_size=leaf_size)
        learner.add_evidence(trainX, trainY)
        in_sample.append(calculate_rmse(learner.query(trainX), trainY))
        out_of_sample.append(calculate_rmse(learner.query(testX), testY))

    plt.close()
    _, ax = plt.subplots()
    ax.xaxis.set_major_locator(plt.FixedLocator(leaf_sizes))  # Set the tick positions
    ax.grid(color='black', linestyle='dotted')
    colors = ['b', 'r']
    plt.plot(leaf_sizes, in_sample, linewidth=2.5, color=colors[0], alpha=0.4, label='In Sample')
    plt.plot(leaf_sizes, out_of_sample, linewidth=2.5, color=colors[1], alpha=0.4, label='Out of Sample')
    plt.title('Overfitting vs Leaf Size in Decision Tree')
    plt.xlabel('Leaf Size', fontsize='20')
    plt.ylabel('RMSE', fontsize='20')
    plt.legend(['In Sample', 'Out of Sample'])
    plt.savefig("images/OverfittingAndLeafSizeInDecisionTree.png", bbox_inches='tight')


def e2_q1_overfitting_leaf_size_bagging_chart():
    trainX, trainY, testX, testY = create_train_and_test_datasets(read_file('Istanbul.csv'))
    leaf_sizes = range(1, 51, 2)  # Leaf size range from 1 to 50 with step 2
    out_of_sample = []
    in_sample = []
    bags = 20


    for leaf_size in leaf_sizes:
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs={'leaf_size': leaf_size}, bags=bags,boost = False, verbose = False)
        learner.add_evidence(trainX, trainY)
        in_sample.append(calculate_rmse(learner.query(trainX), trainY))
        out_of_sample.append(calculate_rmse(learner.query(testX), testY))

    plt.close()
    _, ax = plt.subplots()
    ax.xaxis.set_major_locator(plt.FixedLocator(leaf_sizes))  # Set the tick positions
    ax.grid(color='black', linestyle='dotted')
    colors = ['b', 'r']
    plt.plot(leaf_sizes, in_sample, linewidth=2.5, color=colors[0], alpha=0.4,
             label='In Sample')
    plt.plot(leaf_sizes, out_of_sample, linewidth=2.5, color=colors[1], alpha=0.4,
             label='Out of Sample')
    plt.title('Overfitting vs Leaf Size with {} Bags'.format(bags))
    plt.xlabel('Leaf Size', fontsize='20')
    plt.ylabel('RMSE', fontsize='20')
    plt.legend(['In Sample', 'Out of Sample'])
    plt.savefig("images/OverfittingAndLeafSizeWithBags.png", bbox_inches='tight')


def e3_f1_mae_comparison_dt_and_rt_chart():
    filenames = [
        '3_groups.csv',
        'Istanbul.csv',
        'ripple.csv',
        'simple.csv',
        'winequality-red.csv',
        'winequality-white.csv'
    ]

    out_of_sample_dt = []
    out_of_sample_rt = []
    leaf_size = 20

    for filename in filenames:
        trainX, trainY, testX, testY = create_train_and_test_datasets(read_file(filename))

        learner = dt.DTLearner(leaf_size=leaf_size)
        learner.add_evidence(trainX, trainY)
        out_of_sample_dt.append(calculate_mae(testY, learner.query(testX)))

        learner = rt.RTLearner(leaf_size=leaf_size)
        learner.add_evidence(trainX, trainY)
        out_of_sample_rt.append(calculate_mae(testY, learner.query(testX)))

    plt.close()
    _, ax = plt.subplots()
    ax.xaxis.set_major_locator(plt.FixedLocator(np.arange(len(filenames))))  # Set the tick positions
    ax.set_xticklabels(filenames,rotation = 45,fontsize=10)  # Set the tick labels
    ax.grid(color='black', linestyle='dotted')
    colors = ['b', 'r']
    width = 0.3
    x = np.arange(len(filenames))
    plt.bar(x - width / 2, out_of_sample_dt, width, color=colors[0], alpha=0.4, label='Decision Tree')
    plt.bar(x + width / 2, out_of_sample_rt, width, color=colors[1], alpha=0.4, label='Random Tree')
    plt.title('MAE Comparison: Decision Tree vs Random Tree')
    plt.xlabel('Data', fontsize='10')
    plt.ylabel('MAE', fontsize='10')
    plt.legend(['Decision Tree', 'Random Tree'])
    plt.tight_layout()
    plt.savefig("images/MAEComparisonDecisionTreeAndRandomTree.png", bbox_inches='tight')


def e3_f2_r_squared_comparison_dt_and_rt_chart():
    filenames = [
        '3_groups.csv',
        'Istanbul.csv',
        'ripple.csv',
        'simple.csv',
        'winequality-red.csv',
        'winequality-white.csv'
    ]

    r_squared_dt = []
    r_squared_rt = []
    leaf_size = 10

    for filename in filenames:
        trainX, trainY, testX, testY = create_train_and_test_datasets(read_file(filename))

        learner = dt.DTLearner(leaf_size=leaf_size)
        learner.add_evidence(trainX, trainY)
        r_squared_dt.append(calculate_r_squared(testY, learner.query(testX)))

        learner = rt.RTLearner(leaf_size=leaf_size)
        learner.add_evidence(trainX, trainY)
        r_squared_rt.append(calculate_r_squared(testY, learner.query(testX)))

    plt.close()
    _, ax = plt.subplots()
    ax.xaxis.set_major_locator(plt.FixedLocator(np.arange(len(filenames))))  # Set the tick positions
    ax.set_xticklabels(filenames,rotation = 45,fontsize=10)  # Set the tick labels
    ax.grid(color='black', linestyle='dotted')
    colors = ['b', 'r']
    width = 0.35
    x = np.arange(len(filenames))
    plt.bar(x - width / 2, r_squared_dt, width, color=colors[0], alpha=0.4, label='Decision Tree')
    plt.bar(x + width / 2, r_squared_rt, width, color=colors[1], alpha=0.4, label='Random Tree')
    plt.title('R-squared Comparison: Decision Tree vs Random Tree')
    plt.xlabel('Data', fontsize='10')
    plt.ylabel('R-squared', fontsize='10')
    plt.legend(['Decision Tree', 'Random Tree'])
    plt.tight_layout()
    plt.savefig("images/RSquaredComparisonDecisionTreeVsRandomTree.png", bbox_inches='tight')


def read_file(filename):
    with util.get_learner_data_file(filename) as f:
        alldata = np.genfromtxt(f, delimiter=',')
        if filename == 'Istanbul.csv':
            return alldata[1:, 1:]
        return alldata


def create_train_and_test_datasets(alldata):
    spilt_data = int(alldata.shape[0] * 0.6)
    train_data = alldata[:spilt_data, :]
    trainX = train_data[:, :-1]
    trainY = train_data[:, -1]

    test_data = alldata[spilt_data:, :]
    testX = test_data[:, :-1]
    testY = test_data[:, -1]

    return trainX, trainY, testX, testY


def calculate_rmse(predictions, targets):
    return math.sqrt(np.mean((targets - predictions) ** 2))


def calculate_mae(predictions, targets):
    return np.mean(np.abs(targets - predictions))


def calculate_r_squared(predictions, targets):
    mean_y = np.mean(targets)
    ss_tot = np.sum((targets - mean_y) ** 2)
    ss_res = np.sum((targets - predictions) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared


if __name__ == '__main__':
    main()
