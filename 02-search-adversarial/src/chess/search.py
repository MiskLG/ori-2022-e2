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

    def __init__(self, board, max_depth, last_state):
        """
        :param board: tabla koja predstavlja pocetno stanje.
        :param max_depth: maksimalna dubina pretrage (koliko poteza unapred).
        :return:
        """
        self.initial_state = last_state
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
            return state.calculate_value_based_on_color(maximizing_player), state

        if maximizing_player:
            best_value = -np.inf
            best_state = state
            for child in state.generate_next_states(not maximizing_player):
                value, _ = self.minmax(child, depth - 1, False)
                if value > best_value:
                    best_value = value
                    best_state = child
            return best_value, best_state
        else:
            best_value = np.inf
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
    def alphabet(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.is_final_state():
            return state.calculate_value_based_on_color(maximizing_player), state

        if maximizing_player:
            best_value = -np.inf
            best_state = state
            for child in state.generate_next_states(not maximizing_player):
                value, _ = self.alphabet(child, depth - 1, alpha, beta, False)
                alpha = max(alpha, value)
                if value > best_value:
                    best_value = value
                    best_state = child
                    if beta <= alpha:
                        break
            return best_value, best_state
        else:
            best_value = np.inf
            best_state = state
            for child in state.generate_next_states(not maximizing_player):
                value, st = self.alphabet(child, depth - 1, alpha, beta, True)
                if value < best_value:
                    best_value = value
                    best_state = child
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
            return best_value, best_state

    def perform_adversarial_search(self):
        return self.alphabet(self.initial_state, self.max_depth, -np.inf, np.inf, False)
