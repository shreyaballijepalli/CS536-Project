import csv

with open('paths.txt') as f:
    paths = f.read().splitlines()

subractone = False
with open('routing.csv', 'w') as f:
    header = ['src','dst','path']
    writer = csv.writer(f)
    writer.writerow(header)
    for path in paths:
        print(path)
        segments = path.split("==>")
        src = ""
        dst = ""
        f_path = []
        for i in range(len(segments)):
            segment = segments[i]
            devices = segment.split(";")[0].split("-")
            device1 = devices[0].replace("device:","").split("/")[0].replace("s","")
            device2 = devices[1].replace("device:","").split("/")[0].replace("s","")
            if subractone:
                device1 = str(int(device1) - 1)
                device2 = str(int(device2) - 1)
            if i == 0:
                src = device1
                f_path.append(src)
            
            if i == len(segments) - 1:
                dst = device2
                f_path.append(dst)
            
            
            if i<len(segments) - 1:
                f_path.append(device2)
        
        print("Src ",src)
        print(f_path)
        print("Dst ",dst)
        data = [src, dst, ";".join(f_path)]
        writer.writerow(data)

