import errno
import numpy as np
import os
import argparse
from pypcd import pypcd
import csv
from tqdm import tqdm
import tkinter as tk # Graphic User Interface Programming
from tkinter import filedialog # GUI File Selection

def convert_pcd2bin():

    global original_file_path
    global save2path
    global top_bar
    top_bar.destroy()


    ## Add parser
    parser = argparse.ArgumentParser(description="Convert .pcd to .bin")
    parser.add_argument(
        "--pcd_path",
        help=".pcd file path.",
        type=str,
        default=original_file_path
    )
    parser.add_argument(
        "--bin_path",
        help=".bin file path.",
        type=str,
        default=save2path
    )
    parser.add_argument(
        "--file_name",
        help="File name.",
        type=str,
        default=""
    )
    args = parser.parse_args()

    ## Find all pcd files
    pcd_files = []
    for (path, dir, files) in os.walk(args.pcd_path):
        for filename in files:
            # print(filename)
            ext = os.path.splitext(filename)[-1]
            if ext == '.pcd':
                pcd_files.append(path + "/" + filename)

    ## Sort pcd files by file name
    pcd_files.sort()   
    print("Finish to load point clouds!")

    ## Make bin_path directory
    try:
        if not (os.path.isdir(args.bin_path)):
            os.makedirs(os.path.join(args.bin_path))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print ("Failed to create directory!!!!!")
            raise

    ## Generate csv meta file
    csv_file_path = os.path.join(args.bin_path, "meta.csv")
    csv_file = open(csv_file_path, "w")
    meta_file = csv.writer(
        csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    ## Write csv meta file header
    meta_file.writerow(
        [
            "pcd file name",
            "bin file name",
        ]
    )
    print("Finish to generate csv meta file")

    ## Converting Process
    print("Converting Start!")
    seq = 0
    for pcd_file in tqdm(pcd_files):
        ## Get pcd file
        pc = pypcd.PointCloud.from_path(pcd_file)

        ## Generate bin file name
        bin_file_name = "{}{:05d}.bin".format(args.file_name, seq)
        bin_file_path = os.path.join(args.bin_path, bin_file_name)
        
        ## Get data from pcd (x, y, z, intensity, ring, time)
        np_x = (np.array(pc.pc_data['x'], dtype=np.float32)).astype(np.float32)
        np_y = (np.array(pc.pc_data['y'], dtype=np.float32)).astype(np.float32)
        np_z = (np.array(pc.pc_data['z'], dtype=np.float32)).astype(np.float32)
        np_i = (np.array(pc.pc_data['intensity'], dtype=np.float32)).astype(np.float32)/256

        ## Stack all data    
        points_32 = np.transpose(np.vstack((np_x, np_y, np_z, np_i)))

        ## Save bin file                                    
        points_32.tofile(bin_file_path)

        ## Write csv meta file
        meta_file.writerow(
            [os.path.split(pcd_file)[-1], bin_file_name]
        )

        seq = seq + 1

# Browse PCD Files Directories
def getFileLoc():
    global original_file_path
    original_file_path = filedialog.askdirectory()
    original_file_path = original_file_path + "/"

# "Save to" BIN Files Directories
def save2dir():
    global save2path
    save2path = filedialog.askdirectory()
    save2path = save2path + "/"

# Confirm button
def confirm_button():
    global top_bar
    top_bar.destroy()

# PCD2BIN Converter GUI
def pcd2bin_GUI():
     # Top Bar Title
    global top_bar
    top_bar = tk.Tk()
    top_bar.title("UCSD Autonomous Vehicle Laboratory")                                                            # Title Name
    # Body
    converter_Canvas = tk.Canvas(top_bar, bg='RoyalBlue1', width = 650, height = 260, relief ='raised')            # Background Color and Body Size
    converter_Canvas.pack()
    title_Text = tk.Label(top_bar, text='PCD-to-BIN File Conversion Tool', bg = 'RoyalBlue1')                      # Body Title Text
    title_Text.config(font = ('aerial', 24, 'bold'))                                                               # Set a font type and font size.
    converter_Canvas.create_window(330, 60, window=title_Text)                                                     # Position of the title.
    
    browse_Button = tk.Button(text="      Browse For PCD File Directory      ", command = getFileLoc , bg = 'AntiqueWhite1', fg ='gray1', font = ('aerial', 12, 'bold') )
    converter_Canvas.create_window(330, 130, window=browse_Button)

    save_to_Button = tk.Button(text="      Save to Bin File Directory      ", command = save2dir , bg = 'AntiqueWhite1', fg ='gray1', font = ('aerial', 12, 'bold') )
    converter_Canvas.create_window(330, 180, window=save_to_Button)
    
    convert_Button = tk.Button(text="      Convert PCD to BIN      ", command = convert_pcd2bin , bg = 'AntiqueWhite1', fg ='gray1', font = ('aerial', 12, 'bold') )
    converter_Canvas.create_window(330, 230, window=convert_Button)
    
    top_bar.mainloop()

# Browse Bin Directory GUI
def bin_directory_GUI():
     # Top Bar Title
    global top_bar
    top_bar = tk.Tk()
    top_bar.title("UCSD Autonomous Vehicle Laboratory")                                                            # Title Name
    # Body
    converter_Canvas = tk.Canvas(top_bar, bg='RoyalBlue1', width = 650, height = 260, relief ='raised')            # Background Color and Body Size
    converter_Canvas.pack()
    title_Text = tk.Label(top_bar, text='BIN Files Directory Selection', bg = 'RoyalBlue1')                      # Body Title Text
    title_Text.config(font = ('aerial', 24, 'bold'))                                                               # Set a font type and font size.
    converter_Canvas.create_window(330, 60, window=title_Text)                                                     # Position of the title.

    save_to_Button = tk.Button(text="      Browse the Bin File Directory      ", command = save2dir , bg = 'AntiqueWhite1', fg ='gray1', font = ('aerial', 12, 'bold') )
    converter_Canvas.create_window(330, 180, window=save_to_Button)
    
    convert_Button = tk.Button(text="      Confirm      ", command = confirm_button , bg = 'AntiqueWhite1', fg ='gray1', font = ('aerial', 12, 'bold') )
    converter_Canvas.create_window(330, 230, window=convert_Button)
    
    top_bar.mainloop()

    
if __name__ == "__main__":
    
    pcd2bin_GUI()