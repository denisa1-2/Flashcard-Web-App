from abc import ABC, abstractmethod

class AnswerStrategy(ABC):

    @abstractmethod
    def check_answer(self, answer: str, correct_answer: str) -> bool:
        pass