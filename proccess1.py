import subprocess
import numpy as np
import os
import threading
from PIL import Image

def medium(array, text, image=True):  # 傳np.array 如果要輸出np.array請改False 預設輸出圖檔
    np.savetxt(text, array, fmt='%d')
    row_size, col_size = array.shape
    # 構建命令
    command = ["./medium1", str(row_size), str(col_size), text]
    # 執行命令
    result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    os.remove(text)  # 刪除臨時文件
    if result.returncode == 0:
        print(f"處理 {text} 失敗，錯誤訊息: {result.stderr}")
        return None
    # 獲取返回數據
    rows = [row.strip() for row in result.stdout.strip().split("\n") if row.strip()]
    matrix = [list(map(int, row.split())) for row in rows]
    if not image:
        return np.array(matrix)
    else:
        return Image.fromarray(np.array(matrix, dtype=np.uint8))

def medium_RGB(image_array):
    row_size, col_size, _ = image_array.shape
    result = np.zeros(shape=(row_size, col_size, 3), dtype=np.uint8)

    # 創建線程列表
    threads = []
    r_result = None
    g_result = None
    b_result = None

    # 定義線程的處理函數
    def process_channel(i, text, result_list):
        nonlocal r_result, g_result, b_result
        channel_result = medium(image_array[:,:,i], text, False)
        if i == 0:
            r_result = channel_result
        elif i == 1:
            g_result = channel_result
        elif i == 2:
            b_result = channel_result

    # 創建線程
    a = threading.Thread(target=process_channel, args=(0, "R.txt", r_result))
    b = threading.Thread(target=process_channel, args=(1, "G.txt", g_result))
    c = threading.Thread(target=process_channel, args=(2, "B.txt", b_result))

    # 啟動線程
    a.start()
    b.start()
    c.start()

    # 等待所有線程完成
    a.join()
    b.join()
    c.join()

    # 合併顏色通道
    result[:,:,0] = r_result
    result[:,:,1] = g_result
    result[:,:,2] = b_result

    return Image.fromarray(result)

if __name__ == "__main__":
    image = './photo/a.png'
    img = Image.open(image)
    image_array = np.array(img)
    result = medium_RGB(image_array)
    result.show()
