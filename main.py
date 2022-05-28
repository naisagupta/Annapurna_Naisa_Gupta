import cv2
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import Message ,Text
from tkinter import messagebox
import cv2,os
import shutil
import csv
import numpy as np
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
import smtplib
import glob
from email.message import EmailMessage
from tkinter import *
from PIL import ImageTk, Image


#WELCOME SCREEN UI
splash_root = tk.Tk()
splash_root.configure(background='yellow')
splash_root.title("Annapurna")
splash_root.attributes('-fullscreen', True)

#ADDING BACKGROUND IMAGE- welcome screen
bg = PhotoImage( file = "bg01.png")
label1 = Label( splash_root, image = bg, bg="yellow")
label1.place(x=0, y=0, relwidth=1, relheight=1)



#HEADING
splash_label = tk.Label(splash_root, text=" Welcome to ANNAPURNA : Ration Distribution System " ,bg="#deb889"  ,fg="black"  ,width=70  ,height=2,font=('Pristina', 40, 'bold')) 
splash_label.pack()









#strat and close button functions
def start():
    newscreen()
    
  
    


def on_closing():
    if messagebox.askokcancel("Quit", "Attention : Are you sure you want to QUIT?"):
        splash_root.destroy()
    

splash_root.protocol("WM_DELETE_WINDOW", on_closing)
    
#STARTBUTTON
start = tk.Button(splash_root, text="START" , command=start,fg="white"  ,bg="green"  ,width=30  ,height=1 ,activebackground = "blue" ,font=('nunito',20,'bold'))
start.place(x=370, y=500)
#CLOSEBUTTON
close = tk.Button(splash_root, text="CLOSE" , command=on_closing,fg="white"  ,bg="brown"  ,width=30  ,height=1 ,activebackground = "Red" ,font=('nunito',20,'bold'))
close.place(x=370, y=600)

#MAIN SCREEN defined
def newscreen():
    window = tk.Toplevel()
    #MAIN SCREEN UI
    window.title("Annapurna")
    window.configure(background='yellow')
    window.attributes('-fullscreen', True)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    
    filename = PhotoImage(file = "bg1.png")
    background_label = Label(window, image=filename)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    #ID
    idlabel = tk.Label(window, text="Enter ID",width=16  ,height=2  ,fg="black"  ,bg="white" ,font=('nunito',16, ' bold ') ) 
    idlabel.place(x=300, y=150)
    idtext = tk.Entry(window,width=40  ,bg="white" ,fg="red",font=('nunito',16, ' bold '))
    idtext.place(x=150, y=200)

    #NAME
    namelabel = tk.Label(window, text="Enter Name",width=16  ,fg="black"  ,bg="white"    ,height=2 ,font=('nunito',16, ' bold ')) 
    namelabel.place(x=300, y=250)
    nametext = tk.Entry(window,width=40,bg="white"  ,fg="red",font=('nunito',16, ' bold ')  )
    nametext.place(x=150, y=300)

    #NOTIFICATION
    notification = tk.Label(window, text="WELCOME TO ANNAPURNA!" ,bg="skyblue"  ,fg="red"  ,width=40 ,height=3, activebackground = "white" ,font=('nunito',16, ' bold ')) 
    notification.place(x=150, y=60)

    #RATION DISTRIBUTION:
    rationdis = tk.Label(window, text="Ration Distributed To : ",width=20  ,fg="black"  ,bg="white" ,height=1 ,font=('nunito',16, ' bold  underline')) 
    rationdis.place(x=280, y=430)
    rationdismsg = tk.Label(window, text="" ,fg="red"   ,bg="skyblue",activeforeground = "green",width=40  ,height=3  ,font=('nunito',16, ' bold ')) 
    rationdismsg.place(x=150, y=480)

    #CLEAR BUTTON FUNCTION
    def clear():
        idtext.delete(0, 'end')  
        nametext.delete(0,'end')  
        notification.configure(text= "CLEARED")
    
    #CHECK FOR VALUES   
    def checknum(data):
        try:
            float(data)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(data)
            return True
        except (TypeError, ValueError):
            pass
        return False
    
    #CAPTURE FACE 
    def CaptureImg():        
        userid=(idtext.get())
        username=(nametext.get())
        if(checknum(userid) and username.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    sampleNum=sampleNum+1
                    cv2.imwrite("TrainingImage\ "+username +"."+userid +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('CAPTURING YOUR IMAGE : ',img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            value = "Images Saved : " + userid +" Name : "+ username
            row = [userid , username]
            with open('VillageDetails\Village.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            notification.configure(text= value)
        else:
            if(checknum(userid)):
                value = "Enter Alphabetical Name !"
                notification.configure(text= value)
            if(username.isalpha()):
                value = "Enter Numeric userid !"
                notification.configure(text= value)
    
    #GETTING LABELS AND IMAGES DATA
    def GetData(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        faces=[]
        Ids=[]
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)        
        return faces,Ids

    #TRAINING IMAGES   
    def TrainImages():
        recognizer = cv2.face.LBPHFaceRecognizer_create() 
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces,userid = GetData("TrainingImage")
        recognizer.train(faces, np.array(userid))
        recognizer.save("TrainingImageLabel\Trainner.yml")
        value = "PERSON ADDED ! "
        notification.configure(text= value)

    #TRACK IMAGE FUNCTION
    def ScanPerson():
        recognizer = cv2.face.LBPHFaceRecognizer_create()  
        recognizer.read("TrainingImageLabel\Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);    
        df=pd.read_csv("VillageDetails\Village.csv")
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX        
        col_names =  ['userid','username','Date','Time']
        present = pd.DataFrame(columns = col_names)    
        while True:
            ret,im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)    
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                userid, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
                if(conf < 50):
                    ts = time.time()      
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['userid'] == userid]['username'].values
                    tt=str(userid)+"-"+aa
                    present.loc[len(present)] = [userid,aa,date,timeStamp]
                else:
                    userid='Unknown'                
                    tt=str(userid)  
                if(conf > 75):
                    noOfFile=len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
                present=present.drop_duplicates(subset=['userid'],keep='first')    
                cv2.imshow('SCANNING : PLEASE  STAND STILL ! ',im) 
            if (cv2.waitKey(1)==ord('q')):
                break
            ts = time.time()      
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour,Minute,Second=timeStamp.split(":")
            fileName="Ration_Distribution_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
            present.to_csv(fileName,index=False)
            cam.release()
            cv2.destroyAllWindows()
            print(present) 
            value=present
            rationdismsg.configure(text= value)
            
    #SENDING CSV EMAIL
    def sendmail():
        msg = EmailMessage()
        msg['Subject'] = "REPORT FOR RATION DISTRIBUTION"
        msg['From'] = "emailservicenaisa@gmail.com" 
        msg['To'] = "renunaisa42@gmail.com"

        with open('EmailTemplate.txt') as myfile:
            data=myfile.read()
            msg.set_content(data)
        
        for files in glob.glob("*.csv"):
            with open(files,"rb") as f:
                file_data=f.read() 
                file_name=f.name 
                msg.add_attachment(file_data,maintype="application",subtype="csv",filename=file_name)
                print("ADDED IN ATTACHMENT :",file_name)   
                
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
            server=smtplib.SMTP_SSL('smtp.gmail.com',465)
            server.login("emailservicenaisa@gmail.com","Yaisa@15946")
            server.send_message(msg)
            
        print("EMAIL SENT!")
        value = "EMAIL SENT WITH LIST !"
        notification.configure(text= value)
            
        

        
    #CLEAR
    clearButton = tk.Button(window, text="CLEAR", command=clear  ,fg="white"  ,bg="purple"  ,width=40  ,height=2 ,activebackground = "Red" ,font=('nunito',16, ' bold '))
    clearButton.place(x=150, y=350)
    
    #TAKE IMAGE BUTTON
    takeImg = tk.Button(window, text="TAKE PICTURE", command=CaptureImg  ,fg="white"  ,bg="darkblue"  ,width=20  ,height=4, activebackground = "Red" ,font=('nunito',16, ' bold '))
    takeImg.place(x=820, y=70)
    #vertical,horizontal

    #TRAIN IMAGE
    trainImg = tk.Button(window, text="ADD PERSON", command=TrainImages  ,fg="white"  ,bg="magenta"  ,width=20  ,height=4, activebackground = "Red" ,font=('nunito',16, ' bold '))
    trainImg.place(x=820, y=220)

    #SCAN FACE
    trackImg = tk.Button(window, text="START SCAN", command=ScanPerson  ,fg="white"  ,bg="green"  ,width=20  ,height=4, activebackground = "Red" ,font=('nunito',16, ' bold '))
    trackImg.place(x=820, y=370)
    
    
    def on_closing2():
        if messagebox.askokcancel("Quit", "Attention : Are you sure you want to QUIT?"):
            window.destroy()
            splash_root.destroy()
    #QUIT
    quitWindow = tk.Button(window, text="QUIT", command=on_closing2,fg="white"  ,bg="red"  ,width=20  ,height=4, activebackground = "blue" ,font=('nunito',16, 'bold  underline'))
    quitWindow.place(x=820, y=520) 

    
      #email
    email = tk.Button(window, text="Email Ration Distribution List", command=sendmail  ,fg="white"  ,bg="purple"  ,width=40  ,height=2 ,activebackground = "green" ,font=('nunito',16, ' bold '))
    email.place(x=150, y=580)

    window.protocol("WM_DELETE_WINDOW", on_closing2)
        
    window.mainloop()

splash_root.mainloop()