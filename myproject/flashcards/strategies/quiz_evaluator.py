class QuizEvaluator:

    def __init__(self, strategy):
        self.strategy = strategy

    def evaluate(self, user_answer, correct_answer):
        return self.strategy.check_answer(user_answer, correct_answer)