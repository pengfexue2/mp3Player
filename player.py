from tkinter import *
import binascii
import re
import time
import printPlay
import pygame
import threading

def startPlay():
    global normal
    normal = True
    name = inpt.get()
    lyricList = []
    try:
        with open("music/%s.lrc"%name, encoding="gbk") as f:
            lyricList = f.readlines()
    except:
        try:
            with open("music/%s.lrc"%name, encoding="utf-8") as l:
                lyricList = l.readlines()
        except:
            print("打开歌词文件失败...")
    timeTable = []
    lyricDict = {}

    pattern = r'\d{2}:\d{2}.\d{2}'
    for str in lyricList:
        strList = str.split(']')
        for i in range(len(strList)-1):
            if re.match(pattern,strList[i][1:]):
                t = (int(strList[i][1:][:2]) * 60 + int(strList[i][1:][3:5]))+ int(strList[i][1:][6:8])*0.01
                timeTable.append(t)
                lyricDict[t] = strList[-1][:-1]

    pygame.mixer.init()
    track = pygame.mixer.music.load('music/%s.mp3'%name)
    pygame.mixer.music.play()

    for t in timeTable:
        text = ''.join(lyricDict[t].split(' '))
        timethread = threading.Timer(t, showlyric, args=(text,))
        timethread.start()

def char2bit(textStr):
    KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
    target = []

    for x in range(len(textStr)):
        text = textStr[x]
        rect_list = [] * 16
        for i in range(16):
            rect_list.append([] * 16)

        gb2312 = text.encode('gb2312')
        hex_str = binascii.b2a_hex(gb2312)
        result = str(hex_str, encoding='utf-8')
        area = eval('0x' + result[:2]) - 0xA0
        index = eval('0x' + result[2:]) - 0xA0
        offset = (94 * (area-1) + (index-1)) * 32

        font_rect = None
        with open("HZK16", "rb") as f:
            f.seek(offset)
            font_rect = f.read(32)

        for k in range(len(font_rect) // 2):
            row_list = rect_list[k]
            for j in range(2):
                for i in range(8):
                    asc = font_rect[k * 2 + j]
                    flag = asc & KEYS[i]
                    row_list.append(flag)

        output = []
        for row in rect_list:
            for i in row:
                if i:
                    output.append('★')
                    #print('0', end=' ')
                else:
                    output.append('　')
                    #print('.', end=' ')
            print()

        target.append(''.join(output))
    return target

def insertbit(target):
    global gridList
    for t in gridList:
        t.delete('1.0', 'end')
    if len(target)<=16:
        for i in range(len(target)):
            gridList[i].insert(INSERT, target[i])
            gridList[i].insert(END, '')
    else:
        for x in range(16):
            gridList[x].insert(INSERT,target[x])
            gridList[x].insert(END, '')

def clear():
    global gridList
    for t in gridList:
        t.delete('1.0', 'end')

def close():
    global normal
    normal = False
    pygame.mixer.music.stop()
    #root.destroy()

def transfer():
    inputtext=inpt.get()
    #print(inputtext)
    bitlist = char2bit(inputtext)
    #print(bitlist)
    insertbit(bitlist)

def showlyric(lyric):
    inputtext=lyric
    #print(inputtext)
    bitlist = char2bit(inputtext)
    #print(bitlist)
    insertbit(bitlist)

root = Tk()
root.title("TEDxPY")

frame1 = Frame(width=900,height=60)
canvas=Canvas(root,width=920,height=675,scrollregion=(0,0,900,900)) #创建canvas
canvas.grid(row=1, column=0) #放置canvas的位置
frame2=Frame(canvas) #把frame放在canvas里
frame2.place(x=0,y=0,width=900,height=900)


vbar=Scrollbar(canvas,orient=VERTICAL) #竖直滚动条
vbar.place(x = 900,width=20,height=675)
vbar.configure(command=canvas.yview)

canvas.config(yscrollcommand=vbar.set) #设置
canvas.create_window((450,420), window=frame2)  #create_window


gridList=[]
for l in range(16):
    gridList.append(Text(frame2, width=32, height=16, borderwidth=0))
    gridList[l].grid(row=int(l / 4) + 2, column=l % 4)


frame1.grid(row=0,column=0)


photo=PhotoImage(file="TEDxPY.png")
Label(frame1,image=photo).grid(row=0, rowspan=2, column=0, columnspan=2,sticky=W,ipady=10)
Label(frame1,text="点歌:").grid(row=0, column=2, sticky = E)
inpt=Entry(frame1)
inpt.grid(row=0,column=3,sticky=W )

Button(frame1,text="播放",command=startPlay).grid(row=1,column=2,sticky=E)
Button(frame1,text="清除",command=clear).grid(row=1,column=3)
Button(frame1,text="关闭",command=close).grid(row=1,column=4)

root.mainloop()

