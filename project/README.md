### Commands to run

### Setup controller
```
make controller
```

### Setup mininet
#### Custom topology
```
../scripts/mn-stratum --custom custom-mininet.py --topo=mytopo --link=tc
```

#### Linear topology
```
../scripts/mn-stratum --topo linear,12
```

### Setup onos cli
```
make cli
app activate fwd
```


### ONOS Controller Add Topology

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