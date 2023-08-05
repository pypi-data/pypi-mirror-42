from abc import ABC, abstractmethod
from typing import TypeVar, List

from jmetal.util.comparator import DominanceComparator

S = TypeVar('S')


class Ranking(List[S], ABC):

    def __init__(self):
        super(Ranking, self).__init__()
        self.number_of_comparisons = 0
        self.ranked_sublists = []

    @abstractmethod
    def compute_ranking(self, solutions: List[S], k: int):
        pass

    def get_subfront(self, rank: int):
        if rank >= len(self.ranked_sublists):
            raise Exception('Invalid rank: {0}. Max rank: {1}'.format(rank, len(self.ranked_sublists) - 1))
        return self.ranked_sublists[rank]

    def get_number_of_subfronts(self):
        return len(self.ranked_sublists)


class FastNonDominatedRanking(Ranking[List[S]]):
    """ Class implementing the non-dominated ranking of NSGA-II proposed by Deb et al., see [Deb2002]_ """

    def __init__(self, comparator=DominanceComparator()):
        super(FastNonDominatedRanking, self).__init__()
        self.comparator = comparator

    def compute_ranking(self, solutions: List[S], k: int = None):
        """ Compute ranking of solutions.

        :param solutions: Solution list.
        :param k: Number of individuals.
        """
        # number of solutions dominating solution ith
        dominating_ith = [0 for _ in range(len(solutions))]

        # list of solutions dominated by solution ith
        ith_dominated = [[] for _ in range(len(solutions))]

        # front[i] contains the list of solutions belonging to front i
        front = [[] for _ in range(len(solutions) + 1)]

        for p in range(len(solutions) - 1):
            for q in range(p + 1, len(solutions)):
                dominance_test_result = self.comparator.compare(solutions[p], solutions[q])
                self.number_of_comparisons += 1

                if dominance_test_result == -1:
                    ith_dominated[p].append(q)
                    dominating_ith[q] += 1
                elif dominance_test_result is 1:
                    ith_dominated[q].append(p)
                    dominating_ith[p] += 1

        for i in range(len(solutions)):
            if dominating_ith[i] is 0:
                front[0].append(i)
                solutions[i].attributes['dominance_ranking'] = 0

        i = 0
        while len(front[i]) != 0:
            i += 1
            for p in front[i - 1]:
                if p <= len(ith_dominated):
                    for q in ith_dominated[p]:
                        dominating_ith[q] -= 1
                        if dominating_ith[q] is 0:
                            front[i].append(q)
                            solutions[q].attributes['dominance_ranking'] = i

        self.ranked_sublists = [[]] * i
        for j in range(i):
            q = [0] * len(front[j])
            for m in range(len(front[j])):
                q[m] = solutions[front[j][m]]
            self.ranked_sublists[j] = q

        if k:
            count = 0
            for i, front in enumerate(self.ranked_sublists):
                count += len(front)
                if count >= k:
                    return self.ranked_sublists[:i + 1]
        else:
            return self.ranked_sublists


class EfficientNonDominatedRanking(Ranking[List[S]]):
    """ Class implementing the EDS (efficient non-dominated sorting) algorithm. """

    def __init__(self):
        super(EfficientNonDominatedRanking, self).__init__()

    def compute_ranking(self, solutions: List[S], k: int):
        # todo :)
        return self.ranked_sublists
