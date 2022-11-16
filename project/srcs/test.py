if __name__ == "__main__":
    payload = "Hello"
    prev_seq_number = 0
    next_seq = 0
    payload_size = len(payload)  
    i = 0   
    while len(payload)>0:
        if i==0:
            send_payload_response_ack = 2
        if i==1:
            send_payload_response_ack = 5   
        bytes_transmitted = send_payload_response_ack - next_seq
        payload = payload[bytes_transmitted:]
        next_seq = next_seq + bytes_transmitted
        i+=1
    print(send_payload_response_ack)
    print(next_seq)
    assert (send_payload_response_ack == prev_seq_number + payload_size), "Total payload not transmitted"