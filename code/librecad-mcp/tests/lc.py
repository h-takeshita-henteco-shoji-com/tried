import json,socket,sys
def call(cmd,**a):
    s=socket.create_connection(("127.0.0.1",7471),timeout=60)
    s.sendall((json.dumps({"id":1,"cmd":cmd,"args":a},ensure_ascii=False)+"\n").encode())
    b=b""
    while not b.endswith(b"\n"):
        c=s.recv(1<<20)
        if not c: break
        b+=c
    s.close(); return json.loads(b)
def short(r,n=600): return json.dumps(r,ensure_ascii=False)[:n]
