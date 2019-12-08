#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime as dt


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
    '1-2 & 2-1': f"{node_loc['1']} ⟷ {node_loc['2']}",
    '1-5 & 5-1': f"{node_loc['1']} ⟷ {node_loc['5']}",
    '3-5 & 5-3': f"{node_loc['3']} ⟷ {node_loc['5']}",
    '4-7 & 7-4': f"{node_loc['4']} ⟷ {node_loc['7']}",
    '6-8 & 8-6': f"{node_loc['6']} ⟷ {node_loc['8']}",
}


# ### Set the current working directory to the project root

# In[3]:


os.chdir("/Users/jlahut/UAlbany/comp-comm-networks/final-project/project/")


# ### Read in data files
# Data files have the following format `<type>_<src>-<dest>_<Y-M-D>_<H-M-S>`  
# *The timestamps in the file names are local to the node in which it came from*

# In[4]:


data = []
print(f"Reading in {len(os.listdir('data/'))} files...")
for filename in os.listdir("data/"):
    try:
        items = filename.split('_')

        measure = items[0]
        src, dest = items[1].split('-')

        date = items[2]
        time = items[3].split('.')[0]

        timestamp = dt.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H-%M-%S')
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
    
    # only worries about ping
    if (data['measure'] != 'ping'):
        return data
    
    try:
        # --- parse out statistics ---
        # second to last line will always be calculated values
        # split on '=' sign, then strip all spaces, remove units, and finally split on '/'
        # giving the values we need
        metrics = data['raw_data'].split('\n')[-2].split('=')[1].strip().replace(' ms', '').split(',')[0].split('/')
        data['min_ping_time'], data['avg_ping_time'], data['max_ping_time'], data['sd_ping_time'] =             float(metrics[0]), float(metrics[1]), float(metrics[2]), float(metrics[3])
    except Exception as e:
        print(f"No calculated data for: {data['filename']} [stats]")
        
    try:
         
        # --- parse out packet loss ---
        # third to last line will always be the line with packet loss
        data['packet_loss'] = float(data['raw_data'].split('\n')[-3].split(',')[2].split(' ')[1].replace('%', ''))
    except Exception as e:
        print(f"No calculated data for: {data['filename']} [packetloss]")
    return data

def analyze_traceroute(data):
    
    from pprint import pprint
    
    # only worried about traceroute
    if data['measure'] != 'traceroute':
        return data
    
    try:
        traceroute = [x.strip() for x in data['raw_data'].split('\n')]
        routers = [x.split('  ')[1] for x in traceroute if len(x.split('  ')) > 1]
        ip_addresses = [x.split(' ')[1].replace('(', '').replace(')', '') for x in routers]
        
        data['num_hops'] = len(routers)
        data['ips'] = ip_addresses
        
        
        
    except Exception as e:
        print(f"No calculated data for {data['filename']} {e}")
        
        
    return data


# ### Apply the functions

# In[7]:


df = df.apply(analyze_ping, axis = 1)
df = df.apply(analyze_traceroute, axis = 1)


# In[8]:


df[df['filename'] == 'ping_7-4_2019-12-04_03-09-44.txt']['raw_data'].tolist()


# ### Plotting average ping times for nodes

# In[9]:


for title, group in df[df['measure'] == 'ping'].groupby(['pair']):
   fig, ax = plt.subplots(figsize=(12, 6))
   legend = []
   
   
   
   for t, g in group.groupby(['src_id']):
       plt.plot(g['time'].sort_values(), g['avg_ping_time'])
       legend.append(f'Source: {node_loc[t]}')
       
   ax.legend(legend)
   ax.set_xlabel('Date')
   ax.set_ylabel('Time (ms)')
   ax.set_title(f'Average Pairwise Ping Time {node_pairs[title]} [John Lahut]')
   


# ### Plotting number of hops for each pair

# In[10]:


for title, group in df[df['measure'] == 'traceroute'].groupby(['pair']):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    hop_values = group['num_hops'].unique().tolist()
    hop_values.sort()
    width = 0.35
    
    rect1 = None
    rect2 = None
    x_labels = []
    for i, (t, g) in enumerate(group.groupby(['src_id'])):
        counters = {k:0 for k in hop_values}
        x = np.arange(len(counters.keys()))
        for k in counters.keys():
            if k not in x_labels:
                x_labels.append(k)
        for row in g['num_hops']:
            counters[row] += 1
        if i == 0:
            rect1 = ax.bar(x - width / 2, counters.values(), width, label = f'Source: {node_loc[t]}')
        else:
            rect2 = ax.bar(x + width / 2, counters.values(), width, label = f'Source: {node_loc[t]}')
            
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rect1)
    autolabel(rect2)
    ax.legend()
    ax.set_xlabel('Number of Hops')
    ax.set_ylabel('Frequency')
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_title(f'Hop Distribution {node_pairs[set(group["pair"].values).pop()]} [John Lahut]')


# ### High level results of experiment

# Ping timing statistics

# |                        | US (Citadel) to Brazil | US (Citadel) to US (Rutgers 3) | Japan to US (Rutgers 3) | Mexico to US (Temple) | Hong Kong to US (Rutgers 1) |
# | ---------------------- | :--------------------: | :----------------------------: | :---------------------: | :-------------------: | :-------------------------: |
# | **Minimum ping time**  |        149.011         |             23.237             |         163.377         |        71.734         |           256.876           |
# | **Average ping time**  |        149.284         |             23.338             |         163.529         |        72.768         |           368.329           |
# | **Max ping time**      |        149.970         |             23.744             |         164.266         |        75.229         |           777.954           |
# | **Standard deviation** |         0.516          |             0.214              |          0.502          |         1.167         |           140.994           |

# In[11]:


def calc_gaps(group):
    
    # sort on time, shift column down, subtract the two for gap value
    group = group.assign(gaptime=group.sort_values(
        by=['time'])['time'] - group.sort_values(by=['time']).shift()['time'])
    
    # sort on time, shift column down, add a boolean if it exceeds the threshold
    group = group.assign(gap=group.sort_values(
        by=['time'])['time'] - group.sort_values(by=['time']).shift()['time'] > dt.timedelta(minutes=59))
   
    return group

# calculate the gaps for each node
df = df.groupby(['src_id', 'dest_id']).apply(calc_gaps)
# reset the indicies from the groupby function. columns will be grouped on both 'src_id' and 'dest_id',
# so drop them
df = df.reset_index(level=0, drop=True).reset_index(level=0, drop=True).reset_index().drop(columns=['index'])

# for title, group in df.groupby(['pair']):
    
#     print(f'---- Statistics for {title} ----')
#     print(f"{node_loc[title.split('-')[0]]} to {node_loc[title.split('-')[1].split(' ')[0]]}")
    
#     print(f'Mean minimum ping time: {group["min_ping_time"].describe()["mean"]}')
#     print(f'Mean average ping time: {group["avg_ping_time"].describe()["mean"]}')
#     print(f'Mean max ping time: {group["max_ping_time"].describe()["mean"]}')
#     print(f'Mean sd ping time: {group["sd_ping_time"].describe()["mean"]}')
#     print()


# ### Calculate CDF for packet loss and latency

# In[12]:


for i in range(2):
    # first group by each src, desc pair
    fig, ax = plt.subplots(figsize=(12, 6))
    legend = []
    
    if i == 1:
        ax.set_xlim(0, 1000)
    
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
        legend.append(node_pairs[title])
        
    if i == 0:
        ax.set_title('Nodal Latency CDF [John Lahut]')
    else:
        ax.set_title('Nodal Latency CDF (Max 1000 ms) [John Lahut]')
    ax.set_xlabel('Average Ping Time (ms)')
    ax.set_ylabel('Probability')
    ax.legend(legend)


# In[13]:


# first group by each src, desc pair
for i in range(2):
    fig, ax = plt.subplots(figsize=(12, 6))
    legend = []
    for title, group in df[df['measure'] == 'ping'].groupby(['pair']):

        # then group by the packet_loss
        stats_df = group.groupby('packet_loss')['packet_loss'].agg('count').pipe(pd.DataFrame).rename(
            columns = {'packet_loss': 'frequency'})
        
        

        # probability that the current time occurs
        stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
        # cumulative probability
        stats_df['cdf'] = stats_df['pdf'].cumsum()
        stats_df = stats_df.reset_index()
        
        # add the max value to each plot so that the CDF lines continue to end
        plt.plot([0] + stats_df['packet_loss'].tolist() + [df['packet_loss'].max()], 
                 [0] + stats_df['cdf'].tolist() + [1])

        legend.append(node_pairs[title])

    
    if i == 0:
        ax.set_title('Nodal Packet Loss CDF [John Lahut]')
    else:
        ax.set_xlim(-.1, 10)
        ax.set_title('Nodal Packet Loss CDF - Limit 10% [John Lahut]')
    ax.set_xlabel('Packet Loss (%)')
    ax.set_ylabel('Probability')
    ax.legend(legend)


# In[31]:


df[(df['pair'] == '6-8 & 8-6') & (df['measure'] == 'traceroute') & (df['num_hops'] == 21)]


# In[32]:


for title, group in df[df['measure'] == 'traceroute'].groupby(['pair']):
    data = set()
    with open(f'ips_{title}.txt', 'w') as file:
#         print(file.writelines(group['ips'].flatten().tolist()))
        ips = [x for x in group['ips'].to_numpy().flatten()]
        for x in ips:
            [data.add(y) for y in x]
    print(data)


# ### Reliabilty across Nodes

# In[33]:


def forwardLoop(data):
    #print('hi')
    # only worries about traceroute
   # print("test")
    floop = 0
    if (data['measure'] != 'traceroute'):
        return data
    try:
        traceroute = [x.strip() for x in data['raw_data'].split('\n')]
        routers = [x.split('  ')[1] for x in traceroute if len(x.split('  ')) > 1]
#         print(routers)
        ip_addresses = [x.split(' ')[1].replace('(', '').replace(')', '') for x in routers]
        #print (ip_addresses)
        for index, ip in enumerate(ip_addresses[2:], 2):
            #print(ip_addresses[index],"---" ,ip_addresses[index-1], "---" ,ip_addresses[index-2])
            if((ip_addresses[index] == ip_addresses[index-1]) and (ip_addresses[index] == ip_addresses[index-2])):
            #if((ip_addresses[index] == ip_addresses[index-1])):
                floop += 1
                break
        
        data["forwardLoops"] = floop
        floop = 0
        return data
    except Exception as e:
        print(e)


# In[34]:


df = df.apply(forwardLoop, axis = 1)


# In[35]:


df[ df['forwardLoops'] > 0.0]


# In[36]:


def unreachable(data):
    #print('hi')
    # only worries about traceroute
   # print("test")
    ploop = 0
    if (data['measure'] != 'traceroute'):
        return data
    try:
        traceroute = [x.strip() for x in data['raw_data'].split('\n')]
        routers = [x.split('  ')[1] for x in traceroute if len(x.split('  ')) > 1]
        lstRtr = ''.join(routers[-1:])
        #print(lstRtr)
        #print(lstRtr == '* * *')
        if(lstRtr == '* * *'):
            ploop = 1
            #print(routers)
        #print(ploop)
        data["unreachable"] = ploop
        ploop = 0
        return data
    except Exception as e:
        print(e)


# In[37]:


df = df.apply(unreachable, axis = 1)


# In[38]:


df[ df['unreachable'] == 1]


# In[39]:


def persistantLoop(data):
    #print('hi')
    # only worries about traceroute
   # print("test")
    ploop = 0
    if (data['measure'] != 'traceroute'):
        return data
    dest = data['dest_name'] 
    try:
        traceroute = [x.strip() for x in data['raw_data'].split('\n')]
        routers = [x.split('  ')[1] for x in traceroute if len(x.split('  ')) > 1]
        #print(routers)
        dns = [x.split(' ')[0] for x in routers]
        lastHop = ''.join(dns[-1:])
        if (lastHop != dest):
            ploop +=1
        #print(ploop)
        
        
        data["Persistant Loops"] = ploop
        ploop = 0
        return data
    except Exception as e:
        print(e)


# In[40]:


df = df.apply(persistantLoop, axis = 1)


# In[41]:


df[ df['Persistant Loops'] == 1]


# In[42]:


def flutter(data):
    #print('hi')
    # only worries about traceroute
   # print("test")
    fltr = 0
    if (data['measure'] != 'traceroute'):
        return data
    dest = data['dest_name'] 
    try:
        traceroute = [x.strip() for x in data['raw_data'].split('\n')]
        routers = [x.split('  ')[1:] for x in traceroute if len(x.split('  ')) > 1]
        #print(routers)
        #dns = [x.split(' ') for x in routers if len(x.split('  ')) > ]
        for index in routers:
            line = ''.join(index)
            flutter = line.split(' ')
            #print(len(flutter))
            if(len(flutter) > 5):
                fltr += 1
        #print(fltr)
        
        
        data["Fluttering"] = fltr
        fltr = 0
        return data
    except Exception as e:
        print(e)


# In[43]:


df = df.apply(flutter, axis = 1)


# In[44]:


df[ df['Fluttering'] > 0]


# In[45]:


for title, group in df[df['measure'] == 'traceroute'].groupby(['pair']):
    
    fig, ax = plt.subplots(figsize=(12, 6))
    flutter_values = group['Fluttering'].unique().tolist()
    flutter_values.sort()
    width = 0.35
    
    rect1 = None
    rect2 = None
    
    for i, (t, g) in enumerate(group.groupby(['src_id'])):
        counters = {k:0 for k in flutter_values}
        x = np.arange(len(counters.keys()))
        for row in g['Fluttering']:
            counters[row] += 1
        
        if i == 0:
            rect1 = ax.bar(x - width / 2, counters.values(), width, label = node_loc[t])
        else:
            rect2 = ax.bar(x + width / 2, counters.values(), width, label = node_loc[t])
            
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rect1)
    autolabel(rect2)
    ax.legend()
    ax.set_xlabel('Number of Fluttering Hops')
    ax.set_ylabel('Frequency')
#     ax.set_xticklabels(x_labels)
    ax.set_title(f'Packet Fluttering Distribution {node_pairs[set(group["pair"].values).pop()]}')


# In[ ]:




