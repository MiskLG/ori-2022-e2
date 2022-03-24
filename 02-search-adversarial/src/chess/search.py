from abc import *
from state import State
import sys
import numpy as np

MAX_FLOAT = sys.float_info.max
MIN_FLOAT = -MAX_FLOAT


class AdversarialSearch(object):
    """
    Apstraktna klasa za suparnicku/protivnicku pretragu.
    """

    def __init__(self, board, max_depth):
        """
        :param board: tabla koja predstavlja pocetno stanje.
        :param max_depth: maksimalna dubina pretrage (koliko poteza unapred).
        :return:
        """
        self.initial_state = State(board, parent=None)
        self.max_depth = max_depth

    @abstractmethod
    def perform_adversarial_search(self):
        """
        Apstraktna metoda koja vrsi pretragu i vraca sledece stanje.
        """
        pass


class Minimax(AdversarialSearch):
    def minmax(self, state, depth, maximizing_player):
        if depth == 0 or state.is_final_state():
            return state.calculate_value(), state

        if maximizing_player:
            best_value = -np.inf # privremeno - beskonacno
            best_state = state
            for child in state.generate_next_states(not maximizing_player):
                value, st = self.minmax(child, depth - 1, False)
                if value > best_value:
                    best_value = value
                    best_state = child
            return best_value, best_state
        else:
            best_value = np.inf # privremeno
            best_state = state
            for child in state.generate_next_states(not maximizing_player):
                value, st = self.minmax(child, depth - 1, True)
                if value < best_value:
                    best_value = value
                    best_state = child
            return best_value, best_state

    def perform_adversarial_search(self):
        return self.minmax(self.initial_state, self.max_depth, False)


class AlphaBeta(AdversarialSearch):

    def perform_adversarial_search(self):
        # TODO 4: Implementirati alpha-beta algoritam
        pass
