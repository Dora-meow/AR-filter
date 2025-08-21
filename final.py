#-*- coding: UTF-8 -*-
import tkinter as tk #大小寫要注意,如果小寫不行就改大寫
from tkinter import ttk
from tkinter import filedialog
import time
from PIL import  ImageTk, Image, ImageDraw
import cv2
import numpy as np
import pencil
import random
import proccess as ps
import item

captrue = cv2.VideoCapture(0) #開啟相機，0為預設筆電內建相機  # 開啟相機，參數 0 代表使用內建相機（或默認相機設備）。如果有多個相機，參數可以改為 1 或其他數字，對應不同的設備。
captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數  #CAP_PROP_FOURCC: 設置影像的編碼格式（FourCC 格式）
captrue.set(3,480) #像素 設置影像的寬度為 350 像素（屬性代碼 3 是影像寬度)                    #cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'): 用 MJPG（Motion-JPEG）壓縮格式，減少 CPU 負擔
captrue.set(4,640) #像素 （屬性代碼 4 是影像高度）

img_viode = './photo/a.png'    #影像存放位置


def check():
    global captrue
    frameClose.grid_forget() #把用來遮住功能的frame隱藏
    if captrue.isOpened(): #判斷相機是否有開啟
        open()
    else:
        captrue = cv2.VideoCapture(0) 
        captrue.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) #設置影像參數
        captrue.set(3,480) #像素
        captrue.set(4,640) #像素
        open()
     
def open():
    global s
    ret,frame = captrue.read() #取得相機畫面
    cv2.imwrite(img_viode,frame) #儲存圖片
    img1 = np.array(Image.open(img_viode))
    img1 = img1[:,::-1]
    img_right = ImageTk.PhotoImage(Image.fromarray(img1)) #讀取圖片
    label_right.current_image = img_right  # 保存 PIL.Image (存檔用)
    label_right.imgtk=img_right #換圖片  #維持對圖片的引用，防止圖片被垃圾回收
    label_right.config(image=img_right) #換圖片
    s = label_right.after(1, open) #持續執行open方法，1000為1秒

def close():
    captrue.release() #關閉相機
    label_right.after_cancel(s) #結束拍照
    label_right.config(image=img) #換圖片
    frameClose.grid(row=1, column=0, padx=850, pady=0, sticky="nw") #讓用來遮住功能的frame出現

def save():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
        title="Save image as"
    )
    if file_path:
        if hasattr(label_right, "current_image"): #判斷有沒有"current_image"屬性(?
            pil_image = label_right.current_image  # 取目前畫面上的圖
            pil_image.save(file_path)  # 存檔
        else:
            print("No image to save!")

def show():
    4

def broken(photo):
    photo = pencil.rgb_shift(photo,r_shift=(random.randint(-20, 20), random.randint(0, 0)),
                                                       g_shift=(random.randint(-20, 20), random.randint(0, 0)),
                                                       b_shift=(random.randint(-20, 20), random.randint(0, 0)))
    return photo

def medium_RGB1(photo):
    photo = ps.medium_RGB(np.array(photo))
    return photo

# 存選的背景
def whichBackground(filename):
    global UseBackground
    UseBackground = filename
    print(f"Selected file: {filename}")

# 存選的item
def whichItem(filename):
    global UseItem
    UseItem = filename
    print(f"Selected file: {filename}")

UseItem = ''
UseBackground = ''
function_dic = {'pencilA':pencil.pencilA, 'pencilB':pencil.pencilB, 'old':pencil.old, 'broken':broken, 'animate':pencil.animate, 'fisheye':pencil.fisheye, 'relief':pencil.myRelief, 'hist':pencil.hist, 'negative':pencil.negative }
selected_items = []
def submit():
    global s, function_dic, selected_items
    label_right.after_cancel(s) #結束拍照

    # 按下提交按鈕時，執行所有選中的 Checkbutton 的值
    selected_items = []
    if var1.get():selected_items.append(var1.get())
    if var2.get():selected_items.append(var2.get())
    if var3.get():selected_items.append(var3.get())
    if var4.get():selected_items.append(var4.get())
    if var5.get():selected_items.append(var5.get())
    if var6.get():selected_items.append(var6.get())
    if var7.get():selected_items.append(var7.get())
    if var8.get():selected_items.append(var8.get())
    if var9.get():selected_items.append(var9.get())
    #if var10.get():selected_items.append(var10.get())
    print(selected_items)
    showImage()

def showImage():
    global s, function_dic, selected_items, UseItem, UseBackground
    ret,frame = captrue.read() #取得相機畫面
    cv2.imwrite(img_viode,frame) #儲存圖片
    img_right = Image.open(img_viode)
    for i in selected_items: #用濾鏡
        #print(i)
        img_right = function_dic[i](img_right)
    #判斷是否有其他濾鏡
    if(var10.get()):
        a = value_material.get()
        if(a != 'material'):
            img_right = pencil.painting(img_right, a)

    if(var11.get()):
        a = int(scale_brightness.get())*0.32
        img_right = np.array(img_right)
        img_right = ps.adjust_contrast_brightness(img_right, a)
    if(var12.get()):
        a = 1-int(scale_warm.get())*0.01
        img_right = np.array(img_right)
        img_right = ps.warm(img_right, a)
    if(var13.get()):
        a = 1/2**int(spinbox_split.get())
        img_right = pencil.mySplit(img_right, a)
    if(var14.get()):
        a = int(scale_medium.get())
        img_right = np.array(img_right)
        img_right = ps.medium_RGB(img_right, a)
    if(var15.get()):
        a = int(scale_whiten.get())/100+1
        img_right = np.array(img_right)
        img_right = ps.Whitening(img_right, a)

    #把圖左右相反
    img_right = np.array(img_right)
    img_right = img_right[:,::-1]
    img_right = Image.fromarray(img_right)
    
    #判斷是否有背景及物件
    if(usingItem.get()):
        a = int(scale_size.get())
        b = int(scale_size1.get())
        x1 = int(scale_x.get())
        y1 = int(scale_y.get())
        img_right = np.array(img_right)

        #判斷是絕對位子還是相對位子
        if(val.get()):
            img_right = ps.draw(img_right,UseItem,True,dx=x1,dy=y1,magn_x=a,magn_y=b)
        else:
            img_right = ps.item(img_right,UseItem,True,x=x1,y=y1,magn_x=a,magn_y=b)
    if(usingBackground.get()):
        img_right = np.array(img_right)
        img_right = ps.background(img_right, UseBackground)

    label_right.current_image = img_right  # 保存 PIL.Image (存檔用)
    img_right = ImageTk.PhotoImage(img_right) #讀取圖片
    
    label_right.imgtk=img_right #換圖片
    label_right.config(image=img_right) #換圖片
    s = label_right.after(50, showImage) #持續執行open方法，1000為1秒

def Choose_BG():
    global UseBackground
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.tif")])
    if file_path:
        ps.generate_background(file_path)
        text= file_path.split('/')
        UseBackground=text[-1]


def makeItem():
    global enterWindow, value
    enterWindow=tk.Toplevel(top)
    enterWindow.title('Use other image')
    enterWindow.geometry('310x200')
    btn = tk.Button(enterWindow, text='choose image',height=3,width=15, command=Choose_item)     # 建立 Button 按鈕
    btn.grid(row=1,column=0,padx=30, pady=40, sticky="nw")
    tk.Label(enterWindow, text='the value:').grid(row=1,column=0,padx=200, pady=40, sticky="nw")
    scale_value = tk.Scale(enterWindow, from_=1, to=100, orient='horizontal')   # 加入水平調整滑桿 ( orient='horizontal' )
    scale_value.grid(row=1, column=0, padx=180, pady=57, sticky="nw")
    value = int(scale_value.get())
    #button_submit = tk.Button(enterWindow,text = 'submit',height=2,width=10,bg ='gray94',command = show)
    #button_submit.grid(row=1, column=0, padx=120, pady=130, sticky="nw") 

def Choose_item():
    global UseItem, value
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.tif")])
    if file_path:
        item.item_gernate(file_path, value)
        text= file_path.split('/')
        UseItem=text[-1]


#創建一個視窗
top = tk.Tk() 
#視窗名稱
top.title('GUI') 
#寬:300高:200的視窗,放在寬:600高:300的位置
top.geometry('600x500+200+100') 

#開啟照片
img= ImageTk.PhotoImage(Image.open('./photo/a.png'))

#用label來放照片
label_right= tk.Label(top,height=480,width=640,bg ='gray94',fg='blue',image = img) 

#按鈕
button_1 = tk.Button(top,text = 'open',bd=4,height=4,width=20,bg ='gray94',command =check)
button_2 = tk.Button(top,text = 'close',bd=4,height=4,width=20,bg ='gray94',command =close)
button_11 = tk.Button(top, text='Save', bd=4, height=4, width=20, bg='gray94', command=save)

#位置
label_right.grid(row=1,column=0,padx=120, pady=40, sticky="nw") 
button_1.grid(row=1, column=0, padx=160, pady=600, sticky="nw")  
button_2.grid(row=1, column=0, padx=360, pady=600, sticky="nw") 
button_11.grid(row=1, column=0, padx=560, pady=600, sticky="nw") 


#濾鏡功能
frame1 = tk.LabelFrame(top, text=' Choose filter ', width=550, height=180)
frame1.grid(row=1, column=0, padx=850, pady=40, sticky="nw")
frame1.grid_propagate(0) #固定長寬
var1 = tk.StringVar()
check_btn1 = tk.Checkbutton(frame1, text='pencil',
                            variable=var1, onvalue='pencilA', offvalue='',
                            command=show)
check_btn1.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
check_btn1.deselect() # 開始時不要勾選

var2 = tk.StringVar()
check_btn2 = tk.Checkbutton(frame1, text='pen',
                            variable=var2, onvalue='pencilB', offvalue='',
                            command=show)
check_btn2.grid(row=1, column=0, padx=100, pady=10, sticky="nw")
check_btn2.deselect()

var3 = tk.StringVar()
check_btn3 = tk.Checkbutton(frame1, text='animate',
                            variable=var3, onvalue='animate', offvalue='',
                            command=show)
check_btn3.grid(row=1, column=0, padx=190, pady=10, sticky="nw")
check_btn3.deselect()

var4 = tk.StringVar()
check_btn4 = tk.Checkbutton(frame1, text='fisheye',
                            variable=var4, onvalue='fisheye', offvalue='',
                            command=show)
check_btn4.grid(row=1, column=0, padx=280, pady=10, sticky="nw")
check_btn4.deselect()

var5 = tk.StringVar()
check_btn5 = tk.Checkbutton(frame1, text='broken',
                            variable=var5, onvalue='broken', offvalue='',
                            command=show)
check_btn5.grid(row=1, column=0, padx=370, pady=10, sticky="nw")
check_btn5.deselect()

var6 = tk.StringVar()
check_btn6 = tk.Checkbutton(frame1, text='old photo',
                            variable=var6, onvalue='old', offvalue='',
                            command=show)
check_btn6.grid(row=1, column=0, padx=10, pady=40, sticky="nw")
check_btn6.deselect()

var7 = tk.StringVar()
check_btn7 = tk.Checkbutton(frame1, text='relief',
                            variable=var7, onvalue='relief', offvalue='',
                            command=show)
check_btn7.grid(row=1, column=0, padx=100, pady=40, sticky="nw")
check_btn7.deselect()

var8 = tk.StringVar()
check_btn8 = tk.Checkbutton(frame1, text='negative',
                            variable=var8, onvalue='negative', offvalue='',
                            command=show)
check_btn8.grid(row=1, column=0, padx=190, pady=40, sticky="nw")
check_btn8.deselect()

var9 = tk.StringVar()
check_btn9 = tk.Checkbutton(frame1, text='auto level',
                            variable=var9, onvalue='hist', offvalue='',
                            command=show)
check_btn9.grid(row=1, column=0, padx=280, pady=40, sticky="nw")
check_btn9.deselect()

var10 = tk.StringVar()
check_btn10 = tk.Checkbutton(frame1, text='',
                            variable=var10, onvalue='painting', offvalue='',
                            command=show)
check_btn10.grid(row=1, column=0, padx=370, pady=40, sticky="nw")
check_btn10.deselect()
optionList = ['material','canva1','canva2','canva3','canva4','oil painting1','oil painting2','paper1','paper2','paper3','line1',
                         'yellow','green','blue','blue2','white','purple','pink','brown','brown2','red']
value_material = tk.StringVar()
value_material.set('material')
menu = tk.OptionMenu(frame1, value_material, *optionList)  # 選單
menu.config(width=8, fg='#0d0000')                # 設定樣式
menu.grid(row=1, column=0, padx=390, pady=37, sticky="nw")


var13 = tk.StringVar()
check_btn13 = tk.Checkbutton(frame1, text='split',
                            variable=var13, onvalue='split', offvalue='',
                            command=show)
check_btn13.grid(row=1, column=0, padx=430, pady=78, sticky="nw")
check_btn13.deselect()
spinbox_split = tk.Spinbox(frame1, from_=0, to=4, width=4)
spinbox_split.grid(row=1, column=0, padx=490, pady=80, sticky="nw")

var15 = tk.StringVar()
check_btn15 = tk.Checkbutton(frame1, text='whiten',
                            variable=var15, onvalue='whiten', offvalue='',
                            command=show)
check_btn15.grid(row=1, column=0, padx=10, pady=78, sticky="nw")
check_btn15.deselect()
scale_whiten = tk.Scale(frame1, from_=1, to=100, orient='horizontal')   # 加入水平調整滑桿 ( orient='horizontal' )
scale_whiten.grid(row=1, column=0, padx=100, pady=68, sticky="nw")

var14 = tk.StringVar()
check_btn14 = tk.Checkbutton(frame1, text='pixelate',
                            variable=var14, onvalue='mediun', offvalue='',
                            command=show)
check_btn14.grid(row=1, column=0, padx=240, pady=78, sticky="nw")
check_btn14.deselect()
scale_medium = tk.Scale(frame1, from_=1, to=60, orient='horizontal')   # 加入水平調整滑桿 ( orient='horizontal' )
scale_medium.grid(row=1, column=0, padx=308, pady=68, sticky="nw")

var11 = tk.StringVar()
check_btn11 = tk.Checkbutton(frame1, text='brightness',
                            variable=var11, onvalue='brightness', offvalue='',
                            command=show)
check_btn11.grid(row=1, column=0, padx=10, pady=115, sticky="nw")
check_btn11.deselect() # 開始時不要勾選
scale_brightness = tk.Scale(frame1, from_=1, to=100, orient='horizontal')   # 加入水平調整滑桿 ( orient='horizontal' )
scale_brightness.grid(row=1, column=0, padx=100, pady=105, sticky="nw")

var12 = tk.StringVar()
check_btn12 = tk.Checkbutton(frame1, text='warm',
                            variable=var12, onvalue='warm', offvalue='',
                            command=show)
check_btn12.grid(row=1, column=0, padx=240, pady=115, sticky="nw")
check_btn12.deselect()
scale_warm = tk.Scale(frame1, from_=1, to=100, orient='horizontal')   # 加入水平調整滑桿 ( orient='horizontal' )
scale_warm.grid(row=1, column=0, padx=308, pady=105, sticky="nw")


#放背景
frame2 = tk.LabelFrame(top, text=' Choose background ', width=500, height=120)
frame2.grid(row=1, column=0, padx=850, pady=250, sticky="nw")
frame2.grid_propagate(0)

# 創建內部框架並綁定滾動條
canvas = tk.Canvas(frame2, width=500, height=120)
scrollbar = tk.Scrollbar(frame2, orient="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=scrollbar.set)

# 放置滾動條和畫布
scrollbar.pack(side="bottom", fill="x")
canvas.pack(side="top", fill="both", expand=True)

# 在畫布中創建內部框架
frame2_1 = tk.Frame(canvas, width=2000, height=120)  # 寬度設大一點以測試滾動效果
canvas.create_window((0, 0), window=frame2_1, anchor="nw")

# 動態調整畫布的滾動區域
def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame2_1.bind("<Configure>", configure_canvas)

# 保存所有圖片引用
icons = []

# 添加多個按鈕到 frame2_1
for i in range(14):
    img2 = tk.PhotoImage(file=f"./photo/icon/{i+1}.png")
    icons.append(img2)  # 保持引用，避免被垃圾回收
    btn = tk.Button(frame2_1, text=f"Button {i+1}", image=img2, width=140, height=105, command=lambda path=f"{i+1}.jpg": whichBackground(path))
    btn.grid(row=0, column=i, padx=5, pady=10)

btn1 = tk.Button(frame2_1, text='\n         +         \n\n  Use other image  \n', command=Choose_BG)
btn1.grid(row=0, column=15, padx=5, pady=10)


#放物件
frame3 = tk.LabelFrame(top, text=' Choose item ', width=350, height=100)
frame3.grid(row=1, column=0, padx=850, pady=440, sticky="nw")
frame3.grid_propagate(0)

# 創建內部框架並綁定滾動條
canvas1 = tk.Canvas(frame3, width=350, height=100)
scrollbar = tk.Scrollbar(frame3, orient="horizontal", command=canvas1.xview)
canvas1.configure(xscrollcommand=scrollbar.set)

# 放置滾動條和畫布
scrollbar.pack(side="bottom", fill="x")
canvas1.pack(side="top", fill="both", expand=True)

# 在畫布中創建內部框架
frame3_1 = tk.Frame(canvas1, width=3000, height=100)  # 寬度設大一點以測試滾動效果
canvas1.create_window((0, 0), window=frame3_1, anchor="nw")

# 動態調整畫布的滾動區域
def configure_canvas1(event):
    canvas1.configure(scrollregion=canvas1.bbox("all"))

frame3_1.bind("<Configure>", configure_canvas1)

# 保存所有圖片引用
items = []

# 添加多個按鈕到 frame3_1
for i in range(20):
    img2 = tk.PhotoImage(file=f"./photo/itemIcon/{i+1}.png")
    items.append(img2)  # 保持引用，避免被垃圾回收
    btn = tk.Button(frame3_1, text=f"Button {i+1}", image=img2, width=85, height=85, command=lambda path=f"item{i+1}.jpg": whichItem(path))
    btn.grid(row=0, column=i, padx=5, pady=10)

btn1 = tk.Button(frame3_1, text='\n       +       \nUse other image\n', command=makeItem)
btn1.grid(row=0, column=21, padx=5, pady=10)

# 指定位子或臉的相對位子
val = tk.IntVar()
radio_btn1 = tk.Radiobutton(top, text='relative position (to face)',variable=val, value=1)
radio_btn1.grid(row=1, column=0, padx=1220, pady=450, sticky="nw")
#radio_btn1.select()  # select() 選取 radio_btn1

radio_btn2 = tk.Radiobutton(top, text='absolute position',variable=val, value=0)
radio_btn2.grid(row=1, column=0, padx=1220, pady=470, sticky="nw")

tk.Label(top, text='x :').grid(row=1, column=0, padx=1225, pady=500, sticky="nw")
tk.Label(top, text='y :').grid(row=1, column=0, padx=1225, pady=540, sticky="nw")
tk.Label(top, text='size :').grid(row=1, column=0, padx=1370, pady=480, sticky="nw")
scale_x = tk.Scale(top, from_=0, to=640, orient='horizontal')   # 加入水平調整滑桿 ( orient='horizontal' )
scale_x.grid(row=1, column=0, padx=1240, pady=490, sticky="nw")
scale_y = tk.Scale(top, from_=0, to=480, orient='horizontal')   # 加入水平調整滑桿 ( orient='horizontal' )
scale_y.grid(row=1, column=0, padx=1240, pady=530, sticky="nw")
scale_size = tk.Scale(top, from_=1, to=5, length=70)   # 加入垂直調整滑桿 ( 預設垂直 )
scale_size.grid(row=1, column=0, padx=1350, pady=500, sticky="nw")
scale_size1 = tk.Scale(top, from_=1, to=5, length=70)   # 加入垂直調整滑桿 ( 預設垂直 )
scale_size1.grid(row=1, column=0, padx=1380, pady=500, sticky="nw")
tk.Label(top, text='x').grid(row=1, column=0, padx=1365, pady=573, sticky="nw")
tk.Label(top, text='y').grid(row=1, column=0, padx=1395, pady=573, sticky="nw")

# 是否用background跟item
usingBackground = tk.BooleanVar()
check_btnB = tk.Checkbutton(top, text='use background',
                            variable=usingBackground, onvalue=True, offvalue=False,
                            command=show)
check_btnB.grid(row=1, column=0, padx=900, pady=610, sticky="nw")
check_btnB.deselect()

usingItem = tk.BooleanVar()
check_btnI = tk.Checkbutton(top, text='use item',
                            variable=usingItem, onvalue=True, offvalue=False,
                            command=show)
check_btnI.grid(row=1, column=0, padx=1030, pady=610, sticky="nw")
check_btnI.deselect()

#執行選的所有東西
button_submit = tk.Button(top,text = 'submit',height=2,width=10,bg ='gray94',command = submit)
button_submit.grid(row=1, column=0, padx=1130, pady=600, sticky="nw") 

frameClose = tk.Frame(top, width=850, height=1000)
frameClose.grid(row=1, column=0, padx=850, pady=0, sticky="nw")
top.mainloop() #執行視窗