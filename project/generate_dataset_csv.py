import random
import subprocess
import signal
import time
import os

import pandas as pd

def execute(src,dest):
    proc = subprocess.Popen(
        # Let it ping more times to run longer.
        ['make','ping-unlimited','source='+src,'destination='+dest],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return proc

# Change this
no_hosts = 4
zero_indexed=False

if zero_indexed:
    start=0
else:
    start=1

hosts = ['h'+str(i) for i in range(start,no_hosts+start)]
addresses = ['10.0.0.'+str(i+1) for i in range(no_hosts)]

ping_destinations = [random.choices(['10.0.0.'+str(i+1) for i in range(no_hosts) if i!=x],k=2) for x in range(no_hosts)]

processes=[]
for i in range(no_hosts): 
    processes.append(execute(hosts[i],ping_destinations[i][0]))
    processes.append(execute(hosts[i],ping_destinations[i][1]))

data=[]
for i in range(len(hosts)):
    server = hosts[i]
    for j in range(i+1,len(hosts)):
        proc = subprocess.Popen(
            # Let it ping more times to run longer.
            ['make','iperf-server','source='+server],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        time.sleep(1)
        op = os.popen('make iperf-client source={} destination={}'.format(hosts[j], addresses[i])).read().split('\n')
        op = [x for x in op if '%' in x]

        server_to_client = op[1].split()
        jitter = float(server_to_client[-5])
        bandwidth = float(server_to_client[-7])
        loss = float(server_to_client[-3][:-1]) # to remove /  from /0
        packets = float(server_to_client[-2])
        ping_op = os.popen('make ping source={} destination={}'.format(server,addresses[j])).read().split()
        delay = float(ping_op[-2].split('/')[1])
        data.append([server[1:],hosts[j][1:],packets,bandwidth,delay,jitter,loss])
        
        
        client_to_server = op[0].split()
        jitter = float(client_to_server[-5])
        bandwidth = float(client_to_server[-7])
        loss = float(client_to_server[-3][:-1]) # to remove /  from /0
        packets = float(client_to_server[-2])
        data.append([hosts[j][1:],server[1:],packets,bandwidth,delay,jitter,loss])
df = pd.DataFrame(data)
df.columns=['src','dst','PktsGen','AvgBw','AvgDelay','jitter','loss']
print(df)
df.to_csv('metrics.csv',index=False)
print('Done')

for proc in processes:
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

