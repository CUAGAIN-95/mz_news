

class Gemini():
    def __init__(self) -> None:
        pass

    def gemini(self, chain, input_prompt, in_out):
        response = chain.invoke({"input": input_prompt, "in_out": in_out})
        return response