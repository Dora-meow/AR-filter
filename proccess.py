import subprocess
import numpy as np
import os
import threading
from PIL import Image
import pandas as pd
import time
import face
import background as bd
#調整亮度以log
def adjust_contrast_brightness(image_array,c,image_output=True,image_color=[True,True,True]):
    try:
        if c>32:
            raise print("c太大")
        image_array=image_array.astype(np.float32)
        print(image_array)
        for i in range(3):
            if image_color[i]==True:
                image_array[:,:,i]=c*np.log2(1+image_array[:,:,i])
        image_array=image_array.astype(np.uint8)
    finally:
        if image_output:
            return Image.fromarray(image_array)
        else:
            return image_array
#把影像繪製成暖色調
def warm(image_array,value,image_output=True,RGB=True):
    if RGB:
        if value>1:
            print("value<1")
        else:
            image_array[:,:,0]=np.minimum(image_array[:,:,0]/(value+1e-10),255)
            image_array.astype(np.int8)
    else:
        if value>1:
            print("value<1")
        else:       
            hsi=HSI(image_array)
            hsi["H"]=hsi["H"]*value
            image_array=HSI_to_RGB(hsi)
    if image_output:
        return Image.fromarray(image_array)
    else:
        return image_array
#RGB轉HSI
def HSI(image_array):
    R=image_array[:,:,0].astype(np.float32) / 255.0
    G=image_array[:,:,1].astype(np.float32) / 255.0
    B=image_array[:,:,2].astype(np.float32) / 255.0
    I=(R + G + B) / 3  # 計算 Intensity
    min_rgb = np.minimum(np.minimum(R, G), B)
    S = 1 - (3 / (R + G + B + 1e-10)) * min_rgb  # 計算 Saturation，避免除以零
    # 計算 Hue
    numerator = 0.5 * ((R - G) + (R - B))
    denominator = np.sqrt((R - G)**2 + (R - B) * (G - B)) + 1e-10  # 避免分母為零
    denominator[denominator == 0] = 1e-10  # 額外檢查，確保安全
    # 處理分母為零的情況
    theta = np.arccos(np.clip(numerator / denominator, -1, 1))  # 限制範圍 [-1, 1]
    H = np.where(B > G,2*np.pi-theta,theta)  # 調整 Hue 的值
    H = H / ( 2 * np.pi)*360  # 將 Hue 正規化到 [0, 360]
    return {"H": H, "S": S, "I": I}
#HSI轉RGB
def HSI_to_RGB(HSI):
    # 初始化 RGB
    H=HSI["H"]
    S=HSI["S"]
    I=HSI["I"]
    R = np.zeros_like(H)
    G = np.zeros_like(H)
    B = np.zeros_like(H)
    shape=(H.shape[0],H.shape[1],3)
    RGB = np.zeros(shape=shape,dtype=np.uint8)
    # 紅色主導區域
    mask1 = (H >= 0) & (H < 120)
    H1 = np.deg2rad(H[mask1])
    R[mask1] = I[mask1] * (1 + S[mask1] * np.cos(H1) / np.cos(np.deg2rad(60) - H1))
    B[mask1] = I[mask1] * (1 - S[mask1])
    G[mask1] = 3*I[mask1] - (R[mask1] + B[mask1])
    # 綠色主導區域
    mask2 = (H >= 120) & (H < 240)
    H2 = np.deg2rad(H[mask2] - 120)
    G[mask2] = I[mask2] * (1 + S[mask2] * np.cos(H2) / np.cos(np.deg2rad(60) - H2))
    R[mask2] = I[mask2] * (1 - S[mask2])
    B[mask2] = 3 * I[mask2] - (R[mask2] + G[mask2])
    # 藍色主導區域
    mask3 = (H >= 240) & (H <= 360)
    H3 = np.deg2rad(H[mask3] - 240)
    B[mask3] = I[mask3] * (1 + S[mask3] * np.cos(H3) / np.cos(np.deg2rad(60) - H3))
    G[mask3] = I[mask3] * (1 - S[mask3])
    R[mask3] = 3 * I[mask3] - (G[mask3] + B[mask3])
    # 確保 RGB 範圍 [0, 255]
    R=np.clip(R * 255, 0, 255).astype(np.uint8)
    G=np.clip(G * 255, 0, 255).astype(np.uint8)
    B=np.clip(B * 255, 0, 255).astype(np.uint8)
    RGB[:,:,0]=R
    RGB[:,:,1]=G
    RGB[:,:,2]=B
    return RGB  # 合併為 RGB 圖像
# image_output是要不要輸出圖片
def medium(array,split, image_output=True):
    try:
        # 使用管道與 C++ 程式通訊
        row_size, col_size = array.shape
        input_data = "\n".join(" ".join(map(str, row)) for row in array)
        #print(split)
        command = ["./medium", str(row_size), str(col_size), str(split)]
        result = subprocess.run(command, input=input_data, text=True, capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0:
            print(f"處理 失敗，錯誤訊息: {result.stderr}")
            return None
        # 解析輸出
        #print( result.stdout)

        output_data = result.stdout.strip()
        rows = output_data.split("\n")
        
        """
        for i, row in enumerate(rows):
            print(f"Row {i} length: {len(row.split(','))}")
        """
        matrix = np.array([list(map(int, row.split(','))) for row in output_data.split("\n")])
        #print(matrix)
        return Image.fromarray(matrix.astype(np.uint8)) if image_output else matrix
    except Exception as e:
        print(f"處理 時發生錯誤: {e}")
        return None
"""
帶進image_array,split是決定要捨棄多少圖檔範圍去取直越大越模糊 image_output是要不要輸出圖片
"""
def medium_RGB(image_array,split=1,image_output=True):
    row_size,col_size,_=image_array.shape
    image_array=image_array[::split,::split,:]
    # 創建線程列表
    result_list = [None, None, None]
    # 定義線程的處理函數
    def process_channel(i, text, result_list):
        result_list[i] = medium(image_array[:, :, i], text, False)
    threads = [
        threading.Thread(target=process_channel, args=(0,split, result_list)),
        threading.Thread(target=process_channel, args=(1,split, result_list)),
        threading.Thread(target=process_channel, args=(2,split, result_list))
    ]
    for t in threads:
        t.start()
    # 等待所有線程完成
    for t in threads:
        t.join()
    # 組合三個通道的結果
    channel_shape = result_list[0].shape  # 每個通道應該具有相同的 2D 大小
    result = np.zeros((*channel_shape, 3), dtype=np.uint8)
    result[:, :, 0] = result_list[0]
    result[:, :, 1] = result_list[1]
    result[:, :, 2] = result_list[2]
    if image_output:
        return Image.fromarray(result)
    else:
        return result
#item_name為result_{item_name.xxx} image_output是要步要輸出image mage_x,mage_y是物件大小 x,y是物件要放在拿李
def item(image_array,item_name='item1.png',image_output=True,magn_x=1,magn_y=1,x=0,y=0):
    try:
        item_path="./photo/item_"+item_name
        item_image=Image.open(item_path)
        item_image=item_image.resize((60,60))
        item_array=np.array(item_image)
        item_shape=item_array.shape
        resized_item = item_image.resize((item_shape[1]*magn_y, item_shape[0]*magn_x))
        item_array=np.array(resized_item)
        image_shape=image_array.shape
        item_shape=item_array.shape
        base=np.zeros_like(image_array)
        n=np.sum(item_array,axis=2)
        mask=(n<20)
        mask_expanded = np.expand_dims(mask, axis=-1)  # 變形為 (60, 60, 1)
        mask= np.repeat(mask_expanded, 3, axis=-1)  # 重複成 (60, 60, 3)
        base[y:y+item_shape[0],x:x+item_shape[1],:] = np.where(mask[:,:None], base[y:y+item_shape[0], x:x+item_shape[1], :], item_array)
        mask=(base==0)
        result_array = np.where(mask, image_array, base)
        if image_output:
            return Image.fromarray(result_array)
        else:
            return result_array
    except Exception as e:
        print(e)
        if image_output:
            return Image.fromarray(image_array)
        else:
            return image_array
#draw要帶物品put_on要True(defualt) mage_x,mage_y是調物件大小 dx,dy為相對於人臉要放拿,item_name為result_{item.xxx}
def draw(image_array,item_name='item5.png',image_output=True,magn_x=1,magn_y=1,dx=0,dy=0,face=False,put_on=True):
    try:
        step=4
        O_image_array=image_array
        hsi=HSI(image_array)
        hsi["I"][(hsi["H"]<256)&(hsi["I"]>0.7)]=0
        image_array=hsi["I"]*255
        img=Image.fromarray(image_array.astype(np.int8))
        img = img.convert("L")  # 將浮點數轉換為灰階
        img.save("./photo/example.png")
        coordinates = np.where(image_array>0)
        x_coords = np.array(coordinates[1])
        y_coords= np.array(coordinates[0])
        std_x=np.std(x_coords)
        avg_x=np.mean(x_coords)
        avg_y=np.mean(y_coords)
        std_y=np.std(y_coords)
        count=0
        while std_x*std_y>0.6 and count<3:#把離群值拿掉
            # 定義有效範圍
            valid_x=(x_coords >= avg_x - std_x) & (x_coords <= avg_x + std_x)
            valid_y=(y_coords >= avg_y - std_y) & (y_coords <= avg_y + std_y)           
            # 找出同時符合範圍的點
            valid_indices = valid_x & valid_y      
            # 過濾掉不符合條件的點
            x_coords = x_coords[valid_indices]
            y_coords = y_coords[valid_indices]       
            # 重新計算標準差和平均值
            std_x = np.std(x_coords)
            avg_x = np.mean(x_coords)
            std_y = np.std(y_coords)
            avg_y = np.mean(y_coords)
            count+=1
        """
        coord=np.array(list(zip(x_coords,y_coords)))
        mask=np.zeros_like(O_image_array[:,:,0])
        for x, y in coord:
            mask[x, y] =O_image_array[x,y,0]
        img=Image.fromarray(mask.astype(np.int8))
        img = img.convert("L")  # 將浮點數轉換為灰階
        img.save("./photo/mask.png")
        """
        height, width,_ = O_image_array.shape
        x_min = x_coords.min()
        x_max = x_coords.max()
        y_min = y_coords.min()
        y_max = y_coords.max()
        x_min = max(x_min,5)
        x_max = min(x_max,height-5)
        y_min = max(y_min,5)
        y_max = min(y_max,width-5)
        if put_on:
            dx=x_max-x_min-dx
            dy=y_max-y_min-dy
            image_array=item(O_image_array,item_name=item_name,image_output=False,magn_x=magn_x,magn_y=magn_y,x=x_min-dx,y=y_min-dy)
        if face:
            mask=np.zeros_like(image_array,dtype=bool)
            mask[x_min:x_min+4, y_min:y_max] = True
            mask[x_max-4:x_max, y_min:y_max] = True
            mask[x_min:x_max, y_min:y_min+4] = True
            mask[x_min:x_max, y_max-4:y_max] = True
            O_image_array[mask]=0
            image_array=O_image_array
        if image_output:
            return Image.fromarray(image_array)
        else:
            return image_array
        """
        image_array=HSI_to_RGB(hsi)
        height, width,_ = image_array.shape
        #我要知道save[x][y]==0的x,y座標最大值和最小值
        coordinates = np.where(save>0)
        x_coords = coordinates[0]
        y_coords= coordinates[1]
        # 計算最大值和最小值
        x_min = x_coords.min()
        x_max = x_coords.max()
        y_min = y_coords.min()
        y_max = y_coords.max()
        x_min = max(x_min,5)
        x_max = min(x_max,height-5)
        y_min = max(y_min,5)
        y_max = min(y_max,width-5)
        print(x_min, x_max, y_min, y_max)
        mask = np.zeros((height, width), dtype=bool)
        n=face.detect_face(image_array[::step,::step,:])
        std=np.std(n,axis=0)
        while std[0]*std[1]>0.8:#把離群值拿掉
            a=np.mean(n,axis=0,dtype=np.int64)
            n=np.where((n>=a-0.8*std)&(n<=a+0.8*std),n,np.array([a[0], a[1]]))
            std=np.std(n,axis=0)
        if len(n)==0:
            return O_image_array
        a=np.mean(n,axis=0,dtype=np.int64)
        Max_x=np.max(n[0])
        Min_x=np.min(n[0])
        Max_y=np.max(n[1])
        Min_y=np.min(n[1])
        threshold_x=(Max_x-Min_x)*step//2
        threshold_y=(Max_y-Min_y)*step//2
        face_x_min, face_x_max = max(a[0] - threshold_x, 0), min(a[0] + threshold_x, height)
        face_y_min, face_y_max = max(a[1] - threshold_y, 0), min(a[1] + threshold_y, width)
        face_x_min, face_x_max, face_y_min, face_y_max=step*face_x_min,step*face_x_max,step*face_y_min,step*face_y_max
        a=0.2
        b=1-a
        x_min=int(face_x_min*a+x_min*b)
        y_max=int(face_x_max*a+x_max*b)
        y_min=int(face_y_min*a+y_min*b)
        y_max=int(face_x_max*a+x_max*b)
        mask[x_min:x_min+4, y_min:y_max] = True
        mask[x_max-4:x_max, y_min:y_max] = True
        mask[x_min:x_max, y_min:y_min+4] = True
        mask[x_min:x_max, y_max-4:y_max] = True
        O_image_array[mask] = 0
        print(x_min,x_max,y_min, y_max)
        """
    except Exception as e:
        print(e)
        if image_output:
            return Image.fromarray(O_image_array)
        else:
            return O_image_array
def Whitening(image_array,value=1,image=True):
    hsi=HSI(image_array)
    height, width,_ = image_array.shape
    #print(hsi['H'])
    mask = np.where((hsi["I"]>0.2),True,False)
    #print(mask)
    hsi['I']=np.where(mask,hsi['I']*value,hsi['I'])
    if image==False:
        return HSI_to_RGB(hsi)
    else:
        return Image.fromarray(HSI_to_RGB(hsi))
def generate_background(name='background.jpg'):#生成background帶進圖檔名 要把background存在photo下
    bd.background_gernate(name)
def background(image_array,background_name='background.jpg'):#image_array,background的圖片，background的黑色為image
    background_path="./photo/result_"+background_name
    background_array=np.array(Image.open(background_path))
    image_shape=image_array.shape
    background_shape=background_array.shape
    if image_shape!=background_shape:
        background_image=Image.open(background_path)
        resized_background = background_image.resize((image_shape[1], image_shape[0]))
        background_array=np.array(resized_background)
    n=np.sum(background_array,axis=2)
    mask=(n<20)
    image_shape=image_array.shape
    background_shape=background_array.shape
    result_array = np.where(mask[:, :, None], image_array, background_array)
    return Image.fromarray(result_array)
if __name__ == "__main__":#test
    image = './photo/a.png'
    img = Image.open(image)
    image_array = np.array(img)
    start=time.time()
    result=medium_RGB(image_array)
    #hsi["I"][hsi["I"]<0.1]=1
    #hsi["I"][(hsi["I"]>1)]=0
    #hsi["I"][(hsi["H"]>50)]=0
    #hsi["I"][(hsi["S"]>0.75)]=0
    #print(hsi["H"])
    #result=Whitening(image_array,2,False)
    #result=draw(image_array,put_on=False,face=True)
    #result=medium_RGB(result)
    #result=item(image_array,"item1.png")
    #result=adjust_contrast_brightness(image_array,c=30)
    #result=warm(image_array,0.1,RGB=True)
    result.show()
    """
    result=draw(image_array)
    end=time.time()
    print(end-start)
    result.show()
    t=background(image_array)
    result = medium_RGB(image_array,split=3)
    end=time.time()
    print(end-start)
    result.show()
    end=time.time()
    print(end-start)
    """
