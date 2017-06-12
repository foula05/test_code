# section3_code.py

#!/usr/bin/python

import sys

import pandas as pd
import numpy as np

import math

import matplotlib.pyplot as plt

#pd.options.mode.chained_assignment = None

TOP_JOB_NO = 10

GRAPHED_STATES = ['ca', 'ny', 'ga', 'il', 'wa', 'tx', 'ma']

if len(sys.argv) != 3:
	print "Usage: python section1_code.py <file_path_to_input_file_name> <group_results_bu_state (y/n)>. Aborting..."
	sys.exit(-1)

data_file_name = sys.argv[1]

group_by_state = sys.argv[2].strip().lower()

# *** nation_wide ***
def nation_wide():
    all_rows = pd.read_csv(data_file_name, usecols = ['lca_case_number', 'lca_case_soc_name'])

    # group by occupational group and count how many applications are in each group
    rows_group_by_soc = all_rows['lca_case_soc_name'].value_counts()
    print 'Displaying the most needed job categories nationwide for 2014:\n'
    print rows_group_by_soc[:TOP_JOB_NO]
# *** end nation_wide ***

# *** choose_state ***
def choose_state(row):
    st = None
    if row['lca_case_workloc1_state'] != 'Nan':
        st = row['lca_case_workloc1_state']
    else:
        st = row['lca_case_workloc2_state']
    return (st)
# *** end choose_state ***

# *** by_state ***
def by_state():
    all_rows = pd.read_csv(data_file_name, usecols = ['lca_case_number', 'lca_case_soc_name',
        'lca_case_workloc1_state', 'lca_case_workloc2_state'])
    all_rows['state'] = all_rows.apply(lambda row : choose_state(row), axis = 1)

    # group by (state, occupational group) and count how many applications are in each group
    group_by_st_and_soc_cnt = all_rows.groupby(['state', 'lca_case_soc_name'])['lca_case_soc_name'].agg({'job_count':'count'})

    mask = group_by_st_and_soc_cnt.groupby(level = 0).agg('idxmax')

    group_by_st_and_soc_rnk = group_by_st_and_soc_cnt.loc[mask['job_count']]
    group_by_st_and_soc_rnk = group_by_st_and_soc_rnk.reset_index()
    print("\nOutput\n{}".format(group_by_st_and_soc_rnk))

    # plot results
    x_v = []
    y_v = []
    plt_xticks = []
    lbl = []
    indx = 1
    for r_index, r in group_by_st_and_soc_rnk.iterrows():
        if r['state'].lower() in GRAPHED_STATES: 
            x_v.append(indx) 
            y_v.append(r['job_count']) 
            plt_xticks.append(r['state']) 
            lbl.append(r['lca_case_soc_name'])
            indx = indx + 1
  
    x = np.array(x_v)
    y = np.array(y_v)

    plt.xticks(x, plt_xticks)
    plt.scatter(x, y)
    for i, txt in enumerate(lbl):
        plt.annotate(txt, (x[i], y[i]))
    plt.show()
# *** end by_state ***

if group_by_state == 'y':
    by_state()

if group_by_state == 'n':
    nation_wide()

exit(0)
