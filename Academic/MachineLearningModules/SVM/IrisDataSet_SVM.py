import matplotlib
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split


# We are using famos flower data set which has 4 features and 150 flowers
Iris = datasets.load_iris()

# We will use only 2 features so we could plot the data with 2 dimentional graphs
data = Iris.data[:, 2:4]
names =  Iris.feature_names[2:4]                    
labels = Iris.target

# Define collors for train and test points - we expect 3 clusters.
colorsTrain = ['blue', 'green', 'red']
colorsTest = ['yellow', 'pink', 'brown']


#split data to test and train
X_train, X_test, trainLabels, testLabels = train_test_split(data, labels, test_size = 0.5)

# title for the plots
titles = ['SVC with linear kernel',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 2) kernel']

C = 100.0  # SVM regularization parameter - for high value the module will allow less movment of problematic points.

# generate models
linear_svc = svm.SVC(kernel='linear', C=C).fit(X_train, trainLabels)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X_train, trainLabels)
poly_svc = svm.SVC(kernel='poly', degree=2, C=C).fit(X_train, trainLabels)




# plot the models
for i, svmModel in enumerate((linear_svc, rbf_svc, poly_svc)):
    
    #plot the train data set
    plt.plot()
    plt.title("The Iris Dataset labels")
    plt.xlabel(Iris.feature_names[0])
    plt.ylabel(Iris.feature_names[1])
    plt.scatter(X_train[:,0],X_train[:,1],c = trainLabels,  cmap=matplotlib.colors.ListedColormap(colorsTrain), s=50,label = "train")
    
    plt.xlabel(names[0])
    plt.ylabel(names[1])
    plt.title(titles[i])

    # Execute module classifing with the testing set on current kernel function. 
    predictedLabels = svmModel.predict(X_test)

    # get and plot the support vectors
    suppportVectors = svmModel.support_vectors_
    plt.scatter(suppportVectors[:,0],suppportVectors[:,1],c = "black", marker = "+", s=200, label="support vectors")

    # Plot the testing data set
    plt.scatter(X_test[:, 0], X_test[:, 1], c=testLabels, marker = "X", s=50,  cmap=matplotlib.colors.ListedColormap(colorsTest),label = "test")
    plt.legend()
    plt.show()
    
    

    ## Test results - we jsut compare the arrays.
    errCount = 0
    for i in range(len(testLabels)):
        if testLabels[i] != predictedLabels[i]:
            errCount+=1
    print(f"Errors: {errCount}")
    