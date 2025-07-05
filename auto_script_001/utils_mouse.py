import time
from pynput.mouse import Button, Controller
from typing import Tuple, Union


class MouseTool:
    """鼠标操作工具类（支持移动、点击、拖拽等操作）"""
    
    def __init__(self):
        """初始化鼠标控制器"""
        self.mouse = Controller()
    
    def move_to(self, x: int, y: int, duration: float = 0) -> None:
        """
        移动鼠标到指定坐标

        参数:
            x: 目标X坐标
            y: 目标Y坐标
            duration: 移动耗时(秒)，0表示瞬间移动
        """
        if duration <= 0:
            self.mouse.position = (x, y)
        else:
            # 平滑移动实现
            start_x, start_y = self.mouse.position
            steps = int(duration * 100)
            for i in range(steps + 1):
                progress = i / steps
                current_x = start_x + (x - start_x) * progress
                current_y = start_y + (y - start_y) * progress
                self.mouse.position = (current_x, current_y)
                time.sleep(duration / steps)
    
    def get_position(self) -> Tuple[int, int]:
        """获取当前鼠标坐标"""
        return self.mouse.position
    
    def click(self, button: Union[str, Button] = 'left',
              times: int = 1,
              interval: float = 0.1) -> None:
        """
        点击鼠标

        参数:
            button: 按钮类型 ('left', 'right', 'middle' 或 Button 对象)
            times: 点击次数
            interval: 多次点击之间的间隔(秒)
        """
        btn = self._parse_button(button)
        for _ in range(times):
            self.mouse.click(btn)
            if times > 1:
                time.sleep(interval)
    
    def press(self, button: Union[str, Button] = 'left') -> None:
        """
        按下鼠标按钮

        参数:
            button: 按钮类型 ('left', 'right', 'middle' 或 Button 对象)
        """
        self.mouse.press(self._parse_button(button))
    
    def release(self, button: Union[str, Button] = 'left') -> None:
        """
        释放鼠标按钮

        参数:
            button: 按钮类型 ('left', 'right', 'middle' 或 Button 对象)
        """
        self.mouse.release(self._parse_button(button))
    
    def hold_click(self, button: Union[str, Button] = 'left',
                   duration: float = 1.0) -> None:
        """
        长按鼠标按钮

        参数:
            button: 按钮类型 ('left', 'right', 'middle' 或 Button 对象)
            duration: 按住时长(秒)
        """
        self.press(button)
        time.sleep(duration)
        self.release(button)
    
    def double_click(self, button: Union[str, Button] = 'left',
                     interval: float = 0.1) -> None:
        """
        双击鼠标

        参数:
            button: 按钮类型 ('left', 'right', 'middle' 或 Button 对象)
            interval: 两次点击之间的间隔(秒)
        """
        self.click(button, times=2, interval=interval)
    
    def scroll(self, dx: int, dy: int) -> None:
        """
        滚动鼠标滚轮

        参数:
            dx: 水平滚动量(正=右，负=左)
            dy: 垂直滚动量(正=上，负=下)
        """
        self.mouse.scroll(dx, dy)
    
    def drag(self, start_x: int, start_y: int,
             end_x: int, end_y: int,
             duration: float = 0.5) -> None:
        """
        拖拽操作(按下-移动-释放)

        参数:
            start_x: 起始X坐标
            start_y: 起始Y坐标
            end_x: 结束X坐标
            end_y: 结束Y坐标
            duration: 拖拽时长(秒)
        """
        self.move_to(start_x, start_y)
        self.press('left')
        self.move_to(end_x, end_y, duration)
        self.release('left')
    
    def _parse_button(self, button: Union[str, Button]) -> Button:
        """将字符串按钮转换为Button对象"""
        if isinstance(button, Button):
            return button
        button = button.lower()
        if button == 'left':
            return Button.left
        elif button == 'right':
            return Button.right
        elif button == 'middle':
            return Button.middle
        else:
            raise ValueError(f"无效的鼠标按钮: {button}. 支持 'left', 'right', 'middle'")
