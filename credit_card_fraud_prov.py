from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
import pandas as pd
import sys

from prov.model import ProvDocument

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

    open("out.txt", "w").write("ROC="+str(roc_metric)+"\nF1="+str(f1_metric))


random_seed = 42
if len(sys.argv) > 1:
    random_seed = int(sys.argv[1])

# --- W3C PROV document built BY HAND (manual annotation) ---------------------
# Every entity, activity, and relation below must be declared and kept in sync
# with the code manually; nothing is captured automatically.
doc = ProvDocument()
doc.add_namespace('ex', 'http://example.org/credit_card_fraud#')

e_csv       = doc.entity('ex:creditcard.csv')
e_X         = doc.entity('ex:X')
e_y         = doc.entity('ex:y')
e_resampled = doc.entity('ex:resampled')
e_split     = doc.entity('ex:split_data')
e_ypred     = doc.entity('ex:y_pred')
e_out       = doc.entity('ex:out.txt')

a_load  = doc.activity('ex:get_df')
a_prep  = doc.activity('ex:prepare_features', other_attributes={'ex:pca_components': 3})
a_under = doc.activity('ex:undersample', other_attributes={'ex:random_seed': random_seed})
a_split = doc.activity('ex:split', other_attributes={'ex:test_size': 0.2})
a_train = doc.activity('ex:train_predict', other_attributes={'ex:model': 'RandomForestClassifier'})
a_eval  = doc.activity('ex:evaluate')

# actual computation, interleaved with manual provenance bookkeeping
df = get_df()
doc.wasGeneratedBy(e_csv, a_load)

X = df.drop('Class', axis=1)
y = df['Class']
doc.used(a_prep, e_csv)
doc.wasGeneratedBy(e_X, a_prep)
doc.wasGeneratedBy(e_y, a_prep)

pca = get_pca()
rus = get_rus(random_seed)
X_resampled, y_resampled = rus.fit_resample(pca.fit_transform(X), y)
doc.used(a_under, e_X)
doc.used(a_under, e_y)
doc.wasGeneratedBy(e_resampled, a_under)
doc.wasDerivedFrom(e_resampled, e_X)

X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=random_seed)
doc.used(a_split, e_resampled)
doc.wasGeneratedBy(e_split, a_split)
doc.wasDerivedFrom(e_split, e_resampled)

y_pred = get_ypred(X_train, X_test, y_train)
doc.used(a_train, e_split)
doc.wasGeneratedBy(e_ypred, a_train)
doc.wasDerivedFrom(e_ypred, e_split)

save_metrics(y_test, y_pred)
doc.used(a_eval, e_ypred)
doc.wasGeneratedBy(e_out, a_eval)
doc.wasDerivedFrom(e_out, e_ypred)

# serialize the hand-built provenance graph
doc.serialize('provenance.json')
