import urllib.parse
import httpx, json
from io import BytesIO
import urllib
import os
from pathlib import Path
from PIL import Image
import numpy as np
import cv2
import requests

def getpic(__pic_url):
    # 发送 HTTP GET 请求，下载图片

    response = requests.get((__pic_url))

    # 检查请求是否成功
    if response.status_code == 200:
        # 将图片内容转换为 NumPy 数组
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

        # 使用 OpenCV 将 NumPy 数组解码为图像
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # 显示图像
        return image
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
    
    return None

def getpic2(__pic_url):
    # 发送 HTTP GET 请求，下载图片

    current_directory = os.path.dirname(os.path.abspath(__file__))

    image = cv2.imread(os.path.join(current_directory,__pic_url))

    # 显示图像
    return image