#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class MyTopo( Topo ):

    def __init__(self, topology):
        # Initialize topology
        Topo.__init__(self)
        

        if topology == 'nsf':
            self.nsf_topology()


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
        # num_hosts = 6
        # hosts, switches = self.create_hosts_and_switches(num_hosts)
        switches = []
        hosts = []
        #1
        hosts.append(self.addHost('h0'))
        switches.append(self.addSwitch('s0'))

        hosts.append(self.addHost('h1'))
        switches.append(self.addSwitch('s1'))

        self.addLink(switches[0],switches[1])

        #2
        hosts.append(self.addHost('h2'))
        switches.append(self.addSwitch('s2'))
        self.addLink(switches[0],switches[2])
        self.addLink(switches[1],switches[2])

        #3
        hosts.append(self.addHost('h3'))
        switches.append(self.addSwitch('s3'))
        self.addLink(switches[0],switches[3])

        #4
        hosts.append(self.addHost('h4'))
        switches.append(self.addSwitch('s4'))
        self.addLink(switches[3],switches[4])
        #5

        hosts.append(self.addHost('h5'))
        switches.append(self.addSwitch('s5'))
        self.addLink(switches[2],switches[5])
        self.addLink(switches[4],switches[5])

        # #6
        hosts.append(self.addHost('h6'))
        switches.append(self.addSwitch('s6'))
        self.addLink(switches[4],switches[6])
        # #7
        hosts.append(self.addHost('h7'))
        switches.append(self.addSwitch('s7'))
        self.addLink(switches[1],switches[7])
        self.addLink(switches[6],switches[7])
        # #8
        hosts.append(self.addHost('h8'))
        switches.append(self.addSwitch('s8'))
        self.addLink(switches[3],switches[8])
        # #9
        hosts.append(self.addHost('h9'))
        switches.append(self.addSwitch('s9'))
        self.addLink(switches[8],switches[9])
        # #10
        hosts.append(self.addHost('h10'))
        switches.append(self.addSwitch('s10'))
        self.addLink(switches[7],switches[10])
        self.addLink(switches[9],switches[10])
        # #11
        hosts.append(self.addHost('h11'))
        switches.append(self.addSwitch('s11'))
        self.addLink(switches[8],switches[11])
        self.addLink(switches[10],switches[11])
        # # #12
        # hosts.append(self.addHost('h12'))
        # switches.append(self.addSwitch('s12'))
        # self.addLink(switches[5],switches[12])
        # self.addLink(switches[9],switches[12])
        # self.addLink(switches[11],switches[12])
        # # #13
        # hosts.append(self.addHost('h13'))
        # switches.append(self.addSwitch('s13'))
        # self.addLink(switches[5],switches[13])
        # self.addLink(switches[10],switches[13])

        # for i in range(num_hosts):
        #     self.addLink(hosts[i],switches[i]) #1 Mbps


    
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



topos = { 'mytopo': ( lambda: MyTopo('nsf') ) }