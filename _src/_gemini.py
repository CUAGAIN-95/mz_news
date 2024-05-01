# gemini.py

from _logger import Logger

class Gemini():
    def __init__(self) -> None:
        pass

    def gemini(self, chain, input_prompt, in_out):
        response = chain.invoke({"input": input_prompt, "in_out": in_out})

        Logger().logger(self, "success")
        return response