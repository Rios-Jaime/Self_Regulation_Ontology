import pandas as pd
import numpy as np
import scipy.stats as ss
import sklearn
import sklearn.decomposition as skdec
import matplotlib.pyplot as plt
import random
from rpy2.robjects.packages import importr

from utils.clean_utils import transform_remove_skew, remove_outliers, remove_correlated_task_variables, drop_vars

from utils.r_to_py_utils import missForest

from utils.EFA_assumption_utils import check_sample_size, bartlett_sphericity, kmo

from utils.EFA_HCA_utils import Results

imputed_vars = pd.read_csv('/SRO/dimensional_structure/meaningful_variables_imputed.csv', index_col='Unnamed: 0')
clean_vars = pd.read_csv('/SRO/dimensional_structure/meaningful_variables_clean.csv', index_col='Unnamed: 0')

task_df = drop_vars(imputed_vars, ['survey'], saved_vars = ['holt','cognitive_reflection'])
task_df_no_impute = drop_vars(clean_vars, ['survey'], saved_vars = ['holt','cognitive_reflection'])


verbose=True
bootstrap=False

boot_iter = 1000 
ID = str(random.getrandbits(16)) 
print(ID)


results = Results(data=task_df,
                  data_no_impute = task_df_no_impute,
                  dist_metric='abscorrelation',
                  name='task',
                  filter_regex='task',
                  boot_iter=boot_iter,
                  ID=ID)


for rotate in ['oblimin']:
    results.run_EFA_analysis(rotate=rotate, 
                             verbose=verbose, 
                             bootstrap=bootstrap)
    results.run_clustering_analysis(rotate=rotate, 
                                    verbose=verbose, 
                                    run_graphs=False)
    c = results.EFA.get_c()
    # name factors and clusters
    #factor_names = subset.get('%s_factor_names' % rotate, None)
    #cluster_names = subset.get('%s_cluster_names' % rotate, None)
    #if factor_names:
        #results.EFA.name_factors(factor_names, rotate=rotate)
    #if cluster_names:
        #results.HCA.name_clusters(cluster_names, inp='EFA%s_%s' % (c, rotate))
