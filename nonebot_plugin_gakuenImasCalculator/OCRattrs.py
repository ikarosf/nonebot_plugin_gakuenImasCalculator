import cv2
import numpy as np
import easyocr
import os
from .downloadpic import getpic , getpic2

# 读取大图片和图标图片
current_directory = os.path.dirname(os.path.abspath(__file__))

red_image = cv2.imread(os.path.join(current_directory,'red.png'), cv2.IMREAD_UNCHANGED)
blue_image = cv2.imread(os.path.join(current_directory,'blue.png'), cv2.IMREAD_UNCHANGED)
yellow_image = cv2.imread(os.path.join(current_directory,'yellow.png'), cv2.IMREAD_UNCHANGED)
reader = easyocr.Reader([])
# 将图片转换为灰度图

# 如果图标图像有透明通道，我们需要只使用 BGR 通道
if red_image.shape[2] == 4:
    red_image = cv2.cvtColor(red_image, cv2.COLOR_BGRA2BGR)
if blue_image.shape[2] == 4:
    blue_image = cv2.cvtColor(blue_image, cv2.COLOR_BGRA2BGR)
if yellow_image.shape[2] == 4:
    yellow_image = cv2.cvtColor(yellow_image, cv2.COLOR_BGRA2BGR)

def getattrs(url):
    ret = []
    large_image = getpic(url)
    if large_image is None:
        return []
    if large_image.shape[2] == 4:
        large_image = cv2.cvtColor(large_image, cv2.COLOR_BGRA2BGR)

    best_match_scale = None
    for icon_image in [red_image,blue_image,yellow_image]:
        # 创建一个空变量来记录最佳匹配
        best_match_val = -1
        best_match_location = None
        
        best_match_rectangle = None

        # 定义多尺度匹配的缩放范围（缩放倍数）
        if best_match_scale is None:
            scales = np.linspace(0.5, 2.0, 20)  # 从 0.5 到 2 倍进行 20 步缩放
        else:
            scales = [best_match_scale]

        # 在多个缩放级别上进行模板匹配
        for scale in scales:
            # 调整图标尺寸
            scaled_icon = cv2.resize(icon_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            w, h = scaled_icon.shape[1], scaled_icon.shape[0]  # 获取缩放后的宽和高

            # 进行模板匹配
            res = cv2.matchTemplate(large_image, scaled_icon, cv2.TM_CCOEFF_NORMED)

            # 获取匹配结果中最佳匹配的位置和值
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # 记录最佳匹配
            if max_val > best_match_val:
                best_match_val = max_val
                best_match_location = max_loc
                best_match_scale = scale
                best_match_rectangle = [max_loc, (max_loc[0] + w, max_loc[1] + h)]

        # 在大图上绘制最佳匹配位置的矩形框
        if best_match_rectangle is not None:
            top_left = best_match_rectangle[0]
            bottom_right = best_match_rectangle[1]
            width = bottom_right[0] - top_left[0]
            # 将匹配区域往右移动一个宽度距离
            new_top_left_x = top_left[0] + width
            new_bottom_right_x = bottom_right[0] + 3 * width  # 宽度扩大2倍
            new_top_left_y = top_left[1]
            new_bottom_right_y = bottom_right[1]

            cropped_image = large_image[new_top_left_y:new_bottom_right_y, new_top_left_x:new_bottom_right_x]

            print(f"Best match at location: {best_match_location} with scale: {best_match_scale} and confidence: {best_match_val}")

            # 显示结果
            #cv2.imshow('Matched Image', cropped_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            result = reader.readtext(cropped_image,allowlist="0123456789")
            if len(result) > 0:
                ret.append(result[0][1])
            else:
                return []
        else:
            print("No match found.")
            return []
    return ret


if __name__ == "__main__":
    ret = getattrs("test2.jpg")
    print(ret)