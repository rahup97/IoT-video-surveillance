from boto3 import client

import sys
import logging
import rds_config

import pymysql

import time
from datetime import datetime
import os

now = time.localtime()

rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password

db_name = rds_config.db_name
port = 3306

conn = pymysql.connect(rds_host, user = name, passwd = password, db = db_name, connect_timeout = 5)
cur = conn.cursor()

def insert_entry_time(motionid, time,link):
    #cur.execute("create table Motion_Detection1 (motionid  int NOT NULL, entry_time datetime , exit_time datetime, PRIMARY KEY(motionid))")
    cur.execute("Insert into Motion_Detection  (motionid, entry_time, exit_time,image_link) values ('%s','%s','%s','%s')" % (motionid, time, time,link))
    #print(motionid)
    conn.commit()

def insert_exit_time(motionid, time):
    #cur.execute("create table Motion_Detection1 (motionid  int NOT NULL, entry_time datetime , exit_time datetime, PRIMARY KEY(motionid))")
    cur.execute("Update Motion_Detection set exit_time = '%s' where motionid = '%s'" % (time, motionid))
    #print(motionid)
    conn.commit()



def view_record(motionid):
    conn = pymysql.connect(rds_host, user = name, passwd = password, db = db_name, connect_timeout = 5)
    cur = conn.cursor()
    #cur.execute("create table Motion_Detection1 (motionid  int NOT NULL, entry_time datetime , exit_time datetime, PRIMARY KEY(motionid))")
    cur.execute('select entry_time from Motion_Detection1 where motionid = 47')
    #print(motionid)
    time = cur.fetchone()
    #print(time)


def close_up():
    conn.close()


def Upload_Getlink(drive):
    files = drive.CreateFile()
    files.SetContentFile('motion.jpg')
    files.Upload()

    permission = files.InsertPermission({

                                'type': 'anyone',

                                'value': 'anyone',

                                'role': 'reader'})

    link = files['alternateLink']

    link = link.split('?')[0]

    link = link.split('/')[-2]

    link='https://docs.google.com/open?id='+link

    return link


def send_email(link, motionid):

	conn = client('ses')

	response = conn.send_email(

		Destination = {

		    'BccAddresses': [

		    ],

		    'CcAddresses': [

		    ],

		    'ToAddresses': [

		        '<client address>@gmail.com'

		    ],

		},

		Message = {

		    'Subject': {

		        'Charset': 'UTF-8',

		        'Data': 'Motion Detected' + str(motionid),

		    },

		    'Body': {

		        'Text': {

		            'Data': "Motion detected at " + str(datetime.now()) + " and your image link is " + link,

		            'Charset': 'UTF-8',

		        }
		    }

		},

		ReplyToAddresses = [
		],

		ReturnPath = '<address>@gmail.com',

		ReturnPathArn = 'arn:aws:ses:<region>:<12 digit number>:identity/<address>@gmail.com',

		Source = '<address>@gmail.com',

		SourceArn = 'arn:aws:ses:<address>:<12 digit number>:identity/<address>@gmail.com',

    )

#print(response)
