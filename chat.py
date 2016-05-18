import socket,argparse 
import threading,time

# data=''
# username=dict()
userlist=list()         #record the friend list
userconnec=list()
username = ['aaa','bbb','ccc','ddd','eee']
userpass = ['1111','2222','3333','4444','5555']
userstate = ['offline','offline','offline','offline','offline']
conn_flag = list()    #used to detemine who is talking to you
count=list()             #record the friend list array addr.
off_line=list()           #record offline message

friendlist = []
for  i in range(5):
    friendlist.append([username[i]])
    count.append(0)
    userconnec.append(0)
    conn_flag.append(9999)
    off_line.append(9999)


def talkothers(notify):
    #print(connec)
    for c in userlist:
        c.send(notify.encode())

def clientin(connec):
    
    flag=0      #judge password and account is correct
    userlist.append(connec)         #new connec
    account= connec.recv(1024).decode()
    password= connec.recv(1024).decode()
    num=0
    fileflag=0

    for i in range(len(username)):
        if account == username[i]:
            if password == userpass[i]:
                num=i                        #num is the account number
                flag=1

    if flag == 1:

        print(account,' has been Connected!')
        notify= account + ' has joined the chatroom!'
        talkothers(notify)
        userstate[num]='online'
        userconnec[num]=connec

        now = time.strftime('%Y-%m-%d %H:%M:%S')
        timing = open('log_time','a+')
        timing.write(now + ' : '+ username[num]+' log in\n')
        timing.close


        if off_line[num] != 9999:
            offmsg=off_line[num]
            connec.send(offmsg.encode())
            off_line[num]=9999



        while True:
            try:
                

                data = connec.recv(1024).decode()
                commandflag=0
                # print(conn_flag[num])

                if conn_flag[num] != 9999:            #talk to connection  ' talk john'
                    dst=conn_flag[num]
                    # print('yaaaaa')

                    if data =='bye()':
                        data ='------End the talk!------'
                        userconnec[num].send(data.encode())                        
                        # print('this')
                        conn_flag[num]=9999
                        # print('conn_flag[num]=',conn_flag[num])
                        conn_flag[dst]=9999
                        # print('yaaa',conn_flag[dst])
                    else:
                        if userstate[dst] == 'offline':            #determine whether record the offline message
                            print(username[dst],' is offline!')
                            if off_line[dst] == 9999:
                                off_line[dst] = '\nMessage from '+ username[num] +': '+ data
                            else:
                                off_line[dst] += '\nMessage from '+ username[num] + ': '+ data
                        
                        else:           #dst user is online, send the message                        
                            data = username[num] + ': ' + data
                            userconnec[dst].send(data.encode())

                if data=='friend list':                            
                    commandflag=1                             
                    if count[num]==0 :
                        nofriend = 'Error!You have no friend yet!'
                        connec.send(nofriend.encode())          
                    else:
                        for i in range(len(username)):
                            # print(userstate[i])                      
                            for k in range(count[num]):                                                                         
                                if username[i] == friendlist[num][k+1]:
                                    # print(friendlist[num][k+1])
                                    cc=i
                                    namelist = '\n'+friendlist[num][k+1] +' '+ userstate[cc]
                                    connec.send(namelist.encode()) 
                talkall = data.lstrip('broadcast ')
                if data[0:10] == 'broadcast ':
                    talkall = username[num] + ': ' +talkall
                    talkothers(talkall)



                                                                                    
                for i in range(len(username)): 
                    if data == 'friend add ' + username[i]:  #determine add friend command                        
                        commandflag=1
                        flagcount=0
                        if count[num]!=0 :
                            for j in range (count[num]+1):
                                if friendlist[num][j]== username[i]:    #determine whether friend is added again
                                    flagcount=1
                                    notadd = username[i]+' had been added'
                                    connec.send(notadd.encode()) 
                        if flagcount==0:                                                                                                                            
                            friendlist[num].append(username[i])
                            count[num]+=1
                            add=username[i]+' added into the friend list'
                            connec.send(add.encode())

                    if data == 'talk ' + username[i]:
                        build=username[num]+' start conversation with '+username[i]
                        # print(build)
                        connec.send(build.encode())
                        if userstate[i] == 'online':
                            userconnec[i].send(build.encode())                             
                        conn_flag[i] = num            #record which connection is talking
                        conn_flag[num] = i
                        # print(num)
                        break                                                

                    left = data.lstrip('send '+ username[i] +' ')  # send msg 'send john hello'
                    name = data.lstrip('sendfile' + username[i]+ ' ')
                    if data == 'send '+ username[i] + ' ' + left:
                        msg = username[num] + ': ' + left
                        if userstate[i] == 'online':
                            userconnec[i].send(msg.encode())
                        else:
                            if off_line[i] == 9999:
                                off_line[i] = '\nMessage from '+ username[num] +': '+ left
                            else:
                                off_line[i] += '\nMessage from '+ username[num] + ': '+ left

                    if data == 'friend rm ' + username[i]:   #rm friendlist
                        commandflag=1
                        print(count[num])
                        if count[num]==0 :                                                        
                            nof = 'Error!'+username[i]+' is not your friend!'
                            connec.send(nof.encode())                            
                        else:
                            for fu in range(count[num]):
                                if friendlist[num][fu+1] == username[i]:  #find the addr of the deleted user
                                                                    
                                    for ck in range(fu+1,count[num]):
                                        friendlist[num][ck]=friendlist[num][ck+1]   #delete friend 
                                     
                                    count[num]-=1
                                    friendaddr=i                                    
                            delete=username[friendaddr]+' removed from the friend list'
                            connec.send(delete.encode())
                    # print(data)
                    if data == 'sendfile ' + username[i] + ' ' + name : 
                        # print('jjjjj')                       
                        if userstate[i] == 'online':                                                  
                            # print('kkkkk')
                            request= '99999' 
                            userconnec[i].send(request.encode())                            
                            userconnec[i].send(name.encode())
                            # response = userconnec[i].recieve(1024).decode()
                            # while(True):                                
                                # if response == 'y':
                            while True:
                                try:
                                 
                                    l = connec.recv(1024)

                                    userconnec[i].send(l)  #send file name
                                    
                                except:
                                
                                    break        
                                    # else
                                    #     msg = 'file is not exist!'
                                    #     userconnec[i].send(msg.encode())
                                    #     break
                                # if response == 'n':
                                #     msg = 'denied from ' + username[num] 
                                #     break
                                # else:
                                #     continue
                        else:
                            response = 'Error! '+username[i]+ ' is offline!'
                            connec.send(response.encode())                            
                if data == 'log out()':
                    logout = '99999999999999999999'
                    connec.send(logout.encode())
                    print(username[num],' has left the chatroom ... ...')
                    userstate[num]='offline'
                    leave = time.strftime('%Y-%m-%d %H:%M:%S')
                    sss = open('log_time','a+')
                    print('aaaaaaa')
                    sss.write(leave + ' : '+ username[num]+' log out \n')
                    sss.close
                    connec.close

                # if commandflag==0:
                #     msg = account+' : '+data
                #     talkothers(msg)             
            except:
                print(userstate[num],' has left the chatroom ... ...')
                userstate[num]='offline'
                ddd = time.strftime('%Y-%m-%d %H:%M:%S')
                timing = open('log_time','a+')
                ddd.write(now + ' : '+ username[num]+' log out \n')
                ddd.close
                connec.close    
                break                    
               
    else:
        alert = 'Wrong Account or Password!'
        print(alert)
        userlist.remove(connec)
        



userno=0
host='127.0.0.1'
port=8001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)
print('Listening at {}',format(s.getsockname())) 

while True:
    connec, addr = s.accept()     #waiting connection
    th1=threading.Thread(target = clientin, args=(connec,))
    th1.setDaemon(True)  
    th1.start()   
s.close()



	

