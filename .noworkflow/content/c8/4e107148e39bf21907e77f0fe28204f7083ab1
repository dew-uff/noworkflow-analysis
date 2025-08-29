from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
import pandas as pd
import sys

df = pd.read_csv('creditcard.csv', encoding='utf-8')
X = df.drop('Class', axis=1)
y = df['Class']

# Here we are stamping pca_components as a now_tag_variable, and started 
# monitoring it
pca_components = 3
pca = PCA(n_components=pca_components)
X_pca = pca.fit_transform(X)

# Same here with random_seed
random_seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
for i in range(2):
    rus = RandomUnderSampler(random_state=random_seed)
X_resampled, y_resampled = rus.fit_resample(X_pca, y)

# Same with test_dim
test_dim = 0.2
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=test_dim, random_state=random_seed)

# Keeping the model type 
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# Finally, keeping the metrics roc and f1
roc_metric = roc_auc_score(y_test, y_pred)
f1_metric = f1_score(y_test, y_pred)

open("out.txt", "w").write("ROC="+str(roc_metric)+"\nF1="+str(f1_metric))