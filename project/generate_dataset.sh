topology=topology_2
mkdir -p metrics
mkdir -p metrics/$topology

for value in 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m
do
    sudo python3 generate_dataset_csv.py $value $topology/$value
done