from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory

from urllib import request
import os.path
import time


class Fisher(Frame):
    ''' 自定义一个窗口类，实现这个项目的主界面 '''

    WIDTH = 40 # width of input area
    HEIGHT = 10 # height of input area
    PATH_WIDTH = 42 # width of directory button
    BUTTON_WIDTH = 10 # width of download button
    BUTTON_HEIGHT = 1 # height of button
    FG_COLOR = "#376956"
    BG_COLOR = "#F2EFE6"
    BUTTON_COLOR = "#5E8579"
    FONT = "黑体 14"
    
    def __init__(self):
        Frame.__init__(self) # create a master window
        self.master.title("Fisher") # give it a title
        self.master.resizable(False, False)
        self.path = "Z:/" # saving directory
        self.__addText() # add an input area for user
        self.__addFileName() # add an input area for file name
        self.__addDirectory() # add a path button
        self.__addButton() # add a download button
        self.__putWindowInCenter()

    def __addText(self):
        default = "Put your url here..."
        def mouseIn(event):
            userInput = self.text.get("0.0", "end").strip("\n")
            
            #if userInput == default:
            self.text.delete("0.0", "end")
            self.text.unbind("<Enter>")
            self.text.bind("<Leave>", mouseOut)
        def mouseOut(event):
            userInput = self.text.get("0.0", "end").strip("\n")

            # if True, do something...
            if userInput == "":
                self.text.insert("0.0", default)
                self.text.unbind("<Leave>")
                self.text.bind("<Enter>", mouseIn)
            
        self.text = Text(self.master)
        self.text.insert("0.0", default)
        
        # set size of input area
        self.text.configure(width=Fisher.WIDTH, height=Fisher.HEIGHT)
        
        # set color of input area
        self.text.configure(bg=Fisher.BG_COLOR, font=Fisher.FONT)
        self.text.configure(fg=Fisher.FG_COLOR)

        self.text.bind("<Enter>", mouseIn)
        self.text.pack()

    def __addFileName(self):
        self.filetext = Text(self.master)
        self.filetext.insert("0.0", "singer - song.mp3")
        
        # set size of input area
        self.filetext.configure(width=Fisher.WIDTH, height=1)
        
        # set color of input area
        self.filetext.configure(bg=Fisher.BG_COLOR, font=Fisher.FONT)
        self.filetext.configure(fg=Fisher.FG_COLOR)

        self.filetext.pack()
        
    def __addDirectory(self):
        def updatePath(event):
            pa = askdirectory() # ask for a saving directory
            if pa != "": # for safety
                if pa[-1] != "/": # "D:/" is ok
                    pa += "/" # "D:/temp" need a "/"
                self.path = pa

            # update the path of dirButton
            self.dirButton["text"] = self.path
        
        self.dirButton = Button(self.master, text=self.path)
        self.dirButton.bind("<ButtonRelease-1>", updatePath)
        self.dirButton["width"] = Fisher.PATH_WIDTH
        self.dirButton["height"] = Fisher.BUTTON_HEIGHT
        self.dirButton["bg"] = Fisher.BUTTON_COLOR
        self.dirButton["fg"] = Fisher.BG_COLOR
        self.dirButton["font"] = "黑体 10"
        self.dirButton.pack(side=LEFT)
        
    def __addButton(self):
        # this button is used for starting download
        self.button = Button(self.master, text="download")
        self.button.bind("<ButtonRelease-1>", self.__start)
        self.button["width"] = Fisher.BUTTON_WIDTH
        self.button["height"] = Fisher.BUTTON_HEIGHT
        self.button["bg"] = Fisher.BUTTON_COLOR
        self.button["fg"] = Fisher.BG_COLOR
        self.button["font"] = "黑体 10"
        self.button.pack(side=RIGHT)

    # the main function of this tool...
    def __start(self, event):
        # get url user inputed
        url = self.text.get("0.0", "end")

        begin = time.time()
        data = []
        try:
            sou = request.urlopen(url)
            while True:
                temp = sou.read(4096)
                data.append(temp)
                if len(temp) < 4096:
                    break
            data = b"".join(data)
        except: # if this url is wrong, stop downloading...
            self.text.configure(fg="red")
            messagebox.showerror("Error!", "URL 有误！")
            self.text.configure(fg=Fisher.FG_COLOR)
            return
        usedTime = time.time() - begin
        
        # if mode is text, we need to give a certain encoding...
        # because in Windows, the new text file is "GBK"
        # but not here, binary mode has no attribute named "encoding"
        fileName = self.filetext.get("0.0", "end").strip("\n")
        filePath = self.path + fileName
        try:
            with open(filePath, "wb") as f:#, encoding="UTF8") as f:
                f.write(data)
                    
                # prepare information, including size, usedTime, speed...
                info = "文件大小：%.2f KB\n耗时：%.2f 秒\n速度：%.2f KB/s"
                size = os.path.getsize(filePath) / 1024

                # if size is too large(>= 1 MB), change the unit
                if size / 1024 >= 1:
                    size = size / 1024
                    info = info.replace("KB", "MB")

                speed = size / usedTime

                # show these infomation in a message
                messagebox.showinfo("Done!", info % (size, usedTime, speed))
        except PermissionError:
            err = "没有权限访问 %s\n您可以:\n1、以管理员身份运行程序\n或\n2、更改下载文件夹"
            messagebox.showerror("Error!", err % self.path)
            return

    def __putWindowInCenter(self):
        self.master.update() # update window, must do...

        # get current width
        width = self.master.winfo_reqwidth()

        # get current height
        height = self.master.winfo_height()

        # get screen width and height
        scnWidth,scnHeight = self.master.maxsize()

        # calculate the position window should stay
        posX = (scnWidth - width) / 2
        posY = (scnHeight - height) / 2 - 70 # -50 is for prety...
        pos = "%dx%d+%d+%d" % (width,height, posX, posY)

        # apply to the window
        self.master.geometry(pos)
        
    def work(self):
        self.master.mainloop() # start main message loop


if __name__ == "__main__":
    fisher = Fisher()
    fisher.work()
