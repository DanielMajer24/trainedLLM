
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
import time

class TimerError(Exception):
    "A custom exception used to report errors in use of Timer class"

class Timer:
    def __init__(self):
        self._start_time = None

    def __enter__(self):
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")

class StreamlitChatLoop:
    def __init__(self):
        self.model_id = "lmsys/fastchat-t5-3b-v1.0"
        self.llm = HuggingFacePipeline.from_model_id(
            model_id=self.model_id,
            task="text2text-generation",
            model_kwargs={"temperature": 0, "max_length": 1000},
        )
        template = """
        You are a friendly chatbot assistant that responds in conversation to users' questions.
        Keep the answers short, unless specifically asked by the user to elaborate on something.

        Question: {question}

        Answer:"""

        self.prompt = PromptTemplate(template=template, input_variables=["question"])
        self.llm_chain = LLMChain(prompt=self.prompt, llm=self.llm)

    def ask_question(self, question):
        with Timer():
            result = self.llm_chain(question)
            return result['text']
