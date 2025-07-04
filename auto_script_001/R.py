from typing import Any


class R:
    is_success: bool = True
    message: str = ''
    data: Any
    
    def __init__(self, is_success: bool = True, message: str = '', data: Any = None):
        self.is_success = is_success
        self.message = message
        self.data = data
        return
    
    def print_error_exit(self):
        if not self.is_success:
            print(f"Error: {self.message}")
            exit(1)
        return self
    
    pass
