# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 16:26:32 2020

@author: mdefsrm2
"""

###Code to process and analyse images from a wound-healing assay
###Various parts have been coded separately before, this is a combination program built step-by-step
###Comments are sorted into types:
### 1x# = comment describes exact action of the code
### 2x# = comment describes aim/purpose of code
### 3x# = comment describes what needs/needed to be coded - once completed marked with XX

#---------------------------------------------------------------------------------------------------------#
### Roadmap
### Adding seeing first image to test effect of changing boundary
### Fully commenting code to allow easier use and analysis of code
### Adding progress bar to determine how long proccessing will take
### Adding readme to allow users to see information for instruction of use
### Adding code printout to allow users to see code when just running the GUI
### Automatic scaling of GUI window size
### Adding option to change size of text in GUI
### Adding menu bar to find pages and options
### Adding screen to inform that files have processed and completed.

#--------------------------------------------------------------------------------------------------------#

## Import the required modules; some imported as shorthand version and some only as specific parts
#import tkinter, Python's de-facto GUI package
import tkinter
#import tkinter.ttk, a module providing access to tkinter's themed widgets, to allow for style changes
import tkinter.ttk
#imports tkinter.filedialog, which provides ways to work with files
import tkinter.filedialog
#import imageio, a library to read and write image data
import imageio
#import the RGB to Grayscale function from the colour module of Scikit-image 
from skimage.color import rgb2gray
#import the numpy package, the fundamental package for scientific computing in Python. It is called using np
import numpy as np
#import the scipy.ndimage package, which is dedicated to image processing. It is called using ndi
import scipy.ndimage as ndi
#Import the statistics module from scipy, an open-access resource for scientific python code
from scipy import stats
#import the pandas package, a software library for data manipulation and analysis. It is called using pd
import pandas as pd
#import matplotlib.pyplot which is a package for working with figures. It is called using plt
import matplotlib.pyplot as plt
#import the os function, which provides functions to interact with the operating system
import os
#import datetime, which provides functions to deal with dates and times in python
import datetime
#import csv is a module which allows for using csv files in python
import csv
#import image processing modules from Pillow (PIL)
from PIL import ImageTk
from PIL import Image
#import module for creating and working with temporary files
import tempfile

#----------------------------------------------------------------------------------------------------#

##Set up global variables that are used throughout the code
##When set up here, the variables do not need to be defined using the 'global' function
### Initial variables for character strings set as Null as nothing present in them currently

#Whether the analysis has multiple wells. 1 is yes, 0 is no
multiwells = 0

#How many images were taken for each well
imageperwell = 0

#Time interval between each image
Interval = 0

#Title to be assigned to data and images
Title = ""

#Variable to save path of images located
imagepath = ""

#Variable to where images are to be saved
savepath = ""

#Pixel intensity value to use for the lower bound cutoff for the image mask
Lower_Bound = 0.00

#Pixel intensity value to use for the upper bound cutoff for the image mask
Upper_Bound = 0.00

#Number of iterations to use in the Binary dilation function when refining the mask
Iterations = 1

#Start date of experiment
Exptdate = "01/01/2000"

#Cell line used in experiment
Cellline = "HeLa"

#Oxygen concentration the experiment was carried out with
O2conc = 21

#Radiation dose used to treat the cells
Raddose = 0

#Drug dose used to treat cells
Drugdose = 0

#Seeding density used in the experiment
Seedingdensity = 0

#Time interval between the irradiation treatment and the scratch
Timetoscratch = 0

#Create well variable
well = 1

#Set the global variable pixel width - this is a constant
pixel_width = 1/0.3283

#Create a variable for the start point of the linear range on the graph
LinearStartTime = 1

#Create a variable for the end point of the linear range on the graph
LinearEndTime = 24

#Create the variables for the linear regression analysis
global slope
global intercept
global r_value
global r_squared

test_lower = 0.0
test_upper = 0.0
test_iterations = 1


#----------------------------------------------------------------------------------------------------------------------------#
## Define all the functions that are going to be used by the GUI
## These functions are the functions to run the actual program, show the readme or show the code
## Different frames are created for each possible page

### First step is to create the master Tk widget, this is used as a way of controlling frames below
## Method I am taking from eliminates need for container and also has the frames destroyed before replacing
##  https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028
##  Called as Tk not frame

###A class is a code template for creating objects, like a blueprint for creating objects

## Create the class that acts as the top level frame
class CellMigrationApp(tkinter.Tk):
    #  Define a function to be called when initialising that has the variable 'self'
    def __init__(self):
        tkinter.Tk.__init__(self)
        #  Set it so that it has no frame itself
        self._frame = None
        # When it initialises the first thing that it runs is the function to switch to the main page frame
        self.switch_frame(MainPage)
        
    ## Function is created to allow frames to be switched
    ## This is made in the 'master' frame so can be called by all
    ## This destroys the current frame and then replaces it with a new one    
    # Define a function to be called when switching frames which has the variables 'self' and 'frame_class'
    def switch_frame(self, frame_class):
        #  assigns variable for new frame as the frame that is to be called
        new_frame = frame_class(self)
        ##  Below clause ensures that master frame not destroyed
        ##  This has it call itself as a frame that exists a.k.a it is not None
        if self._frame is not None:
            self._frame.destroy()
        ##  it then has the self frame be classified as the frame to be called
        self._frame = new_frame
        ##  New frame is created. Grid function used as is how arranging is occured
        self._frame.grid()

##  Class is created for the starting page
##  It is called as a frame in tkinter
class MainPage(tkinter.Frame):
    #  First initialising self calls itself and master
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)            
        ###  Create the starting window
        ###  This window will have buttons that will then allow user to run programs, see readme on use of program or see the code used directly
        ##  The title card for the window is made
        self.master.title("Cell Migration and Invasion Analysis Program - Main Menu")

        #  Windows size is specified (widthxheight)
        #  Where new window opens is also specificed (+x+y)
        self.master.geometry('600x400+300+200')
        
        ## Create instruction text for the window
        self.Label1 = tkinter.Label(self, text = "Quick Use Guide", bg = 'white', font=('Calibri Bold', 15))
        self.Label1.grid(row=1, column =0, columnspan = 20)
        
        self.Label2 = tkinter.Label(self, text = " ", font=('Calibri Bold', 15))
        self.Label2.grid(row=2, column =0, columnspan = 20)
        
        self.Label3 = tkinter.Label(self, text = "   This program can be used to quantify gap closure rate in wound healing assays.", font=('Calibri', 10))
        self.Label3.grid (row=3, column=0, columnspan=20)

        self.Label4 = tkinter.Label(self, text = "   A mask is applied to the image to separate the gap pixels from the cell pixels.", font=('Calibri', 10))
        self.Label4.grid (row=4, column=0, columnspan=20)
        
        self.Label5 = tkinter.Label(self, text = "   The gap width is calculated, then the average gap width at each time point is plotted.", font=('Calibri', 10))
        self.Label5.grid (row=5, column=0, columnspan=20)
                
        self.Label6 = tkinter.Label(self, text = "   The linear portion of the graph is manually selected and the gap closure rate calculated.", font=('Calibri', 10))
        self.Label6.grid (row=6, column=0, columnspan=20)   
        
        self.Label7 = tkinter.Label(self, text = " ", font=('Calibri Bold', 15))
        self.Label7.grid(row=7, column =0, columnspan = 20)

        self.Label8 = tkinter.Label(self, text = "   If the Mask Parameters are known*, begin analysis using the 'Begin Data Analysis' tab.", font=('Calibri', 10))
        self.Label8.grid (row=8, column=0, columnspan=20)  
        
        self.Label9 = tkinter.Label(self, text = "   If the Mask Parameters are not known, use the 'Define Mask Parameters' tab.", font=('Calibri', 10))
        self.Label9.grid (row=9, column=0, columnspan=20)  
        
        self.Label10 = tkinter.Label(self, text = " ", font=('Calibri Bold', 15))
        self.Label10.grid(row=10, column =0, columnspan = 20)
        
        self.Label11 = tkinter.Label(self, text = "   * It is advised to 'Define Mask Parameters' for each cell line within an experiment to ensure accuracy.", font=('Calibri italic', 10))
        self.Label11.grid (row=11, column=0, columnspan=20)  
                
        self.Label12 = tkinter.Label(self, text = "   The same parameters can be used within an experiment (e.g. for repeats or different conditions)", font=('Calibri italic', 10))
        self.Label12.grid (row=12, column=0, columnspan=20)  
        ##  The option buttons are created:
        ##  Functions to be run when they are pressed are selected
        ##  Buttons given name, label and command to run when selected
        ##  For creating tkinter objects they are assigned as variables to be able to be called up elsewhere if needed
        ### Need to code action for Parametersbutton
        ### Need to code action for Extractionbutton
        ### Need to code action for Readmebutton
        ### Need to code action for Codebutton
        Parametersbutton = tkinter.Button(self, text = "Define Mask Parameters", command=lambda: master.switch_frame(DefineMaskParameters)).grid(row=0)
        Analysisbutton = tkinter.Button(self, text = "Begin Data Analysis", command=lambda: master.switch_frame(ExperimentInfo)).grid(row=0, column=3)
        Extractionbutton = tkinter.Button(self, text= "Extract Results").grid(row=0, column = 5)
        Readmebutton = tkinter.Button(self, text = "Readme").grid(row=0, column = 7)
        Codebutton = tkinter.Button(self, text = "Raw Code").grid(row=0, column = 9)

#------------------------------------------------------------------------------------------------------------------------------#
### What happens when the Define Mask Parameters button is pressed is defined below.
### It is a process where a single raw data image is imported and a mask applied, with the user able to vary the parameters 
### and see in the window which parameters work best

class DefineMaskParameters(tkinter.Frame):
    #define global parameters
    global testimage
    global test_upper
    global test_lower
    global test_iterations
    
    #  First initialising self calls itself and master
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        #Window is named
        self.master.title("Cell Migration and Invasion Analysis Program - Define Mask Parameters")
        #  Windows size is specified (widthxheight)
        #  Where new window opens is also specificed (+x+y)
        self.master.geometry('1500x1000+0+0')
        #  Create variable for frame
        self.var1 = tkinter.IntVar()      
        
        ## Create instruction text for the window
        self.Label1 = tkinter.Label(self, text = "1. Select an example image. Once selected, this raw image will be shown in the window.", font=('Calibri', 10))
        self.Label1.grid(row=5, column =0, columnspan = 20)
        
        self.Label2 = tkinter.Label(self, text = "2. Use the sliders to alter the three parameters. After the first adjustment, the masked image will be shown next to the raw image, and will update in real time", font=('Calibri', 10))
        self.Label2.grid (row=6, column=0, columnspan=20)
        
        self.Label3 = tkinter.Label(self, text = "3. By comparing the raw and masked images, select the parameters for use. A good mask has minimum 'gap' pixels in the cell monolayer and a good gap edge definition.", font=('Calibri', 10))
        self.Label3.grid (row=7, column=0, columnspan=20)
        
        self.Label4 = tkinter.Label(self, text = "The lower and upper bounds change which pixels are excluded from the mask as 'cell' pixels. Higher iterations value blur around the 'cell' pixels, which are useful for reducing noise in the monolayer but blur edges ", font=('Calibri', 10))
        self.Label4.grid (row=8, column=0, columnspan=20)
        
        self.Label5 = tkinter.Label(self, text = "4. Once parameters have been selected, note down for use in the analysis program. Currently the software does not save the parameters for use later", font=('Calibri', 10))
        self.Label5.grid (row=9, column=0, columnspan=20)      
        
        self.Label6 = tkinter.Label(self, text = " ", font=('Calibri', 10))
        self.Label6.grid (row=10, column=0, columnspan=20) 

        self.Label7 = tkinter.Label(self, text = "A panel of test masks can be generated using the 'Test Panel' button to help narrow down parameter range.", font=('Calibri', 10))
        self.Label7.grid(row=11, column =0, columnspan = 20)        

        ##  Create a 'select test image' upload box
        ###  Using in-built function to browse files for this info
        ###  Creating a function to allow button to be pressed to browse directory
        self.Label1 = tkinter.Label(self, text = "Test Image Location:")
        self.Label1.grid(row=0, column =0)
        #  create a string text variable that is used
        self.imagepathtxt = tkinter.StringVar()
        ##  Text in entry is the filepath chosen by the user when selecting the browse button
        self.Entry1 = tkinter.Entry(self, textvariable=self.imagepathtxt)
        self.Entry1.grid(row=0, column =1)
        self.Entry1.insert(0, str(imagepath))
        #  Command is the function that initialises browsing file path locations when selected
        self.Button1 = tkinter.Button(self, text = "Browse", command = lambda: self.SelectImage())
        self.Button1.grid(row = 0, column=2)  
       
        
        ##  Input created to allow lower boundary to be adjusted
        self.Label2 = tkinter.Label(self, text = "Lower Boundary:")
        self.Label2.grid(row=2, column =0)
        #  Create a string text variable that is used
        self.test_lowertxt = tkinter.StringVar()
        self.test_lowertxt.set(test_lower)
        self.Entry2 = tkinter.Scale(self, from_=0, to=1, resolution=0.01, orient = tkinter.HORIZONTAL)
        self.Entry2.bind('<ButtonRelease>', lambda x: self.NextButton1())
        self.Entry2.grid(row=2, column =1)
        
        ## Input created to allow upper boundary to be adjusted
        self.Label3 = tkinter.Label(self, text = "Upper Boundary:")
        self.Label3.grid(row=3, column =0)
        # Create a string text variable that is used
        self.test_uppertxt = tkinter.StringVar()
        self.test_uppertxt.set(test_upper)
        self.Entry3 = tkinter.Scale(self, from_=0, to=1, resolution=0.01, orient = tkinter.HORIZONTAL)
        self.Entry3.bind('<ButtonRelease>', lambda x: self.NextButton1())
        self.Entry3.grid(row=3, column =1)
        
        ## Input created to allow iterations to be adjusted
        self.Label4 = tkinter.Label(self, text = "Iterations:")
        self.Label4.grid(row=4, column =0)
        # Create a string text variable that is used
        self.test_iterationstxt = tkinter.StringVar()
        self.test_iterationstxt.set(test_iterations)
        self.Entry4 = tkinter.Scale(self, from_=1, to=5, orient = tkinter.HORIZONTAL)
        self.Entry4.bind('<ButtonRelease>', lambda x: self.NextButton1())
        self.Entry4.grid(row=4, column =1)

        ##  Create a button that will produce a panel of example mask styles
        ###  Creating a function to allow button to be pressed to generate panel
        #  Command is the function that initialises browsing file path locations when selected
        self.Button2 = tkinter.Button(self, text = "Test Panel", command = lambda: self.MaskedPanel())
        self.Button2.grid(row = 12, column=2)          

        
        #Create a new button that will go on all frames that have it go back to previous frame if user wants
        self.BackButton = tkinter.Button(self, text = "Back", command=lambda: master.switch_frame(MainPage))
        self.BackButton.grid(row=12, column = 0, pady = 10)
    

        
        ## Create the function to allow browsing of file location
    def SelectImage(self):
        imagepath = self.GetImages = tkinter.filedialog.askopenfilename ()
        #  Have the label on the screen change to reflect chosen destination
        self.imagepathtxt.set(imagepath)
        ###  display image in the window
        ##  convert the image saved at the path name into a Tkinter compatible format
        img3 = Image.open(imagepath)
        img4 = img3.resize((250, 250), Image.ANTIALIAS)
        img5 = ImageTk.PhotoImage(img4)
        ##  place the image in the window. To get it to be displayed and not garbage-collected, the second line of code keeps a reference to the image
        panel = tkinter.Label(self, image = img5)
        panel.image = img5
        panel.grid(row=0, column=5, rowspan=5)
        
    ## Create the function that creates the panel of masked images
    def MaskedPanel(self):
        paneltestimage = str(self.Entry1.get())
        
        #create a temporary file location to save the nine panel images
        global panel_temp_folder
        panel_temp_folder = tempfile.mkdtemp()
        
        # Import test image
        Panel_Test_Image = imageio.imread(str(paneltestimage))
        #Convert to a grayscale
        Gray_Panel_Test_Image = rgb2gray(Panel_Test_Image)
        
        #Apply nine different masks to image
        #Image 1 0.45, 0.50, 1
        Panel_Mask_1A = np.logical_or(Gray_Panel_Test_Image<0.45, Gray_Panel_Test_Image>0.5)
        Panel_Mask_1B = ndi.binary_dilation(Panel_Mask_1A, iterations = 1)
        Panel_Mask_1C = np.where(Panel_Mask_1B, 0, 1)
        Panel_Mask_1D = ndi.morphology.binary_fill_holes(Panel_Mask_1C)
        plt.imsave(panel_temp_folder + 'panel 1.png', Panel_Mask_1D, cmap='gray')
        
        
        #Image 2 0.45, 0.52, 1
        Panel_Mask_2A = np.logical_or(Gray_Panel_Test_Image<0.45, Gray_Panel_Test_Image>0.52)
        Panel_Mask_2B = ndi.binary_dilation(Panel_Mask_2A, iterations = 1)
        Panel_Mask_2C = np.where(Panel_Mask_2B, 0, 1)
        Panel_Mask_2D = ndi.morphology.binary_fill_holes(Panel_Mask_2C)
        plt.imsave(panel_temp_folder + 'panel 2.png', Panel_Mask_2D, cmap='gray')
        
        #Image 3 0.45, 0.54, 1
        Panel_Mask_3A = np.logical_or(Gray_Panel_Test_Image<0.45, Gray_Panel_Test_Image>0.54)
        Panel_Mask_3B = ndi.binary_dilation(Panel_Mask_3A, iterations = 1)
        Panel_Mask_3C = np.where(Panel_Mask_3B, 0, 1)
        Panel_Mask_3D = ndi.morphology.binary_fill_holes(Panel_Mask_3C)
        plt.imsave(panel_temp_folder + 'panel 3.png', Panel_Mask_3D, cmap='gray')
        
        #Image 4 0.47, 0.50, 1
        Panel_Mask_4A = np.logical_or(Gray_Panel_Test_Image<0.47, Gray_Panel_Test_Image>0.5)
        Panel_Mask_4B = ndi.binary_dilation(Panel_Mask_4A, iterations = 1)
        Panel_Mask_4C = np.where(Panel_Mask_4B, 0, 1)
        Panel_Mask_4D = ndi.morphology.binary_fill_holes(Panel_Mask_4C)
        plt.imsave(panel_temp_folder + 'panel 4.png', Panel_Mask_4D, cmap='gray')
        
        #Image 5 0.47, 0.52, 1
        Panel_Mask_5A = np.logical_or(Gray_Panel_Test_Image<0.47, Gray_Panel_Test_Image>0.52)
        Panel_Mask_5B = ndi.binary_dilation(Panel_Mask_5A, iterations = 1)
        Panel_Mask_5C = np.where(Panel_Mask_5B, 0, 1)
        Panel_Mask_5D = ndi.morphology.binary_fill_holes(Panel_Mask_5C)
        plt.imsave(panel_temp_folder + 'panel 5.png', Panel_Mask_5D, cmap='gray')

        #Image 6 0.47, 0.54, 1
        Panel_Mask_6A = np.logical_or(Gray_Panel_Test_Image<0.47, Gray_Panel_Test_Image>0.54)
        Panel_Mask_6B = ndi.binary_dilation(Panel_Mask_6A, iterations = 1)
        Panel_Mask_6C = np.where(Panel_Mask_6B, 0, 1)
        Panel_Mask_6D = ndi.morphology.binary_fill_holes(Panel_Mask_6C)
        plt.imsave(panel_temp_folder + 'panel 6.png', Panel_Mask_6D, cmap='gray')
        
        #Image 7 0.49, 0.50, 1
        Panel_Mask_7A = np.logical_or(Gray_Panel_Test_Image<0.49, Gray_Panel_Test_Image>0.5)
        Panel_Mask_7B = ndi.binary_dilation(Panel_Mask_7A, iterations = 1)
        Panel_Mask_7C = np.where(Panel_Mask_7B, 0, 1)
        Panel_Mask_7D = ndi.morphology.binary_fill_holes(Panel_Mask_7C)
        plt.imsave(panel_temp_folder + 'panel 7.png', Panel_Mask_7D, cmap='gray')
        
        #Image 8 0.49, 0.52, 1
        Panel_Mask_8A = np.logical_or(Gray_Panel_Test_Image<0.49, Gray_Panel_Test_Image>0.52)
        Panel_Mask_8B = ndi.binary_dilation(Panel_Mask_8A, iterations = 1)
        Panel_Mask_8C = np.where(Panel_Mask_8B, 0, 1)
        Panel_Mask_8D = ndi.morphology.binary_fill_holes(Panel_Mask_8C)
        plt.imsave(panel_temp_folder + 'panel 8.png', Panel_Mask_8D, cmap='gray')
        
        #Image 9 0.49, 0.54, 1
        Panel_Mask_9A = np.logical_or(Gray_Panel_Test_Image<0.45, Gray_Panel_Test_Image>0.5)
        Panel_Mask_9B = ndi.binary_dilation(Panel_Mask_9A, iterations = 1)
        Panel_Mask_9C = np.where(Panel_Mask_9B, 0, 1)
        Panel_Mask_9D = ndi.morphology.binary_fill_holes(Panel_Mask_9C)
        plt.imsave(panel_temp_folder + 'panel 9.png', Panel_Mask_9D, cmap='gray')
        
        ## finally, display these nine images in a panel below the test images. 
        
        ###  display masked image in the window
        ##  convert the image saved at the path name into a Tkinter compatible format
        ##  place the image in the window. To get it to be displayed and not garbage-collected, the second line of code keeps a reference to the image
        img1A = Image.open(panel_temp_folder + 'panel 1.png')
        img1B = img1A.resize((100, 100), Image.ANTIALIAS)
        img1C = ImageTk.PhotoImage(img1B)
        
        panel = tkinter.Label(self, image = img1C)
        panel.image = img1C
        panel.grid(row=17, column=1, rowspan=5)
        Label1 = tkinter.Label(self, text = "L=0.45, U=0.50, It=1")
        Label1.grid(row=23, column =1)
        
        
        img2A = Image.open(panel_temp_folder + 'panel 2.png')
        img2B = img2A.resize((100, 100), Image.ANTIALIAS)
        img2C = ImageTk.PhotoImage(img2B)
        
        panel = tkinter.Label(self, image = img2C)
        panel.image = img2C
        panel.grid(row=17, column=2, rowspan=5)
        Label2 = tkinter.Label(self, text = "L=0.45, U=0.52, It=1")
        Label2.grid(row=23, column =2)
        
        
        img3A = Image.open(panel_temp_folder + 'panel 3.png')
        img3B = img3A.resize((100, 100), Image.ANTIALIAS)
        img3C = ImageTk.PhotoImage(img3B)
        
        panel = tkinter.Label(self, image = img3C)
        panel.image = img3C
        panel.grid(row=17, column=3, rowspan=5)
        Label3 = tkinter.Label(self, text = "L=0.45, U=0.54, It=1")
        Label3.grid(row=23, column =3)
        
        
        img4A = Image.open(panel_temp_folder + 'panel 4.png')
        img4B = img4A.resize((100, 100), Image.ANTIALIAS)
        img4C = ImageTk.PhotoImage(img4B)
        
        panel = tkinter.Label(self, image = img4C)
        panel.image = img4C
        panel.grid(row=24, column=1, rowspan=5)
        Label4 = tkinter.Label(self, text = "L=0.47, U=0.50, It=1")
        Label4.grid(row=30, column =1)        
        
        
        img5A = Image.open(panel_temp_folder + 'panel 5.png')
        img5B = img5A.resize((100, 100), Image.ANTIALIAS)
        img5C = ImageTk.PhotoImage(img5B)
        
        panel = tkinter.Label(self, image = img5C)
        panel.image = img5C
        panel.grid(row=24, column=2, rowspan=5)
        Label5 = tkinter.Label(self, text = "L=0.47, U=0.52, It=1")
        Label5.grid(row=30, column =2)
        
        
        img6A = Image.open(panel_temp_folder + 'panel 6.png')
        img6B = img6A.resize((100, 100), Image.ANTIALIAS)
        img6C = ImageTk.PhotoImage(img6B)
        
        panel = tkinter.Label(self, image = img6C)
        panel.image = img6C
        panel.grid(row=24, column=3, rowspan=5)
        Label6 = tkinter.Label(self, text = "L=0.47, U=0.54, It=1")
        Label6.grid(row=30, column =3)


        img7A = Image.open(panel_temp_folder + 'panel 7.png')
        img7B = img7A.resize((100, 100), Image.ANTIALIAS)
        img7C = ImageTk.PhotoImage(img7B)
        
        panel = tkinter.Label(self, image = img7C)
        panel.image = img7C
        panel.grid(row=31, column=1, rowspan=5)
        Label7 = tkinter.Label(self, text = "L=0.49, U=0.50, It=1")
        Label7.grid(row=36, column =1)
        
        
        img8A = Image.open(panel_temp_folder + 'panel 8.png')
        img8B = img8A.resize((100, 100), Image.ANTIALIAS)
        img8C = ImageTk.PhotoImage(img8B)
        
        panel = tkinter.Label(self, image = img8C)
        panel.image = img8C
        panel.grid(row=31, column=2, rowspan=5)
        Label8 = tkinter.Label(self, text = "L=0.49, U=0.52, It=1")
        Label8.grid(row=36, column =2)
        
        
        img9A = Image.open(panel_temp_folder + 'panel 9.png')
        img9B = img9A.resize((100, 100), Image.ANTIALIAS)
        img9C = ImageTk.PhotoImage(img9B)
        
        panel = tkinter.Label(self, image = img9C)
        panel.image = img9C
        panel.grid(row=31, column=3, rowspan=5)
        Label9 = tkinter.Label(self, text = "L=0.49, U=0.54, It=1")
        Label9.grid(row=36, column =3)
        


    def NextButton1(self):    
        #Get information from entry widgets and save as global variables
        testimage = str(self.Entry1.get())
        
        test_lower = float(self.Entry2.get())
        
        test_upper = float(self.Entry3.get())
        
        test_iterations = int(self.Entry4.get())
        
        #create a temporary file location to save the image as
        global temp_folder
        temp_folder = tempfile.mkdtemp()

        #  Import test image
        Test_Image = imageio.imread(str(testimage))
        
        #  Convert to grayscale
        Gray_Test_Image = rgb2gray(Test_Image)
        
        #Apply mask to image
        Mask_A = np.logical_or(Gray_Test_Image<test_lower, Gray_Test_Image>test_upper)      
        Mask_B = ndi.binary_dilation(Mask_A, iterations=test_iterations)
        Masked_Test= np.where(Mask_B, 0, 1)
        Filled_Masked_Test = ndi.morphology.binary_fill_holes(Masked_Test)
        #Save masked image as a png file
        plt.imsave(temp_folder + 'test.png', Filled_Masked_Test, cmap='gray')
                              
        ###  display masked image in the window
        ##  convert the image saved at the path name into a Tkinter compatible format
        ##  place the image in the window. To get it to be displayed and not garbage-collected, the second line of code keeps a reference to the image
        img6 = Image.open(temp_folder + 'test.png')
        img7 = img6.resize((250, 250), Image.ANTIALIAS)
        img8 = ImageTk.PhotoImage(img7)

        panel = tkinter.Label(self, image = img8)
        panel.image = img8
        panel.grid(row=0, column=6, rowspan=5)



#-----------------------------------------------------------------------------------------------------------------------------#
### What happens when the Analysis button is pressed is defined below. 
### It is a process of entering experiment details, importing and analysing the images, saving the analysed images, analysing the data and saving the result

# Create frame to open if ProgramButton is selected
class ExperimentInfo(tkinter.Frame):
    # First initialising self calls itself and master
    def __init__(self, master):
        ## reference the required global variables
        global Exptdate
        global Cellline
        global O2conc
        global Raddose
        global Drugdose
        global Seedingdensity
        global Timetoscratch
        global imageperwell
        global Interval
        global Title
        global imagepath
        global savepath
        ## initialise the frame)
        tkinter.Frame.__init__(self, master)
        #  Window is named
        self.master.title("Cell Migration and Invasion Analysis Program - Data Analysis")
        #  Windows size is specified (widthxheight)
        #  Where new window opens is also specificed (+x+y)
        self.master.geometry('500x500+400+200')
        #  Create variable for frame
        self.var1 = tkinter.IntVar()
    
        ###  First window asks for user to input the relevant information about their experiment
        ###  This will then be saved for output to text file with all info on
        ###  These are saved as global variables so will be using the global() function
        ###  User will then have button to press to confirm these changes
    
        ###  Create the labels and entry boxes for the user to input their information
        ###  Labels are numbered sequentially
        ###  Interactive widgets are numbered based on relevant label
        ###  Each widget has relative information added if needed:
            ###  Named, labelled, text information, command if selected
            ###  Grid defines where the widget is placed in relation to the rest of the widgets
        ## Create title text for the window
        self.Label1 = tkinter.Label(self, text = "Enter Experiment Parameters", bg = 'white', font=('Calibri Bold', 16))
        self.Label1.grid(row=0, column =0, columnspan = 3)
               
        ##  Ask user when they started the experiment
        self.Label2 = tkinter.Label(self, text = "Experiment start date:")
        self.Label2.grid(row=5)
        self.Entry2 = tkinter.Entry(self)
        self.Entry2.grid(row = 5, column=2)
        ##  To have a value automatically inserted into the entry box use insert and then the string wanted from the global variable
        self.Entry2.insert(0, str(Exptdate))
        
        ##  Then ask what cell line they used
        self.Label3 = tkinter.Label(self, text = "Cell line:")
        self.Label3.grid(row=9, column =0)
        self.Entry3 = tkinter.Entry(self)
        self.Entry3.grid(row=9, column =2)
        self.Entry3.insert(0, str(Cellline))
        
        ## Then ask what experimental conditions they used - oxygen concentration
        self.Label4 = tkinter.Label(self, text = "Oxygen Concentration (%):")
        self.Label4.grid(row=12, column =0)
        self.Entry4 = tkinter.Entry(self)
        self.Entry4.grid(row=12, column =2)
        self.Entry4.insert(0, str(O2conc))

        ## Then ask what experimental conditions they used - radiation treatment
        self.Label5 = tkinter.Label(self, text = "Radiation Dose (Gy):")
        self.Label5.grid(row=15, column =0)
        self.Entry5 = tkinter.Entry(self)
        self.Entry5.grid(row=15, column =2)
        self.Entry5.insert(0, str(Raddose))
        
        ##Then ask what experimental conditions they used - drug treatment
        self.Label6 = tkinter.Label(self, text = "Drug Concentration (uM):")
        self.Label6.grid(row=18, column =0)
        self.Entry6 = tkinter.Entry(self)
        self.Entry6.grid(row=18, column =2)
        self.Entry6.insert(0, str(Drugdose))
        
        #Then ask what experimental conditions they used - seeding density
        self.Label7 = tkinter.Label(self, text = "Seeding Density (cells/well):")
        self.Label7.grid(row=21, column =0)
        self.Entry7 = tkinter.Entry(self)
        self.Entry7.grid(row=21, column =2)
        self.Entry7.insert(0, str(Seedingdensity))
        
        #Then ask what experimental conditions they used - timings
        self.Label8 = tkinter.Label(self, text = "Time between treatment and scratch:")
        self.Label8.grid(row=24, column =0)
        self.Entry8 = tkinter.Entry(self)
        self.Entry8.grid(row=24, column =2)
        self.Entry8.insert(0, str(Timetoscratch))
        
        ###  Then create entry form for the time difference between each image
        self.Label9 = tkinter.Label(self, text = "Time between images:")
        self.Label9.grid(row=27, column =0)
        self.Entry9 = tkinter.Entry(self)
        self.Entry9.grid(row=27, column =2)
        self.Entry9.insert(0, str(Interval))
        self.Label91 = tkinter.Label(self, text = "hrs")    
        
        ###  Then entry forms for how the files are to be named
        self.Label10 = tkinter.Label(self, text = "Analysed Images Name:")
        self.Label10.grid(row=30, column =0)
        self.Entry10 = tkinter.Entry(self)
        self.Entry10.grid(row=30, column =2)
        self.Entry10.insert(0, str(Title))
        ##  Save the information as a StringVar() from tkinter so that it automatically updates when value is changed
        self.master.filepathnametxt = tkinter.StringVar()
        
        ###  Entry form for the location to save the files
        ###  Using in-built function to browse files for this info
        ###  Creating a function to allow button to be pressed to browse directory
        self.Label11 = tkinter.Label(self, text = "Raw Image Location:")
        self.Label11.grid(row=33, column =0)
        # create a string text variable that is used
        self.imagepathtxt = tkinter.StringVar()
        ##  Text in entry is the filepath chosen by the user when selecting the browse button
        self.Entry11 = tkinter.Entry(self, textvariable=self.imagepathtxt)
        self.Entry11.grid(row=33, column =2, columnspan=2)
        self.Entry11.insert(0, str(imagepath))
        #  Command is the function that initialises browsing file path locations when selected
        self.Button11 = tkinter.Button(self, text = "Browse", command = lambda: self.BrowseImage())
        self.Button11.grid(row = 33, column=3)
        
        ###  Entry form for the location of where the files are located
        self.Label12 = tkinter.Label(self, text = "Analysed File Destination:")
        self.Label12.grid(row=36, column =0)
        self.savepathtxt = tkinter.StringVar()
        self.Entry12 = tkinter.Entry(self, textvariable=self.savepathtxt)
        self.Entry12.grid(row=36, column =2, columnspan=3)
        self.Entry12.insert(0, str(savepath))
        #  Command is the function that initialises browsing file path locations when selected
        self.Button12 = tkinter.Button(self, text = "Browse", command = lambda: self.SaveImageLocation())
        self.Button12.grid(row = 36, column=5)        
        
        ##  Finally we have a submit button created
        ### This will then save the relevant input information as global variables for use in the next step of running the code
        self.Button13 = tkinter.Button(self, text = "Next", command=lambda: self.NextButton1())
        self.Button13.grid(row=39, column = 3, pady = 30, sticky = 'w')
        
        #Create a new button that will go on all frames that have it go back to previous frame if user wants
        self.BackButton = tkinter.Button(self, text = "Back", command=lambda: master.switch_frame(MainPage))
        self.BackButton.grid(row=39, column = 0, pady = 10, sticky = 'w')
        
        ##  Create the function to allow browsing of file location
    def BrowseImage(self):
        imagepath = self.GetImages = tkinter.filedialog.askdirectory(initialdir = "/",title = "Select location of RAW images")
        # Have the label on the screen change to reflect chosen destination
        self.imagepathtxt.set(imagepath)

    ##  Create function to get location to save processed images to
    def SaveImageLocation(self):
        savepath = self.SaveImages = tkinter.filedialog.askdirectory(initialdir = "/",title = "Select location for ANALYSED images")
        #Have the label on the screen change to reflect chosen destination
        self.savepathtxt.set(savepath)
    
        
    ###  Create the function that runs when the submit button is pressed to submit information
    ###  This stores the relevant information as global variables
    ###  Global variables are used so that any frame can call them
    ###  May store them in master would work as well but global will be used for now
    ### Now have moved up to store in the master so have removed the global definitions here
    ## Define what happens when you press 'Next'
    def NextButton1(self):
        #Get information from entry widgets and save as global variables
        global Exptdate
        global Cellline
        global O2conc
        global Raddose
        global Drugdose
        global Seedingdensity
        global Timetoscratch
        global imageperwell
        global Interval
        global Title
        global imagepath
        global savepath
        
        Exptdate = self.Entry2.get()
        
        Cellline = self.Entry3.get()
        
        O2conc = self.Entry4.get()
        
        Raddose = self.Entry5.get()
        
        Drugdose = self.Entry6.get()
        
        Seedingdensity = self.Entry7.get()
        
        Timetoscratch = self.Entry8.get()
      
        Interval = float(self.Entry9.get())
        
        Title = self.Entry10.get()
        
        imagepath = self.Entry11.get()
        
        savepath = self.Entry12.get()
        
        ##  Finally Switch to the MigrationRun frame to double check info before it runs the program    
        self.master.switch_frame(MigrationRun)

#---------------------------------------------------------------------------------------------------------------------------------------#

###  Create the frame which will run the analysis program and output the raw data

##  Class is created for the frame
class MigrationRun (tkinter.Frame):
    ##  When initialising title is added and all widgets are made for tkinter
    def __init__(self, master):
        ##  define global variables for referencing
        global Lower_Bound
        global Upper_Bound
        global Iterations
        tkinter.Frame.__init__(self,master)
        self.master.title("Cell Migration and Invasion Analysis Program - Data Analysis")
        
        #  Windows size is specified (widthxheight)
        #  Where new window opens is also specificed (+x+y)
        self.master.geometry('700x300+300+200')
        
        #  Title to show ask user to adjust mask parameters
        ### Is there a way to have a library of previously used parameters? Or to save the parameters from the determine
        ### mask parameters input window so this autofills or has a selection? 
        self.Label9 = tkinter.Label(self, text = "Adjust mask parameters as required", bg = 'white', font=('Calibri Bold', 12))
        self.Label9.grid(row=17, column =0, columnspan = 3, pady = 10)
                
        ##  Input created to allow lower boundary to be adjusted
        self.Label10 = tkinter.Label(self, text = "Lower_Boundary")
        self.Label10.grid(row=18, column =0)
        #  Create a string text variable that is used
        self.Lower_Boundarytxt = tkinter.StringVar()
        self.Lower_Boundarytxt.set(Lower_Bound)
        self.Entry10 = tkinter.Entry(self, textvariable=self.Lower_Boundarytxt)
        self.Entry10.grid(row=18, column =1)
        
        ##  Input created to allow upper boundary to be adjusted
        self.Label11 = tkinter.Label(self, text = "Upper_Boundary")
        self.Label11.grid(row=19, column =0)
        #  create a string text variable that is used
        self.Upper_Boundarytxt = tkinter.StringVar()
        self.Upper_Boundarytxt.set(Upper_Bound)
        self.Entry11 = tkinter.Entry(self, textvariable=self.Upper_Boundarytxt)
        self.Entry11.grid(row=19, column =1)
        
        #  Input created to allow number of iterations to be adjusted
        self.Label12 = tkinter.Label(self, text = "Iterations")
        self.Label12.grid(row=20, column =0)
        #  create a string text variable that is used
        self.Iterationstxt = tkinter.StringVar()
        self.Iterationstxt.set(Iterations)
        self.Entry12 = tkinter.Entry(self, textvariable=self.Iterationstxt)
        self.Entry12.grid(row=20, column =1)
        
        ##  Finally we have a submit button created
        ###  This will then save the relevant input information as global variables for use in the next step of running the code
        ##  Command for the button then runs the code to calculate cell migration values and output masked images and raw data
        self.Button13 = tkinter.Button(self, text = "Confirm", command=lambda: self.ConfirmInfo())
        self.Button13.grid(row=22, column = 1, pady = 30, sticky = 'w')
        
        ##  Create a new button that will go on all frames that have it go back to previous frame if user wants
        self.BackButton = tkinter.Button(self, text = "Back", command=lambda: master.switch_frame(ExperimentInfo))
        self.BackButton.grid(row=22, column = 0, pady = 10, sticky = 'w')
        
###  This function will run the analysis program as it currently is
##  Code used below is a mixture of original RCM code and new NIM code

    def ConfirmInfo (self):
        ##  define global variables
        global Lower_Bound
        global Upper_Bound
        global Iterations
        ##  Fetch global variables of bounds and iterations to update from MigrationeRun frame
        ### Because these are now in the master, this bit of code was deleted
      
        ##  Get the values input by user or default if unchanged
        Lower_Bound = float(self.Entry10.get())
        Upper_Bound = float(self.Entry11.get())
        Iterations = int(self.Entry12.get())
        
        ##  Create a list of all the image file names for that folder. Then sort the list alphabetically
        Image_List = os.listdir(imagepath)
        Sorted_Image_List = sorted(Image_List, key=str.lower)
        
        ###  For use in naming them we then have the length of the images counted
        ##  Count the number of images that are present
        self.Number_of_Images = len(Sorted_Image_List)
        
        #  Create an empty list to store the file names
        File_Names = []
        
        #  For loop to make a list of the file names you want.
        ## We start a loop to go through z (the image it is processing) until it has done all images
        ##  Loop goes through all images but the list of file names is saved according to the well and time in well

        for z in range(1,(self.Number_of_Images+1)):
                temp1 = "_" + str(z * Interval) + "_Hour"
                File_Names.append(temp1)
                
        ##  Converted Sorted_Image_List to a list of the numpy arrays
        ##  The range needs to be changed to the total number of images (the index starts at 0)
        for y in range(self.Number_of_Images):
            ###  Due to way tkinter retrieves file directory final / is not included in file name when saving directory
            ###  Using tkinter.askopenfile here would replace the earlier location asking
            ###  For now will fix with insertion of extra backslash add (as \\)
            Sorted_Image_List[y]= imageio.imread(str(imagepath)+ "\\" + str(Sorted_Image_List[y]))
            
###  Original RCM code Starts Here

        ##  Merge the two lists together into a dictionary by zipping two lists together.
        ##  The File-Name list is used as the key and the images from Sorted_Image_List are the values. Both lists are alphabetical and so they should map directly to each other
        Original_Images = dict(zip(File_Names, Sorted_Image_List))

        ##  Convert images in Original_Images dictionary to grayscale using the rgb2gray function.
        ##  Create an empty dictionary to store the grayscale images in
        Gray_Images = {}
        #  Use a for loop to iterate over the dictionary and apply the function to the values i.e. the images
        for key, value in Original_Images.items():
            Gray_Images[key] = rgb2gray(value)
        ##  Define the apply_mask function, which creates a mask and applies it to the image, to output a yellow and purple image for analysis
        def apply_mask(image):
            ##  Use the upper and lower bounds chosen by the user to filter the image
            ##  This creates Mask_1 which is a numpy array of Boolean values where True (yellow) are pixels outside this range and False (purple) are pixels inside this range
            Mask_1 = np.logical_or(image<Lower_Bound, image>Upper_Bound)
            ##  Use the binary dilation function using the number of iterations chosen by the user on the first mask created
            ##  This fills in the gaps in the image making the cell layer and gap less spotty
            Mask_2 = ndi.binary_dilation(Mask_1, iterations=Iterations)
            ###  The output value is the gap dimensions, so need to create an image where the cell pixels have a value of 0 and the gap pixels have a value of 1
            ##  Create Masked_Image_1 and apply Mask_2. Where mask 2 is true these are cell containing pixels which are given the value 0 
            ##  Where Mask_2 is false, this is the gap and it is given the value 1.
            Masked_Image_1 = np.where(Mask_2, 0, 1)
            ##  Masked_Image_1 contains a spotty gap, so use the binary_fill_holes function to reduce these and give clearly defined gap and cell regions
            Masked_Image_2 = ndi.morphology.binary_fill_holes(Masked_Image_1)
            ##  The final output of the function is Masked_Image_2
            return(Masked_Image_2)

        # Create a new empty dictionary to add the masked images to
        Masked_Images = {}
        #  Use a for loop on the Gray-Images dictionary and use the apply_mask function on each image
        #  Add the masked images to the dictionary, keeping the same key in both dictionaries.
        for key, value in Gray_Images.items():
            Masked_Images[key] = apply_mask(value)
       
        ###  Measure gap width along each row for each image. Currently create empty dictionaries for each time stamp, iterate through the rows of the image to get a 
        ###  total and multiply this by the pixel width and add these to the dictionary. 
        #  Create empty dataframe for raw data as Df_1
        Df_1 =  pd.DataFrame()
        ##  To find image dimensions to get the number of rows used for transferring image information from dictionary to data frame
        ##  To do this will call any image from the list of images as all should have the same dimensions
        ##  Key in dictionary is File_Names, so first step is to save first file name from list File_Names as variable DimVar_1
        DimVar1=str(File_Names[0])
        #  Then use the file name extracted to get the corresponding numpy array of the image from the dictionary
        # It is saved as DimVar2
        DimVar2=Gray_Images.get(DimVar1)
        #  Then use .shape function on numpy array to determine its dimensions
        #  .shape[0] is used to get the row length
        #  This is saved as DimVar3
        DimVar3=DimVar2.shape[0]
        #  This is now a single integer that is the number of pixels high each image is
        # This is then used to determine the maximum value for the range
        #  Python excludes last number in range so DimVar3+1 is used
        Df_1['Row'] = range(1,DimVar3+1)

        #  Iterate through images using a nested for loop
        #  In the outer for loop, the key is the image name with the timepoint, and the value is the masked image
        for key, value in Masked_Images.items():
            # create an empty, temporary dictionary
            temp = {}
            ##  Iterate through the images in the Masked_Image dictionary
            ##  In the inner for loop, the index is the row number in the image, which is a numpy array. The row is the row of pixels in the numpy array
            #  The starting index is set at 1, so that this can be mapped to the rows in Df_1, as set above
            for index,row in enumerate(value, start=1):
                #  Use the .update function to add a new key,value pair
                #  The index is automatically generated starting from 1 as set in the for loop. This is used as the key
                #  The np.sum function is used across each row in the numpy array to add up the total number of gap pixels (which were set with a value of 1)
                #  The pixel_width variable is used to convert this from a pixel distance to a measured distance. This is the associated value in the temp dict
                temp.update({index : (np.sum(row)*pixel_width)})
                ##  The temp dict is mapped into Df_1 as a new column. The column heading is the image name, i.e. the key in the Masked_Images dictionary
                #  The key in the temp dictionary is matched to the 'Row' column values already in the dictionary using the .map function
                Df_1[str(key)] = Df_1['Row'].map(temp)

        #  Save dataframe in file as raw data
        Df_1.to_csv(str(savepath)+"\\"+"Raw Data_" + str(Title) + ".csv")
        
        #  Save masked images, which are Numpy arrays, as image files
        # add each image path to a list which can then be converted into a GIF. So also create an empty list
        image_path = []
        for key, value in Masked_Images.items():
            plt.imsave(str(savepath) +"\\" + str(Title) + str(key) + '.png', value, cmap='gray')
            image_path.append(str(savepath + "\\" + str(Title) + str(key) + '.png'))
        
        image_list = []
        for file_name in image_path:
            image_list.append(imageio.imread(file_name))
        
        image_list
        
        imageio.mimwrite(str(savepath) + "\\" + str(Title) + 'gif.gif', image_list)
    
###  Once the gap width is measured, the average gap width is plotted against time
###  from that the user selects the timepoints between which the gap closure is linear
###  using those times, a trendline is fitted and the slope of the trendline and the R^2 value is calculated

        ##  Create a dataframe with time as the first column and the average gap width as the second column
        #  Create a second dataframe to contain the output data
        Df_2 = pd.DataFrame()
        #  Add column calculating the average gap width by averaging the values in Df_1
        Df_2['Average Gap Width'] = Df_1.mean()
        #  Add column calculating the standard error for the average gap width
        Df_2['SEM Gap Width'] = Df_1.sem()
        # Add column calculating the total gap area
        Df_2['Total Gap Area'] = Df_1.sum()
        #  Add column with the time in hours, as an integer
        Df_2.insert(0, 'time (h)', range(0*int(Interval),(len(Df_2))*int(Interval), int(Interval)))
        #  Remove the first row, called 'Row'by creating a new dataframe selecting all rows after 1
        Df_3 = Df_2.iloc [1:,]
        # Plot a scatter graph of time vs gap width
        Df_3.plot.scatter(x='time (h)', y='Average Gap Width',marker='x')
        # change x axis to have a tick every hour
        plt.xticks(np.arange(0*int(Interval), len(Df_2)*int(Interval), step = int(Interval)))
        # turn on the grid
        plt.grid()        
        #  plot error bars in red - because they are likely to be very small, might not be visible
        plt.errorbar(Df_3['time (h)'],Df_3['Average Gap Width'],yerr=Df_3['SEM Gap Width'], linestyle='None',ecolor='r')
        #  save graph as a gif file because that makes it easier to import back into the interface
        plt.savefig(str(savepath) +"\\" + str(Title) + 'Plot.png')
        ###  because i need to refer back to Df_3 later on, save as a csv file so it can be imported again later
        Df_3.to_csv(str(savepath)+"\\"+"Plotted Data_" + str(Title) + ".csv")
        #  Switch to the next frame for displaying and saving parameters 
        self.master.switch_frame(DataAnalysisParameters)  
        
       
### Want a new frame to display the graph in once the image analysis is complete
### What about adding in a image check? So can the masked images be saved as a gif then imported and viewed to check it looks good?

class DataAnalysisParameters(tkinter.Frame):
    #  First initialising self calls itself and master
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        #Window is named
        self.master.title("Cell Migration and Invasion Analysis Program - Data Analysis")
        #  Windows size is specified (widthxheight)
        #  Where new window opens is also specificed (+x+y)
        self.master.geometry('1000x500+100+100')
        #  Create variable for frame
        self.var1 = tkinter.IntVar()      
        #  Create the labels and entry boxes detailing the process
        #  Labels are numbered sequentially
        #  Interactive widgets are numbered based on relevant label
        #  Each widget has relative information added if needed:
            #  Named, labelled, text information, command if selected
            #  Grid defines where the widget is placed in relation to the rest of the widgets
        self.Label2 = tkinter.Label(self, text = "Select Linear Portion of Graph", bg = 'white', font=('Calibri Bold', 12))
        self.Label2.grid(row=0, column =0, columnspan = 3)
        #  Ask user the starting time point of the linear section
        self.Label3 = tkinter.Label(self, text = "Start Time:")
        self.Label3.grid(row=5)
        self.Entry3 = tkinter.Entry(self)
        self.Entry3.grid(row = 5, column=1)
        #  To have a value automatically inserted into the entry box use insert and then the string wanted from the global variable
        self.Entry3.insert(0, str(LinearStartTime))
        #  Then ask the finishing time point of the linear section
        self.Label4 = tkinter.Label(self, text = "End Time:")
        self.Label4.grid(row=9, column =0)
        self.Entry4 = tkinter.Entry(self)
        self.Entry4.grid(row=9, column =1)
        self.Entry4.insert(0, str(LinearEndTime))
        
        #  Title to remind user to check gif/images if the graph isn't correct
        self.Label9 = tkinter.Label(self, text = "If graph is not as expected, check masked images and GIF in the Save Folder", bg = 'white', font=('Calibri Bold', 12))
        self.Label9.grid(row=30, column =0, columnspan = 3, pady = 10)
                
               
        ### Need to get the saved plot file to be displayed in the GUI
        ## define the path name for the saved plot as an image file - created earlier in the code
        path2 = str(savepath) +"\\" + str(Title) + 'Plot.png'
        ##  convert the image saved at the path name into a Tkinter compatible format
        img2 = ImageTk.PhotoImage(Image.open(path2))
        ##  place the image in the window. To get it to be displayed and not garbage-collected, the second line of code keeps a reference to the image
        panel = tkinter.Label(self, image = img2)
        panel.image = img2
        panel.grid(row=13, column=0, rowspan=5, columnspan=5)

        #  Finally we have a submit button created
        #  This will then save the relevant input information as global variables for use in the next step of running the code
        self.Button9 = tkinter.Button(self, text = "Next", command=lambda: self.SubmitInfo())
        self.Button9.grid(row=18, column = 1, pady = 30, sticky = 'w')
        
        #Create a new button that will go on all frames that have it go back to previous frame if user wants
        #But may want to remove the back button for this step, because going back shouldn't be necessary
        self.BackButton = tkinter.Button(self, text = "Back", command=lambda: master.switch_frame(MainPage))
        self.BackButton.grid(row=18, column = 0, pady = 10, sticky = 'w')
     
    ##  Create the function that runs when the submit button is pressed to submit information
    ##  This stores the relevant information as global variables
    ##  Global variables are used so that any frame can call them
    ##  First definition is named and given variables
    def SubmitInfo(self):
        #  First have global variables potentially used called for later
        global LinearStartTime
        global LinearEndTime
        global slope
        global intercept
        global r_value
        global r_squared
        global gapclosurerate
        #  Get information from entry widgets and save as global variables
        LinearStartTime = self.Entry3.get()
        
        LinearEndTime = self.Entry4.get()
        
        ##  Using these timings, create new dataframe which will only have the linear portion of the graph in it
        ### need to import the saved csv file of the plotted data
        Df_4 = pd.read_csv(str(savepath)+"\\"+"Plotted Data_" + str(Title) + ".csv")
        ##  Create a second dataframe which only contains the linear portion of the graph and without the SEM column
        ##  Do this using slices
        ###  Note, the first bit of a slice is included while the last bit is excluded
        ###  Also, the row indexing starts at 0
        ##  So need to start the slice at StartTime-1 and end at EndTime
        Df_5 = Df_4.iloc[int(LinearStartTime)-1:int(LinearEndTime), 1:3]
        ##  calculate the slope, intercept etc. using the scipy linregress function
        slope, intercept, r_value, p_value, std_err = stats.linregress(Df_5['time (h)'], Df_5['Average Gap Width'])
        #  calculate R squared value by squaring the r value output
        r_squared = r_value**2
        #calculate gap closure rate by multiplying by -1
        gapclosurerate = slope*-1
        #Finally Switch to the next frame for displaying and saving parameters 
        self.master.switch_frame(Results)   
#-------------------------------------------------------------------------------------------------------------------#
     
class Results(tkinter.Frame):
    #  First initialising self calls itself and master
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        
        #  Window is named
        self.master.title("Cell Migration and Invasion Analysis Program")
        
        #  Windows size is specified (widthxheight)
        #  Where new window opens is also specificed (+x+y)
        self.master.geometry('500x200+100+100')
        
        #  Create variable for frame
        self.var1 = tkinter.IntVar()
    
        ###  this window needs to display the results of the analysis
        ###  The only button option will be 'Save Results and Return to Home Screen'
        ###  Clicking that will create the parameters file with all the global variables
        ###  It will also create an excel sheet that has the linear regression parameters saved in cell A1
        ###  This file can be used with the data extraction package to average all wells (In theory)
        ###  Need to decide if want to combine that with this package
                
        ##  Create the labels and entry boxes detailing the process
        ##  Labels are numbered sequentially
        ##  Interactive widgets are numbered based on relevant label
        #  Each widget has relative information added if needed:
            #  Named, labelled, text information, command if selected
            #  Grid defines where the widget is placed in relation to the rest of the widgets

        
        ##  Give clsoure rate results
        self.Label8 = tkinter.Label(self, text = "Gap Closure Rate:")
        self.Label8.grid(row=12, column =0)
        self.Label8 = tkinter.Label(self, text= gapclosurerate)
        self.Label8.grid(row=12, column =1)
        
        ##  Detail R squared value
        self.Label9 = tkinter.Label(self, text = "R Squared:")
        self.Label9.grid(row=15, column =0)
        self.Label9 = tkinter.Label(self, text= r_squared)
        self.Label9.grid(row=15, column =1)

        
        ###  Finally we have a save and return to menu button
        ###  This will then save the information as a csv file and a text file
        ##  Then the program returns to the homescreen
        self.Button13 = tkinter.Button(self, text = "Save Changes and Return to Menu", command=lambda: self.SaveInfo())
        self.Button13.grid(row=22, column = 1, pady = 30, sticky = 'w')

    def SaveInfo (self): 
        ##  We then create a text file to save all of the parameters used during the analysis
        ##  First create a variable to call the text file
        ##  Open function is used to create it
        ##  File is saved in same place as other images and named according to preferred file name
        ##  Variable for text file is infofile
        infofile = open(str(savepath) +"\\" + str(Title)+"_parameters.txt", "w+")
        ##  We then opoen the text file and input the data we want
        ##  Have info for the experiment parameters first then analysis parameters
        ##  Left in bold is what is shown on right
        infofile.write(
                "               EXPERIMENT PARAMETERS:         \n"
                "EXPERIMENT START DATE:     " + str(Exptdate) + "\n"
                "CELL LINE:      " + str(Cellline) + "\n"
                "OXYGEN CONCENTRATION:     " + str(O2conc) + "\n"
                "RADIATION DOSE:          " + str(Raddose) + "\n"
                "DRUG DOSE:              " + str(Drugdose) + "\n"
                "SEEDING DENSITY:             " + str(Seedingdensity) + "\n"
                "TIME BETWEEN RADIATION AND SCRATCH:         " + str(Timetoscratch) + "\n"
                "\n"
                "\n"
                "\n"
                
                "               ANALYSIS PARAMETERS:         \n"
                "PROCESSED FILENAMES:     " + str(Title) + "\n"
                "DATE AND TIME OF ANALYSIS:      " + str(datetime.datetime.now()) + "\n"
                #well is parameter above used to save the number of wells it records while doing multiple wells
                #loop that saves this has it go to next well before finding out no images left
                #As such actual number of well is 1 below what is recorded
                "TOTAL WELLS:     " + str(well-1) + "\n"
                "IMAGES PER WELL:     " + str(imageperwell) + "\n"
                "TIME BETWEEN IMAGES:     " + str(Interval) + "\n"
                "UPPER BOUND:     " + str(Upper_Bound) + "\n"
                "LOWER BOUND:     " + str(Lower_Bound) + "\n"
                "ITERATIONS:     " + str(Iterations) + "\n"
                "PIXEL CONVERSION FACTOR:     " + str(pixel_width) + "\n"
                                "\n"
                "\n"
                "\n"
                
                "               RESULTS:         \n"
                "SLOPE START TIME:             " + str(LinearStartTime) + "\n"
                "SLOPE END TIME:               " + str(LinearEndTime) + "\n"
                "GAP CLOSURE RATE:             " + str(slope) + "\n"
                "R SQUARED VALUE:              " + str(r_squared) + "\n"
                )
        
        ##  Want to create an excel document with the gap closure rate 
        with open(str(savepath)+"\\"+"Gap Closure Rate_" + str(Title) + ".csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(str(slope))

        
        ## Switch to the main menu frame after it runs the program   
        self.master.switch_frame(MainPage)

## Finally we run the final code that creates the first window when code is run
   
#  Following code is used to identify if it is imported as a module or not
#  Not used in this code but may be useful if run as a module elsewhere
if __name__ == '__main__':
    #set variable to be used for creting mainloop as start page
    app = CellMigrationApp()
    
    #Finally the mainloop is started with the app window
    app.mainloop()