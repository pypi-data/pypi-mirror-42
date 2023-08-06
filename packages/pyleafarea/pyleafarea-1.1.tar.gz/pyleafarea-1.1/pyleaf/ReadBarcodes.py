import os
import subprocess
from pyzbar.pyzbar import decode
from PIL import Image
import shutil
import datetime
import cv2
import pandas as pd

suffix = '.JPG'
prefix = 'IMG_'
separator = '-'

official_plots = pd.read_csv("C:\\Users\\Joseph Crawford\\OneDrive\\GWAS d13C\\SF-BAP-2017 Entries\\BAP_entries.csv")

mydir = 'E:\\100CANON\\'

cleandir = 'E:\\Sorghum Named Originals\\'

inspectdir = 'E:\\Misread\\'

#Track the Successful Reads
success_bcode_scans_plots = []
success_bcode_scans_ss = []
timestamps_of_files = []
unique_names = []

def Convert_Barcode_Move_File(barcodedata):
    if barcodedata == []:
        return
    barcodedata = str(barcodedata)
    barcodedata = barcodedata.split('\'')[1]
    barcodedata_plot = barcodedata[0:13]
    print(barcodedata)
    success_bcode_scans_plots.append(barcodedata_plot)
    success_bcode_scans_ss.append(barcodedata)
    # print(success_bcode_scans_plots)
    # print(success_bcode_scans_ss)
    timestamp = (os.path.getmtime(mydir + filename))
    timestamps_of_files.append(timestamp)
    # print(timestamps_of_files)
    newname = str(barcodedata + "_" + filename)
    unique_names.append(newname)
    shutil.copy2(mydir + filename, cleandir + newname)


for filename in os.listdir(mydir):
    print(filename)
    image = cv2.imread(mydir+filename)
    height, width = image.shape[:2]
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(grey,(5,5),0)
    ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    barcodedata = decode(th3)
    Convert_Barcode_Move_File(barcodedata)
    if barcodedata == []:
        # Otsu's thresholding
        ret2, th2 = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        barcodedata = decode(th2)
        Convert_Barcode_Move_File(barcodedata)
        if barcodedata == []:
            # Threshing on greyscale image
            thresh2 = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                            cv2.THRESH_BINARY, 11, 2)
            barcodedata = decode(thresh2)
            Convert_Barcode_Move_File(barcodedata)

            if barcodedata == []:
                image = cv2.imread(mydir + filename)
                height, width = image.shape[:2]  # gets it into 8bpp for python
                # 8 bpp by considering just the blue channel
                barcodedata = decode((image[:, :, 0].astype('uint8').tobytes(), width, height))
                Convert_Barcode_Move_File(barcodedata)
                if barcodedata == []:
                    shutil.copy2(mydir + filename, inspectdir + filename)

my_results = pd.DataFrame(
	{'plot':success_bcode_scans_plots,
	 'subsample': success_bcode_scans_ss,
	 'timestamp': timestamps_of_files,
     'unique_name': unique_names})
my_results.to_csv('sampleresults_test.csv')

mission_accomp = list(set(my_results.loc[:,'plot']))
official_plot_list = official_plots['PlotID'].tolist()
search_and_rescue = list([x for x in mission_accomp if x not in official_plot_list])  #Generates a list of the envelope packets that did not get at least 1 from the plot
search_and_rescue_df = pd.DataFrame({'PlotID': search_and_rescue})                    #The plots that don't have any successful reads at all should go to
search_and_rescue_df.to_csv('search_and_rescue_df_test.csv')                               #HandInspect folder. For plots with a few missing then deal with diff

