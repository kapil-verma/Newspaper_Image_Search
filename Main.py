#!/usr/bin/env python
# coding: utf-8
# 
### NewsPaper Image Search ###
# It takes a ZIP file of images (newspaper images) and process them, and finally it will return a contact sheet of all of the faces 
# which were located on the newspaper page which mentions the name we search for. 
#
# we use OpenCV to detect faces, tesseract to do optical character recognition, and PIL to composite images together into contact sheets.
# 
# Dataset: Each page of the newspapers is saved as a single PNG image in a file images.zip These newspapers are in english, and contain a 
# variety of stories, advertisements and images. 
# Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use a smaller subset of these
# images for testing.


### Making global database (stored in ziplist variable)

import zipfile
import cv2 as cv
from PIL import Image, ImageDraw
import pytesseract
import numpy as np
import string
# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
#reading and opening files from zip file
zf = zipfile.ZipFile("readonly/images.zip")
zf_list = zf.infolist()

def show_bbox(faces, img):
    """function for showing bounding boxes over an image.
       Params:  Faces- coordinates of bounding box.
                img- image over which boxes have to be shown.
    """
    drawing=ImageDraw.Draw(img)
    # iterate through the faces sequence with tuple unpacking
    for x,y,w,h in faces:
        # Adding width and height
        drawing.rectangle((x,y,x+w,y+h), outline="white")
    display(img)

    
def zip_routine():
    """function for making and returning  a database of images, filenames of images, text extracted and face detected from 
       every image as a list of tuples (myzip_list).
    """
    myzip_list = []
    for i in zf_list:
        with zf.open(i) as file:
            img = Image.open(file)
            print("File name: {}".format(i.filename))
            #image mode is already RGB
            #extracting text after converting image to gray scale and performing binarization
            text = pytesseract.image_to_string(img.convert('L').convert('1'))
            text=text.lower()
            # face detection
            cvim = np.array(img)
            gray = cv.cvtColor(cvim, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)
            #dislpaying detected faces on every page
            show_bbox(faces, img)
            myzip_list.append((i.filename, img.copy(),text, faces))
    print(myzip_list)
    return myzip_list
    
ziplist = zip_routine()


### Making contact sheet of the results of search

import math
import PIL
def displayC_sheet(list):
    """function: returns a contact sheet which shows resized detected faces from page containg the keyword we look for.
       params: list of tuples containg image, filename, text and bounding boxes of detected face.
    """
    image = list[1]
    #creating blank contact sheet based on no. of detected faces on a page
    if len(list[3])<=5:
        contact_sheet = PIL.Image.new(image.mode,(500,100))
    else:
        contact_sheet = PIL.Image.new(image.mode,(500,math.ceil(len(list[3])/5)*100))
    x=0
    y=0
    for img in list[3]:
        # Lets paste detected face image into the contact sheet
        size = (100, 100)
        contact_sheet.paste((image.crop((img[0],img[1],img[2]+img[0],img[3]+img[1]))).resize((100,100)), (x,y))
        # Now we update our X position. If it is going to be the width of the image, then we set it to 0
        # and update Y as well to point to the next "line" of the contact sheet.
        if (x+100 == 500):
            x=0
            y=y+100
        else:
            x=x+100
    return contact_sheet

def find_name(person):
    """function: Allows user to search the name in all images and returns the finished contact sheet with results
       params: a string containing either a name or any keyword
    """
    #using lower case alphabets for searching as we have already converted extracted text to lower case
    person = person.lower()
    for i in ziplist:
        if (person not in i[2].split()):
            continue
        print('Results in file {}'.format(i[0]))
        if ((len(i[3]) == 0)):
            print('No faces in this file')
        else:
            display(displayC_sheet(i))
            
#an example            
find_name('Mark')

