import networkx as nx
import csv
import os

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


class InputFiles:
    def __init__(self, num_nodes, topology_file, flow_file, routing_file):
        self.num_nodes = num_nodes
        self.topology_file = topology_file
        self.flow_file = flow_file
        self.routing_file = routing_file


def read_topology(topology_file,graph):
    with open(topology_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src = int(row['src'])
            dst = int(row['dst'])
            bw = float(row['bandwidth'])
            qsize = int(row['queueSize'])
            graph[src][dst] = Link(bw, qsize)
            graph[dst][src] = Link(bw, qsize)
    return graph


def read_flows(flows_file,flows):
    with open(flows_file, newline='') as csvfile:
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


def read_routing_matrix(routing_file,routing_matrix):
    with open(routing_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            src = int(row['src'])
            dst = int(row['dst'])
            path = row['path']
            routing_matrix[src][dst] = path
    return routing_matrix


def get_subdirectories(dir):
    input_files_list = []
    topology_file = "topology.csv"
    routing_file = "routing.csv"
    flow_files = ["1m","2m","3m","4m","5m","6m","7m","8m","9m","10m"]
    folders = [ f.path for f in os.scandir(dir) if f.is_dir()]
    for folder in folders:
        num_nodes = folder.split("/")[-1]
        file_list = os.listdir(folder)
        subfolders = [ f.path for f in os.scandir(folder) if f.is_dir()]
        for subfolder in subfolders:
            for flow_file in flow_files:
                input_files = InputFiles(num_nodes,subfolder+"/"+topology_file,
                subfolder+"/"+flow_file+".csv", subfolder+"/"+routing_file)
                input_files_list.append(input_files)
    
    return input_files_list



def getDGraph(num_nodes, topology_file, flows_file, routing_file):
    graph = [[None for x in range(num_nodes)] for y in range(num_nodes)]
    flows = [[None for x in range(num_nodes)] for y in range(num_nodes)] 
    routing_matrix = [["" for x in range(num_nodes)] for y in range(num_nodes)] 
    D_G = nx.DiGraph()
    graph = read_topology(topology_file,graph)
    # print(graph)
    flows = read_flows(flows_file,flows)
    # print(flows)
    routing_matrix = read_routing_matrix(routing_file,routing_matrix)
    # print(routing_matrix)

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

    D_G.remove_nodes_from([node for node, out_degree in D_G.out_degree() if out_degree == 0])
    return D_G

if __name__ == "__main__":
    input_files_list = get_subdirectories("data/train")
    for input_files in input_files_list:
        num_nodes = int(input_files.num_nodes)
        topology_file = input_files.topology_file
        routing_file = input_files.routing_file
        flow_file = input_files.flow_file
        print(num_nodes)
        print(topology_file)
        print(routing_file)
        print(flow_file)
        D_G = getDGraph(num_nodes,topology_file,flow_file,routing_file)
        print(D_G)
    
    # D_G_1 = getDGraph(4,"data/train/4/topology_3_3/topology.csv",
    # "data/train/4/topology_3_3/4m.csv","data/train/4/topology_3_3/routing.csv")
    # D_G_2 = getDGraph(4,"data/train/4/topology_1_3/topology.csv",
    # "data/train/4/topology_1_3/4m.csv","data/train/4/topology_1_3/routing.csv")
    # print(D_G_1.edges)
    # print(D_G_2.edges)
