import numpy as np 
import pandas as pd 

# Input data files are available in the same directory in the repo.

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA, IncrementalPCA

sample_submission = pd.read_csv("sample_submission.csv")
test_data = pd.read_csv("test.csv")
training_data = pd.read_csv("train.csv")

training_data.shape

"""It has 42000 rows and 785 columns (features)"""

training_data.info()

training_data.head()

training_data.max().sort_values()

training_data.isna().sum().sort_values(ascending=False)

training_data.duplicated().sum()

"""There are no duplicated rows in the dataframe"""

training_data.columns

count_table = training_data.label.value_counts()
count_table = count_table.reset_index().sort_values(by='label')
count_table = count_table.rename(columns={'label': 'index', 'count': 'label'})
count_table

plt.figure(figsize=(10, 5))
sns.barplot(x='index', y='label', data=count_table)

digit_means = training_data.groupby('label').mean()
digit_means.head()
plt.figure(figsize=(18, 10))
sns.heatmap(digit_means)

# average feature values
round(training_data.drop('label', axis=1).mean(), 2).sort_values()

# splitting into X and y
X = training_data.drop("label", axis = 1)
y = training_data['label']

# scaling the features
X_scaled = scale(X)

# train test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size = 0.3, random_state = 101)

# applying PCA to find number of Principal components to use
pca = PCA(svd_solver='randomized', random_state=42)
pca.fit(X_train)


fig = plt.figure(figsize = (12,8))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.show()

pca = IncrementalPCA(n_components=400)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)

X_train.shape


# model with optimal hyperparameters

# model
model = SVC(C=10, gamma = 0.001, kernel="rbf")

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# metrics
print("accuracy", metrics.accuracy_score(y_test, y_pred), "\n")

# scaling test data
# splitting into X and y
X_test_data = test_data
X_test_data = scale(X_test_data)
X_test_data = pca.transform(X_test_data)
y_test_pred = model.predict(X_test_data)
y_test_pred

output = pd.DataFrame({"ImageId": i+1 , "Label": y_test_pred[i]} for i in range(0, X_test_data.shape[0]))
output.to_csv('submission.csv', index=False)