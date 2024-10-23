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
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# 禁用不安全的警告
requests.packages.urllib3.disable_warnings()

# 自定义 SSL 上下文适配器
class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = self.ssl_context or ssl.create_default_context()
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# 创建自定义 SSL 上下文并进行配置
ssl_context = ssl.create_default_context()

# 如果需要，禁用证书验证
ssl_context.check_hostname = False  # 禁用主机名检查
ssl_context.verify_mode = ssl.CERT_NONE  # 不验证证书

# 只允许 AES 加密
ssl_context.set_ciphers('AES')

# 如果需要自定义 CA 证书文件，可以指定 cafile
# ssl_context = ssl.create_default_context(cafile="/path/to/your/cafile.pem")

# 创建会话并安装自定义 SSL 适配器
session = requests.Session()
adapter = SSLAdapter(ssl_context=ssl_context)
session.mount('https://', adapter)

def getpic(__pic_url):
    # 发送 HTTP GET 请求，下载图片
    response = session.get(__pic_url, verify=False)

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
    current_directory = os.path.dirname(os.path.abspath(__file__))

    image = cv2.imread(os.path.join(current_directory,__pic_url))

    # 显示图像
    return image


if __name__ == "__main__":
    ret = getpic('http://multimedia.nt.qq.com.cn/download?appid=1406&fileid=CgoyNTExNDYyNTA4EhQfVzcAN61BTyouY_v7PhboAGHN_BjJ5Qkg_gooyvuciOLQiAMyBHByb2RQgLsv&spec=0&rkey=CAESKBkcro_MGujokCQEjS-KTYkIVJASmREiXxD3z7jj0Bs6IXK_pGbJH3s')
    print(ret)