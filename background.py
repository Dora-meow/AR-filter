from PIL import Image
import numpy as np
import os

def background_gernate(image_name='background.jpg'):
    # 開啟圖片
    if os.path.exists(image_name):
        print(1)
        img = Image.open(image_name)
        image_name = image_name.split('/')[-1]
    else:
        print(2)
        img = Image.open("./photo/" + image_name)
    
    image_name = './photo/result_' + image_name
    print(image_name)
    img_array = np.array(img)
    print(img_array.shape)
    
    # 保留原始影像陣列
    O_array = img_array.copy()
    
    # 找出最頻繁的數字
    unique, counts = np.unique(img_array[:,:,0], return_counts=True)
    R = unique[np.argmax(counts)]
    unique, counts = np.unique(img_array[:,:,1], return_counts=True)
    G = unique[np.argmax(counts)]
    unique, counts = np.unique(img_array[:,:,2], return_counts=True)
    B = unique[np.argmax(counts)]
    base = [R, G, B]
    print(base)
    
    # 設定範圍 ±30
    threshold = 30

    # 使用 float64 類型處理數值範圍
    O_array = O_array.astype(np.float64)
    
    # 確保 base 和 threshold 也是 float64 類型
    base = np.array(base, dtype=np.float64)
    threshold = float(threshold)  # 確保 threshold 是浮點數

    # 計算範圍的邏輯掩碼
    mask = (
        (O_array[:, :, 0] >= base[0] - threshold) & (O_array[:, :, 0] <= base[0] + threshold) &
        (O_array[:, :, 1] >= base[1] - threshold) & (O_array[:, :, 1] <= base[1] + threshold) &
        (O_array[:, :, 2] >= base[2] - threshold) & (O_array[:, :, 2] <= base[2] + threshold)
    )

    # 將符合條件的像素改為 [0, 0, 0]
    O_array[mask] = [0, 0, 0]
    
    # 儲存修改後的影像
    result_img = Image.fromarray(np.uint8(O_array))  # 轉回 uint8 類型
    result_img.save(image_name)
    print("成功儲存:)", image_name)

if __name__ == "__main__":
    background_gernate()
    background_gernate("background1.jpg")
