import os,sys
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from tsfresh import extract_features, extract_relevant_features, select_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import ComprehensiveFCParameters
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report

import ipdb

def load_robot_execution_failures( data_file_name, multiclass=False):
    """
    Load the Robot Execution Failures LP1 Data Set[1].
    The Time series are passed as a flat DataFrame.

    Examples
    ========

    >>> from tsfresh.examples import load_robot_execution_failures
    >>> df, y = load_robot_execution_failures()
    >>> print(df.shape)
    (1320, 8)

    :param multiclass: If True, return all target labels. The default returns only "normal" vs all other labels.
    :type multiclass: bool
    :return: time series data as :class:`pandas.DataFrame` and target vector as :class:`pandas.Series`
    :rtype: tuple
    """
    id_to_target = {}
    df_rows = []

    with open(data_file_name) as f:
        cur_id = 0
        time = 0

        for line in f.readlines():
            # New sample --> increase id, reset time and determine target
            if line[0] not in ['\t', '\n']:
                cur_id += 1
                time = 0
                if multiclass:
                    id_to_target[cur_id] = line.strip()
                else:
                    id_to_target[cur_id] = (line.strip() == 'normal')
            # Data row --> split and convert values, create complete df row
            elif line[0] == '\t':
                values = list(map(int, line.split('\t')[1:]))
                df_rows.append([cur_id, time] + values)
                time += 1

    df = pd.DataFrame(df_rows, columns=['id', 'time', 'F_x', 'F_y', 'F_z', 'T_x', 'T_y', 'T_z'])
    ipdb.set_trace()
    y = pd.Series(id_to_target)

    return df, y

# load and visualize data
cwd = os.path.dirname(os.path.abspath(__file__))
data_file_name = os.path.join(cwd, 'data', 'robot-failure-dataset', 'lp1.data.txt')
df, y = load_robot_execution_failures(data_file_name)
ipdb.set_trace()
df[df.id == 3][['time', 'F_x', 'F_y', 'F_z', 'T_x', 'T_y', 'T_z']].plot(x='time', title='Success example (id 3)', figsize=(12, 6));
df[df.id == 20][['time', 'F_x', 'F_y', 'F_z', 'T_x', 'T_y', 'T_z']].plot(x='time', title='Failure example (id 20)', figsize=(12, 6));
plt.show()

#extract features
extraction_settings = ComprehensiveFCParameters()
X = extract_features(df, 
                     column_id='id', column_sort='time',
                     default_fc_parameters=extraction_settings,
                     impute_function= impute)



X_filtered = extract_relevant_features(df, y, 
                                       column_id='id', column_sort='time', 
                                       default_fc_parameters=extraction_settings)



X_train, X_test, X_filtered_train, X_filtered_test, y_train, y_test = train_test_split(X, X_filtered, y, test_size=.4)


cl = DecisionTreeClassifier()
cl.fit(X_train, y_train)
print(classification_report(y_test, cl.predict(X_test)))
print cl.n_features_

cl2 = DecisionTreeClassifier()
cl2.fit(X_filtered_train, y_train)
print(classification_report(y_test, cl2.predict(X_filtered_test)))
print cl2.n_features_


ipdb.set_trace()
