# logger.py

import datetime
import pytz
import inspect

class Logger():
    def __init__(self) -> None:
        self.tz = pytz.timezone('Asia/Seoul')
        pass

    def logger(self, target, message="test"):
        file_path = "../_log/logger.txt"
        
        locals_time = datetime.datetime.now(self.tz)
        _time = locals_time.strftime("%Y-%m-%d %H:%M:%S")

        class_name = type(target).__name__
        function_name = inspect.currentframe().f_back.f_code.co_name
        # 파일경로에 "시간 : 사용된 함수, 메세지 출력"
        with open(file_path, "a") as f:
            f.write(f"{_time} : {class_name}.{function_name} >> {message}\n")