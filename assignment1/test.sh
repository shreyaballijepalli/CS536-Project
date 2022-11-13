#!/bin/bash

PID= ps -ef | awk '/^$12/ {/mininet:h1/}'
echo $PID
