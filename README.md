# AX.25 Messaging System (AMS)

#### Created by AF5E

[https://github.com/evanchodora/radio_ams](http://github.com/evanchodora/radio_ams)

Python-based amatuer radio messaging system that uses AX.25 tools to allow clients to interact with a remote server for storing, retrieving, and managing messages.
Clients that connect to the server are presented with a CLI to allow them to view recently active users, view/delete messages sent to them, and write messages to others to be stored in the database.
Offers a convenient way to provide a messaging system for mobile operations and local communications without internet connectivity.  

## Getting Started

This getting started section goes over some of the prerequisites and install directions for the server and client software.

### Disclaimer

This software is designed for amateur radio use using the AX.25 protocol. Therefore, in accordance with FCC rules, it does not use any type of encryption.
Any messages sent or received using this software should be considered public and while it is designed to only allow users to view messages addressed to their callsign, nothing stops a user spoofing their callsign to read the messages of others or sending messages on behalf of others.

### Prerequisites

- Linux system setup with AX.25 ([here](https://www.tldp.org/HOWTO/AX25-HOWTO/index.html) and [here](https://xastir.org/index.php/HowTo:AX.25_-_Ubuntu/Debian) are some good resources for getting setup)
- Connection to a hardware/virtual TNC and radio linked to computer ([Direwolf](https://github.com/wb2osz/direwolf) is an awesome modem that only relies on your soundcard)
- netcat (nc) compiled with the `-e` option (if your system does not support the `-e` option I recommend the [busybox](https://busybox.net/) compiled binary that contains `nc` and is how the server is written to run with)
- Python 3 and pip3 to install requirements

### Installing

Installation is simple: just clone the repository onto your server station and then copy `run_client` onto any clients that you want to use to connect.

```
git clone https://github.com/evanchodora/radio_ams.git
cd radio_ams
pip3 install -r requirements.txt
```

I recommend downloading the busybox compiled binary for your architecture.
Check the [latest directory](https://busybox.net/downloads/binaries/) and find the url for your architecture (i.e. x86_64, armv7l, armv8l, etc).

```
curl $busybox_binary_url -o busybox
chmod +x busybox
```

### AX.25

Install AX.25 tools and apps if you haven't already:
```
sudo apt-get install libax25 ax25-tools ax25-apps
```

Edit the `/etc/ax25/axports` file to add your interface:
```
# /etc/ax25/axports 
# Example axports file:
#
# name callsign speed paclen window description
ax0 AF5E    9600    255 1   AMS port
```

Attach your TNC using `kissattach`
```
sudo kissattach device ax0 ip_addr
```
Where `device` is your device location (i.e. `/dev/ttyUSB0`) and `ip_addr` is address you'd like to assign to the interface.

## Server and Database

The first step is to create the message database in the desired server directory:
```
python3 create_db.py
```

Run the server with `./run_server $server_port` to start the server and listen for incoming connections with the specified server port.

## Clients

After setting up the radio interface on the clients, a user can edit the `run_client` script with their callsign, server ip, and port.
The client can then connect by running `./run_client $local_callsign $server_ip $port` and interact with the AMS through the CLI in their terminal once the connection is made.

After exiting the AMS software, `CTRL+D` can be used to end the connection.

## Contact

Evan Chodora - AF5E - [github.com/evanchodora](https://github.com/evanchodora)

## License

This software is licensed under the MIT license.
Feel free to modify it, distribute it, sell it, or whatever.
If you have any suggestions or pull requests feel free to submit those as well. 
