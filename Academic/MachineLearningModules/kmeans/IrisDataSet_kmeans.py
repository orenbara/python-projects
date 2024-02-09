
#import libraries
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score
#import datasets 
from sklearn import datasets
import pandas as pd

# plot the Iris data in a scatter diagram 
def plotData(data, names,labels,col1,col2, labelsType, centroids = np.empty([0,0])):
    plt.plot()
    #plot the titles
    plt.title("The Iris Dataset " + labelsType +  " labels")
    plt.xlabel(names[col1])
    plt.ylabel(names[col2])
    # plot the data with different color for every label and size of 50 pixels 
    myplot =plt.scatter(data[:,col1],data[:,col2],c = labels, s=50)
    # plot the centroids if exists in blue and with X marker 
    if (centroids.any()):
        plt.scatter(centroids[:,col1], centroids[:,col2], c='blue', marker = "x", s=80)
    plt.show(myplot)
    
# plot a bar diagram for the labels
def plotLabels(labels,labelsType):
    xmax=len(labels)
    plt.title("The Iris Dataset" + labelsType + " labels")
    plt.xlabel("Iris sample number")
    plt.ylabel("label")
    plt.bar(range(xmax),labels)
    plt.show()

#from sklearn import the Iris dataset
Iris = datasets.load_iris()
data = Iris.data
# Plot the Iris data with the true label
trueLabels = Iris.target+1 # true labeling
names = Iris.feature_names
labelType = "true"
plotData(data, names,trueLabels,0,1,labelType)
plotData(data, names,trueLabels,2,3,labelType)
plotLabels(trueLabels,labelType)

# Use the k-means algorithm to predict the data labels
k=3
#data = data[:, 2:4]
kmeans = KMeans(n_clusters = k).fit(data)
predictedLabels = kmeans.predict(data)+1      
centroids = kmeans.cluster_centers_

labelType = "predicted"
# plot the predicted results for the 0-1 data colomns
plotData(data, names,predictedLabels,0,1,labelType,centroids)
# plot the predicted results for the 2-3 data colomns
#plotData(data, names,predictedLabels,2,3,labelType,centroids)
plotLabels(predictedLabels,labelType)

# Find the silhouette values and its avrrage 
silhouetteAvg = silhouette_score(data, predictedLabels)
silhouetteValues = silhouette_samples(data, predictedLabels)  
#Plot the  silhouette results
plt.title("The silhouette plot for the various clusters.")
plt.xlabel("The silhouette coefficient values")
plt.ylabel("Cluster label")
plt.plot(silhouetteValues) 
plt.axis([0,len(predictedLabels),0,1])

# plot the silhouette average line
plt.hlines(silhouetteAvg, 0, len(predictedLabels), colors='red', linestyles="--") 
plt.show()

print("For clusters =", k,
      "The average silhouette_score is: %.2f"  %silhouetteAvg)


## Test results
# We cannot use simple array comparison between the predicted and true arrays - kmeans lables the clusters randomly
# So the solution for comparison here is:
    # first check which lable is the most predicted in each section (I beleve kmeans is more right then wrong here)
    # The compare each predicted section element to the most predicted in his section
df = pd.DataFrame({
    'predictedLabels': predictedLabels,
    'labels': trueLabels
})

# Create sections
section1 = df.loc[0:49]
section2 = df.loc[50:99]
section3 = df.loc[100:149]

# Count occurrences for each section
count_section1 = section1['predictedLabels'].value_counts().idxmax()
count_section2 = section2['predictedLabels'].value_counts().idxmax()
count_section3 = section3['predictedLabels'].value_counts().idxmax()

# Print results
print("Most common value in section 0-49:", count_section1)
print("Most common value in section 50-99:", count_section2)
print("Most common value in section 100-149:", count_section3)

## Test if any object is not matching the most repeated value in the cluster
# We are assuming the algorithm is correct for most decistions
error_counter=0
for item in predictedLabels[:50]:
    if item != count_section1:
        error_counter += 1
for item in predictedLabels[50:100]:
    if item != count_section2:
        error_counter += 1
for item in predictedLabels[100:]:
    if item != count_section3:
        error_counter += 1
print("Errors of kmenas", error_counter)
  
        