from skimage.io import imread
from skimage.feature import match_template
from skimage.color import rgb2gray
import numpy as np
import scipy
from PIL import Image
import os
from time import sleep
import warnings

warnings.filterwarnings("ignore")


"""Function to open Instagram"""
def open_insta():
    # Open Instagram
    os.system("adb shell monkey -p com.instagram.android 1 -")
    sleep(3)
    
    # Click Search Icon
    x = "339"
    y = "1712"
    os.system("adb shell input tap " + x + " " + y)
    sleep(3)

"""Function to close Instagram"""
def close_insta():
    # Exit
    x = "805"
    y = "1853"
    os.system("adb shell input tap " + x + " " + y)
    sleep(2)
    x = "933"
    y = "554"
    os.system("adb shell input tap " + x + " " + y)
    sleep(5)

"""Function to get to the Recent page of an hashtag"""
def hashtag_util(hashtag):     
    # Click Search Icon
    x = "339"
    y = "1712"
    os.system("adb shell input tap " + x + " " + y)
    sleep(2)

    # Click Search
    x = "275"
    y = "148"
    os.system("adb shell input tap " + x + " " + y)
    sleep(3)

    # Enter Hashtag
    os.system("adb shell input text " + "\"" + hashtag + "\"")
    sleep(3)

    # Click Hashtag
    x = "481"
    y = "459"
    os.system("adb shell input tap " + x + " " + y)
    sleep(3)

    # Go to Recent
    x = "822"
    y = "752"
    os.system("adb shell input tap " + x + " " + y)
    sleep(3)

    # Click the first picture
    x = "150"
    y = "1060"
    os.system("adb shell input tap " + x + " " + y)
    sleep(3)

"""Function that iteratively likes n_likes photos"""
def like(n_likes):
    warnings.filterwarnings("ignore")
    n = 0
    n_error = 0
    n_mis = 0
    while n < n_likes:
        if n_error == 5:
            close_insta()
            open_insta()
            break
        # Start Liking Posts
        # Scroll up to see the like button
        os.system("adb shell input swipe 540 960 540 700")
        sleep(0.5)

        # Screenshot of post
        os.system("adb exec-out screencap -p > /home/pi/InstaBotAndroid/post.png")
        #sleep(1)
        
        ### Find coordinates with image recognition
        try:
            # Crop the screenshot
            im = Image.open('/home/pi/InstaBotAndroid/post.png') 
            
            # Setting the points for cropped image 
            left = 0
            top = 0
            right = 1080
            bottom = 1633
                
            # Cropped image of above dimension 
            # (It will not change orginal image) 
            im1 = im.crop((left, top, right, bottom)) 
            im1.save('/home/pi/InstaBotAndroid/post.png','png' )

            # Start image reco
            image = imread('/home/pi/InstaBotAndroid/post.png')
            template = imread('/home/pi/InstaBotAndroid/heart.png')

            image_gray = rgb2gray(image)
            template_gray = rgb2gray(template)

            result = match_template(image_gray, template_gray)
            ij = np.unravel_index(np.argmax(result), result.shape)
            x, y = ij[::-1]

            x_like = x + 30
            y_like = y + 32
            
            if x_like == 70 and 97 <= y_like <= 1620:
                # Like the post
                n = n + 1
                x_like = str(x + 30)
                y_like = str(y +32)
                os.system("adb shell input tap " + x_like + " " + y_like)
                print("Like #" + str(n))
                n_error = 0
            else:
                n_mis = n_mis + 1
                print("No like button, scrolling down ...")

            ###

            # Prepare next post
            x_start = "540"
            y_start = y_like
            x_end = "540"
            y_end = "0"
            os.system("adb shell input swipe " + x_start + " " + y_start + " " + x_end + " " + y_end)
        except:
            print("Error locating like button, going to the next post ...")
            n_error = n_error + 1
    return n, n_mis