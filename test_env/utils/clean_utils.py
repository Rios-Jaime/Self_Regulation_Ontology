import pandas as pd
import numpy as np


def remove_outliers(data, quantile_range = 2.5):
    '''Removes outliers more than 1.5IQR below Q1 or above Q3
    '''
    data = data.copy()
    quantiles = data.apply(lambda x: x.dropna().quantile([.25,.5,.75])).T
    lowlimit = np.array(quantiles.iloc[:,1] - quantile_range*(quantiles.iloc[:,2] - quantiles.iloc[:,0]))
    highlimit = np.array(quantiles.iloc[:,1] + quantile_range*(quantiles.iloc[:,2] - quantiles.iloc[:,0]))
    data_mat = data.values
    data_mat[np.logical_or((data_mat<lowlimit), (data_mat>highlimit))] = np.nan
    data = pd.DataFrame(data=data_mat, index=data.index, columns=data.columns)
    return data

def transform_remove_skew(data, threshold=1, 
                          positive_skewed=None,
                          negative_skewed=None,
                          verbose=True):
    data = data.copy()
    if positive_skewed is None:
        positive_skewed = data.skew()>threshold
    if negative_skewed is None:
        negative_skewed = data.skew()<-threshold
    positive_subset = data.loc[:,positive_skewed]
    negative_subset = data.loc[:,negative_skewed]
    # transform variables
    # log transform for positive skew
    shift = pd.Series(0, index=positive_subset.columns)
    shift_variables = positive_subset.min()<=0
    shift[shift_variables] -= (positive_subset.min()[shift_variables]-1)
    positive_subset = np.log(positive_subset+shift)
    # remove outliers
    positive_tmp = remove_outliers(positive_subset)
    successful_transforms = positive_subset.loc[:,abs(positive_tmp.skew())<threshold]
    if verbose:
        print('*'*40)
        print('** Successfully transformed %s positively skewed variables:' % len(successful_transforms.columns))
        print('\n'.join(successful_transforms.columns))
        print('*'*40)
    dropped_vars = set(positive_subset)-set(successful_transforms)
    # replace transformed variables
    data.drop(positive_subset, axis=1, inplace = True)
    successful_transforms.columns = [i + '.logTr' for i in successful_transforms]
    if verbose:
        print('*'*40)
        print('Dropping %s positively skewed data that could not be transformed successfully:' % len(dropped_vars))
        print('\n'.join(dropped_vars))
        print('*'*40)
    data = pd.concat([data, successful_transforms], axis = 1)
    # reflected log transform for negative skew
    negative_subset = np.log(negative_subset.max()+1-negative_subset)
    negative_tmp = remove_outliers(negative_subset)
    successful_transforms = negative_subset.loc[:,abs(negative_tmp.skew())<threshold]
    if verbose:
        print('*'*40)
        print('** Successfully transformed %s negatively skewed variables:' % len(successful_transforms.columns))
        print('\n'.join(successful_transforms.columns))
        print('*'*40)
    dropped_vars = set(negative_subset)-set(successful_transforms)
    # replace transformed variables
    data.drop(negative_subset, axis=1, inplace = True)
    successful_transforms.columns = [i + '.ReflogTr' for i in successful_transforms]
    if verbose:
        print('*'*40)
        print('Dropping %s negatively skewed data that could not be transformed successfully:' % len(dropped_vars))
        print('\n'.join(dropped_vars))
        print('*'*40)
    data = pd.concat([data, successful_transforms], axis=1)
    return data.sort_index(axis = 1)


def drop_vars(data, drop_vars = [], saved_vars = []):
    if len(drop_vars) == 0:
        # variables that are calculated without regard to their actual interest
        basic_vars = ["\.missed_percent$","\.acc$","\.avg_rt_error$","\.std_rt_error$","\.avg_rt$","\.std_rt$"]
        #unnecessary ddm params
        ddm_vars = ['.*\.(EZ|hddm)_(drift|thresh|non_decision).+$']
        # variables that are of theoretical interest, but we aren't certain enough to include in 2nd stage analysis
        exploratory_vars = ["\.congruency_seq", "\.post_error_slowing$"]
        # task variables that are irrelevent to second stage analysis, either because they are correlated
        # with other DV's or are just of no interest. Each row is a task
        task_vars = ["demographics", # demographics
                    "(keep|release)_loss_percent", # angling risk task
                    ".first_order", "bis11_survey.total", # bis11
                    "bis_bas_survey.BAS_total", 
                    "dietary_decision.prop_healthy_choice", # dietary decision
                    "dot_pattern_expectancy.*errors", # DPX errors
                    "eating_survey.total", # eating total score
                    "five_facet_mindfulness_survey.total", 
                    "\.risky_choices$", "\.number_of_switches", # holt and laury
                    "boxes_opened$", # information sampling task
                    "_total_points$", # IST
                    "\.go_acc$", "\.nogo_acc$", "\.go_rt$", "go_nogo.*error.*", #go_nogo
                    "discount_titrate.hyp_discount_rate", "discount_titrate.hyp_discount_rate_(glm|nm)"  #delay discounting
                    "kirby.percent_patient","kirby.hyp_discount_rate$",  "kirby.exp_discount.*", 
                    "\.warnings$", "_notnow$", "_now$", #kirby and delay discounting
                    "auc", # bickel
                    "local_global_letter.*error.*", # local global errors
                    "PRP_slowing", # PRP_two_choices
                    "shape_matching.*prim.*", # shape matching prime measures
                    "sensation_seeking_survey.total", # SSS
                    "DDS", "DNN", "DSD", "SDD", "SSS", "DDD", "stimulus_interference_rt", # shape matching
                    "shift_task.*errors", "shift_task.model_fit", "shift_task.conceptual_responses", #shift task
                    "shift_task.fail_to_maintain_set", 'shift_task.perseverative_responses', # shift task continued
                     "go_acc","stop_acc","go_rt_error","go_rt_std_error", "go_rt","go_rt_std", # stop signal
                     "stop_rt_error","stop_rt_error_std","SS_delay", "^stop_signal.SSRT$", # stop signal continue
                     "stop_signal.*errors", "inhibition_slope", # stop signal continued
                     "stroop.*errors", # stroop
                     "threebytwo.*inhibition", # threebytwo
                     "num_correct", "weighted_performance_score", # tower of london
                     "sentiment_label" ,# writing task
                     "log_ll", "match_pct", "min_rss", #fit indices
                     "num_trials", "num_stop_trials"#num trials
                    ]
        drop_vars = basic_vars + exploratory_vars + task_vars + ddm_vars
    drop_vars = '|'.join(drop_vars)
    if len(saved_vars) > 0 :
        saved_vars = '|'.join(saved_vars)
        saved_columns = data.filter(regex=saved_vars)
        dropped_data =  data.drop(data.filter(regex=drop_vars).columns, axis = 1)
        final_data = dropped_data.join(saved_columns).sort_index(axis = 1)
    else:
        final_data = data.drop(data.filter(regex=drop_vars).columns, axis = 1)
    return final_data

    
def remove_correlated_task_variables(data, threshold=.85):
    tasks = np.unique([i.split('.')[0] for i in data.columns])
    columns_to_remove = []
    for task in tasks:
        task_data = data.filter(regex = '^%s' % task)
        corr_mat = task_data.corr().replace({1:0})
        i=0
        while True:
            kept_indices = np.where(abs(corr_mat.iloc[:,i])<threshold)[0]
            corr_mat = corr_mat.iloc[kept_indices,kept_indices]
            i+=1
            if i>=corr_mat.shape[0]:
                break
        columns_to_remove += list(set(task_data.columns)-set(corr_mat.columns))
    print( '*' * 50)
    print('Dropping %s variables with correlations above %s' % (len(columns_to_remove), threshold))
    print( '*' * 50)
    print('\n'.join(columns_to_remove))
    data = drop_vars(data,columns_to_remove)
    return data