#!python3
import errno, socket
import threading
from queue import Queue
import time
import random

_port_from = 27015
_port_to = 27099

_ip = 'csko.cz'
_mod = 'cstrike'

_threads = 10

# lock to serialize console output

def prefix():
    return "[pFilter message]: "

def parsing(data):
    """Parses recieved data to readable form. Null('\0') is delimiter
Returns list of data."""
    data = data.replace(b'\377',b'')
    data = data.decode(encoding='UTF-8')
    li = data.split('\0')
    return li

def pf(port, ip, mod):
    osock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    osock.connect((ip,port))
    osock.settimeout(1.5)
    osock.send(b'\377\377\377\377TSource Engine Query\0')

    while 1:
        data = ''
        try:
            data = osock.recv(1024)
        except socket.error as e:
            if e.errno ==errno.ECONNREFUSED:
                err_str = prefix()+"connection to port %d refused" % (port)
                return ("[error]", err_str)
        if not data:
            err_str = prefix()+"no data recieved from port "+str(port)
            return ("[error]", err_str)
        else:
            li = parsing(data)
            if li[3] != mod:
                err_str = prefix()+"there's another mod(%s) on port %d!" % (li[3],port)
                return ("[error]",err_str)
            else:
                return (port, li[1])
    osock.close()

def srcQuery(ip, mod, port_from, port_to, threads=10):
    lock = threading.Lock()
    result = []
    q = Queue()

    # The worker thread pulls an item from the queue and processes it
    def worker():
        while True:
            item = q.get()
            # print(*item)
            result.append(pf(*item))
            q.task_done()

    def solver(data):
        # Solve errors in filtered data, return final list
        servers = []
        errors = []
        for server in data:
            if server[0] != "[error]":
                servers.append((server[1],server[0]))
            else:
                errors.append(server[1])
        return (servers, errors, socket.gethostbyname(ip))

    # Create the queue and thread pool.
    for i in range(threads):
         t = threading.Thread(target=worker)
         t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
         t.start()

    # stuff work items on the queue (in this case, just a number).
    for port in range(_port_from,_port_to):
        q.put((port, ip, mod))

    q.join()       # block until all tasks are done

    return solver(result)

def main():
    start = time.perf_counter()
    q = srcQuery(_ip, _mod, _port_from, _port_to, _threads)

    print("using func srcQuery()_____________________________________________")

    for s in q[0]:
        print("Server: " + s[0].ljust(40, " ") + "Port:" + str(s[1]))

    for e in q[1]:
        print(e)
    print('time: %f with %d threads'%(time.perf_counter() - start,_threads))

if __name__ == '__main__':
    main()