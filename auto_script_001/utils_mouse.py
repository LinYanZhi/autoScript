import pyautogui
import time
import math
import random


class MouseController:
    """鼠标控制类，提供各种鼠标操作方法"""
    
    def __init__(self, move_duration=0.5, pause_between_actions=0.1):
        """
        初始化鼠标控制器

        参数:
            move_duration: 默认的鼠标移动持续时间(秒)
            pause_between_actions: 操作之间的默认暂停时间(秒)
        """
        self.move_duration = move_duration
        self.pause_between_actions = pause_between_actions
        pyautogui.FAILSAFE = True  # 启用安全特性(鼠标移动到屏幕左上角会触发异常)
    
    def move_to(self, x, y, duration=None, smooth=True):
        """
        移动鼠标到指定位置

        参数:
            x: 目标X坐标
            y: 目标Y坐标
            duration: 移动持续时间，None则使用默认值
            smooth: 是否使用平滑移动(有轨迹)
        """
        if duration is None:
            duration = self.move_duration
        
        if smooth:
            # 使用贝塞尔曲线生成平滑移动轨迹
            current_x, current_y = pyautogui.position()
            self._bezier_move(current_x, current_y, x, y, duration)
        else:
            # 瞬间移动
            pyautogui.moveTo(x, y, duration=0)
    
    def _bezier_move(self, start_x, start_y, end_x, end_y, duration):
        """使用贝塞尔曲线实现平滑的鼠标移动"""
        # 计算中间控制点
        cp1_x = start_x + (end_x - start_x) * 0.3 + random.randint(-10, 10)
        cp1_y = start_y + (end_y - start_y) * 0.3 + random.randint(-10, 10)
        cp2_x = start_x + (end_x - start_x) * 0.7 + random.randint(-10, 10)
        cp2_y = start_y + (end_y - start_y) * 0.7 + random.randint(-10, 10)
        
        # 生成曲线上的点
        points = []
        steps = max(10, int(duration * 30))  # 根据持续时间确定步数
        for t in range(steps + 1):
            t /= steps
            x = (1 - t) ** 3 * start_x + 3 * (1 - t) ** 2 * t * cp1_x + 3 * (1 - t) * t ** 2 * cp2_x + t ** 3 * end_x
            y = (1 - t) ** 3 * start_y + 3 * (1 - t) ** 2 * t * cp1_y + 3 * (1 - t) * t ** 2 * cp2_y + t ** 3 * end_y
            points.append((x, y))
        
        # 移动鼠标经过这些点
        for x, y in points:
            pyautogui.moveTo(x, y, duration=0)
            time.sleep(duration / steps)
    
    def click(self, button='left', clicks=1, interval=0.1):
        """
        点击鼠标

        参数:
            button: 按钮类型('left', 'right', 'middle')
            clicks: 点击次数
            interval: 多次点击之间的间隔时间(秒)
        """
        pyautogui.click(button=button, clicks=clicks, interval=interval)
        time.sleep(self.pause_between_actions)
    
    def left_click(self, clicks=1, interval=0.1):
        """点击左键"""
        self.click(button='left', clicks=clicks, interval=interval)
    
    def right_click(self, clicks=1, interval=0.1):
        """点击右键"""
        self.click(button='right', clicks=clicks, interval=interval)
    
    def double_click(self):
        """双击左键"""
        self.left_click(clicks=2, interval=0.1)
    
    def right_double_click(self):
        """双击右键"""
        self.right_click(clicks=2, interval=0.1)
    
    def press(self, button='left'):
        """按下鼠标按钮不放"""
        pyautogui.mouseDown(button=button)
    
    def release(self, button='left'):
        """释放鼠标按钮"""
        pyautogui.mouseUp(button=button)
    
    def drag_to(self, x, y, duration=None, button='left'):
        """
        从当前位置拖动鼠标到指定位置

        参数:
            x: 目标X坐标
            y: 目标Y坐标
            duration: 拖动持续时间，None则使用默认值
            button: 拖动时按下的按钮
        """
        if duration is None:
            duration = self.move_duration
        
        pyautogui.dragTo(x, y, duration=duration, button=button)
    
    def scroll(self, amount_to_scroll, direction='vertical'):
        """
        滚动鼠标滚轮

        参数:
            amount_to_scroll: 滚动量(正数向上/右滚动，负数向下/左滚动)
            direction: 滚动方向('vertical'或'horizontal')
        """
        if direction.lower() == 'vertical':
            pyautogui.scroll(amount_to_scroll)
        elif direction.lower() == 'horizontal':
            pyautogui.hscroll(amount_to_scroll)
        else:
            raise ValueError("方向必须是'vertical'或'horizontal'")
        
        time.sleep(self.pause_between_actions)


if __name__ == "__main__":
    # 使用示例
    mouse = MouseController(move_duration=0.8)
    
    try:
        # 移动到屏幕中央(1920x1080分辨率)
        screen_width, screen_height = pyautogui.size()
        center_x, center_y = screen_width // 2, screen_height // 2

        # 平滑移动到中心并点击
        mouse.move_to(center_x, center_y)
        mouse.left_click()

        # 移动到右上角并右键点击
        mouse.move_to(screen_width - 100, 100)
        mouse.right_click()

        # 双击中心位置
        mouse.move_to(center_x, center_y)
        mouse.double_click()

        # 按住左键并拖动
        mouse.move_to(center_x - 200, center_y)
        mouse.press()
        mouse.drag_to(center_x + 200, center_y, duration=1.5)
        mouse.release()
        

    
    except pyautogui.FailSafeException:
        print("安全模式触发，程序已停止")
    except Exception as e:
        print(f"发生错误: {e}")
