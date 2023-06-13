################################################
## analyze eye gazing with labels
################################################

import matplotlib.pyplot as plt
import csv
import os
import  sys
import json
from shapely.geometry import Point, Polygon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


################################################
# global variables
################################################
result = pd.read_csv("/Users/fevroniavansickle/Desktop/EyeTrack/Data/001/Eye_Data_001_XYZ/result.csv")
# interval = 500000 # half second NEEDS TO CHANGE
# scene_dict = {0:'p1', 1:'p2', 2:'scene1'}
# id_set_dict = {'A': 1, 'B':2}

# participants = pd.read_csv('participants_label.csv', sep=',')
# print(participants.head())
participants = pd.DataFrame()
################################################
# longest duration of time spent looking at the suspect
################################################
def fixation(df, label, start1, end1):
    start = 0
    end = 0
    length = 0
    for i in range(start1, end1):

        if df[label][i] == True:

            if start == 0:
                start = df['timestamp'][i]
                end = start
            else:
                end = df['timestamp'][i]
        else:
            if end - start > length:
                length = end - start
            start = 0
            end = 0
    return length*120 / 1000

################################################
# This could simply be calculated as the number of seconds spent looking at the suspect divided by 30
################################################
def percentage_of_time_on_suspect(df, label, start, end):
    count_spend = 0
    for i in range(start, end):
        if df[label][i] == True:
            count_spend += 1
    return count_spend / len(df[label])

################################################
# how many times participant return to suspect
################################################
def returns_to_suspect(df, label, start, end):
    flag = False
    count_return = 0
    for i in range(start, end):
        if df[label][i] == True and flag == False:
            count_return += 1
            flag = True
        elif df[label][i] != True:
            flag = False
    return count_return



data_dir_name = '/Users/fevroniavansickle/Desktop/EyeTrack/Data'
print ("the folder is %s" % (data_dir_name))

tobii_eye_folder_name = 'HIT'
tobii_path = ''
participants_ids = os.listdir(data_dir_name)
participants_ids.sort()
label_list = []
for par_id in participants_ids:
    # files are 001, 002
    if len(par_id) == 3:
        par_dict = {}
        par_dict['id'] = par_id
        #THIS THROWS KEYERROR########################################
        setVal = result['setVal'][np.where(result['id'] == int(par_id))[0][0]]
        par_dict['setVal'] = setVal
        ############################################################3
        single_par_folder = os.listdir(data_dir_name + '/' + par_id)
        hit_folder_path = data_dir_name + '/' + par_id +'/'+ par_id+'_HIT'
        print(hit_folder_path)

        for single_file in single_par_folder:
            if 'RT' in single_file:
                with open(data_dir_name + '/' + par_id + '/' + single_file, "r") as ins:
                    for line in ins:
                        if'CalScene' in line[:-1].split(' ')[0]:
                            l = 'scene'+line[:-1].split(' ')[0][8:-1]

                            par_dict[l+'_rt'] = line[:-1].split(' ')[1]

            if 'PR' in single_file:
                flag_pr = False
                with open(data_dir_name + '/' + par_id + '/' + single_file, "r") as ins:
                    for line in ins:
                        l = 'scene'+(re.search(r'\d+', line.split(';')[0]).group())+'_pr'
                        if '(suppose to shoot)' in line.split(';')[0] and ': shoot' in line.split(';')[0]:
                            par_dict[l] = True
                        elif '(not suppose to shoot)' in line.split(';')[0] and ': did not shoot' in line.split(';')[0]:
                            par_dict[l] = True
                        else:
                            par_dict[l] = False
                        if l == 'scene12_pr':
                            par_dict['score'] = line.split(';')[1].split(':')[1]
                            print('par_dict[score]: ', par_dict['score'])


            if tobii_eye_folder_name in single_file:
                tobii_path = data_dir_name + '/' + par_id + '/' + single_file
                print('current in : '+tobii_path)     #/.../WSU_ED_001_EYE
                file_list = os.listdir(tobii_path)

                file_list.sort()                    # sort by time
                print('This folder has ', len(file_list), ' files: ',file_list )
                for scene_name in file_list:
                    df = pd.read_csv(tobii_path + '/'+ scene_name)
                    cols = df.columns

                    for i in range(3,len(cols)):
                        label = cols[i]
                        # print('scene_name: ', scene_name, ', long fix: ', fixation(df, label), ', percen: ', percentage_of_time_on_suspect(df, label), ', return: ', returns_to_suspect(df, label))
                        scene_label = scene_name.split('.')[0].split('_')[-1]+'_'+label

                        par_dict[scene_label+'_fix'] = fixation(df, label, 0, len(df[label]) )
                        par_dict[scene_label+'_per'] = percentage_of_time_on_suspect(df, label, 0, len(df[label]))
                        par_dict[scene_label+'_ret'] = returns_to_suspect(df, label, 0, len(df[label]))
                        for i in range(3):
                            unit_length = int(len(df[label]) / 3)
                            par_dict[scene_label + '_fix'+ str(i)] = fixation(df, label, i * unit_length, (i+1) * unit_length)
                            par_dict[scene_label + '_per'+ str(i)] = percentage_of_time_on_suspect(df, label,  i * unit_length, (i+1) * unit_length)
                            par_dict[scene_label + '_ret'+ str(i)] = returns_to_suspect(df, label, i * unit_length, (i+1) * unit_length)
        # print(par_dict)
        participants = participants.append(par_dict, ignore_index=True)
        participants.to_csv('participants2.csv', sep=',')


print('all finish')