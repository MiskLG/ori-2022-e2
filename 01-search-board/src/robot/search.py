from __future__ import print_function

from collections import deque
from abc import *


class Search(object):
    """
    Apstraktna klasa za pretragu.
    """

    def __init__(self, board):
        self.board = board

    def search(self, initial_state):
        """
        Implementirana pretraga.

        :param initial_state: Inicijalno stanje. Tip: implementacija apstraktne klase State.
        :return: path, processed_list, states_list
        """
        # inicijalizacija pretrage
        initial_state = initial_state(self.board)  # pocetno stanje
        states_list = deque([initial_state])  # deque - "brza" lista u Python-u
        states_set = {initial_state.unique_hash()}  # set - za brzu pretragu stanja

        processed_list = deque([])  # deque procesiranih stanja
        processed_set = set()  # set procesiranih stanja

        # pretraga
        while len(states_list) > 0:  # dok ima stanja za obradu
            curr_state = self.select_state(states_list)  # preuzmi sledece stanje za obradu
            states_set.remove(curr_state.unique_hash())  # izbaci stanja iz seta stanja

            processed_list.append(curr_state)  # ubaci stanje u listu procesiranih stanja
            processed_set.add(curr_state.unique_hash())  # ubaci stanje u set procesiranih stanja

            kraj, refresh = curr_state.is_final_state()
            if kraj:  # ako je krajnje stanje
                # rekonsturisi putanju
                return Search.reconstruct_path(curr_state), processed_list, states_list
            if refresh == 1:
                processed_set = set()
                states_set = set()
                states_list = deque([curr_state])
                processed_list = deque([])
                states_set.add(curr_state.unique_hash())
            # ako nije krajnje stanje
            # izgenerisi sledeca moguca stanja
            new_states = curr_state.get_next_states()
            # iz liste sledecih mogucih stanja izbaci ona koja su vec u listi i koja su vec procesirana
            new_states = [new_state for new_state in new_states if
                          new_state.unique_hash() not in processed_set and
                          new_state.unique_hash() not in states_set]
            # dodaj sledeca moguca stanja na kraj liste stanja
            states_list.extend(new_states)
            # dodaj sledeca moguca stanja u set stanja
            states_set.update([new_state.unique_hash() for new_state in new_states])
        return None, processed_list, states_list

    @staticmethod
    def reconstruct_path(final_state):
        path = []
        while final_state is not None:
            path.append(final_state.position)
            final_state = final_state.parent
        return reversed(path)

    @abstractmethod
    def select_state(self, states):
        """
        Apstraktna metoda koja, na osnovu liste svih mogucih sledecih stanja,
        bira sledece stanje za obradu.
        *** STRATEGIJA PRETRAGE SE IMPLEMENTIRA OVERRIDE-ovanjem OVE METODE ***

        :param states: lista svih mogucih sledecih stanja
        :return: odabrano sledece stanje za obradu
        """
        pass


class BreadthFirstSearch(Search):
    def select_state(self, states):
        # struktura podataka je red (queue)
        # dodaj na kraj (linija 50), uzimaj sa pocetka
        return states.popleft()


class DepthFirstSearch(Search):
    def select_state(self, states):
        return states.pop()


class IterativeDepthFirstSearch(Search):

    def search(self, initial_state, depthStep = 3 , maxDepth = 10000):
        """
        Implementirana pretraga.

        :param initial_state: Inicijalno stanje. Tip: implementacija apstraktne klase State.
        :return: path, processed_list, states_list
        """
        initial_state = initial_state(self.board)  # pocetno stanje
        # inicijalizacija pretrage
        for currentDepth in range(0,maxDepth,depthStep):
            states_list = deque([initial_state])  # deque - "brza" lista u Python-u
            states_set = {initial_state.unique_hash()}  # set - za brzu pretragu stanja

            processed_list = deque([])  # deque procesiranih stanja
            processed_set = set()  # set procesiranih stanja

            # pretraga
            while len(states_list) > 0:  # dok ima stanja za obradu
                curr_state = self.select_state(states_list)  # preuzmi sledece stanje za obradu

                states_set.remove(curr_state.unique_hash())  # izbaci stanja iz seta stanja
                #print(str(currentDepth) +"   "+ str(curr_state.depth))
                #print(processed_set)
                if curr_state.depth > currentDepth:
                    continue

                processed_list.append(curr_state)  # ubaci stanje u listu procesiranih stanja
                processed_set.add(curr_state.unique_hash())  # ubaci stanje u set procesiranih stanja
                kraj , refresh = curr_state.is_final_state()
                if kraj:  # ako je krajnje stanje
                    # rekonsturisi putanju
                    return Search.reconstruct_path(curr_state), processed_list, states_list

                # ako nije krajnje stanje
                # izgenerisi sledeca moguca stanja

                new_states = curr_state.get_next_states()
                # iz liste sledecih mogucih stanja izbaci ona koja su vec u listi i koja su vec procesirana

                new_states = [new_state for new_state in new_states if
                              new_state.unique_hash() not in processed_set and
                              new_state.unique_hash() not in states_set]

                # dodaj sledeca moguca stanja na kraj liste stanja
                states_list.extend(new_states)
                # dodaj sledeca moguca stanja u set stanja
                states_set.update([new_state.unique_hash() for new_state in new_states])

        return None, processed_list, states_list

    def select_state(self, states):
        return states.pop()


class IterativeDepthFirstSearch2(Search):

    def search(self, initial_state, depthStep=35, maxDepth=10000):
        """
        Implementirana pretraga.

        :param initial_state: Inicijalno stanje. Tip: implementacija apstraktne klase State.
        :return: path, processed_list, states_list
        """
        initial_state = initial_state(self.board)  # pocetno stanje
        # inicijalizacija pretrage
        for currentDepth in range(0, maxDepth, depthStep):
            states_list = deque([initial_state])  # deque - "brza" lista u Python-u
            states_set = {initial_state.unique_hash()+'/'+str(initial_state.depth)}  # set - za brzu pretragu stanja

            processed_list = deque([])  # deque procesiranih stanja
            processed_set = set()  # set procesiranih stanja

            # pretraga
            while len(states_list) > 0:  # dok ima stanja za obradu
                curr_state = self.select_state(states_list)  # preuzmi sledece stanje za obradu
                print('///////////////////////')
                print(currentDepth)
                states_set.remove(str(curr_state.unique_hash())+'/'+str(curr_state.depth))  # izbaci stanja iz seta stanja
                # print(str(currentDepth) +"   "+ str(curr_state.depth))
                # print(processed_set)

                processed_list.append(curr_state)  # ubaci stanje u listu procesiranih stanja
                processed_set.add(str(curr_state.unique_hash())+'/'+str(curr_state.depth))  # ubaci stanje u set procesiranih stanja
                if curr_state.depth > currentDepth:
                    continue
                kraj, refresh = curr_state.is_final_state()
                if kraj:  # ako je krajnje stanje
                    # rekonsturisi putanju
                    return Search.reconstruct_path(curr_state), processed_list, states_list

                # ako nije krajnje stanje
                # izgenerisi sledeca moguca stanja

                new_states = curr_state.get_next_states()
                # iz liste sledecih mogucih stanja izbaci ona koja su vec u listi i koja su vec procesirana
                states = []
                for new_state in new_states:
                    ind1 = 0
                    ind2 = 0
                    ind3 = 0
                    ind4 = 0
                    ind5 = 0
                    print(new_state.unique_hash() + str(new_state.depth))
                    for processed in processed_set:
                        if processed.split('/')[0] == new_state.unique_hash():
                            ind2 = 1
                            if int(processed.split('/')[1]) < new_state.depth:
                                ind1 = 1

                    if ind2 == 0 and ind1 == 1:
                        ind3 = 1

                    if ind2 == 1 and ind1 == 1:
                        continue

                    for processed in states_set:
                        if processed.split('/')[0] == new_state.unique_hash():
                            ind4 = 1
                            if int(processed.split('/')[1]) < new_state.depth:
                                ind5 = 1
                                break
                    if ind4 == 0 and ind5 == 0:
                        states.append(new_state)
                        continue
                    if ind2 == 0 and ind4 == 0:
                        states.append(new_state)
                new_states = states
                # dodaj sledeca moguca stanja na kraj liste stanja
                states_list.extend(new_states)
                for s in states_list:
                    print(s.unique_hash()+str(s.depth))
                # dodaj sledeca moguca stanja u set stanja
                states_set.update([new_state.unique_hash() + '/' + str(new_state.depth) for new_state in new_states])

        return None, processed_list, states_list

    def select_state(self, states):
        # TODO 2: Implementirati IDFS
        return states.pop()


class GreedySearch(Search):

    def search(self, initial_state):
        """
        Implementirana pretraga.

        :param initial_state: Inicijalno stanje. Tip: implementacija apstraktne klase State.
        :return: path, processed_list, states_list
        """
        # inicijalizacija pretrage
        initial_state = initial_state(self.board)  # pocetno stanje
        states_list = deque([initial_state])  # deque - "brza" lista u Python-u
        states_set = {initial_state.unique_hash()}  # set - za brzu pretragu stanja

        processed_list = deque([])  # deque procesiranih stanja
        processed_set = set()  # set procesiranih stanja

        # pretraga
        while len(states_list) > 0:  # dok ima stanja za obradu
            curr_state = self.select_state(states_list)  # preuzmi sledece stanje za obradu
            states_set.remove(curr_state.unique_hash())  # izbaci stanja iz seta stanja

            processed_list.append(curr_state)  # ubaci stanje u listu procesiranih stanja
            processed_set.add(curr_state.unique_hash())  # ubaci stanje u set procesiranih stanja

            if curr_state.is_final_state():  # ako je krajnje stanje
                # rekonsturisi putanju
                return Search.reconstruct_path(curr_state), processed_list, states_list

            # ako nije krajnje stanje
            # izgenerisi sledeca moguca stanja
            new_states = curr_state.get_next_states()
            # iz liste sledecih mogucih stanja izbaci ona koja su vec u listi i koja su vec procesirana
            new_states = [new_state for new_state in new_states if
                          new_state.unique_hash() not in processed_set and
                          new_state.unique_hash() not in states_set]
            # dodaj sledeca moguca stanja na kraj liste stanja
            states_list.extend(new_states)
            # dodaj sledeca moguca stanja u set stanja
            states_set.update([new_state.unique_hash() for new_state in new_states])
        return None, processed_list, states_list

    def select_state(self, states):
        # TODO 3: Implementirati GS
        # implementirati get_cost metodu u RobotState
        return states.pop()


class AStarSearch(Search):
    def select_state(self, states):
        # TODO 4: Implementirati A*
        # implementirati get_cost i get_current_cost metode u RobotState
        pass
