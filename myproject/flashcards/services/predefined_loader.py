import json
import os
from django.conf import settings

class PredefinedLoader:

    @staticmethod
    def load_sets():
        path = os.path.join(settings.BASE_DIR,
                            "flashcards",
                            "data",
                            "predefined_sets.json")
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)