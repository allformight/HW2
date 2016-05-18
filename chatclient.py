import socket ,time
import threading
from getpass import getpass




def clientsend():
    while True:

        try:
            
            myword = input()
            if myword[0:9] == 'sendfile ':
                s.send(myword.encode())
                print('sssssssend')
                flag=0
                a=0
                while True:                #get filename
                       
                    if myword[a] == ' ':
                        flag+=1
                        if flag==2 : 
                            print(a)
                            break
                    a+=1
                print('aaaaaa')
                filname = myword.lstrip(myword[0:a])
                print(filname)
                
                file = open(filname , 'rb')
                l=file.read()                
                s.send(l)
                    

            else:         
                s.send(myword.encode())
        except:
            print('Server closed this connection!')


def clientrecv():
    while True:
        
        otherword = s.recv(1024).decode()
        alert = 'Wrong Account or Password!'
        if otherword == '99999999999999999999':
            print('The connection is closed!')
            break

        if otherword != alert:
            if otherword[0:5] == '99999':
                print('rrrrrrrrrrr')
                
                dataname = otherword.lstrip('99999') 
                print(dataname)
                print('--------------------',dataname)
                file = open(dataname,'wb')
                try:
                    data = s.recv(1024)                    
                    file.write(data)
                    print('sdfsdf')
                                 
                    file.flush()
                    file.close()
                    print('File is stored!')
                except:
                    print('File transmissiont Error!')
            print(otherword)
        else:
            print(alert)
            break
    return




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = ''
port = 8001
s.connect((host,port))
account=input('Input your account: ')
s.send(account.encode())
password= getpass()
s.send(password.encode())
    
th1=threading.Thread(target=clientsend)
th2=threading.Thread(target=clientrecv)
threads = [th1, th2]  
  
for t in threads :  
    t.setDaemon(True)  
    t.start()  
t.join()  
#s.close()
