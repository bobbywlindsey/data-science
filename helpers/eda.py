import pandas as pd
import matplotlib.pyplot as plt
import operator
import numpy as np
import itertools
import missingno as msno
import IPython.display as ipd
from .pre_processing import get_numerical_variables, get_categorical_variable_names


# Plots

def histogram(categorical_variable, plot_size=None):
    """
    :param categorical_variable: pandas.Series
    :param plot_size: 2-dim tuple
    :return: histogram
    """
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(categorical_variable.name)
    return categorical_variable.hist(bins=categorical_variable.nunique(), figsize=plot_size)


def plot_3d(dataframe, target_variable):
    """
    3d plot of data frame columns
    :param dataframe: pandas.DataFrame
    :param target_variable: pandas.Series
    :return: None
    """
    unique_labels = target_variable.unique()
    ordinal_encoding = [np.where(unique_labels == label)[0][0]
                        for label in target_variable]
    color_dict = {0: 'red', 1: 'green', 2: 'blue'}
    colors = [color_dict[each] for each in ordinal_encoding]
    threedee = plt.figure().gca(projection='3d')
    threedee.scatter(dataframe[[0]], dataframe[[1]],
                     dataframe[[2]], color=colors)
    threedee.set_xlabel(dataframe.columns.values[0])
    threedee.set_ylabel(dataframe.columns.values[1])
    threedee.set_zlabel(dataframe.columns.values[2])
    plt.show()
    return None


def plot_image(train, train_labels, dimensions, index):
    """
    :param train: pandas.DataFrame
    :param train_labels: pandas.DataFrame
    :param dimensions: tuple
    :param index: int
    :return: None
    """
    plt.imshow(train.iloc[index].values.reshape(dimensions))
    print("y = " + str(np.squeeze(train_labels.values[index])))
    return None


def plot_confusion_matrix(cm, class_labels, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    (This function is copied from the scikit docs.)
    :param cm: sklearn.metrics.confusion_matrix
    :param class_labels: numpy.array
    :param normalize: boolean
    :param title: str
    :param cmap: plt.cm
    :return None
    """
    plt.figure()
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(class_labels))
    plt.xticks(tick_marks, class_labels, rotation=45)
    plt.yticks(tick_marks, class_labels)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print(cm)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j], horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return None


# Tables, etc...

def show_missing_data(df):
    """ returns table of completeness of each row of the data from most incomplete to most complete"""
    # diplay table for missing percentages
    num_rows = df.shape[0]
    percent_missing = {}
    for column_name in df.columns.values:
        num_missing = df[column_name].isnull().sum()
        try:
            num_missing += (df[column_name] == '').sum()
        except:
            continue
        percent_missing[column_name] = (num_missing / num_rows) * 100
    percent_missing_df = pd.DataFrame({'% missing': pd.Series(percent_missing)})
    if percent_missing_df.empty:
        print('No missing data!')
    else:
        display(percent_missing_df)
    return None

def get_numerical_variable_names(df):
    """
    Gets numerical column names from dataframe
    :param df: pd.DataFrame
    :return: list
    """
    return list(get_numerical_variables(df).columns)


def exist_nan(pandas_series):
    """
    Checks if a series contains NaN values
    :param pandas_series: pandas.DataFrame
    :return: boolean
    """
    return pandas_series.isnull().values.any()


def series_contains(pandas_series, array_of_values):
    """
    Checks if a series contains a list of values
    :param pandas_series: pandas.DataFrame
    :param array_of_values: array
    :return: boolean
    """
    return not pandas_series[pandas_series.isin(array_of_values)].empty


def get_labels_to_rows_ratio(dataframe):
    """
    Gets ratio of unique labels to number of rows
    :param dataframe: pd.DataFrame
    :return: array of tuples
    """
    cat_columns = get_categorical_variable_names(dataframe)
    ratios = {col:len(dataframe[col].unique()) / dataframe[col].count() for col in cat_columns}
    sorted_ratios = sorted(ratios.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_ratios


def display(design_matrix):
    """
    Pretty print for numpy arrays and series
    :param design_matrix: numpy.array or pandas.Series
    :return: None
    """
    if isinstance(design_matrix, pd.Series) or (isinstance(design_matrix, np.ndarray) and design_matrix.ndim <= 2):
        ipd.display(pd.DataFrame(design_matrix))
    else:
        ipd.display(design_matrix)
    return None
