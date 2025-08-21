# AR-filter
AR濾鏡

組員：張文睿、陳姵涵、湯昆璋

## 簡介
運用影像處理的基礎原理，用python與C++實作出AR濾鏡，下面的功能皆可以疊加使用

主要功能：
1. 濾鏡
    * 素描、點畫、美式漫畫
    * 魚眼鏡頭
    * 老照片、負片
    * RGB失真(壞掉的電視)
    * 浮雕
    * 直方圖均化 
    * 分割畫面：可選要切幾次(1次會把1張圖分4塊)
    * 各種質感(布、紙、漸層等)
    * 像素畫(馬賽克)
    * 調亮
    * 美肌
    * 暖色調
    

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
### 首頁 
按 open 按鈕後相機就會開啟，所有特效在勾選後按 submit 按鈕才會打開
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 143254" src="https://github.com/user-attachments/assets/c1c12360-4246-47d8-8194-97107a01f79b" />

### 濾鏡
用Lenna的效果
<img width="1919" height="989" alt="image" src="https://github.com/user-attachments/assets/a5cd4850-a2f0-4ae8-9a1f-d7201fef5cd3" />

#### 素描 (pencil)
原理：圖轉灰階 ➜ 做高斯模糊 ➜ 處理後的圖/原圖 *250 (模糊效果越強變化率越大) ➜ 做指數運算(調亮)<br>
運用 numpy array (`sol[x,y]=∑(kernel[i,j]×img[x+i,y+j]`) 來加速高斯運算
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 114408" src="https://github.com/user-attachments/assets/ca42ef26-923a-4a3b-888b-1afa43815974" />

#### 點畫 (pen)
原理：做3*3 medium filter (用C++加速)
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

#### 老照片 (old photo)
公式：
<p>$$R   = 0.393 * R + 0.769 * G + 0.189 * B$$
$$G  = 0.349 * R + 0.686 * G + 0.168 * B$$
$$B   = 0.272 * R + 0.534 * G + 0.131 * B$$</p>
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 160713" src="https://github.com/user-attachments/assets/5ff2ac0d-15be-4d80-bfc0-6f5b583a1717" />

#### 負片 (negative)
公式：
$$圖 = 255-原圖$$
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 160809" src="https://github.com/user-attachments/assets/2e8984f6-7c3e-4a1a-a1f1-2f5127a7ba6a" />

#### rgb失真 (broken)
原理：分別對RGB做隨機的x軸滾動式偏移<br>
<img src="https://github.com/user-attachments/assets/009df65d-57c3-45e9-a163-3f74dd271a08" width="900">

#### 浮雕 (relief)
原理：圖轉灰階
➜ 用遮罩:<br>
<img width="193" height="60" alt="https://latex.codecogs.com/svg.latex?kernel%20=%20%5Cbegin{bmatrix}-1.5&0&0%5C%5C0&1.5&0%5C%5C0&0&0%5Cend{bmatrix}" src="https://github.com/user-attachments/assets/ec6152ee-3abd-4722-a61a-558ff4b97304" />
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 160750" src="https://github.com/user-attachments/assets/481cf208-e576-4562-b292-715077791d01" />

#### 直方圖均化 (auto level)
原理：得到圖片中每個色階值有幾個點，算每個色階值出現的機率 -> 算色階跟數量的CDF -> 全部乘255 -> 四捨五入到整數  (把公式分步驟做)，把圖片的色階值改成調整後的
```
ex : 運算後的陣列 :
              0 1 2 3 4 5
		   s=[0,0,1,2,3,5]  -> 色階0變0,色階1變0,色階2變1,色階3變2,色階4變3,色階5還是5
```
<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 160821" src="https://github.com/user-attachments/assets/373d9e48-2b45-4ca3-86fe-0c718d9faf83" />

#### 分割畫面 (split)
可選要切幾次(1次會把1張圖分4塊)<br>
原理：把圖縮小再複製很多個到對應的位子
<img src="https://github.com/user-attachments/assets/f935473b-c83b-464f-a82d-81b507634a5f" width="900">

#### 各種質感 (materil)
共20種質感可選
<img width="1738" height="385" alt="image" src="https://github.com/user-attachments/assets/e48e121d-d059-445a-b161-d25e935a10d7" />

原理：影像跟素材調整透明度，有的影像有先用用中位數遮罩(如canva, oil painting...)<br>
公式：d*(照片/255)+(1-d)*(素材/255)
<img width="1123" height="445" alt="image" src="https://github.com/user-attachments/assets/af122c3c-8687-42c0-86c4-d5bd649d8a7e" />


#### 像素畫 (pixelate)
原理：用numpy切片，每 a * a 像素取1點 ➜ 用 3*3 median filter 去雜訊 (C++加速) ➜ 橫向插值，每個點橫向放大回 a 個 (公式：
$$a點中第k個點 = 第1個點 +  6 * diff * (\frac{k}{a})^5 - 15 * diff * (\frac{k}{a})^4 + 10 * diff * (\frac{k}{a})^3$$) (C++加速) ➜ 用相通公式縱向插值，每個點縱向放大回 a 個 (C++加速)<br>
<img src="https://github.com/user-attachments/assets/8b5592fb-4b40-466c-9e3d-e918edf5a329" width="900">

#### 調亮 (brightness)
原理：以log去調整RBG的光強度c*log2(1+f(x,y))
![light-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/5c4c723d-ed58-4dc7-866f-df8e802e5fa1)

#### 暖色調
原理：直接調R值
![warm-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/492ff4f1-07e9-4fbe-9283-543f3452f31c)

#### 美肌
原理：取HSI的I值>0.2來調整
![white-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/045c3a48-6f27-4aa0-83cb-97e378de0733)

### 邊框
可往右滑，點選一個邊框，把 `use background` 打勾，按 `submit` 就會出現<br>
原理：把圖片黑色部分都換成同一位置的影像(用np.where)
* 使用者上傳圖片會先去背<br>
   把整張圖片中出現頻率最高的顏色±閥值(30)範圍內的變成黑色

### 貼圖
可往右滑，點選一個圖案，把 `use item` 打勾，按 `submit` 就會出現<br>
size調整放大倍數，absolute position 調整圖案在畫面中的位置<br>
原理：把圖片黑色部分去除，圖片貼到影像中的指定位置
* 使用者上傳圖片會先去背，跟邊框相同
* 偵測人臉<br>
   以人臉的HSI裡的H值去做解取，並找出將對於集中之區域以平均坐標取作偵測人臉的位置

### 推薦組合
1. 底片邊框+紙的質感+老照片的濾鏡
	<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-19 161021" src="https://github.com/user-attachments/assets/c18742e3-bdce-426a-88b1-762245e0d056" />

2. 電視邊框+RGB偏差+負片開開關關
	![broken-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/6a4e045e-19f4-4f94-8d59-8db30d952bf9)

3. 萬聖節+負片
	<img width="1920" height="1080" alt="螢幕擷取畫面 2025-08-22 013806" src="https://github.com/user-attachments/assets/be6985b3-17c6-4fcc-9033-a4d204945c39" />

4. 相機畫面+畫布質感+兔耳朵
	<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/79881d16-60bd-4471-b377-942f341aa3fd" />


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
