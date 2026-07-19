import sys
import datetime
import socket
import parsley
from pyfiglet import Figlet
from blessings import Terminal

def main():
    # some good ones:
    # ansi_regular, blocky, future, mono12, mono9, smblock, smbraille, smmono12, smmono9
    f = Figlet(font="smmono12")
    t = Terminal()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], int(sys.argv[2])))

    usb_parser = parsley.USBDebugParser()
    buffer = b''
    log = ''

    lat = 0.0
    lon = 0.0
    num_sats = 0

    try:
        while True:
            buffer += s.recv(4096)
            text_buff = buffer.decode("utf-8", errors="backslashreplace")
            i = text_buff.find("\n")
            if i < 0: continue

            msg = text_buff[:i]
            buffer = buffer[i+1:]
            parsed_object = usb_parser.parse(msg)
            full_message = False

            if parsed_object['board_type_id'] == 'GPS':
                data = parsed_object['data']
                match parsed_object['msg_type']:
                    case 'GPS_LONGITUDE':
                        lon = data['degs'] + data['mins'] + data['dmins'] / 10000
                        if data['direction'] == 'W': lon = -lon
                    case 'GPS_LATITUDE':
                        lat = data['degs'] + data['mins'] + data['dmins'] / 10000
                        if data['direction'] == 'S': lat = -lat
                    case 'GPS_INFO':
                        num_sats = data['num_sats']
                        full_message = True

            if not full_message: continue

            now = datetime.datetime.now().isoformat()

            log += '{} sats: {}, {:.4},{:.4}\n'.format(now, num_sats, lat, lon)
            ns = 'N' if lat > 0 else 'S'
            ew = 'E' if lon > 0 else 'W'

            with t.location(0, 0), t.fullscreen():
                print(f.renderText('{:7.4f}{}\n{:7.4f}{}'.format(abs(lat), ns, abs(lon), ew)).strip_surrounding_newlines())
                print("num sats: {}".format(num_sats))
                print("last received: {}".format(now))
    except KeyboardInterrupt:
        print(t.clear)
        print(log, end='')
        pass

if __name__ == "__main__":
    main()
