#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
import csv

#Update this based on number of hosts
num_hosts = 7


class MyTopo( Topo ):

    def __init__(self, topology):
        # Initialize topology
        Topo.__init__(self)
        

        if topology == 'nsf':
            self.nsf_topology()
        else:
            self.read_topology_from_file()


    #   node0.port[0] <--> Channel10kbps <--> node1.port[0];
    #   node0.port[1] <--> Channel10kbps <--> node3.port[0];
    #   node0.port[2] <--> Channel10kbps <--> node2.port[0];
    #   node1.port[1] <--> Channel10kbps <--> node2.port[1];
    #   node1.port[2] <--> Channel10kbps <--> node7.port[0];
    #   node2.port[2] <--> Channel10kbps <--> node5.port[0];
    #   node3.port[1] <--> Channel40kbps <--> node4.port[0];
    #   node3.port[2] <--> Channel10kbps <--> node8.port[0];
    #   node4.port[1] <--> Channel40kbps <--> node5.port[1];
    #   node4.port[2] <--> Channel10kbps <--> node6.port[0]; 
    #   node5.port[2] <--> Channel10kbps <--> node12.port[0];
    #   node5.port[3] <--> Channel10kbps <--> node13.port[0];
    #   node6.port[1] <--> Channel10kbps <--> node7.port[1];
    #   node7.port[2] <--> Channel40kbps <--> node10.port[0];
    #   node8.port[1] <--> Channel10kbps <--> node9.port[0];
    #   node8.port[2] <--> Channel10kbps <--> node11.port[0];
    #   node9.port[1] <--> Channel10kbps <--> node10.port[1];
    #   node9.port[2] <--> Channel10kbps <--> node12.port[1];
    #   node10.port[2] <--> Channel10kbps <--> node11.port[1];
    #   node10.port[3] <--> Channel10kbps <--> node13.port[1];
    #   node11.port[2] <--> Channel10kbps <--> node12.port[2];
    def nsf_topology(self):
        num_hosts = 14
        hosts, switches = self.create_hosts_and_switches(num_hosts)
        
        b = 5000
        self.addLink(switches[0],switches[1],bw = b)
        self.addLink(switches[0],switches[3],bw = b)
        self.addLink(switches[0],switches[2],bw = b)

        self.addLink(switches[1],switches[2],bw = b)
        self.addLink(switches[1],switches[7],bw = b)

        self.addLink(switches[2],switches[5],bw = b)
        
        self.addLink(switches[3],switches[4],bw = b)
        self.addLink(switches[3],switches[8],bw = b)

        self.addLink(switches[4],switches[5],bw = b)
        self.addLink(switches[4],switches[6],bw = b)

        self.addLink(switches[5],switches[12],bw = b)
        self.addLink(switches[5],switches[13],bw = b)


        self.addLink(switches[6],switches[7],bw = b)
        self.addLink(switches[7],switches[10],bw = b)

        self.addLink(switches[8],switches[9],bw = b)
        self.addLink(switches[8],switches[11],bw = b)

        self.addLink(switches[9],switches[10],bw = b)
        self.addLink(switches[9],switches[12],bw = b)

        self.addLink(switches[10],switches[11],bw = b)
        self.addLink(switches[10],switches[13],bw = b)
        self.addLink(switches[11],switches[12],bw = b)



    def read_topology_from_file(self):
        hosts, switches = self.create_hosts_and_switches(num_hosts)
        with open('topology.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                src = int(row['src'])
                dst = int(row['dst'])
                bandwidth = float(row['bandwidth'])
                self.addLink(switches[src],switches[dst],bw=bandwidth,
                cls=TCLink)

    
    def create_hosts_and_switches(self, num_hosts):
        hosts = []
        switches = []
        for i in range(num_hosts):
            hostname = 'h' + str(i)
            switchname = 's' + str(i)
            host = self.addHost(hostname)
            hosts.append(host)
            switch = self.addSwitch(switchname)
            switches.append(switch)
        
        for i in range(num_hosts):
            self.addLink(hosts[i],switches[i]) #1 Mbps
        
        return hosts, switches



topos = { 'mytopo': ( lambda: MyTopo('custom') ) }