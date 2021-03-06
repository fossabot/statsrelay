import argparse
import socket
import time


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8125)
    parser.add_argument('-n', '--num-stats', type=int, default=0)
    parser.add_argument('-r', '--reconnect-interval', type=int, default=0)
    parser.add_argument('-d', '--delay', type=float, default=0.0)
    parser.add_argument('--word-file')
    parser.add_argument('host')
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))

    reconn = args.reconnect_interval
    count = args.num_stats
    words = []
    if args.word_file:
        with open(args.word_file) as wf:
            x = 0
            for line in wf:
                words.append(line.strip())
                x += 1
        if count == 0:
            count = x
    else:
        words = ['test']

    x = 0
    while True:
        break_out = False
        for word in words:
            x += 1
            print x, count
            stat = word + ':1|c\n'
            sock.sendall(stat)
            if count and x >= count:
                break_out = True
                break
            elif reconn and x % reconn == 0:
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((args.host, args.port))
        if break_out:
            break
        if args.delay:
            time.sleep(args.delay)
