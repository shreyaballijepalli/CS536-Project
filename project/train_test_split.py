import pandas as pd
from os import listdir
import os
import random

# Put all the data points in the folder data/complete before running this script


def clean_data():

    try:
        for folder in listdir('data/train'):
            if 'DS_Store' in folder:
                continue
            for topology in listdir('data/train/'+folder):
                if 'DS_Store' in topology:
                    continue
                for csv_file in listdir('data/train/'+folder+'/'+topology):
                    if 'routing' in csv_file or 'topology' in csv_file or '.csv' not in csv_file:
                        continue
                    df = pd.read_csv('data/train/'+folder+'/'+topology+'/'+csv_file)
                    df.loc[df['AvgBw']<10,'AvgBw'] = df[df['AvgBw']<10]['AvgBw']*1000
                    df.to_csv('data/train/'+folder+'/'+topology+'/'+csv_file, index=False)
                    # if len(df[(df['AvgBw']>=10) & (df['AvgBw']<=99)]) > 0 :
                    #     print('data/train/'+folder+'/'+topology+'/'+csv_file)
                    #     print(df)
                    #     exit(0)

    except:
        print('data/train/'+folder+'/'+topology+'/'+csv_file,df)

os.system('mkdir -p data/train')

def train_test_split():
    for folder in listdir('data/complete'):
        if 'DS_Store' in folder:
            continue
        for topology in listdir('data/complete/'+folder):
            if 'DS_Store' in topology:
                continue
            os.system('mkdir -p data/train/{}/{}'.format(folder,topology))
            os.system('cp data/complete/{0}/{1}/routing.csv data/train/{0}/{1}/routing.csv'.format(folder,topology))
            os.system('cp data/complete/{0}/{1}/topolo* data/train/{0}/{1}/topology.csv'.format(folder,topology))
            os.system('mkdir -p data/test/{}/{}'.format(folder,topology))
            os.system('cp data/complete/{0}/{1}/routing.csv data/test/{0}/{1}/routing.csv'.format(folder,topology))
            os.system('cp data/complete/{0}/{1}/topolo* data/test/{0}/{1}/topology.csv'.format(folder,topology))


            files = listdir('data/complete/'+folder+'/'+topology)
            files = [csv_file for csv_file in files if ('routing' not in csv_file and 'topology' not in csv_file and '.csv' in csv_file)]
            random_files = random.sample(files, int(len(files)*0.8))
            for _file in files:
                if _file in random_files:
                    os.system('cp data/complete/{0}/{1}/{2} data/train/{0}/{1}/{2}'.format(folder,topology,_file))
                else:
                    os.system('cp data/complete/{0}/{1}/{2} data/test/{0}/{1}/{2}'.format(folder,topology,_file))


