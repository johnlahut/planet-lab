#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime


# # Utilities and analysis setup

# In[2]:


# dict to map node ID to node address
node_map = {
    '1': 'planetlab2.citadel.edu',
    '2': 'planetlab2.c3sl.ufpr.br',
    '3': 'planetlab6.goto.info.waseda.ac.jp',
    '4': 'pl-dccd-01.cua.uam.mx',
    '5': 'planetlab3.rutgers.edu',
    '6': 'planetlab2.ie.cuhk.edu.hk',
    '7': 'planetlab1.temple.edu',
    '8': 'planetlab1.rutgers.edu'
}

node_loc = {
    '1': 'US (Citadel)',
    '2': 'Brazil',
    '3': 'Japan',
    '4': 'Mexico',
    '5': 'US (Rutgers 3)',
    '6': 'Hong Kong',
    '7': 'US (Temple)',
    '8': 'US (Rutgers 1)'
}

node_pairs = {
    '1': '1-2 & 2-1'
}

# dict to map each node's to its respective timezone


# ### Set the current working directory to the project root

# In[3]:


os.chdir("/Users/jlahut/UAlbany/comp-comm-networks/final-project/project/")


# ### Read in data files
# Data files have the following format `<type>_<src>-<dest>_<Y-M-D>_<H-M-S>`  
# *The timestamps in the file names are local to the node in which it came from*

# In[4]:


data = []
for filename in os.listdir("data/"):
    try:
        items = filename.split('_')

        measure = items[0]
        src, dest = items[1].split('-')

        date = items[2]
        time = items[3].split('.')[0]

        timestamp = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H-%M-%S')
        content = ''

        with open(os.path.join('data', filename), 'r') as file:
            content = file.read()
            
        if (src == '1' and dest == '2') or (src == '2' and dest == '1'):
            pair = '1-2 & 2-1'
        elif (src == '3' and dest == '5') or (src == '5' and dest == '3'):
            pair = '3-5 & 5-3'
        elif (src == '4' and dest == '7') or (src == '7' and dest == '4'):
            pair = '4-7 & 7-4'
        elif (src == '6' and dest == '8') or (src == '8' and dest == '6'):
            pair = '6-8 & 8-6'
        elif (src == '1' and dest == '5') or (src == '5' and dest == '1'):
            pair = '1-5 & 5-1'
        else:
            pair = 'Error'

        data.append([src, dest, timestamp, measure, node_map[src], node_map[dest], content, filename, pair])
    except:
        print(f'Could not read file: {filename}')


# ### Create 'master' dataframe to hold all raw data

# In[5]:


df = pd.DataFrame(data, columns = ['src_id', 'dest_id', 'time', 'measure', 'src_name', 'dest_name', 'raw_data', 'filename', 'pair'])


# ### Ping and Traceroute functions to be applied accross the dataframe
# - Used mainly for file parsing
# 

# In[6]:


# example format
# rtt min/avg/max/mdev = 68.244/68.337/68.498/0.129 ms or
# rtt min/avg/max/mdev = 68.244/68.337/68.498/0.129 ms, pipe n
# 20 packets transmitted, 20 received, 0% packet loss, time 19029ms
def analyze_ping(data):
    try:
        # --- parse out statistics ---
        # second to last line will always be calculated values
        # split on '=' sign, then strip all spaces, remove units, and finally split on '/'
        # giving the values we need
        metrics = data['raw_data'].split('\n')[-2].split('=')[1].strip().replace(' ms', '').split(',')[0].split('/')
        data['min_ping_time'], data['avg_ping_time'], data['max_ping_time'], data['sd_ping_time'] =             float(metrics[0]), float(metrics[1]), float(metrics[2]), float(metrics[3])
        
        # --- parse out packet loss ---
        # third to last line will always be the line with packet loss
        data['packet_loss'] = float(data['raw_data'].split('\n')[-3].split(',')[2].split(' ')[1].replace('%', ''))
    except Exception as e:
        print(f"No calculated data for: {data['filename']}")
    return data

def analyze_traceroute(data):
    # TODO
    return data


# ### Apply the functions

# In[7]:


df = df[df['measure'] == 'ping'].apply(analyze_ping, axis = 1)
# df = df[df['measure'] == 'traceroute'].apply(analyze_traceroute, axis = 1)


# ### Plotting average ping times for nodes

# In[8]:


for title, group in df[df['measure'] == 'ping'].groupby(['src_id', 'dest_id']):
    ax = group.plot(x = 'time', y = 'avg_ping_time', title = f'{node_loc[title[0]]} to {node_loc[title[1]]}')
    ax.legend(['Average Ping Time'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Time (ms)')


# ### Calculate CDF for packet loss and latency

# **Create CDF latency and CDF packet loss plots**

# In[9]:


# first group by each src, desc pair
fig, ax = plt.subplots(figsize=(12, 6))
legend = []
for title, group in df[df['measure'] == 'ping'].groupby(['pair']):
    
    # then group by the avg_ping_time
    stats_df = group.groupby('avg_ping_time')['avg_ping_time'].agg('count').pipe(pd.DataFrame).rename(
        columns = {'avg_ping_time': 'frequency'})
    
    # probability that the current time occurs
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
    # cumulative probability
    stats_df['cdf'] = stats_df['pdf'].cumsum()
    stats_df = stats_df.reset_index()
    
    # add the max value to each plot so that the CDF lines continue to end
    plt.plot(stats_df['avg_ping_time'].tolist()+[df['avg_ping_time'].max()],stats_df['cdf'].tolist()+[1])
    
    if '1-2' in title:
        legend.append('Nodes 1 and 2')
    elif '1-5' in title:
        legend.append('Nodes 1 and 5')
    elif '3-5' in title:
        legend.append('Nodes 3 and 5')
    elif '4-7' in title:
        legend.append('Nodes 4 and 7')
    elif '6-8' in title:
        legend.append('Nodes 6 and 8')
    ax.legend(legend)
    ax.set_title('Nodal Latency CDF')
    ax.set_xlabel('Average Ping Time (ms)')
    ax.set_ylabel('Probability')


# In[10]:


# first group by each src, desc pair
fig, ax = plt.subplots(figsize=(12, 6))
legend = []
for title, group in df[df['measure'] == 'ping'].groupby(['pair']):
    
    # then group by the avg_ping_time
    stats_df = group.groupby('packet_loss')['packet_loss'].agg('count').pipe(pd.DataFrame).rename(
        columns = {'packet_loss': 'frequency'})
    
    # probability that the current time occurs
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
    # cumulative probability
    stats_df['cdf'] = stats_df['pdf'].cumsum()
    stats_df = stats_df.reset_index()
    
    # add the max value to each plot so that the CDF lines continue to end
    plt.plot(stats_df['packet_loss'].tolist()+[df['packet_loss'].max()],stats_df['cdf'].tolist()+[1])
    
    if '1-2' in title:
        legend.append('Nodes 1 and 2')
    elif '1-5' in title:
        legend.append('Nodes 1 and 5')
    elif '3-5' in title:
        legend.append('Nodes 3 and 5')
    elif '4-7' in title:
        legend.append('Nodes 4 and 7')
    elif '6-8' in title:
        legend.append('Nodes 6 and 8')
    ax.legend(legend)
    ax.set_title('Nodal Packet Loss CDF')
    ax.set_xlabel('Packet Loss (%)')
    ax.set_ylabel('Probability')

