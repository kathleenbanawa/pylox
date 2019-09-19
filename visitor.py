#!/usr/local/bin/python3

from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visit(self, x):
        pass
