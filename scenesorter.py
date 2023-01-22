import sys
import getopt
import shutil

from imageio.v2 import imread
from scipy.linalg import norm
from numpy import average, sum
import os
import cv2
import imutils 



class CompareImg:

    def __init__(self):

        #move into set0 before comparing


        argv = sys.argv[1:]
        self.pix_diff=0.5
        self.folder=""
        try:

            options, args = getopt.getopt(argv,"f:d:",["folder =", "difference ="])
        
        except:
            pass

        for flag, value in options:
            if flag in ["-f","--folder"]:
                self.folder= value

            if flag in ["-d","--difference"]:
                self.pix_diff= float(value)

        if self.folder !="":


            self.main()
            os.rename(f"{self.set_holder_folder}/", f"{self.folder}/{self.set_holder_folder}/")

        else:
            print("folder not defined please use flags -f <folder_name> or --folder <folder_name> when running python script")


    def uniquify(self,path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = filename + " (" + str(counter) + ")" + extension
            counter += 1

        return path

    def main(self):



        img_seq_list = os.listdir(self.folder)
        img_seq_list.sort()
        remove_buffer=[]

        l=0
        r=1
        for i in range(len(img_seq_list)):
                
            if img_seq_list[i][0] =="." or "." not in img_seq_list[i]:
                print(f"Skipping hidden file or folder: {img_seq_list[i]}")

                remove_buffer.append(img_seq_list[i])

        for i in remove_buffer:
                
                img_seq_list.remove(i)
                    

        self.set_holder_folder= os.path.basename(self.uniquify(f"{os.getcwd()}/{self.folder}/image_sequences"))

        self.diff_num=0

        os.mkdir(( self.set_holder_folder))

        

        os.mkdir(f"set{self.diff_num}")
        shutil.copy(f"{self.folder}/{img_seq_list[l]}", f"set{self.diff_num}/{img_seq_list[l]}")

        

        while r < len(img_seq_list):

            try:

                print()
                
                print(f"{img_seq_list[l]} >>>>> {img_seq_list[r]} ")
                self.get_answer(img_seq_list[l],img_seq_list[r])
                print()
                

                if self.difference <=self.pix_diff:
                    shutil.copy(f"{self.folder}/{img_seq_list[r]}", f"set{self.diff_num}/{img_seq_list[r]}")
                    

                else:

                    os.rename(f"set{self.diff_num}/", f"{self.set_holder_folder}/set{self.diff_num}/")
                    self.diff_num+=1
                    os.mkdir((f"set{self.diff_num}"))

                    self.changes(f"{os.getcwd()}/{self.set_holder_folder}/set{self.diff_num-1}/{img_seq_list[l]}",f"{os.getcwd()}/{self.folder}/{img_seq_list[r]}")

                    os.rename(f"{os.getcwd()}/changes{self.diff_num}.png", f"set{self.diff_num}/changes{self.diff_num}.png")

                    shutil.copy(f"{self.folder}/{img_seq_list[r]}", f"set{self.diff_num}/{img_seq_list[r]}")
                    
                    l=r

                r+=1

            except Exception as e:
                print(e)
                
        os.rename(f"set{self.diff_num}/", f"{self.set_holder_folder}/set{self.diff_num}/")


    def get_answer(self,file1,file2):
        
        # read images as 2D arrays (convert to grayscale for simplicity)
        img1 = self.to_grayscale(imread(f"{os.getcwd()}/set{self.diff_num}/{file1}").astype(float))
        img2 = self.to_grayscale(imread(f"{os.getcwd()}/{self.folder}/{file2}").astype(float))
        # compare
        n_m, n_0 = self.compare_images(img1, img2)

        self.difference=n_m/img1.size

        #print ("Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size)
        #print ("Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size)
        print(self.difference)


    def compare_images(self,img1, img2):
        # normalize to compensate for exposure difference, this may be unnecessary
        # consider disabling it
        img1 = self.normalize(img1)
        img2 = self.normalize(img2)
        # calculate the difference and its norms
        diff = img1 - img2  # elementwise for scipy arrays
        m_norm = sum(abs(diff))  # Manhattan norm
        z_norm = norm(diff.ravel(), 0)  # Zero norm
        return (m_norm, z_norm)


    def to_grayscale(self,arr):
        "If arr is a color image (3D array), convert it to grayscale (2D array)."
        if len(arr.shape) == 3:
            return average(arr, -1)  # average over the last axis (color channels)
        else:
            return arr


    def normalize(self,arr):
        rng = arr.max()-arr.min()
        amin = arr.min()
        return (arr-amin)*255/rng



    def changes(self,one,two):

        #get the images you want to compare.
        original = cv2.imread(one)
        new = cv2.imread(two)
        #resize the images to make them small in size. A bigger size image may take a significant time
        #more computing power and time
        original = imutils.resize(original, height = 600)
        new = imutils.resize(new, height = 600)


        #create a copy of original image so that we can store the
        #difference of 2 images in the same on
        diff = original.copy()
        cv2.absdiff(original, new, diff)

        #converting the difference into grayscale images
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        #increasing the size of differences after that we can capture them all
        for i in range(0, 3):
            dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)
        

        
        #threshold the gray image to binary it. Anything pixel that has
        #value higher than 3 we are converting to white
        #(remember 0 is black and 255 is exact white)
        #the image is called binarised as any value lower than 3 will be 0 and
        # all of the values equal to and higher than 3 will be 255
        (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

        # now we have to find contours in the binarized image
        cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)


        for c in cnts:
            # nicely fiting a bounding box to the contour
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #remove comments from below 2 lines if you want to
        #for viewing the image press any key to continue
        #simply write the identified changes to the diskss
        cv2.imwrite(f"changes{self.diff_num}.png", new)
                



CompareImg()


