import numpy as np
from PIL import  ImageTk, Image
import math
import cv2
import proccess1 as ps1
import proccess as ps
import random




def pencilA(photo): #用高斯模糊後跟原本照片相除
    w, h = photo.size
    img = RGBtoGray(photo)
    #img = np.log(img*float(0.3)+float(0.1))
    #img = img**1.5
    img2=img.copy()
    #img = cv2.GaussianBlur(img, (25,25), 0)
    img = gaussian(img, w, h, 25, 1.7)
    img = img2/(img+1)*250 # 避免除以零
    img = 0.00025*img**2.5
    img = np.clip(img,0,255).astype('uint8')
    sol = np.zeros((h,w,3)).astype('uint8')
    sol[:,:,0]=img
    sol[:,:,1]=img
    sol[:,:,2]=img
    #img = img[:,::-1]
    photo = Image.fromarray(sol)
    return photo

def pencilB(photo): #用中位數+拉普拉斯遮罩+非黑即白
    w, h = photo.size
    img = ps1.medium_RGB(np.array(photo))
    img = RGBtoGray(img)
    #img = RGBtoGray(photo)
    #img = gaussian(img, w, h, 10, 1)
    img = laplacian(img, w, h, 2.1)
    img = 255-img
    img = doglSlicing(img, h, w, 247, 255)
    sol = np.zeros((h,w,3)).astype('uint8')
    sol[:,:,0]=img
    sol[:,:,1]=img
    sol[:,:,2]=img
    #img = img[:,::-1]
    photo = Image.fromarray(img)
    return photo

def animate(photo):
    w, h = photo.size
    edge = RGBtoGray(photo)
    edge = gaussian(edge, w, h, 5, 2)
    edge = laplacian(edge, w, h, 6)
    edge = 255-edge
    edge = doglSlicing(edge, h, w, 247, 255)
    edgeColor = np.stack((edge,edge,edge), axis=-1) #1通道變3通道
    #edgeColor = ps.medium_RGB(edgeColor)
    #photo = Image.fromarray(edge) #雜點多但較快
    
    #img = np.array(ps.medium_RGB(np.array(photo)))
    img = np.array(photo)
    #img = RGBtoHSI(img,h,w) #把飽和度調高
    #img = cv2.cvtColor(photo, cv2.COLOR_BGR2HSV)
    #print(img)
    #img = np.array(img)
    #img[1] = img[1]**0.7
    #img = np.array(HSItoRGB(img,h,w))
    img[:,:,0] = gaussian(img[:,:,0],w,h,7,2)
    img[:,:,1] = gaussian(img[:,:,1],w,h,7,2)
    img[:,:,2] = gaussian(img[:,:,2],w,h,7,2)
    img[:,:,0] = np.clip(img[:,:,0],0,255).astype('uint8')
    img[:,:,1] = np.clip(img[:,:,1],0,255).astype('uint8')
    img[:,:,2] = np.clip(img[:,:,2],0,255).astype('uint8')
    img = np.bitwise_and(img, edgeColor)
    #img = img[:,::-1]
    photo = Image.fromarray(img)
    #photo = Image.fromarray(edge)
    return photo

def fisheye(photo):
    '''
    photo = np.array(photo)
    row, col, channel = photo.shape

    # 中心點與半徑
    center_x, center_y = row / 2, col / 2
    radius = min(center_x, center_y)

    # 生成距離矩陣
    y, x = np.meshgrid(np.arange(col), np.arange(row))
    distance_squared = (x - center_x) ** 2 + (y - center_y) ** 2
    mask = distance_squared <= radius ** 2  # 判斷哪些點在圓內

    # 計算距離和比例
    distance = np.sqrt(distance_squared, where=mask, out=np.zeros_like(distance_squared))
    scale = np.where(mask, distance / radius, 1)

    # 新的像素坐標
    new_x = np.clip(((x - center_x) * scale + center_x).astype(int), 0, row - 1)
    new_y = np.clip(((y - center_y) * scale + center_y).astype(int), 0, col - 1)

    # 應用凸透鏡效果
    new_img = np.zeros_like(photo)
    new_img[x, y, :] = photo[new_x, new_y, :]

    photo = Image.fromarray(new_img)
    #photo = Image.fromarray(edge)
    return photo
    '''
    w, h = photo.size
    img = np.array(photo)
    sol = img.copy()
    centerY = w//2
    centerX = h // 2
    radius = min(centerX, centerY)
    no = centerY-radius
    for i in range(h):
        for j in range(no, w-no):
            distance = ((i - centerX) ** 2 + (j - centerY) ** 2)
            new_dist = np.sqrt(distance)
            #sol[i, j, :] = photo[i, j, :]
            if distance <= radius**2:
                new_i = int(np.floor(new_dist * (i - centerX) / radius + centerX))
                new_j = int(np.floor(new_dist * (j - centerY) / radius + centerY))
                if 0 <= new_i < h and 0 <= new_j < w:  # 確保索引有效
                    sol[i, j, :] = img[new_i, new_j, :]
    #sol = sol[:,::-1]
    photo = Image.fromarray(sol)
    return photo
    

def old(photo):
    w, h = photo.size
    img = np.array(photo)
    
    # 分别取 RGB 通道
    R = img[:, :, 0].astype(np.float32)
    G = img[:, :, 1].astype(np.float32)
    B = img[:, :, 2].astype(np.float32)

    sol = np.zeros((h, w, 3), dtype="float64")

    # 懷舊特效公式
    sol[:, :, 0] = 0.393 * R + 0.769 * G + 0.189 * B
    sol[:, :, 1] = 0.349 * R + 0.686 * G + 0.168 * B
    sol[:, :, 2] = 0.272 * R + 0.534 * G + 0.131 * B
    
    # 限制像素值範圍在 0-255
    sol1 = np.clip(sol, 0, 255).astype('uint8')
    #sol1 = sol1[:,::-1]
    photo1 = Image.fromarray(sol1)
    return photo1

def negative(photo):
    img = np.array(photo)
    img = 255-img
    #img = img[:,::-1]
    photo = Image.fromarray(img)
    return photo

def rgb_shift(photo, r_shift=(0, 0), g_shift=(0, 0), b_shift=(0, 0)):#圖, R的偏移量, G的偏移量, B的偏移量
    w, h =photo.size
    img = np.array(photo)

    # 取 R、G、B 
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    # 偏移紅色通道
    r_shift_x, r_shift_y = r_shift
    R_shifted = myRoll(R, r_shift_x, r_shift_y)

    # 偏移綠色通道
    g_shift_x, g_shift_y = g_shift
    G_shifted = myRoll(G, g_shift_x, g_shift_y)

    # 偏移藍色通道
    b_shift_x, b_shift_y = b_shift
    B_shifted = myRoll(B, b_shift_x, b_shift_y)

    img[:,:,0] = R_shifted
    img[:,:,1] = G_shifted
    img[:,:,2] = B_shifted
    #img = img[:,::-1]
    return Image.fromarray(img)

def mySplit(photo, a): 
    w, h =photo.size
    img = np.array(photo)
    if(a==1.0): #原圖的1倍不用調整
        return photo
    elif(a<=0): #不能有0倍或負的倍數
        return

    newW = round(w*a)
    newH = round(h*a)
    sol = np.zeros((newH, newW, 3), dtype="uint8")
    fsol = np.zeros((h, w, 3), dtype="uint8")
    sol[:, :, 0]=myresize(img[:, :, 0], w, h, a)
    sol[:, :, 1]=myresize(img[:, :, 1], w, h, a)
    sol[:, :, 2]=myresize(img[:, :, 2], w, h, a)
    for i in range(int(1//a)):
        for j in range(int(1//a)):
            fsol[newH*i:newH*(i+1),newW*j:newW*(j+1),0]=sol[:, :, 0]
            fsol[newH*i:newH*(i+1),newW*j:newW*(j+1),1]=sol[:, :, 1]
            fsol[newH*i:newH*(i+1),newW*j:newW*(j+1),2]=sol[:, :, 2]
    #fsol = fsol[:,::-1]
    return Image.fromarray(fsol)

def hist(photo):
    w, h =photo.size
    img = np.array(photo)
    img[:,:,0] = myHistogram(img[:,:,0],w,h)
    img[:,:,1] = myHistogram(img[:,:,1],w,h)
    img[:,:,2] = myHistogram(img[:,:,2],w,h)
    #img = img[:,::-1]
    return Image.fromarray(img)

def myRelief(photo):
    w, h =photo.size
    img = RGBtoGray(photo)
    sol = np.zeros((h, w), dtype="float16")
    img_padded = np.pad(img, ((1,1), (1,1)), mode='reflect')  # 邊界填充
    kernel = np.array([[-1.5, 0, 0],
                       [0,  1.5, 0],
                       [ 0,  0, 0]])
    #將遮罩應用到影像的每一個像素上 (較快)
    for i in range(3):
        for j in range(3):
            sol += kernel[i, j] * img_padded[i:i + h, j:j + w]
    sol = sol+128
    sol = np.clip(sol, 0, 255).astype('uint8')
    #sol = sol[:,::-1]
    photo = Image.fromarray(sol)
    return photo
    
def painting(photo, a):
    dic = {'canva1':['0.jpg',0.84,1], 'canva2':['9.jpg',0.84,1], 'canva3':['15.jpg',0.84,1], 'canva4':['8.jpg',0.84,1], 
           'oil painting1':['2.jpg',0.80,1], 'oil painting2':['3.jpg',0.84,1], 
           'paper1':['4.jpg',0.70,0], 'paper2':['5.jpg',0.80,0], 'paper3':['17.jpg',0.80,0],
           'yellow':['6.jpg',0.75,0], 'green':['6_1.jpg',0.75,0], 'blue':['7.jpg',0.75,0], 'blue2':['19.jpg',0.75,0], 'white':['11.jpg',0.75,0], 'purple':['12.jpg',0.75,0], 'pink':['13.jpg',0.75,0], 'brown':['14.jpg',0.75,0], 'brown2':['20.jpg',0.70,0], 'red':['18.jpg',0.80,0],
           'line1':['16.jpg',0.80,1]}
    back = np.array(Image.open('./photo/material/'+dic[a][0]))
    #print(back)
    w, h =photo.size
    img = np.array(photo)
    if(dic[a][2]):
        img = ps.medium_RGB(img ,2,False)
    newH, newW, _ = img.shape
    img2 = np.zeros((h,w,3), dtype="uint8")
    img2[0:newH, 0:newW] = img
    d=dic[a][1]
    sol = d*(img2/255)+(1-d)*(back/255)
    sol = sol*255
    sol = sol.astype('uint8')
    photo = Image.fromarray(sol)
    return photo






def myHistogram(img,w,h): #img 圖的矩陣
    img1 = [[0] * w for i in range(h)] #存改完的圖
    img1 = np.array(img1)
    histo = np.array(count(img))
    histo = histo/(w*h) #每個色階出現的機率
    s=np.zeros(256,float)
    s[0]=histo[0]
    for i in range(1,256):
        s[i]=s[i-1]+histo[i] #色階跟數量的CDF
    s=s*255   #L-1=255                             (ex:   0,1,2,3,4,5
    s=np.around(s).astype('uint16') #四捨五入取整數     s=[0,0,1,2,3,5]  色階0變0,色階1變0,色階2變1,色階3變2,色階4變3,色階5還是5
    s[255]=255
    for i in range(h):
        for j in range(w):
            img1[i][j]=s[img[i][j]]
    
    img1 = img1.astype('uint8')
    return img1

def count(img): #算每個色階有幾個點
    img1 = np.array(img) #圖片轉陣列
    c=np.zeros(256,int)
    for i in range(0,256):
        c[i]=np.sum(img1==i)
    return c

def myresize(img, w, h, a): #矩陣->矩陣
    if(a==1.0): #原圖的1倍不用調整
        return img
    elif(a<=0): #不能有0倍或負的倍數
        return
    #print(a)
    newW = round(w*a)
    newH = round(h*a)
    done = [[0] * (newW) for i in range(newH)] #存縮放好的陣列(x,y,value 的那個)
    b=int(1//a)
    for i in range(newH): #把圖片轉成img1並變成縮放後的座標
        for j in range(newW):
            done[i][j]=img[i*b][j*b]
    #done = done.astype('uint8')
    return done

def myRoll(img, shiftX, shiftY): #偏移矩陣
    h, w = img.shape

    # 垂直方向偏移
    if shiftY != 0:
        shiftY %= h  # 防止超出範圍
        img = np.vstack((img[-shiftY:], img[:-shiftY])) #img[-shiftY:] img的最後shiftY列 ,img[:-shiftY] img的開頭到倒數shiftY列

    # 水平方向偏移
    if shiftX != 0:
        shiftX %= w  # 防止超出範圍
        img = np.hstack((img[:, -shiftX:], img[:, :-shiftX]))

    return img



def RGBtoHSI(img, h, w): 
    imgArrayH=np.zeros((h,w))
    imgArrayI=np.zeros((h,w))
    imgArrayS=np.zeros((h,w))
    done=[] #done[0]:H, done[1]:S, done[2]:I
    for i in range(h):
        for j in range(w): #帶公式
            imgArrayI[i][j]=sum(img[i][j])/3  #I = 1/3 * (R+G+B)
            imgArrayS[i][j]=1-(3*min(img[i][j]))/sum(img[i][j]) #S = 1 - 3min(R,G,B)/(R+G+B)
            #θ = cos^-1( 0.5(R-G)+(R-B)/根號((R-G)^2+(R-B)(G-B)) )
            v=0.5*(2*img[i][j][0]-img[i][j][1]-img[i][j][2])/(((img[i][j][0]-img[i][j][1])**2+(img[i][j][0]-img[i][j][2])*(img[i][j][1]-img[i][j][2])+1)**0.5)
            #print(v)
            theta=math.acos(max(-1, min(1, v))) #加1才不會有除0的情況
            #H = θ ,G>=B 
            #  = 2π-θ  ,G<B
            if(img[i][j][1]<img[i][j][2]):
                imgArrayH[i][j]=2*math.pi-theta
            else:
                imgArrayH[i][j]=theta
            
            #print(imgArrayH[i][j],imgArrayS[i][j],imgArrayI[i][j])
    done.append(np.array(imgArrayH))
    done.append(np.array(imgArrayS))
    done.append(np.array(imgArrayI).astype('uint8'))
    return done

def HSItoRGB(img, h, w): 
    imgArrayR=np.zeros((h,w))
    imgArrayG=np.zeros((h,w))
    imgArrayB=np.zeros((h,w))
    for i in range(h):
        for j in range(w): #帶公式
            H = img[0][i][j]  # 色調
            S = img[1][i][j]  # 飽和度
            I = img[2][i][j]  # 亮度
            
            if 0 <= H < 2 * math.pi / 3:
                imgArrayB[i][j] = I * (1 - S)
                imgArrayR[i][j] = I * (1 + S * math.cos(H) / math.cos(math.pi / 3 - H))
                imgArrayG[i][j] = 3 * I - (imgArrayR[i][j] + imgArrayB[i][j])
            elif 2 * math.pi / 3 <= H < 4 * math.pi / 3:
                H -= 2 * math.pi / 3
                imgArrayR[i][j] = I * (1 - S)
                imgArrayG[i][j] = I * (1 + S * math.cos(H) / math.cos(math.pi / 3 - H))
                imgArrayB[i][j] = 3 * I - (imgArrayR[i][j] + imgArrayG[i][j])
            else:
                H -= 4 * math.pi / 3
                imgArrayG[i][j] = I * (1 - S)
                imgArrayB[i][j] = I * (1 + S * math.cos(H) / math.cos(math.pi / 3 - H))
                imgArrayR[i][j] = 3 * I - (imgArrayG[i][j] + imgArrayB[i][j])
    
    imgArrayR = np.clip(imgArrayR, 0, 255).astype('uint8')
    imgArrayG = np.clip(imgArrayG, 0, 255).astype('uint8')
    imgArrayB = np.clip(imgArrayB, 0, 255).astype('uint8')

    rr=Image.fromarray(imgArrayR)
    gg=Image.fromarray(imgArrayG)
    bb=Image.fromarray(imgArrayB)
    return Image.merge("RGB" ,(rr,gg,bb))

def doglSlicing(img, h, w, a, b): #圖的陣列,高,寬,變白色的範圍(a,b)
    for i in range(h):
        for j in range(w):
            p=img[i][j]
            if(p>a and p<=b):img[i][j]=255
            else:img[i][j]=0
            #if(p>c and p<=d):img[i][j]=0
    return img
    
def laplacian(img, w, h, v): #輸入圖的矩陣,長,寬,銳利程度
    kernal=np.array([[0,1,0],[1,-4,1],[0,1,0]])*v
    sol=np.zeros_like(img).astype('float') #跟img尺寸相同的0矩陣
    img_padded = np.pad(img, ((1,1), (1,1)), mode='reflect')  # 邊界填充
    #將遮罩應用到影像的每一個像素上 (較快)
    for i in range(3):
        for j in range(3):
            sol += kernal[i, j] * img_padded[i:i + h, j:j + w] #sol[x,y]=∑(kernel[i,j]×img[x+i,y+j])
    sol = np.clip(sol,0,255).astype('uint8')
    return sol

def gaussian(img, w, h, k, sigma): #img:圖片(array),w:寬, h:長, k:kernel大小, sigma:標準差(越大中型曲線越胖)
    k1=0-k//2
    k2=1+k//2
    kx, ky=np.mgrid[k1:k2, k1:k2] #ex: np.mgrid[-1:2,-1:2]=[ [[-1 -1 -1][0 0 0][1 1 1]] [[-1 0 1][-1 0 1][-1 0 1]] ]
    kernal=np.exp(-(kx**2+ky**2)/(2*(sigma**2)))/((2*math.pi*(sigma**2))**0.5)
    kernal /= np.sum(kernal) # 正規化，使權重總和為1
    #print(kernal, np.sum(kernal))
    sol=np.zeros_like(img).astype('float') #跟img尺寸相同的0矩陣
    img_padded = np.pad(img, ((-k1, -k1), (-k1, -k1)), mode='reflect')  # 邊界填充
    
    #將高斯遮罩應用到影像的每一個像素上 (較快)
    for i in range(k):
        for j in range(k):
            sol += kernal[i, j] * img_padded[i:i + h, j:j + w] #sol[x,y]=∑(kernel[i,j]×img[x+i,y+j])
    
    """
    for i in range(h-k):
        for j in range(w-k):
            #print(img[i:i+k,j:j+k])
            sol[i-k1][j-k1]=np.sum(kernal*img[i:i+k,j:j+k])
    """
    return sol

def RGBtoGray(img): #圖片 -> 矩陣
    w, h = img.size
    img = np.array(img).astype(float)
    # 使用加權公式轉換為灰階
    sol = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[:, :, 2]
    #sol = (img[0:h, 0:w, 0] + img[0:h, 0:w, 1] + img[0:h, 0:w, 2]) / 3
    sol=np.clip(sol,0,255).astype('uint8')
    #print(sol)
    return sol



if __name__ == "__main__": #直接執行此程式才會出現，在其他程式中用到此程式時不會執行以下程式碼
    image = './photo/a.png' #Lenna_512_color.tif #test.png
    img = Image.open(image)
    #print(int(1//0.3))
    #print(np.array(img).shape)
    img = painting(img,'brown2')
    #img = pencilB(img)
    img.show()
"""
w, h = img.size
img = RGBtoGray(img)
img2=img.copy()
img = gaussian(img, w, h,25)
img = img2/img*250
result = Image.fromarray(img)
result.show()
"""

"""
k=25
sigma=1.5
k1=0-k//2
k2=1+k//2
kx, ky=np.mgrid[k1:k2, k1:k2] #ex: np.mgrid[-1:2,-1:2]=[ [[-1 -1 -1][0 0 0][1 1 1]] [[-1 0 1][-1 0 1][-1 0 1]] ]
kernal=np.exp(-(kx**2+ky**2)/(2*(sigma**2)))/(2*math.pi*(sigma**2))
print(kernal)
"""