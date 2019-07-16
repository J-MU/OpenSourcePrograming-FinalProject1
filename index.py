# -*- coding: utf-8 -*-
import requests
import sqlite3 as sqlite
from flask import Flask, render_template,request
from bs4 import BeautifulSoup
from cgitb import html


import datetime
from datetime import time,date

app=Flask(__name__)



@app.route('/action',methods=["POST"])
def action():
    correctlist=[]
    classnumber=[]
    
    mybuilding=request.form['building']
    
    con=sqlite.connect('ydb.db')
    
    with con:
        cur=con.cursor()      
        cur.execute("select * from lecture")
        rows=cur.fetchall()
    
    for row in rows:
        if(row[2]==mybuilding):
            correctlist.append(row)
            classnumber.append(row[3])
            
    classnumber=list(set(classnumber))          
      
    return render_template('action.html',correctlist=correctlist,Mybuilding=mybuilding,classnumber=classnumber)


@app.route('/pick_class',methods=["POST"])
def pick_class():
    correctlist=[]
    classnumber=[]
    lecture=[]
    ttime=['1A(09:00 - 09:30)','1B(09:30 - 10:00)','2A(10:00 - 10:30)','2B(10:30 - 11:00)','3A(11:00 - 11:30)','3B(11:30 - 12:00)','4A(12:00 - 12:30)','4B(12:30 - 13:00)','5A(13:00 - 13:30)','5B(13:30 - 14:00)','6A(14:00 - 14:30)','6B(14:30 - 15:00)','7A(15:00 - 15:30)','7B(15:30 - 16:00)','8A(16:00 - 16:30)','8B(16:30 - 17:00)','9A(17:00 - 17:30)','9B(17:30 - 18:00)','10A(18:00 - 18:30)','10B(18:30 - 19:00)','11A(19:00 - 19:30)','11B(19:30 - 20:00)','12A(20:00 - 20:30)','12B(20:30 - 21:00)','13A(21:00 - 21:30)','13B(21:30 - 22:00)','14A(22:00 - 22:30)']
    t3time=['09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30']
    weekend=['월','화','수','목','금']
    number=[0,1,2,3,4]  # template에 필요한 배열을 넘기기위해 선언
    number2=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    
    paint=[]
    
    
    mybuilding=request.form['Building']                #선택한 건물
    
    myClassRoom=request.form['ClassRoom']               #선택한 강의실
    con=sqlite.connect('ydb.db')
    
    print(mybuilding)
    print(myClassRoom)
    
    with con:
        cur=con.cursor()      
        cur.execute("select * from lecture")
        rows=cur.fetchall()
    
    for row in rows:
        if(row[2]==mybuilding):
            correctlist.append(row)
            classnumber.append(row[3])
            if(row[3]==myClassRoom):
                lecture.append(row)
            
    classnumber=list(set(classnumber))
    

    
    
    
    '''
        paint에 값을 집어넣는 부분을 구현해야하는데
                요일은 4,시작시간 5,종료시간6
    '''
    
    for lec in lecture:
        i=0
        j=0
        temptime=lec[5]
        tendtime=lec[6]
        tweek=lec[4]
        
        for w in weekend:
            if(tweek==w):
                ntweek=j;
            
            j=j+1
            
        for tm in t3time:
            if(temptime==tm):
                ntemptime=i
            if(tendtime==tm):
                ntendtime=i
            
            i=i+1
                    
        while ntemptime!=ntendtime:
            print(ntemptime,ntendtime)
            paint.append(27*ntweek+ntemptime)
            ntemptime=ntemptime+1
        
        
           
   
    print(classnumber)    
        
    return render_template('pick_class.html',correctlist=correctlist,Mybuilding=mybuilding,classnumber=classnumber,lecture=lecture,ttime=ttime,number=number,paint=paint,number2=number2,myClassRoom=myClassRoom)

@app.route('/')
def demo():
    
    number=0
    
    placearr=[]             
    time=[]                 
    numoftime=[]           
    
    classroom=[]           
    Building=[]            
    subject=[]             
    scode=[]                                                
    week=[]               
    classtime=[]           
    start=[]
    end=[]
    
    lecture=()             
    i=0
    
    url='http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/list.action?search_open_crse_cde=1O0204&sub=1O&search_open_yr_trm=20191';
    res=requests.get(url);
    
    html=BeautifulSoup(res.content,'html.parser')
    html_scode=html.find_all(attrs={'class':'th4'})         #get subject code
    html_subjectname=html.find_all(attrs={'class':'th5'})   #get subject name
    html_time=html.find_all(attrs={'class':'th17'})         #get class time    
    html_lectureplace=html.find_all(attrs={'class':'th11'}) #get class place
    
    #print(html_time) 여기까진 타임에 문제없음
    

    
    del html_time[0]
    del html_subjectname[0]
    del html_scode[0]
    
    
    
    for place in html_lectureplace:
        placearr+=place
    del placearr[0]
       
    try:
        for i in range(0,len(placearr)-1):           
            placearr[i]=str(placearr[i])
    except IndexError:
        pass
          
    for i in range(0,58):           #58=count(<br/>)
        placearr.remove('<br/>')                        
    
    
    '''
                 
        placearr->str->'-'을 기준으로 나눈다->홀 짝 기준으로 새로운 배열에 분리시킨다
    '''
        
    tmpstr="-".join(placearr)
    placearrfinal=tmpstr.split('-')     #건물과 호수사이에도 -를 삽입
    
    
    for i in range(0,len(placearrfinal)):
        if(i%2==1):
            classroom.append(placearrfinal[i])
        else:
            Building.append(placearrfinal[i])
    
    '''
                    여기까지 place구현
    '''
    
    for sb in html_subjectname:
        subject.append(sb.text)
    
    
    for sc in html_scode:
        scode.append(sc.text)
        
    
    tmpst="".join(scode)
    tmpst=tmpst.replace("\t","")
    tmpst=tmpst.replace("\n"," ")
    scode=tmpst.split(" ")
    try:
        for i in range(0,101):
            scode.remove('')
    except ValueError:
        pass
    '''
        scode구현
    '''
    
    #print(html_time) 여기까진 time에 문제없음
    try:
        for i in range(0,len(html_time)):           
            html_time[i]=str(html_time[i])
    except IndexError:
        pass
    
    tempstr=" ".join(html_time)
    tempstr=tempstr.replace("<br/>","/");
    tempstr=tempstr.replace('<td class="th17">','');
    tempstr=tempstr.replace('</td>','/&/');
    time=tempstr.split("/")
    
    #print(time) 여기까진 time에 문제없음
   
    for i in range(0,len(time)):
        if(time[i]!='&'):
            number=number+1
        else:
            numoftime.append(number)
            number=0
    '''
                    이부분은 numoftime구현
    '''
    
                    
    
    tempstr=tempstr.replace('/&/ ','&')
    tempstr=tempstr.replace('/','&')
    tempstr=tempstr.replace('월','월&')
    tempstr=tempstr.replace('화','화&')
    tempstr=tempstr.replace('수','수&')
    tempstr=tempstr.replace('목','목&')
    tempstr=tempstr.replace('금','금&')
    tempstr=tempstr.replace('토','토&')
    tempstr=tempstr.replace('일','일&')
    
    
    time=tempstr.split('&')
    #print(time)여기까진 문제가 없는듯 합니다/
    time.pop(len(time)-1)         #데이터가 더 늘어났을때 이부분이 오류가 발생하여 데이터가 누락되는 경우가 생길 수 있다 . 이부분을 꼼꼼히 확인하자
    time.pop(len(time)-1)
    time.pop(len(time)-1)
    
    for i in range(0,len(time)):      
        if(i%2==0):
            week.append(time[i])
        else:
            classtime.append(time[i])
    
    #print(classtime) 여기까찐 문제가 없는듯 합니다.
    
    
    timestr="~".join(classtime)
    timestr=timestr.replace(" ","")
    classtime=timestr.split('~')
    #print(classtime) ;; 여기가 문제일줄알았는데;;;
    
    for i in range(0,len(classtime)):        
        if(i%2==0):
            start.append(classtime[i])
        else:
            end.append(classtime[i])
            
    #print(start)
    #print(end)여기까지도 문제가 없어요;;
    
        
        
    
    
    '''위에까지 parsing하는 부분 지금부터 데이터 베이스에 삽입해보자'''
    con=sqlite.connect('ydb.db')

    with con:
        k=0
        cur=con.cursor()
        cur.execute("DROP TABLE IF EXISTS lecture")
        cur.execute("CREATE TABLE lecture(code TEXT,subject TEXT,Building TEXT,classroom Text,week TEXT,start TEXT,end TEXT)")
        for j in range(0,len(classroom)):   #strat와 end를 제외한 배열의 길이만큼
            #print(numoftime[j])
            for i in range(0,numoftime[j]):
                print(j,i)
                
                cur.execute("insert into lecture(code,subject,Building,classroom,week,start,end) values (?,?,?,?,?,?,?)",(scode[j],subject[j],Building[j],classroom[j],week[k],start[k],end[k]))
                k=k+1
            
        cur.execute("select * from lecture")
        rows=cur.fetchall()
        
     
        '''
        for row in rows:
            print(row)
        '''
    
    
    
    return render_template('home.html')        
    
@app.route('/emptyroom',methods=['POST'])
def empty():
    mybuilding=request.form['Building']      #선택했던 mybuilding이 무엇인지 str형태로 받아옴.
    
    t3time=['09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30']
  
    correctlist=[]    #Building과 일치하는 애들만 모음
    correctlistweek=[]  #correctlist의 요일을 저장
    ccorrectlist=[]   #현재 요일과 일치하는 애들을 한번 더 추림
    complete=[]       #시간까지 만족시키는 아이들로 추림 (강의실만 담음.)
    exceptlist=[]

    
    today=date.today()      #년 월 일 저장.(요일을 출력하기 위함)
    weekday=today.weekday() #오늘 요일 저장
    now=datetime.datetime.now()      #현재 시간정보.
    
    con=sqlite.connect('ydb.db')   
    with con:
        cur=con.cursor()      
        cur.execute("select * from lecture")
        rows=cur.fetchall()
    
    for row in rows:
        if(row[2]==mybuilding):
            correctlist.append(row)     #myBuilding과 일치하는 애들만 모음
             
    for i in range(0,len(correctlist)):
        if(correctlist[i][4]=='월'):
            correctlistweek.append(0)
        elif(correctlist[i][4]=='화'):
            correctlistweek.append(1)
        elif(correctlist[i][4]=='수'):
            correctlistweek.append(2)
        elif(correctlist[i][4]=='목'):
            correctlistweek.append(3)
        elif(correctlist[i][4]=='금'):
            correctlistweek.append(4)
        else:
            print('오류가 발생하였습니다.')
    

    for i in range(0,len(correctlistweek)): 
        if(weekday==correctlistweek[i]):
            ccorrectlist.append(correctlist[i])
        else:
            complete.append(correctlist[i][3])

            
    #    ccorrectlist는 correctlist중에서 오늘 요일과 일치하는 친구만 골라서 담은아이다.
    
    
    #nowtime=nowtime.strftime('%H:%M')
    #'{0.hour:02}:{0.minute:02}'.format(nowtime)
   
    
    
    for i in range(0,len(ccorrectlist)):
        stime=datetime.datetime.strptime(ccorrectlist[i][5],'%H:%M')
        stime=stime.replace(year=now.year)
        stime=stime.replace(month=now.month)
        stime=stime.replace(day=now.day)
        
        etime=datetime.datetime.strptime(ccorrectlist[i][6],'%H:%M')
        etime=etime.replace(year=now.year)
        etime=etime.replace(month=now.month)
        etime=etime.replace(day=now.day)
        
        print(ccorrectlist[i][3],stime,etime)
        print(now)
        print(stime<now)
        print(now<etime)
        #ccorrect에서만 complete을 하는게 문제다.
        if(not((stime<now)and(now<etime))):             #수업중이지 않은 강의실을 넣어야함.
            complete.append(ccorrectlist[i][3])
        elif((stime<now)and(now<etime)):
            exceptlist.append(ccorrectlist[i][3])
            
            
    print(complete)
    print(exceptlist)
        
    
    
   
    for j in range(0,len(complete)):
        try:
            while True:
                complete.remove(exceptlist[j])         
        except ValueError:
            pass
        except IndexError:
            pass
    
    
        
    '''            
    for co in ccorrectlist:
        print(co)
      '''  
    #print(complete)
  
    complete=list(set(complete))
   
    print(complete)
    
    
    return render_template('empty.html',correctlist=correctlist,complete=complete,MyBuilding=mybuilding)
     
if __name__ == '__main__':
    app.run()