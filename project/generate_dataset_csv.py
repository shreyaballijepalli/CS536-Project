import sys
import random
import subprocess
import signal
import time
import os
import psutil

import pandas as pd

def execute(src,dest):
    print("Execute ",src, ", ",dest)
    proc = subprocess.Popen(
        # Let it ping more times to run longer.
        ['make','ping-unlimited','source='+src,'destination='+dest],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return proc

def kill_process(src,dst):
    name = "{src:s} ping {dst:s}".format(src=src,dst=dst)
    child = subprocess.Popen(['pgrep','-f',name], stdout=subprocess.PIPE, shell=False)
    result = child.communicate()[0]
    pid = int(result)
    print("Terminating ",pid)
    p = psutil.Process(pid)
    p.terminate()

def kill_iperf(src):
    name = "{src:s} iperf".format(src=src)
    child = subprocess.Popen(['pgrep','-f',name], stdout=subprocess.PIPE, shell=False)
    result = child.communicate()[0]
    pid = int(result)
    print("Terminating ",pid)
    p = psutil.Process(pid)
    p.terminate()

# Change this
no_hosts = 4
zero_indexed=True

bw = sys.argv[1]
print('bandwidth:', bw)

if zero_indexed:
    start=0
else:
    start=1

hosts = ['h'+str(i) for i in range(start,no_hosts+start)]
addresses = ['10.0.0.'+str(i+1) for i in range(no_hosts)]

ping_destinations = [list(set(random.sample(['10.0.0.'+str(i+1) for i in range(no_hosts) if i!=x],k=4)))[:2] for x in range(no_hosts)]

processes=[]

for i in range(no_hosts): 
    processes.append(execute(hosts[i],ping_destinations[i][0]))
    processes.append(execute(hosts[i],ping_destinations[i][1]))

data=[]
for i in range(len(hosts)):
    server = hosts[i]
    proc = subprocess.Popen(
            ['make','iperf-server','source='+server],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    time.sleep(1)
    for j in range(i+1,len(hosts)):
        command = 'make iperf-client source={} destination={} bandwidth={}'.format(hosts[j], addresses[i], bw)
        print(command)
        op = os.popen(command).read().split('\n')
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
df.to_csv('metrics/'+sys.argv[2]+'.csv',index=False)
print('Done')

for proc in processes:
    proc.terminate()
    time.sleep(0.5)
    proc.poll()
    del proc

for i in range(no_hosts):
    kill_process(hosts[i],ping_destinations[i][0])
    kill_process(hosts[i],ping_destinations[i][1])

for i in range(no_hosts):
    kill_iperf(hosts[i])