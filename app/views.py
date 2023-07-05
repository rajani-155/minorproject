from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import Attendence,Student
from .forms import StudentCreationForm

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import shutil



# Create your views here.

def Home(request):
    return render(request,'index.html')


def Login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        print(password)
        user=User.objects.filter(username=username).first()
        if user == None:
            context={
                'message':'Username or Password Incorrect'
            }
            print("User not found")
            return render(request,'login.html',context)
        else:
            if check_password(password,user.password):
                login(request,user)
                return redirect("/")
                print("User logged in")
            else:
                context={
                    'message':'Password is Incorrect'
                }
                print("Incorrect password")
                return render(request,'login.html',context)
    return render(request,'login.html')

def Logout(request):
    logout(request)
    return redirect("/")


@login_required(login_url="login")
def ViewAttend(request):
    if request.method=="POST":
        print("Viewing student attendence function called")
        studentID=request.POST.get('stdID')
        std=Student.objects.get(std_id=studentID)
        std_att=Attendence.objects.filter(std_id=std)
        context={
            'student':std_att,
        }
        return render(request,'viewattend.html',context)
    else:
        return render(request,'viewattend.html')

@login_required(login_url="login")
def AddStudent(request):
    if request.method=="POST":
        form=StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
        id=request.POST.get('std_id')
        url="static/images/Std_images/"+id+".jpg"
        print(url)
        context={
            'id':id,
            'f_name': request.POST.get('first_name'),
            'm_name': request.POST.get('middle_name'),
            'l_name': request.POST.get('last_name'),
            'faculty': request.POST.get('faculty'),
            'address': request.POST.get('address'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'imgurl':url
        }
        try:
            takeimage(id)
        except:
            return render(request,'success_student.html',context)
        return render(request, 'success_student.html', context)
    else:
        form = StudentCreationForm()
        context={
            'form':form
        }
        return render(request,'addstd.html',context)


@login_required(login_url="login")
def Edit(request):
    if request.method=="POST":
        if request.POST.get('stdID'):
            id=request.POST.get('stdID')
            std=Student.objects.get(std_id=id)
            context={
                'std_detail':std
            }
            return render(request,'edit_details.html',context)
        elif request.POST.get('std_id'):
            id=request.POST.get('std_id')
            std=Student.objects.get(std_id=id)
            std.first_name=request.POST.get('first_name')
            std.middle_name=request.POST.get('middle_name')
            std.last_name=request.POST.get('last_name')
            std.address=request.POST.get('address')
            std.phone=request.POST.get('phone')
            std.email=request.POST.get('email')
            std.save()
            context={
                'message':'Student details updated sucessfully'
            }
            return render(request,'edit_details.html',context)
    else:
        return render(request,'edit_details.html')



def takeimage(stdid):
    name = stdid

    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    x=True

    while x==True:
        try:

            check, frame = webcam.read()
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                # image=cv2.inwrite(filename='{}.jpg'.format(name),img=frame)
                # img=StudentImage(std_id=name,image=cv2.inwrite(filename='{}.jpg'.format(name),img=frame))
                # img.save()

                cv2.imwrite(filename='StudentImages/{}.jpg'.format(name), img=frame)
                # cv2.imwrite(filename='static/images/Std_images/{}.jpg'.format(name), img=frame)
                webcam.release()
                img_new = cv2.imread('StudentImages/{}.jpg'.format(name), cv2.IMREAD_GRAYSCALE)
                x=False
                # img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
                print("Processing image...")
                img_ = cv2.imread('StudentImages/{}.jpg'.format(name), cv2.IMREAD_ANYCOLOR)
                print("Converting RGB image to grayscale...")
                gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                # print("Converted RGB image to grayscale...")
                # print("Resizing image to 28x28 scale...")
                img_ = cv2.resize(gray, (1920, 1820))
                # print("Resized...")
                # img_resized = cv2.imwrite(filename='E:\\project codes\\111\\dataset\\{}-final.jpg'.format(name), img=img_)
                img_resized = cv2.imwrite(filename='E:\\test\\{}-final.jpg'.format(name), img=img_)
                print("Image saved!")
                shutil.copy('StudentImages/'+name+".jpg",'static/images/std_images')
                print("Image Copied")

            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break


def TakeAttendence(request):

    path = 'StudentImages'
    images = []
    personNames = []
    myList = os.listdir(path)
    print(myList)
    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])
    print(personNames)

    def faceEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    # print (faceEncodings(images))

    def attendance(name):
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                time_now = datetime.now()
                tStr = time_now.strftime('%H:%M:%S')
                dStr = time_now.strftime('%d/%m/%Y')
                f.writelines(f'\n{name},{tStr},{dStr}')
                std=Student.objects.get(std_id=name)
                print(std)
                attend=Attendence(std_id=std,time=tStr,date=dStr)
                attend.save()

    encodeListKnown = faceEncodings(images)
    print('All Encodings Complete!!!')

    cap = cv2.VideoCapture(0)
    x=True

    while x==True:
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)
        # face matches and face distances
        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                attendance(name)

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == 27:
            break
        try:
            key = cv2.waitKey(1)
            if key == ord('k'):
                print("Turning off camera.")
                # webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                x=False
                return redirect("/")
        except:
            print("Program is terminated")
    cap.release()
    cv2.destroyAllWindows()

