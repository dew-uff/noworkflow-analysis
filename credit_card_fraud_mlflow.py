import mlflow
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
import pandas as pd
import sys

def get_df():
    return pd.read_csv('creditcard.csv', encoding='utf-8')

def get_pca():
    pca_components = 3
    return PCA(n_components=pca_components)

def get_rus(random_seed):
    for i in range(2):
        rus = RandomUnderSampler(random_state=random_seed)
    return rus

def get_ypred(X_train, X_test, y_train):
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    return rf.predict(X_test)

def save_metrics(y_test, y_pred):
    roc_metric = roc_auc_score(y_test, y_pred)
    f1_metric = f1_score(y_test, y_pred)

    with open("out.txt", "w") as f:
        f.write("ROC="+str(roc_metric)+"\nF1="+str(f1_metric))


mlflow.set_experiment("credit_card_fraud")
with mlflow.start_run():
    df = get_df()
    X = df.drop('Class', axis=1)
    y = df['Class']
    pca = get_pca()
    # The PCA size lives inside get_pca(); to record it the user must repeat the
    # literal here -- if get_pca() later changes to 10, this annotation goes stale.
    mlflow.log_param("pca_components", 3)               # manual annotation
    random_seed = 42
    if len(sys.argv) > 1:
        random_seed = int(sys.argv[1])
    mlflow.log_param("random_seed", random_seed)        # manual annotation
    mlflow.log_param("test_size", 0.2)                  # manual annotation
    mlflow.log_param("model", "RandomForestClassifier") # manual annotation
    rus = get_rus(random_seed)
    X_resampled, y_resampled = rus.fit_resample(pca.fit_transform(X), y)
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=random_seed)
    y_pred = get_ypred(X_train, X_test, y_train)
    mlflow.log_metric("roc_auc", roc_auc_score(y_test, y_pred))  # manual annotation
    mlflow.log_metric("f1", f1_score(y_test, y_pred))           # manual annotation
    save_metrics(y_test, y_pred)
    mlflow.log_artifact("out.txt")                              # manual annotation
