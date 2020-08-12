# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:40:43 2020
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html

@author: AL Ma
"""

import boto3
import time
import urllib.request
import json

import os
from os import listdir
from os.path import isfile, isdir, join


# 指定要列出所有檔案的目錄
MYPATH = "~~~"


def aws_flow(relative_path):
    AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'
    AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
    
    job_name = relative_path.replace('/', '-')
    job_base_uri = 'https://~~~'
    job_uri = job_base_uri + relative_path
    
    
    print ('job_uri : ' + job_uri)
    
    transcribe = boto3.client('transcribe', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='ap-northeast-1')
    
    try:
        transcribe.start_transcription_job(TranscriptionJobName=job_name, Media={'MediaFileUri': job_uri}, MediaFormat='mp3', LanguageCode='zh-CN')
    except Exception as e:
        print(e)
    
    # while True:
    #     status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    # #    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
    # #        break
        
    #     if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
    #         response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
    #         data = json.loads(response.read())
    #         text = data['results']['transcripts'][0]['transcript']
    #         print(text)
    #         break
    #     print("Not ready yet...")
    #     time.sleep(2)
    # print(status)



file_count = 0
def getFilePath(mypath):
    # 取得所有檔案與子目錄名稱
    files = listdir(mypath)
    global file_count
    # 以迴圈處理
    for f in files:
      # 產生檔案的絕對路徑
      fullpath = join(mypath, f)
      # 判斷 fullpath 是檔案還是目錄
      if isfile(fullpath):
        print("mypath：", mypath)
        print("檔案：", fullpath)
        print("檔案 f ：", fullpath.replace(MYPATH, ''))
        print(os.stat(fullpath).st_size)
        print("al_test" + fullpath.replace(MYPATH, '').replace('\\', '-'))
        aws_flow(fullpath.replace(MYPATH, '').replace('\\', '/'))
        file_count = file_count + 1
        print('i : %d ' % file_count)
        if file_count%98==0 :
            time.sleep(300)
        

        # time.sleep(3)
        
      elif isdir(fullpath):
        print("目錄：", fullpath)
        getFilePath(fullpath)



getFilePath(MYPATH)