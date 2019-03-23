'''
Code for the paper titled "IoT Enabled Video Surveillance System using Raspberri Pi".
Authors: Rahul Patil, NR Vinay, Ram Srinivas, Rohith Y and Pratiba D.

Credits: The initial idea and starting point for is from Adrian Rosebrock's blog post -
https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/
This was our main source of inspiration and we would like to give him credits.
'''
import cv2
from imutils.video import VideoStream
from imutils.video import FPS

import numpy as np

import datetime
import time

import ouraws

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import csv


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

times = []
initial_frame = None
flag_record = []
for i in range(3):
    flag_record.append(None)
#dataframe_motion = pandas.DataFrame(columns = ("Start_of_Motion", "End_of_Motion"))
#name = input("Enter your name: ")
#email = input("Enter your email: ")
motion_id = 287
motion_count = 0
prev_upload = datetime.datetime.now()
entry_flag = 0
cloud_times = []

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
video_record = VideoStream(src = 0).start()
time.sleep(3.0)

while True:
    frame = video_record.read()
    motion_flag = 0
    height_frame, width_frame = frame.shape[:2]
    frame_small = cv2.resize(frame, (int(0.5*width_frame), int(0.5*height_frame)), interpolation = cv2.INTER_CUBIC)
    to_send_frame = frame_small
    gray_frame = cv2.cvtColor(frame_small, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)


    if initial_frame is None:
        initial_frame = gray_frame.copy().astype("float")
        continue

    cv2.accumulateWeighted(gray_frame, initial_frame, 0.1)

    delta_frame = cv2.absdiff(cv2.convertScaleAbs(initial_frame), gray_frame)

    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 50)

    (_,contours,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 4000:
            continue

        motion_flag = 1
        (x_cord, y_cord, width, height) = cv2.boundingRect(contour)
        cv2.rectangle(frame_small, (x_cord, y_cord), (x_cord+width, y_cord+height), (0, 255, 0), 2)

    if motion_flag == 1:
        cv2.putText(frame_small, "Something is moving!", (10, 20),
    		cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 2)
        time_ = datetime.datetime.now()
        #warning_email(name, email, time_)
    else:
        cv2.putText(frame_small, "Nothing has moved for some time", (10, 20),
    		cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 255), 2)

    flag_record.append(motion_flag)
    current_time = datetime.datetime.now()

    if motion_flag == 1:
        if(current_time - prev_upload).seconds >= 5:
            motion_count += 1
            #print("if " + str(motion_count))
            if motion_count >= 15 and entry_flag == 0:
                timelist = []
                x = time.time()
                cv2.imwrite("motion.jpg", to_send_frame)
                write = time.time()
                timelist.append(write - x)
                #print("to write " + str(write - x))
                drive1 = time.time()
                link1 = ouraws.Upload_Getlink(drive)
                drive2 = time.time()
                timelist.append(drive2 - drive1)
                #print("to drive " + str(drive2 - drive1))
                rds1 = time.time()
                ouraws.insert_entry_time(motion_id, datetime.datetime.now(),link1)
                rds2 = time.time()
                timelist.append(rds2-rds1)
                #print("upload on rds " + str(rds2 - rds1))
                #ouraws.send_email(link1, motion_id)
                y = time.time()
                timelist.append(y-rds2)
                #print("trigger email " + str(y - rds2))
                z = y - x
                timelist.append(z)
                #print(str(z) + " " + str(motion_id))
                with open('times.csv', 'a') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(timelist)
                motion_count = 0
                prev_upload = current_time
                print("uploaded entry time")
                entry_flag = 1

    elif motion_flag == 0:
        motion_count = 0

    if flag_record[-1] == 0 and flag_record[-2] == 1 and entry_flag == 1:
        #times.append(datetime.datetime.now())
        #instead send data to database instead of adding to list
        rds11 = time.time()
        ouraws.insert_exit_time(motion_id, datetime.datetime.now())
        rds12 = time.time()
        print("Upload exit rds " + str(rds12 - rds11) + " " + str(motion_id))
        motion_id = motion_id + 1
        print("Exit time entered")

        print(" ")
        print(" ")

        entry_flag = 0

    cv2.imshow("Motion Detection", frame_small)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
	    if motion_flag == 1:
		    ouraws.insert_exit_time(motion_id, datetime.datetime.now())
            break

cv2.imwrite("test.jpeg", frame_small)

print(cloud_times)

ouraws.close_up()
cv2.destroyAllWindows()
video_record.stop()
