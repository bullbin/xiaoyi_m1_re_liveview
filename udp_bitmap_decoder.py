from prot_http.const_wifi import UDP_PORT_LIVEVIEW
import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    print("Started receiver!")
    sock.bind(('', UDP_PORT_LIVEVIEW))
    sock.settimeout(2)

    data = bytearray(b'')
    data_idx_frame = None
    data_idx_last_packet = -1
    data_valid : bool = True
    was_last_frame_invalid : bool = False

    try:
        while True:
            try:
                pack, addr = sock.recvfrom(1024000)
                
                if len(pack) < 12:
                    continue

                idx_frame           = int.from_bytes(pack[:4], byteorder='big')
                len_packet_frame    = int.from_bytes(pack[4:8], byteorder='big')
                idx_packet_frame    = int.from_bytes(pack[8:12], byteorder='big')

                # If the reconstructed frame is not the delivered one, start reconstruction again
                if data_idx_frame != idx_frame:
                    data = bytearray(b'')
                    data_idx_frame = idx_frame
                    data_idx_last_packet = -1
                    data_valid = True
                
                if data_valid:
                    if (idx_packet_frame - 1) == data_idx_last_packet:
                        data.extend(pack[12:])
                        data_idx_last_packet = idx_packet_frame
                    else:
                        data_valid = False
                        continue

                    if (data_idx_last_packet == len_packet_frame - 1):
                        if len(data) > 2048:
                            with open("packet_%d.txt" % data_idx_frame, 'wb') as out:
                                out.write(data[:2048])
                            with open("packet_%d.jpg" % data_idx_frame, 'wb') as out:
                                out.write(data[2048:])
                        else:
                            with open("packet_unk_%d.raw" % data_idx_frame, 'wb') as out:
                                out.write(data)

            except TimeoutError:
                print("Timed out...")

    except KeyboardInterrupt:
        pass