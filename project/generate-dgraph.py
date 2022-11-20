import networkx as nx
import csv

num_nodes = 7
graph = [[None for x in range(num_nodes)] for y in range(num_nodes)]
flows = [[None for x in range(num_nodes)] for y in range(num_nodes)] 
routing_matrix = [["" for x in range(num_nodes)] for y in range(num_nodes)] 

class Link:
    def __init__(self, bw, qsize):
        self.bw = bw
        self.qsize = qsize

    
    def __str__(self):
        return f"Bw is {self.bw}, qsize is {self.qsize}"


class Flow:
    def __init__(self, pkts, bw, delay, jitter, loss):
        self.pkts = pkts
        self.bw = bw
        self.delay = delay
        self.jitter = jitter
        self.loss = loss


def read_topology():
    with open('topology.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src = int(row['src'])
            dst = int(row['dst'])
            bw = float(row['bandwidth'])
            qsize = int(row['queueSize'])
            graph[src][dst] = Link(bw, qsize)
            graph[dst][src] = Link(bw, qsize)
    return graph


def read_flows():
    with open('flows.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src = int(row['src'])
            dst = int(row['dst'])
            packets = float(row['PktsGen'])
            avgBw = float(row['AvgBw']) * pow(10,6) #to get in bits/sec
            delay = float(row['AvgDelay'])
            jitter = float(row['jitter'])
            loss = float(row['loss'])
            flows[src][dst] = Flow(packets,avgBw,delay,jitter,loss)
    return flows


def read_routing_matrix():
    with open('routing.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src = int(row['src'])
            dst = int(row['dst'])
            path = row['path']
            routing_matrix[src][dst] = path
    return routing_matrix

D_G = nx.DiGraph()

graph = read_topology()
print(graph)
flows = read_flows()
print(flows)
routing_matrix = read_routing_matrix()
print(routing_matrix)

for src in range(num_nodes):
    for dst in range(num_nodes):
        if src != dst:
            link = graph[src][dst]
            if link is not None:
                 D_G.add_node('l_{}_{}'.format(src, dst),
                                 capacity=link.bw,
                                 occupancy=link.qsize)
            flow = flows[src][dst]
            f_id = 0    #TODO: Include multiple flows
            if flow.bw !=0 and flow.pkts!=0:
                D_G.add_node('p_{}_{}_{}'.format(src, dst, f_id),
                                    traffic=flow.bw,
                                    packets=flow.pkts,
                                    delay=flow.delay)
                path = routing_matrix[src][dst].split(";")
                for h_1, h_2 in [path[i:i + 2] for i in range(0, len(path) - 1)]:
                            D_G.add_edge('p_{}_{}_{}'.format(src, dst, f_id), 'l_{}_{}'.format(h_1, h_2))
                            D_G.add_edge('l_{}_{}'.format(h_1, h_2), 'p_{}_{}_{}'.format(src, dst, f_id))
