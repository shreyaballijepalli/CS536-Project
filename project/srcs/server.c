/*****************************************************************************
 *
 *     This file is part of Purdue CS 536.
 *
 *     Purdue CS 536 is free software: you can redistribute it and/or modify
 *     it under the terms of the GNU General Public License as published by
 *     the Free Software Foundation, either version 3 of the License, or
 *     (at your option) any later version.
 *
 *     Purdue CS 536 is distributed in the hope that it will be useful,
 *     but WITHOUT ANY WARRANTY; without even the implied warranty of
 *     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *     GNU General Public License for more details.
 *
 *     You should have received a copy of the GNU General Public License
 *     along with Purdue CS 536. If not, see <https://www.gnu.org/licenses/>.
 *
 *****************************************************************************/

/*
 * server.c
 * Name: Shreya Ballijepalli
 * PUID: sballije
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <netinet/in.h>
#include <errno.h>

#define QUEUE_LENGTH 10
#define RECV_BUFFER_SIZE 2048

/* Open socket and wait for client to connect
 * Print received message to stdout
 * Return 0 on success, non-zero on failure
 */
int server(char *server_port)
{
  int socket_fd;
  struct sockaddr_in server_addr;
  int yes=1;

  //Initialize new socket
  if((socket_fd = socket(PF_INET,SOCK_STREAM,0)) == -1)
  {
    perror("Socket intialization failed");
    return -1;
  }

  //Allow reuse of port
  if (setsockopt(socket_fd,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof(yes)) == -1) {
    perror("Error in setsocketopt");
    return -1;
  }

  //Server address information allowing to bind to localhost
  server_addr.sin_family = AF_INET;
  server_addr.sin_addr.s_addr = INADDR_ANY;
  server_addr.sin_port = htons(atoi(server_port));

  //Bind socket to localhost, server_port
  if(bind(socket_fd,(struct sockaddr*)&server_addr,sizeof(server_addr)) == -1)
  {
    perror("Unable to bind port to socket\n");
    return -1;
  }

  //Listen to connections with incoming queue of size QUEUE_LENGTH
  if(listen(socket_fd,QUEUE_LENGTH) == -1)
  {
    perror("Error in listening for connections\n");
    return -1;
  }

  /* Accept connections from clients in an infinite loop.
  * For every new connection, receive messages from client and print
  * to the console till the number of bytes read becomes 0.
  */
  while(1)
  {
    struct sockaddr_storage client_addr;
    socklen_t addr_len = sizeof(client_addr);
    int new_socket_fd = accept(socket_fd,(struct sockaddr *)&client_addr,
    &addr_len);
    if(new_socket_fd == -1)
    {
      perror("Accept connection failed\n");
      return -1;
    }
    
    char buf[RECV_BUFFER_SIZE] = {};
    int num_bytes_received = recv(new_socket_fd, buf, RECV_BUFFER_SIZE, 0);
    while (num_bytes_received>0)
    {
      buf[num_bytes_received]='\0';
      fwrite(buf,sizeof(char),num_bytes_received,stdout);
      fflush(stdout);
      num_bytes_received = recv(new_socket_fd, buf, RECV_BUFFER_SIZE, 0);
    }
    if (num_bytes_received == -1)
    {
      perror("Error in receiving from client");
      return -1;
    }

    close(new_socket_fd);
  }

  return 0;
}

/*
 * main():
 * Parse command-line arguments and call server function
 */
int main(int argc, char **argv)
{
  char *server_port;

  if (argc != 2)
  {
    fprintf(stderr, "Usage: ./server-c (server port)\n");
    exit(EXIT_FAILURE);
  }

  server_port = argv[1];
  return server(server_port);
}
