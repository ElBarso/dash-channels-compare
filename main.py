import os
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport
from scipy.io import loadmat
from tsfresh import extract_features, feature_selection
from tsfresh.feature_extraction import MinimalFCParameters, EfficientFCParameters
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute
from sklearn.tree import DecisionTreeClassifier
from dtreeviz.trees import dtreeviz

def main():
    classes = []
    df = None

    count = 0
    for root, dirs, files in os.walk("C:/Users/Jonathan/Documents/Programmazione/Jupyter folder"):
        for file in [f for f in files if f.endswith(".mat")]:
            #parasites = file.split("g")[1].split("(")[0]
            parasites = file.split("(")[0][-3:] #to modify
            if parasites == "008":
                classes.append(0)
            elif parasites == "083":
                classes.append(1)
            else:
                classes.append(2)
            data_tmp = loadmat(os.path.join(root, file))
            df_loaded = pd.DataFrame(data_tmp['meas_plot_array']).transpose()
            df_loaded.drop(4, axis=1, inplace=True)
            dim = len(df_loaded.iloc[:, 1])
            df_loaded['id'] = count * np.ones(dim)
            time = np.array(range(0, dim))
            df_loaded['time'] = time
            if count != 0:
                df = pd.concat([df, df_loaded], axis=0)
            else:
                df = df_loaded
            count = count + 1

    ex_feat = extract_features(df,
                               column_id='id',
                               column_sort='time',
                               default_fc_parameters=MinimalFCParameters(),
                               #default_fc_parameters=EfficientFCParameters(),
                               #column_kind=None,
                               #column_value=None
                               )

    impute(ex_feat)
    X = ex_feat.to_numpy()
    y = np.array(classes)

    tree = DecisionTreeClassifier(max_depth=3)
    model = tree.fit(X,y)

    viz = dtreeviz(tree,
                   X,
                   y,
                   target_name='Infection',
                   feature_names=ex_feat.columns)
    viz.view()

    #y = np.array(classes)
    #features_filtered = select_features(ex_feat, y)
    #print(features_filtered.head())


if __name__ == '__main__': main()
