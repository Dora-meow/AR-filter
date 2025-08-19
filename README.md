# AR-filter
AR濾鏡

## 簡介
運用影像處理的基礎原理，用python與C++實作出AR濾鏡，下面的功能可以疊加使用

主要功能：
1. 濾鏡
    * 素描、點畫、美式漫畫
    * 魚眼鏡頭
    * 老照片、負片
    * RGB失真(壞掉的電視)
    * 浮雕
    * 直方圖均化 
    * 分割畫面：可選要切幾次(1次會把1張圖分4塊)
    * 像素畫
    * 調亮
    * 美肌
    * 暖色調
    * 其他質感(布、紙、漸層等)

2. 邊框
    * 有一些預設邊框可以選，例如:張大嘴巴的巨人、相框
    * 可自己上傳圖片，會自動去背
3. 貼圖
    * 有一些預設邊框可以選，例如:雙馬尾髮型、墨鏡、項鍊等
    * 可自己上傳圖片，會自動去背
    * 可自動找到臉的位置
    * 可手動調整圖片大小跟位置

4. 可隨時儲存照片

## 程式原理與介面
### 首頁 (按 open 按鈕後相機就會開啟)
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 143254" src="https://github.com/user-attachments/assets/c1c12360-4246-47d8-8194-97107a01f79b" />

### 濾鏡
用Lenna的效果
<img width="1919" height="992" alt="image" src="https://github.com/user-attachments/assets/7c16c0c3-17f8-49c2-b5d1-227f6077a869" />

#### 素描 (pencil)
原理：圖轉灰階 ➜ 做高斯模糊 ➜ 處理後的圖/原圖 *250 (模糊效果越強變化率越大) ➜ 做指數運算(調亮)<br>
運用 numpy array (`sol[x,y]=∑(kernel[i,j]×img[x+i,y+j]`) 來加速高斯運算
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 114408" src="https://github.com/user-attachments/assets/ca42ef26-923a-4a3b-888b-1afa43815974" />

#### 點畫 (pen)
原理：做3*3 medium filter
➜ 圖轉灰階 
➜ 做拉普拉斯遮罩  (找邊界)
➜ 255-圖 (變化越多的越黑)
➜ 247以上的變255其他0 <br>
一樣運用運用 numpy array 加快拉普拉斯的運算
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 142842" src="https://github.com/user-attachments/assets/415a6935-3e3c-4660-922d-33c045e61983" />

#### 美式漫畫 (animate)
原理：
* 線搞：
圖轉灰階 
➜ 做高斯模糊 
➜ 拉普拉斯遮罩
➜ 247以上的變255其他0
* 著色：
做高斯模糊 
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 155314" src="https://github.com/user-attachments/assets/d0634a21-132c-442c-8e26-74e8ccdd6128" />


#### 魚眼鏡頭 (fish eye)
原理：在圖的中心以1/2高為半徑的圓內把圖往圓周上拉，離圓心越近拉得越開<br>
公式：
$$新的x = 點離圓心的距離*\frac{(目前x-圓心x)}{半徑}  + 圓心x$$
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 160057" src="https://github.com/user-attachments/assets/fb423436-7127-4a86-be8c-93e469e41333" />

#### 
原理：

####
原理：

####
原理：

#### rgb失真 (broken)
原理：分別對RGB做隨機的x軸滾動式偏移<br>
![未命名的影片_ 使用 Clipchamp 製作 (1)](https://github.com/user-attachments/assets/98624a98-c893-4625-8c21-c9072d9649db)

https://github.com/user-attachments/assets/8fb3c1db-986f-4f40-987d-ee6886d6f824

<video scr='https://github.com/user-attachments/assets/8fb3c1db-986f-4f40-987d-ee6886d6f824'></video>

### 儲存圖片
按save按紐可選儲存位置並儲存
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6ea82798-fa66-4637-ba62-bc595cd843fd" />

## 如何安裝
1. 下載專案到電腦本地端的 `Downloads` 資料夾，並移動到專案的資料夾
    ```
    cd %HOMEPATH%\Downloads
    git clone https://github.com/Dora-meow/AR-filter.git
    ```
     * 也可點進[https://github.com/Dora-meow/AR-filter](https://github.com/Dora-meow/AR-filter)
    按綠色的code按鈕下載壓縮檔，並解壓縮


2. 確認python及套件版本 (下面是我使用的版本，不確定用其他版本是否能正常執行)
    * python (3.7.8)
    
    * 套件
        * Pillow (9.0.1)
        * tk (0.1.0)
        * numpy (1.21.6)
        * opencv-python (4.8.1.78)
    
    如果需要，可在在終端機輸入 `pip install -r requirements.txt` 來下載套件 

3. 在終端機輸入 `python final.py` 開啟程式，按畫面中的 `open` 按鈕即可開始使用
    <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6b1d8c03-20f8-4360-b8d7-1990a4e26147" />
