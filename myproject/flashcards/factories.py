from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Iterable, Dict, Any, Optional

from .models import FlashcardSet, Flashcard

@dataclass(frozen=True)
class CardDTO:
    question: str
    answer: str

class FlashcardSetCreator(ABC):
    @abstractmethod
    def create_set(selfself) -> FlashcardSet:
        raise NotImplementedError

class UserFlashcardSetCreator(FlashcardSetCreator):
    def __init__(self, name: str, cards: Iterable[CardDTO]):
        self.name = (name or "").strip()
        self.cards = list(cards)

    def create_set(self) -> FlashcardSet:
        flashcard_set = FlashcardSet.objects.create(name=self.name)

        objs: List[Flashcard] = []
        for c in self.cards:
            q = (c.question or "").strip()
            a = (c.answer or "").strip()
            if q and a:
                objs.append(Flashcard(set=flashcard_set, question=q, answer=a))

        if objs:
            Flashcard.objects.bulk_create(objs)

        return flashcard_set