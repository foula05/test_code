# section1_code.py

#!/usr/bin/python

import sys

import pandas as pd
import numpy as np

import math

import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

TOP_APPLICATIONS_COMPANY_NO = 10

NY_POSSIBLE_NAMES = ['NEW YORK', 'NEW YORK CITY', 'NEW YORK, NEW YORK', 'NEW YORK, NY',
                     'NEW YORK, NEW YORK 10003' 'NEW YORK,NEW YORK', 'NEW YORK,', 'NEW YORKI',
                     'NEW YOK', 'NEW YROK', 'NEW YORK CIY', 'MANHATTAN', 'NEW YORK, 10003',
                     'NEWYORK', 'MANHATTA', 'NEW YOUR', 'MANHATAN', 'NEW YORK CITY,',
                     'MANHATTAN, NEW YORK', 'NEW YORK, NY -', 'NEW YOURK', 'NEWYORK CITY', 'NEW YORK NY']

CA_POSSIBLE_NAMES = ['MOUNTAIN VIEW']

CONFIDENCE_INTERVAL = 0.95

if len(sys.argv) != 3:
	print "Usage: python section1_code.py <choose_question_to_answer (1/2/3)> <file_path_to_input_file_name>. Aborting..."
	sys.exit(-1)

which_question = int(sys.argv[1])

data_file_name = sys.argv[2]

# *** question1 ***
def question1():
    all_rows = pd.read_csv(data_file_name, usecols = ['lca_case_number', 'lca_case_employer_name', 
        'lca_case_workloc1_city', 'lca_case_workloc1_state', 'lca_case_workloc2_city', 'lca_case_workloc2_state'])
    # select only rows where the job location is in NYC
    ny_rows = all_rows.loc[(all_rows['lca_case_workloc1_city'].isin(NY_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc1_state'] == 'NY')) |
                            (all_rows['lca_case_workloc2_city'].isin(NY_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc2_state'] == 'NY'))]
    # group by employer name and count how many applications are in each group
    ny_rows_group_by_employer = ny_rows['lca_case_employer_name'].value_counts()
    print 'Displaying the top ' + str(TOP_APPLICATIONS_COMPANY_NO) + ' companies that have applied for the most VISAs in NYC:\n'
    print ny_rows_group_by_employer[:TOP_APPLICATIONS_COMPANY_NO]
# *** end question1 ***


# converts all salaries # in a dataframe to yearly salaries ******
def convert_wage_to_year(w, u):
    y_w = w 
    
    if str(u).lower() == 'month': 
        y_w = w * 12.0
    elif str(u).lower() == 'week': 
        y_w = w * 52.0
    elif str(u).lower() == 'bi-weekly': 
        y_w = w * 26.0
    elif str(u).lower() == 'day': 
        y_w = w * 365.0
    elif str(u).lower() == 'hour': 
        y_w = w * 8.0 * 5 * 52.0

    return (y_w)
# *** end convert_wage_to_year ***

# *** question2 ***
def question2():
    all_rows = pd.read_csv(data_file_name, usecols = ['lca_case_number', 'lca_case_employer_name', 
        'lca_case_workloc1_city', 'lca_case_workloc1_state', 'lca_case_workloc2_city',
        'lca_case_workloc2_state', 'lca_case_wage_rate_from', 'lca_case_wage_rate_unit'])
    # find all possible for workers located in NYC
    ny_rows = all_rows.loc[(all_rows['lca_case_workloc1_city'].isin(NY_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc1_state'] == 'NY')) |
                            (all_rows['lca_case_workloc2_city'].isin(NY_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc2_state'] == 'NY'))]

    # compute actual wage for each rwo and project it to a year
    ny_wage = ny_rows.apply(lambda row : convert_wage_to_year(row['lca_case_wage_rate_from'], row['lca_case_wage_rate_unit']), axis = 1)

    # and then the mean and standard deviation
    ny_wage_mean = np.nanmean(ny_wage)
    ny_wage_std = np.nanstd(ny_wage)
    print 'Mean and standard deviation of NYC wages: ' + str(ny_wage_mean) + ' ' + str(ny_wage_std)

    # find all possible for workers located in MOUNTAIN VIEW
    ca_rows = all_rows.loc[(all_rows['lca_case_workloc1_city'].isin(CA_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc1_state'] == 'CA')) |
                            (all_rows['lca_case_workloc2_city'].isin(CA_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc2_state'] == 'CA'))]
    # compute actual wage for each rwo and project it to a year
    ca_wage = ca_rows.apply(lambda row : convert_wage_to_year(row['lca_case_wage_rate_from'], row['lca_case_wage_rate_unit']), axis = 1)

    # and then the mean and standard deviation
    ca_wage_mean = np.nanmean(ca_wage) 
    ca_wage_std = np.nanstd(ca_wage)
    print 'Mean and standard deviation of Mountain View wages: ' + str(ca_wage_mean) + ' ' + str(ca_wage_std)

    mean_diff = abs(ny_wage_mean - ca_wage_mean)
    sterr_diff = math.sqrt(ny_wage_std * ny_wage_std / len(ny_wage) + ca_wage_std * ca_wage_std / len(ca_wage)) 
    df = len(ny_wage) - 1 + len(ca_wage) - 1
    ci = 1.96 # df = 40064, 95% interval
    ci_low = mean_diff - ci * sterr_diff
    ci_high = mean_diff + ci * sterr_diff
    print 'Confidence interval of mean difference: ' + str(ci_low) + ' : ' + str(ci_high)
# *** end question2 ***

# *** question3 ***
def question3():
    all_rows = pd.read_csv(data_file_name, usecols = ['lca_case_number', 'lca_case_employer_name', 
        'lca_case_workloc1_city', 'lca_case_workloc1_state', 'lca_case_workloc2_city', 'lca_case_workloc2_state',
        'lca_case_wage_rate_from', 'lca_case_wage_rate_unit'])
    # select only rows where the job location is in NYC
    ny_rows = all_rows.loc[(all_rows['lca_case_workloc1_city'].isin(NY_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc1_state'] == 'NY')) |
                            (all_rows['lca_case_workloc2_city'].isin(NY_POSSIBLE_NAMES) &
                                                (all_rows['lca_case_workloc2_state'] == 'NY'))]

    # compute number of VISA request per employer
    ny_visa_requests_group_by_employer = pd.DataFrame({'visa_count' : ny_rows.groupby(['lca_case_employer_name']).size()}).reset_index()
    #for r_index, r in ny_visa_requests_group_by_employer.iterrows():
    #    print r['lca_case_employer_name'] + ' ' + str(r['visa_count'])

    # and average proposed salary
    cs_lst = []
    emp_lst = []
    wg_lst = []
    for r_index, r in ny_rows.iterrows():
        c = r['lca_case_number']
        cs_lst.append(c)

        e = r['lca_case_employer_name']
        emp_lst.append(e)

        w = r['lca_case_wage_rate_from']
        u = r['lca_case_wage_rate_unit']
        wg = w
        if str(u).lower() == 'month':
            wg = w * 12.0
        elif str(u).lower() == 'week':
            wg = w * 52.0
        elif str(u).lower() == 'bi-weekly':
            wg = w * 26.0
        elif str(u).lower() == 'day':
            wg = w * 365.0
        elif str(u).lower() == 'hour':
            wg = w * 8.0 * 5 * 52.0
        wg_lst.append(wg)

    dt = { 'lca_case_number' : cs_lst,
           'lca_case_employer_name' : emp_lst,
           'lca_case_wage_rate' : wg_lst}
    df = pd.DataFrame(dt)
    avg_ny_wages_by_employer = pd.DataFrame({'wage_avg' : df.groupby('lca_case_employer_name')['lca_case_wage_rate'].mean()}).reset_index()
    avg_ny_wages_by_employer['log_wage_avg'] = avg_ny_wages_by_employer.apply(lambda row : math.log(row['wage_avg']), axis = 1) 

    # and then compute their Pearson correlation coefficient
    pearson_corr_coeff = pd.merge(ny_visa_requests_group_by_employer, avg_ny_wages_by_employer, on = 'lca_case_employer_name')
    pearson_corr_coeff['log_wage_avg_visa_count'] = pearson_corr_coeff.apply(lambda row : row['log_wage_avg'] * row['visa_count'], axis = 1)
    pearson_corr_coeff['log_wage_avg_2'] = pearson_corr_coeff.apply(lambda row : row['log_wage_avg'] * row['log_wage_avg'], axis = 1)
    pearson_corr_coeff['visa_count_2'] = pearson_corr_coeff.apply(lambda row : row['visa_count'] * row['visa_count'], axis = 1)
    sum_wage_avg = pearson_corr_coeff['log_wage_avg'].sum()
    sum_visa_count = pearson_corr_coeff['visa_count'].sum()
    sum_wage_avg_visa_count = pearson_corr_coeff['log_wage_avg_visa_count'].sum()
    sum_wage_avg_2 = pearson_corr_coeff['log_wage_avg_2'].sum()
    sum_visa_count_2 = pearson_corr_coeff['visa_count_2'].sum()
    sigma = pearson_corr_coeff.size

    pearson_corr_coeff_value = (sigma * sum_wage_avg_visa_count - sum_wage_avg * sum_visa_count) / math.sqrt((sigma * sum_wage_avg_2 - sum_wage_avg * sum_wage_avg) * (sigma * sum_visa_count_2 - sum_visa_count * sum_visa_count))
    print 'Pearson correlation coefficient: ' + str(pearson_corr_coeff_value)

    # plot variables
    dt_plot = pearson_corr_coeff[['visa_count', 'wage_avg']]
    plt.scatter(pearson_corr_coeff['visa_count'], pearson_corr_coeff['wage_avg'])
    plt.ylabel('Average Proposed Wage')
    plt.xlabel('Number of VISA requests')
    plt.show()
    
# *** end question3 ***

if which_question == 1:
    question1()

if which_question == 2:
    question2()

if which_question == 3:
    question3()

exit(0)
