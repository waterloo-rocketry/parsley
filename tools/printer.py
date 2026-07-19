import sys
import datetime
import socket
import parsley

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))

    usb_parser = parsley.USBDebugParser()
    buffer = b''
    try:
        while True:
            buffer += s.recv(4096)
            text_buff = buffer.decode("utf-8", errors="backslashreplace")
            i = text_buff.find("\n")
            if i < 0: continue
            msg = text_buff[:i]
            buffer = buffer[i+1:]
            parsed_object = usb_parser.parse(msg)
            print(parsley.format_line(parsed_object))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
