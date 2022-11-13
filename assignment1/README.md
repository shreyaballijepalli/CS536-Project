### Commands

1. ### Setup controller
```
make controller
```

2. ### Setup mininet
```
../scripts/mn-stratum --custom custom-mininet.py --topo=mytopo --link=tc
```

3. ### Setup onos cli
```
make cli
app activate fwd
```


4. ### ONOS Controller Add Topology
```
../scripts/onos-netcfg cfg/nsfcfg.json
```
### ONOS Cli Commands
```
topology
links
nodes
```

