# logger.py
import datetime
import pytz

class Logger():
    def __init__(self) -> None:
        self.tz = pytz.timezone('Asia/Seoul')
        pass

    def logger(self, func_name, message):
        # 저장 파일 경로
        file_path = "../_log/logger.txt"

        # 시간 타임존 설정 pytz 라이브러리 설치 필요
        locals_time = datetime.datetime.now(self.tz)
        _time = locals_time.strftime("%Y-%m-%d %H:%M:%S")

        # 파일경로에 "시간 : 사용된 함수, 메세지 출력"
        with open(file_path, "a") as f:
            f.write(f"{_time} : '{func_name}', {message}\n")