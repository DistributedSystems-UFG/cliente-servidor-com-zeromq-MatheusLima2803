[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/k52jMr_H)
# Client-Server-ZeroMQ
Simple example of the client-server pattern using ZeroMQ
(from distributed-systems.net)

### First, install ZeroMQ (on each machine):

    sudo apt update

    sudo apt install python3-zmq

### Or, with virtual environments (also on each machine -- only install pip3 and venv if not yet installed):

    sudo apt update
    sudo apt install python3-pip
    sudo apt install python3-venv
    python3 -m venv myvenv
    source myvenv/bin/activate
    pip3 install pyzmq

### Next, configure the IP address and port number of the server's machine in the const.py file

Note: Make sure that this repo is cloned in all the machines used for this experiment.

### Then, run the client and server:

On the machine for which the IP address was configured:

    python3 server.py

On another machine:

    python3 client.py

### Now, add other services (operations) in the server and call them from the client.

    
