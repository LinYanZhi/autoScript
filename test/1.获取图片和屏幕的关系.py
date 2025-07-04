import cv2
import numpy as np
from PIL import ImageGrab
import time


def locate_on_screen(template_path, threshold=0.8, grayscale=True):
    """
    在屏幕上定位模板图片的位置

    参数:
        template_path: 模板图片的路径
        threshold: 匹配阈值，值越高匹配越严格，范围0-1
        grayscale: 是否使用灰度模式进行匹配

    返回:
        如果找到，返回匹配区域的左上角坐标(x,y)和中心点坐标，以及匹配度;
        如果未找到，返回None
    """
    # 加载模板图片
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"无法加载模板图片: {template_path}")
    
    # 转换为灰度图(如果需要)
    if grayscale:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    h, w = template.shape[:2]  # 获取模板图片的高度和宽度
    
    # 循环查找，直到找到或超时
    start_time = time.time()
    while time.time() - start_time < 10:  # 设置10秒超时
        # 截取当前屏幕
        screenshot = ImageGrab.grab()
        screen_np = np.array(screenshot)
        screen_cv = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
        
        # 转换为灰度图(如果需要)
        if grayscale:
            screen_cv = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)
        
        # 执行模板匹配
        result = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # 如果匹配度超过阈值，认为找到了
        if max_val >= threshold:
            top_left = max_loc
            center = (top_left[0] + w // 2, top_left[1] + h // 2)
            return {
                'top_left': top_left,
                'center': center,
                'confidence': max_val
            }
        
        # 没找到，等待一下再试
        time.sleep(0.5)
    
    return None  # 超时仍未找到


if __name__ == "__main__":
    # 使用示例
    template_image_path = r"C:\Users\Administrator\Desktop\3.png"  # 替换为实际的模板图片路径
    
    try:
        result = locate_on_screen(template_image_path, threshold=0.7)
        if result:
            print(f"找到图片!")
            print(f"左上角坐标: {result['top_left']}")
            print(f"中心点坐标: {result['center']}")
            print(f"匹配度: {result['confidence']:.2f}")
        else:
            print("未找到匹配的图片，可能图片不在屏幕上或匹配阈值设置过高。")
    except Exception as e:
        print(f"发生错误: {e}")
