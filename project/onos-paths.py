num_hosts = 7
path_command = "paths device:{switch1:s} device:{switch2:s}"
f = open("path_commands.txt", "w")

if __name__ == "__main__":
    for i in range(1, num_hosts+1):
        for j in range(1,num_hosts+1):
            if j!=i:
                f.write(path_command.format(switch1 = 's'+str(i), switch2 = 's'+str(j)))
                f.write(";")
    f.close()

                
