import os
from subprocess import Popen, CREATE_NEW_CONSOLE
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


ffmpeg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"ffmpeg","ffmpeg.exe")


def get_raw_videos(searchPath):
    fileList = []
    print("Finding raw videos")
    for dirpath, dirnames, filenames in os.walk(searchPath):
        for filename in filenames:
            foundFile = os.path.join(dirpath, filename)
            if foundFile.endswith('.webm'):
                fileList.append(foundFile)
                continue
    print("Found",len(fileList),"raw videos")
    return fileList


def directory_gui():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("","Select recording folder")
    searchDir = filedialog.askdirectory()
    root.update()
    return searchDir


def recode_videos(fileList):
    recode_list = []
    for rawVidPath in fileList:
        outDir = os.path.dirname(os.path.dirname(rawVidPath))
        outFile = os.path.splitext(os.path.basename(rawVidPath))[0]+".mp4"
        outFilePath = os.path.join(outDir, outFile)

        if(os.path.exists(outFilePath)):
            answer = messagebox.askquestion ("Overwrite?", "{0} already exists, overwrite?".format(outFile), icon = 'warning')
            if(answer == "yes"):
                recode_list.append([rawVidPath, outFilePath, outFile, True])
        else:
            recode_list.append([rawVidPath, outFilePath, outFile, False])

    print(len(recode_list),"videos to process")
    for vid in recode_list:
        # danger zone
        inVidPath = vid[0]
        outVidPath = vid[1]
        outVidFile = vid[2]
        overwriteVid = vid[3]

        number_left = len(recode_list) - recode_list.index(vid)
        print("Processing",outVidFile,"-",number_left,"left")
        ffmpeg_cmd = '{0} -i {1} {2}'
        if(overwriteVid):
            os.remove(outVidPath)
        subProc = Popen(ffmpeg_cmd.format(ffmpeg_path, inVidPath, outVidPath), shell=False, bufsize=0, creationflags=CREATE_NEW_CONSOLE)
    return


if __name__ == '__main__':
    start_path = directory_gui()
    file_list = get_raw_videos(start_path)
    recode_videos(file_list)
