### Commands to run

1. ### Setup controller
```
make controller
```

2. ### Setup mininet
#### Custom topology
```
../scripts/mn-stratum --custom custom-mininet.py --topo=mytopo --link=tc
```

#### Linear topology
```
../scripts/mn-stratum --topo linear,5
```

1. ### Setup onos cli
```
make cli
app activate fwd
```


4. ### ONOS Controller Add Topology

#### Custom topology
```
../scripts/onos-netcfg cfg/nsfcfg.json
```

#### Linear topology
```
../scripts/onos-netcfg cfg/linearcfg.json
```

### ONOS Cli Commands
```
topology
links
nodes
wipe-out please
```