import os, re
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


def dataload(root_path):

    df = None
    classes = []
    count = 0
    unique_par = []

    # recursively search into folder tree opening all matlab files ".mat"
    for root, dirs, files in os.walk(root_path):
        for file in [f for f in files if f.endswith(".mat")]:

            # define target string to search for and isolate, for each file name
            target_string = re.compile(r'_\w\d\d\d+')
            parasites = target_string.findall(file)[0][2:]

            # fill unique with unique target string values
            # and store the corresponding index value of the
            # item (used as class index) into classes
            if parasites in unique_par:
                classes.append(unique_par.index(parasites))
            else:
                unique_par.append(parasites)
                classes.append(unique_par.index(parasites))

            # load data file from selected path and import it as pandas dataframe,
            # add the 'id' and 'time' columns later used for features extraction
            data_tmp = loadmat(os.path.join(root, file))
            df_loaded = pd.DataFrame(data_tmp['meas_plot_array']).transpose()
            dim = len(df_loaded.iloc[:, 1])
            df_loaded['id'] = count * np.ones(dim)
            time = np.array(range(0, dim))
            df_loaded['time'] = time

            #build the dataframe concatenating all opened files
            if count != 0:
                df = pd.concat([df, df_loaded], axis=0)
            else:
                df = df_loaded
            count = count + 1

    # remove not desired data Channele (Ch1 = 0, Ch2 = 1, Ch3 =2 , Ch4 = 3)
    # and the motor value column (4) indicating 'close' or 'far' position of
    # the motor from the chip (0 = close, 1= far)
    cols_to_remove = [0,1,2,4]
    df.drop(cols_to_remove, axis=1, inplace=True)

    if 4 in cols_to_remove:
        print('\nMotor column removed.\n')
    for i in range(4):
        if i in cols_to_remove:
            ch = i + 1
            print('Ch' + '{} '.format(ch) + 'EXCLUDED from analysis.')
        else:
            ch = i + 1
            print('Ch' + '{} '.format(ch) + 'USED for analysis.')



    # create and print a useful legend for class identification
    legend = dict(enumerate(unique_par))
    print('\nClasses legend:')
    print(legend)
    print('\n')

    return df, classes

def dataClassification(df=None, classes=None):

    # extract features frm data and substitute NaN, -inf and +inf
    # with 'mean', 'min' and 'max', respectively
    ex_feat = extract_features(df,
                               column_id='id',
                               column_sort='time',
                               default_fc_parameters=MinimalFCParameters(),
                               #default_fc_parameters=EfficientFCParameters(),
                               #column_kind=None,
                               #column_value=None
                               )
    impute(ex_feat)

    # prepare test dataset to train the Decision tree model
    X = ex_feat.to_numpy()
    y = np.array(classes)

    # create, train and visualize the decision tree model
    tree = DecisionTreeClassifier(max_depth=4)
    model = tree.fit(X,y)
    viz = dtreeviz(tree,
                   X,
                   y,
                   target_name='Infection',
                   feature_names=ex_feat.columns)
    viz.view()

    ## filter relevant features from all the extracted
    #features_filtered = select_features(ex_feat, y)
    #print(features_filtered.head())

def main():
    path = "C:/Users/Jonathan/Documents/Programmazione/Jupyter folder"
    df, classes = dataload(path)
    dataClassification(df, classes)


if __name__ == '__main__': main()