import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets

# Create a grid - The grid will create a huge set of points which covers most of the options
# In this example the grid will even look like a background
# Since python does not have native matrix - the work here is done using np arrays.
def gen_grid(data):
    # Find min and max values - so we could define the first and last point of the grid
    x_min, x_max = data[:, 0].min() - 0.1, data[:, 0].max() + 0.1
    y_min, y_max = data[:, 1].min() - 0.1, data[:, 1].max() + 0.1
    h = .02  # step size in the mesh - small number here will result in a lot of points

    # create  mesh grid 
    xGrid, yGrid = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

    # Flat the arrays
    xGridFlat = xGrid.reshape(-1)
    yGridFlat = yGrid.reshape(-1)
    #concatenate  the arrays 
    grid = np.c_[xGridFlat,yGridFlat]
    return grid


Iris = datasets.load_iris()
data = Iris.data[:, 2:4]  # we only take two features. We could
names =  Iris.feature_names[2:4]                    
labels = Iris.target

grid = gen_grid(data)

# title for the plots
titles = ['SVC with linear kernel',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 3) kernel']

C = 10.0  # SVM regularization parameter

# generate models
linear_svc = svm.SVC(kernel='linear', C=C).fit(data, labels)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(data, labels)
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(data, labels)

# plot the models
for i, svmModel in enumerate((linear_svc, rbf_svc, poly_svc)):
    plt.xlabel(names[0])
    plt.ylabel(names[1])
    plt.title(titles[i])    
    # predict the grid labels
    predictedLabels = svmModel.predict(grid)
    # plot the grid labels (will look like a background)
    plt.scatter(grid[:,0],grid[:,1], c=predictedLabels, cmap=plt.cm.coolwarm)
    # Plot the real data points 
    # get and plot the support vectors
    suppportVectors = svmModel.support_vectors_
    
    plt.scatter(suppportVectors[:,0],suppportVectors[:,1],c = "black", marker = "+", s=200, label="support vectors")
    plt.scatter(data[:, 0], data[:, 1], c=labels,s=30)
    plt.show()