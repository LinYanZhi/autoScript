import time
from typing import Union

from pynput import keyboard
from pynput.keyboard import Key, Controller


class KeyboardTool:
    """键盘操作工具类（支持按键模拟和状态检测）"""
    
    def __init__(self):
        """初始化键盘控制器"""
        self.keyboard = Controller()
    
    def press_key(self, key: Union[str, Key]) -> None:
        """
        按下某个键（不释放）

        参数:
            key: 可以是字符(如'a')或Key对象(如Key.shift)
        """
        self.keyboard.press(key)
    
    def release_key(self, key: Union[str, Key]) -> None:
        """
        释放某个键

        参数:
            key: 可以是字符(如'a')或Key对象(如Key.shift)
        """
        self.keyboard.release(key)
    
    def press_and_release(self, key: Union[str, Key],
                          delay: float = 0.1) -> None:
        """
        按压并释放某个键（单个按键）

        参数:
            key: 要按下的键
            delay: 按键按下和释放之间的时间间隔(秒)
        """
        self.press_key(key)
        time.sleep(delay)
        self.release_key(key)
    
    def hotkey(self, *keys: Union[str, Key],
               delay_between: float = 0.05,
               hold_duration: float = 0.1) -> None:
        """
        执行自定义快捷键（组合键）

        示例: hotkey('ctrl', 'c')  # 模拟Ctrl+C

        参数:
            *keys: 组合键序列(如'ctrl', 'c')
            delay_between: 按键之间的时间间隔(秒)
            hold_duration: 按键按下的持续时间(秒)
        """
        # 按下所有组合键
        for key in keys:
            self.press_key(key)
            time.sleep(delay_between)
        
        # 保持组合键状态
        time.sleep(hold_duration)
        
        # 释放所有组合键(按相反顺序)
        for key in reversed(keys):
            self.release_key(key)
            time.sleep(delay_between)
    
    def tap_key(self, key: Union[str, Key],
                times: int = 1,
                interval: float = 0.1,
                delay: float = 0.05) -> None:
        """
        点击某个键（一次或多次）

        参数:
            key: 要点击的键
            times: 点击次数
            interval: 多次点击之间的间隔时间(秒)
            delay: 按键按下和释放之间的时间间隔(秒)
        """
        for i in range(times):
            self.press_and_release(key, delay)
            if i < times - 1:  # 最后一次点击后不需要等待
                time.sleep(interval)
    
    def is_lock_on(self, lock_key: str) -> bool:
        """
        检测锁定键的状态（大小写锁定、数字锁定等）

        参数:
            lock_key:
                'caps' - 大小写锁定
                'num' - 数字锁定
                'scroll' - 滚动锁定

        返回:
            bool: 锁定状态(True表示开启)
        """
        lock_key = lock_key.lower()
        
        if lock_key == 'caps':
            return not self._is_caps_lock_off()
        elif lock_key == 'num':
            return not self._is_num_lock_off()
        elif lock_key == 'scroll':
            return not self._is_scroll_lock_off()
        else:
            raise ValueError(f"不支持的锁定键类型: {lock_key}. 支持 'caps', 'num', 'scroll'")
    
    def get_key_state(self, key: Union[str, Key]) -> bool:
        """
        检测某个键的当前按下状态
        注意: 此功能需要额外的监听器，可能会消耗资源

        参数:
            key: 要检测的键(只能是单个字符或Key常量)

        返回:
            bool: 该键当前是否被按下
        """
        if isinstance(key, str) and len(key) == 1:
            return self._is_char_pressed(key)
        elif isinstance(key, Key):
            return self._is_key_pressed(key)
        else:
            raise ValueError("只能检测单个字符或Key常量")
    
    # 辅助函数 - 检测锁定键状态
    def _is_caps_lock_off(self) -> bool:
        """模拟按CapsLock键两次来检测状态（无副作用）"""
        # 保存当前状态
        self.keyboard.press(Key.caps_lock)
        self.keyboard.release(Key.caps_lock)
        initial_state = self.keyboard.pressed(Key.caps_lock)
        
        # 按两次CapsLock确保回到原始状态
        for _ in range(2):
            self.keyboard.press(Key.caps_lock)
            self.keyboard.release(Key.caps_lock)
        
        # 检测最后状态
        final_state = self.keyboard.pressed(Key.caps_lock)
        
        # 恢复原始状态
        if initial_state != final_state:
            self.keyboard.press(Key.caps_lock)
            self.keyboard.release(Key.caps_lock)
        
        return not final_state
    
    def _is_num_lock_off(self) -> bool:
        """模拟按NumLock键两次来检测状态（无副作用）"""
        # 保存当前状态
        self.keyboard.press(Key.num_lock)
        self.keyboard.release(Key.num_lock)
        initial_state = self.keyboard.pressed(Key.num_lock)
        
        # 按两次NumLock确保回到原始状态
        for _ in range(2):
            self.keyboard.press(Key.num_lock)
            self.keyboard.release(Key.num_lock)
        
        # 检测最后状态
        final_state = self.keyboard.pressed(Key.num_lock)
        
        # 恢复原始状态
        if initial_state != final_state:
            self.keyboard.press(Key.num_lock)
            self.keyboard.release(Key.num_lock)
        
        return not final_state
    
    def _is_scroll_lock_off(self) -> bool:
        """模拟按ScrollLock键两次来检测状态（无副作用）"""
        # 保存当前状态
        self.keyboard.press(Key.scroll_lock)
        self.keyboard.release(Key.scroll_lock)
        initial_state = self.keyboard.pressed(Key.scroll_lock)
        
        # 按两次ScrollLock确保回到原始状态
        for _ in range(2):
            self.keyboard.press(Key.scroll_lock)
            self.keyboard.release(Key.scroll_lock)
        
        # 检测最后状态
        final_state = self.keyboard.pressed(Key.scroll_lock)
        
        # 恢复原始状态
        if initial_state != final_state:
            self.keyboard.press(Key.scroll_lock)
            self.keyboard.release(Key.scroll_lock)
        
        return not final_state
    
    # 辅助函数 - 检测按键实时状态
    def _is_char_pressed(self, char: str) -> bool:
        """检测字符键是否被按下"""
        # 使用监听器检测按键状态
        with keyboard.Events() as events:
            for event in events:
                if isinstance(event, keyboard.Events.Press) and event.key == char:
                    return True
                time.sleep(0.01)  # 避免CPU占用过高
        return False
    
    def _is_key_pressed(self, key: Key) -> bool:
        """检测特殊键是否被按下"""
        # 使用监听器检测按键状态
        with keyboard.Events() as events:
            for event in events:
                if isinstance(event, keyboard.Events.Press) and event.key == key:
                    return True
                time.sleep(0.01)  # 避免CPU占用过高
        return False


if __name__ == '__main__':
    # 创建键盘工具实例
    kbt = KeyboardTool()
    
    # 1. 按下任意键（不释放）
    # kbt.press_key('a')  # 按住a键
    # time.sleep(0.5)  # 保持0.5秒
    # kbt.release_key('a')  # 释放a键
    
    # 2. 按压任意键（按下并释放）
    kbt.press_and_release('b')
    kbt.press_and_release('b')
    kbt.press_and_release('b')
    
    # 3. 自定义快捷键
    # kbt.hotkey('ctrl', 'c')  # 模拟Ctrl+C
    # kbt.hotkey('ctrl', 'alt', 'del')  # 模拟Ctrl+Alt+Del
    
    # 4. 点击某键
    # kbt.tap_key('c')  # 单次点击c键
    # kbt.tap_key('d', times=2)  # 双击d键
    # kbt.tap_key('e', times=5, interval=0.05)  # 快速点击e键5次
    
    # 5. 读取按键状态
    # if kbt.is_lock_on('caps'):
    #     print("大写锁定已开启")
    # else:
    #     print("大写锁定已关闭")
    #
    # if kbt.is_lock_on('num'):
    #     print("数字键盘已开启")
    # else:
    #     print("数字键盘已关闭")
    
    # 6. 实时检测按键状态（需要用户实际按键）
    # print("请按住'f'键（检测3秒）")
    # start_time = time.time()
    # while time.time() - start_time < 3:
    #     if kbt.get_key_state('f'):
    #         print("检测到f键被按下")
    #         break
    #     time.sleep(0.1)
    # else:
    #     print("3秒内未检测到f键按下")
    
    # 7. 组合键特殊操作
    # 模拟Alt+Tab切换窗口
    # kbt.press_key(Key.alt)
    # kbt.tap_key(Key.tab, times=1, interval=0.2)
    # kbt.release_key(Key.alt)
    
    # 模拟Windows键打开开始菜单
    kbt.tap_key(Key.cmd)
