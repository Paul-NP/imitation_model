from random import random
import csv
import numpy as np

"""
Стадии только по номерам. Названия можно сделать дополнительно вне взаимодействия классов.
"""


class Flow:
    def __init__(self, source, targets, factor, ind_stages={}):
        """
        Класс потока особей между стадиями. Содержит информацию об источнике, цели (целях), индуцирующих стадиях.
        Вычисляет вероятности для перехода.
        :param source: int, номер стадии источника
        :param targets: dict, номер стадии : вероятность попадания в неё
        :param factor: float, коэффициент потока
        :param ind_stages: dict, номер стадии : коэффициент индуцировнаия, пустой если неиндуцированный поток
        """
        self.source = source
        self.targets = targets
        self.factor = factor
        self.ind_stages = ind_stages

    def get_propab(self, model_state):
        flow = self.factor
        if self.ind_stages:
            for i_s in self.ind_stages:
                flow *= model_state[i_s] * self.ind_stages[i_s]
        propab = {}
        for t in self.targets:
            propab[t] = flow * self.targets[t]

        return propab


class Model:
    def __init__(self, stages, flows):
        """
        Класс модели. Содержит информацию о стадиях и потоках. Обеспечивает процесс симуляции.
        :param stages: list, количества индивидов на каждой стадии в начале симуляции, индекс в этом списке и будет уникальным номером стадии.
        :param flows: list[Flow], список потоков
        """
        self.flows = flows
        self.model_state = stages
        self.step = 0
        population_size = sum(stages)
        self.population = np.zeros(population_size, dtype=int)

        ind_id = 0
        for s_i in range(len(self.model_state)):
            for i in range(self):

    def model_step(self):
        flow_propab = []
        for f in self.flows:
            flow_propab.append(f.get_propab(self.model_state))

        trans_propab = []
        for s_i in range(len(self.model_state)):
            trans_propab.append({})
            for f_i in range(len(self.flows)):
                if self.flows[f_i].source == s_i:
                    trans_propab[s_i].update(flow_propab[f_i])

        for ind in range(len(self.population))




