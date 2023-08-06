__author__='sudhir'

'''
This module contains goodness of fit test
>best_fit_distributions
'''

import math
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings("ignore")

import os





def best_fit_distributions(data ,max_shape_par=1,plot_dist=True,verbose=True):
    '''
    Chi-square goodness of fit test to check best fit of distribution for data.
    95 continious distribution checked from https://docs.scipy.org/doc/scipy/reference/stats.html
    :param data: Data input(should be a 1-d array/list)
    :param max_shape_par[int]: Distributions with max shape par, 0 to 3.eg. norm->0, t->1.Defaults to 2.
    :param plot_dist[binary]: Show top 10 distribution plots with p-value
    :return: Pandas Dataframe with distribution,p-value,shape parameters
    '''
    if isinstance(data, pd.core.frame.DataFrame):
        data = data[data.columns[0]]

    minimum_value = float(np.min(data))
    maximum_value = float(np.max(data))
    length_of_data = len(data)

    no_bin = int(1 + 3.3 * math.log10(length_of_data))
    expected_value, observed_value = [0 for i in range(no_bin)], [0 for i in range(no_bin)]
    bin_length = (maximum_value - minimum_value) / no_bin


    for value in data:
        try:
            observed_value[int((value - minimum_value) / bin_length)] += 1
        except IndexError:
            observed_value[no_bin - 1] += 1

    test_result = []
    dist_list = pd.DataFrame(distribution_data())
    dist_list = dist_list[dist_list["No_of_Shape_Parametrs"] <= max_shape_par]['Distribution'].values.tolist()
    if verbose:
        print(len(dist_list)," Distributions to be checked")
    for i in dist_list:
        start_range = minimum_value
        parameters_tuple = eval('stats. ' + i + '.fit(data)')
        a, b, c = '', '', ''
        if len(parameters_tuple) <= 5:
            add_string = str(parameters_tuple)[1:-1] + ")"
        else:
            continue
        loc = parameters_tuple[-2]
        scale = parameters_tuple[-1]
        if len(parameters_tuple) == 3: a = parameters_tuple[0]
        if len(parameters_tuple) == 4: a, b = parameters_tuple[0], parameters_tuple[1]
        if len(parameters_tuple) == 5: a, b, c = parameters_tuple[0], parameters_tuple[1], parameters_tuple[2]
        for nos in range(no_bin):
            expected_value[nos] = len(data) * (eval("stats. " + i + ".cdf(start_range + bin_length, " + add_string) -
                                               eval("stats. " + i + ".cdf(start_range, " + add_string))
            start_range += bin_length
        chi, p_value = stats.chisquare(observed_value, f_exp=expected_value)
        test_result += [[i, p_value, loc, scale, a, b, c]]
    column_name = ['Distribution', 'p-value', 'loc', 'scale', 'shape_par_1', 'shape_par_2', 'shape_par_3']
    if max_shape_par<3:
        test_result = pd.DataFrame([i[:-3 + max_shape_par] for i in test_result], columns=column_name[:-3 + max_shape_par])
    else:
        test_result = pd.DataFrame([i for i in test_result],
                                   columns=column_name)
    test_result = test_result.sort_values('p-value', ascending=False)
    test_result.reset_index(drop=True, inplace=True)
    if plot_dist:
        fig, ax = plt.subplots(2, 5, figsize=(20, 20))
        plt.figure(figsize=(10, 10))
        for dist in range(10):
            sns.distplot(data, color='b', ax=ax[int(dist / 5)][dist % 5])
            tuple_fit = eval('stats. ' + test_result.values[dist][0] + '.fit(data)')
            add_string = str(tuple_fit)[1:-1]
            sns.distplot(eval("stats. " + test_result.values[dist][0] + ".rvs( " + add_string + ",size=len(data))")
                         , color='r', ax=ax[int(dist / 5)][dist % 5])
            ax[int(dist / 5)][dist % 5].set_title \
                (test_result.values[dist][0] + " p-> " + "%.2f " % test_result.values[dist][1])

    return test_result

def distribution_data():
    return {'Distribution': {0: 'alpha',
  1: 'anglit',
  2: 'arcsine',
  3: 'argus',
  4: 'beta',
  5: 'betaprime',
  6: 'bradford',
  7: 'burr',
  8: 'burr12',
  9: 'cauchy',
  10: 'chi',
  11: 'chi2',
  12: 'cosine',
  13: 'crystalball',
  14: 'dgamma',
  15: 'dweibull',
  16: 'erlang',
  17: 'expon',
  18: 'exponnorm',
  19: 'exponweib',
  20: 'exponpow',
  21: 'f',
  22: 'fatiguelife',
  23: 'fisk',
  24: 'foldcauchy',
  25: 'foldnorm',
  26: 'frechet_r',
  27: 'frechet_l',
  28: 'genlogistic',
  29: 'gennorm',
  30: 'genpareto',
  31: 'genextreme',
  32: 'gamma',
  33: 'gengamma',
  34: 'genhalflogistic',
  35: 'gilbrat',
  36: 'gompertz',
  37: 'gumbel_r',
  38: 'gumbel_l',
  39: 'halfcauchy',
  40: 'halflogistic',
  41: 'halfnorm',
  42: 'halfgennorm',
  43: 'hypsecant',
  44: 'invgamma',
  45: 'invgauss',
  46: 'invweibull',
  47: 'johnsonsb',
  48: 'johnsonsu',
  49: 'kappa4',
  50: 'kappa3',
  51: 'ksone',
  52: 'kstwobign',
  53: 'laplace',
  54: 'levy',
  55: 'levy_l',
  56: 'logistic',
  57: 'loggamma',
  58: 'loglaplace',
  59: 'lognorm',
  60: 'lomax',
  61: 'maxwell',
  62: 'mielke',
  63: 'moyal',
  64: 'nakagami',
  65: 'ncx2',
  66: 'nct',
  67: 'norm',
  68: 'norminvgauss',
  69: 'pareto',
  70: 'pearson3',
  71: 'powerlaw',
  72: 'powerlognorm',
  73: 'powernorm',
  74: 'rdist',
  75: 'reciprocal',
  76: 'rayleigh',
  77: 'rice',
  78: 'recipinvgauss',
  79: 'semicircular',
  80: 'skewnorm',
  81: 't',
  82: 'trapz',
  83: 'triang',
  84: 'truncexpon',
  85: 'truncnorm',
  86: 'uniform',
  87: 'vonmises',
  88: 'vonmises_line',
  89: 'wald',
  90: 'weibull_min',
  91: 'weibull_max',
  92: 'wrapcauchy'},
 'No_of_Shape_Parametrs': {0: 1,
  1: 0,
  2: 0,
  3: 1,
  4: 2,
  5: 2,
  6: 1,
  7: 2,
  8: 2,
  9: 0,
  10: 1,
  11: 1,
  12: 0,
  13: 2,
  14: 1,
  15: 1,
  16: 1,
  17: 0,
  18: 1,
  19: 2,
  20: 1,
  21: 2,
  22: 1,
  23: 1,
  24: 1,
  25: 1,
  26: 1,
  27: 1,
  28: 1,
  29: 1,
  30: 1,
  31: 1,
  32: 1,
  33: 2,
  34: 1,
  35: 0,
  36: 1,
  37: 0,
  38: 0,
  39: 0,
  40: 0,
  41: 0,
  42: 1,
  43: 0,
  44: 1,
  45: 1,
  46: 1,
  47: 2,
  48: 2,
  49: 2,
  50: 1,
  51: 1,
  52: 0,
  53: 0,
  54: 0,
  55: 0,
  56: 0,
  57: 1,
  58: 1,
  59: 1,
  60: 1,
  61: 0,
  62: 2,
  63: 0,
  64: 1,
  65: 2,
  66: 2,
  67: 0,
  68: 2,
  69: 1,
  70: 1,
  71: 1,
  72: 2,
  73: 1,
  74: 1,
  75: 2,
  76: 0,
  77: 1,
  78: 1,
  79: 0,
  80: 1,
  81: 1,
  82: 2,
  83: 1,
  84: 1,
  85: 2,
  86: 0,
  87: 1,
  88: 1,
  89: 0,
  90: 1,
  91: 1,
  92: 1}}

