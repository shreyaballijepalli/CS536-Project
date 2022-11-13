#!/usr/bin/env python

"""
  client-3wh.py
  Name: Shreya Ballijepalli
  PUID: sballije
"""


from scapy.all import *
import threading

SEND_PACKET_SIZE = 1000  # should be less than max packet size of 1500 bytes

# A client class for implementing TCP's three-way-handshake connection establishment and closing protocol,
# along with data transmission.

#TCP flags
FIN = 'F'
SYN = 'S'
PSH = 'P'
ACK = 'A'


class Client3WH:

    def __init__(self, dip, dport):
        """Initializing variables"""
        self.dip = dip
        self.dport = dport
        # selecting a source port at random
        self.sport = random.randrange(0, 2**16)

        self.next_seq = 0                       # TCP's next sequence number
        self.next_ack = 0                       # TCP's next acknowledgement number

        self.ip = IP(dst=self.dip)              # IP header

        self.connected = False
        self.timeout = 3

    def _start_sniffer(self):
        t = threading.Thread(target=self._sniffer)
        t.start()

    def _filter(self, pkt):
        if (IP in pkt) and (TCP in pkt):  # capture only IP and TCP packets
            return True
        return False

    def _sniffer(self):
        while self.connected:
            sniff(prn=lambda x: self._handle_packet(
                x), lfilter=lambda x: self._filter(x), count=1, timeout=self.timeout)

    """
    Handles incoming packets from the server and acknowledge them accordingly.
    1. If the incoming packet has data (or payload), send an ACK packet with ack number
    taking into account the payload size and sequence number of packet. ACK = PKT.SEQ + SIZE(PAYLOAD)
    2. If the incoming packet is a FIN (or FINACK) packet, send a FINACK packet with ACK = ACK + 1
    and wait for a ACK packet from the server with ACK = SEQ + 1
    """
    def _handle_packet(self, pkt):
        if pkt[TCP].dport == self.sport:
            if pkt.haslayer(Raw):
                payload_size = len(pkt[Raw].payload)
                self.next_ack = pkt[TCP].seq + payload_size
                ack_packet = self.build_packet(tcp_flags=ACK)
                send(ack_packet)
            
            elif FIN in pkt.sprintf('%TCP.flags%'):
                self.connected = False
                self.next_ack = self.next_ack + 1
                fin_ack_packet = self.build_packet(tcp_flags='FA')
                ack_response = sr1(fin_ack_packet,timeout=self.timeout)
                ack_response_flags = ack_response.sprintf('%TCP.flags%')
                self.next_seq = self.next_seq + 1
                assert (ACK in ack_response_flags), "Missing ACK flag"
                assert (ack_response[TCP].ack == self.next_seq), "Incorrect ACK number"

    """
    Implements TCP's three-way-handshake protocol for establishing a connection.
    1. Send SYN packet and wait for SYNACK from server
    2. Assert SYNACK packet from server has ACK = SYN.SEQ + 1
    3. Send ACK packet to server with ACK = SYNACK.SEQ + 1
    """
    def connect(self):
        self.next_seq = random.randrange(0, pow(2,32)-1)
        syn_packet = self.build_packet(tcp_flags=SYN)
        syn_ack_response = sr1(syn_packet,timeout=self.timeout)
        syn_ack_response_flags = syn_ack_response.sprintf('%TCP.flags%')
        self.next_seq = self.next_seq+1
        assert (SYN in syn_ack_response_flags), "Missing SYN flag"
        assert (ACK in syn_ack_response_flags), "Missing ACK flag"
        assert (syn_ack_response[TCP].ack == self.next_seq), "Incorrect ACK number"

        self.next_ack=syn_ack_response[TCP].seq+1
        ack_packet = self.build_packet(tcp_flags=ACK)
        send(ack_packet)
        
        self.connected = True
        self._start_sniffer()
        print('Connection Established')

    
    """
    Implements TCP's three-way-handshake protocol for closing a connection.
    1. Send FINACK packet and wait for FINACK from server
    2. Assert packet from server has ACK = FINACK.SEQ + 1
    """
    def close(self):
        self.connected = False
        fin_packet = self.build_packet(tcp_flags='FA')
        fin_ack_response = sr1(fin_packet,timeout=self.timeout)
        fin_ack_response_flags = fin_ack_response.sprintf('%TCP.flags%')
        self.next_seq=self.next_seq+1
        assert (FIN in fin_ack_response_flags), "Missing FIN flag"
        assert (ACK in fin_ack_response_flags), "Missing ACK flag"
        assert (fin_ack_response[TCP].ack == self.next_seq), "Incorrect ACK number"
        self.next_ack=fin_ack_response[TCP].seq+1
        print('Connection Closed')
        
    """
    Sends TCP data packets for sharing given payload.
    1. Send packet with PA flag and payload in Raw data of packet and wait for ACK packet.
    2. If received ACK is not equal to PA.SEQ + SIZE(PAYLOAD), get number of bytes transmitted
    by calculating ACK - PA.SEQ, this corresponds to a partial send.
    3. Handle partial sends by resending data till entire payload is sent.
    4. Assert entire payload is sent by verifying ACK = PA.SEQ + SIZE(PAYLOAD)
    
    """ 
    def send(self, payload):
        prev_seq_number = self.next_seq 
        payload_size = len(payload)     
        while len(payload)>0:
            payload_packet = self.build_packet(tcp_flags='PA',payload=payload)
            send_payload_response = sr1(payload_packet,timeout=self.timeout)
            send_payload_response_flags = send_payload_response.sprintf('%TCP.flags%')
            assert (ACK in send_payload_response_flags), "Missing ACK flag"
            bytes_transmitted = send_payload_response[TCP].ack - self.next_seq
            payload = payload[bytes_transmitted:]
            self.next_seq = self.next_seq + bytes_transmitted
        assert (send_payload_response[TCP].ack == prev_seq_number + payload_size), "Total payload not transmitted"

    
    """
    Creates a TCP/IP packet with the given flags and payload if present.
    """ 
    def build_packet(self,tcp_flags,payload=None):
        packet = self.ip/TCP(sport=self.sport, dport=self.dport, flags=tcp_flags,seq=self.next_seq,ack=self.next_ack)
        if payload is not None:
            return packet/payload
        else:
            return packet


def main():
    """Parse command-line arguments and call client function """
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: ./client-3wh.py [Server IP] [Server Port] < [message]")
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    client = Client3WH(server_ip, server_port)
    client.connect()

    message = sys.stdin.read(SEND_PACKET_SIZE)
    while message:
        client.send(message)
        message = sys.stdin.read(SEND_PACKET_SIZE)

    client.close()


if __name__ == "__main__":
    main()

