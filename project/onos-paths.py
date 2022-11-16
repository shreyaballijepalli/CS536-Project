num_hosts = 10
path_command = "paths device:{switch1:s} device:{switch2:s}"
f = open("path_commands.txt", "w")

if __name__ == "__main__":
    for i in range(num_hosts):
        for j in range(num_hosts):
            if j!=i:
                f.write(path_command.format(switch1 = 's'+str(i), switch2 = 's'+str(j)))
                f.write(";")
    f.close()

                
