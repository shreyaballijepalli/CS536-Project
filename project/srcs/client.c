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
 * client.c
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
#include <arpa/inet.h>

#define SEND_BUFFER_SIZE 2048

/* Open socket and send message from stdin.
 * Return 0 on success, non-zero on failure
 */
int client(char *server_ip, char *server_port)
{
  int socket_fd;
  struct sockaddr_in server_addr;

  ///Initialize new socket
  if((socket_fd = socket(PF_INET,SOCK_STREAM,0)) == -1)
  {
    perror("Socket intialization failed");
    return -1;
  }

  //Server address information with provided server_ip and server_port
  server_addr.sin_family = AF_INET;
  server_addr.sin_addr.s_addr = inet_addr(server_ip);
  server_addr.sin_port = htons(atoi(server_port));

  //Connect to server
  if(connect(socket_fd,(struct sockaddr*)&server_addr,sizeof(server_addr)) == -1)
  {
    perror("Unable to connect to server\n");
    return -1;
  }
  
  /* Read input from the console into a buffer till a configured size and 
  *  send to server till EOF is reached.
  *  Handles partial sends by resending the buffer till all the data has been sent.
  */
  int num_bytes_read;
  char buf[SEND_BUFFER_SIZE]={};
  do
  {
    num_bytes_read = fread(buf, sizeof(char),SEND_BUFFER_SIZE,stdin);
    if(num_bytes_read == 0)
      break;

    int num_bytes_to_send = num_bytes_read;
    int num_bytes_sent = 0;

    while (num_bytes_sent < num_bytes_to_send)
    {
      int num_sent = send(socket_fd, buf+num_bytes_sent, num_bytes_to_send, 0);
      if (num_sent == -1)
      {
        perror("Error in sending to server");
        return -1;
      }
      num_bytes_to_send-=num_sent;
      num_bytes_sent+=num_sent;
    }

  } while(num_bytes_read>0);
  
  close(socket_fd);
  return 0;
}

/*
 * main()
 * Parse command-line arguments and call client function
 */
int main(int argc, char **argv)
{
  char *server_ip;
  char *server_port;

  if (argc != 3)
  {
    fprintf(stderr, "Usage: ./client-c (server IP) (server port) < (message)\n");
    exit(EXIT_FAILURE);
  }

  server_ip = argv[1];
  server_port = argv[2];
  return client(server_ip, server_port);
}