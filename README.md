# Newspaper_Image_Search
This project code allows one to search through the images from many newspaper looking for the occurrences of keywords and faces. E.g. if you search for "Mike" it will return a contact sheet of all of the faces which were located on the newspaper page which mentions the name "Mike"
<br>

#### Contents
* `Main.py` takes a ZIP file of images (newspaper images) and process them, and finally it will return a contact sheet of all of the faces 
which were located on the newspaper page which mentions the name we search for. <br>
* `readonly` folder contains face (front profile) detection classifier and an image containing face detection result for searching the key word "Mark".
* we use `OpenCV` to detect faces, `tesseract` to do optical character recognition, and `PIL` to composite images together into contact sheets.
### Dataset
Each page of the newspapers is saved as a single PNG image in a file images.zip These newspapers are in english, and contain a 
variety of stories, advertisements and images. <br>
*Note: This file is fairly large (~200 MB) and may take some time to work with, I would encourage you to use a smaller subset of these images for testing.*
<br> [Dataset link](https://drive.google.com/file/d/1ShWzDqKZdbSqYWh_E7m9u9Aq8xAtCj2q/view?usp=sharing)
