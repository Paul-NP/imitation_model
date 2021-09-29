from random import random
import csv
import numpy as np
import matplotlib.pyplot as plt

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
        flow = np.random.normal(self.factor, 0)
        if self.ind_stages:
            flow /= sum(model_state)
            for i_s in self.ind_stages:
                flow *= model_state[i_s] * self.ind_stages[i_s]
        propab = {}
        for t in self.targets:
            propab[t] = flow * self.targets[t]

        return propab


class Model:
    def __init__(self, stages, flows, num_step=1000):
        """
        Класс модели. Содержит информацию о стадиях и потоках. Обеспечивает процесс симуляции.
        :param stages: list, количества индивидов на каждой стадии в начале симуляции, индекс в этом списке и будет уникальным номером стадии.
        :param flows: list[Flow], список потоков
        """
        self.flows = flows
        self.num_step = num_step
        self.model_state = stages
        self.step = 0
        population_size = sum(stages)
        self.population = np.zeros(population_size, dtype=int)

        ind_id = 0
        for s_i in range(len(self.model_state)):
            for i in range(self.model_state[s_i]):
                self.population[ind_id] = s_i
                ind_id += 1

    def model_step(self):
        flow_propab = []
        for f in self.flows:
            flow_propab.append(f.get_propab(self.model_state))

        trans_propab = []
        summ_propab = []
        for s_i in range(len(self.model_state)):
            trans_propab.append({})
            summ_propab.append(0)
            for f_i in range(len(self.flows)):
                if self.flows[f_i].source == s_i:
                    trans_propab[s_i].update(flow_propab[f_i])
                    summ_propab[s_i] += sum([flow_propab[f_i][t] for t in flow_propab[f_i]])

            if summ_propab[s_i] > 1:
                #print("sum_propab > 1")
                #print(trans_propab[s_i])
                for t in trans_propab[s_i]:
                    trans_propab[s_i][t] /= summ_propab[s_i]
                #print(trans_propab[s_i])

        self.model_state = [0] * len(self.model_state)

        for ind in range(len(self.population)):
            step_value = random()
            kumul_propab = 0
            change = False
            #print("individ {0} - {1}".format(ind, self.population[ind]))
            #print(trans_propab)
            for targ in trans_propab[self.population[ind]]:
                kumul_propab += trans_propab[self.population[ind]][targ]
                if step_value < kumul_propab and not change:
                    #print("{0} < {1}".format(step_value, kumul_propab))
                    self.population[ind] = targ
                    change = True

            self.model_state[self.population[ind]] += 1

    def start_model(self, stage_names, filename="result_file.csv"):
        result_file = open(filename, "w", encoding="utf-8-sig", newline="")
        writer = csv.writer(result_file, delimiter=";")
        writer.writerow(["step"] + stage_names)
        writer.writerow([self.step] + self.model_state)

        print("Start")
        while self.step < self.num_step:
            print("Step {0}".format(self.step))
            self.model_step()
            writer.writerow([self.step] + self.model_state)
            self.step += 1
        print("End")
        result_file.close()

    def show_graphs(self, filename):
        file = open(filename, "r", encoding="utf-8-sig")
        reader = csv.reader(file, delimiter=";")
        result = []
        for row in reader:
            result.append(row)

        columns = [list(map(int, col[1:])) for col in zip(*result)]
        for c in columns:
            print(c)
        for i in range(1, len(columns)):
            plt.plot(columns[0], columns[i])

        plt.show()



if __name__ == "__main__":
    stage_name = ["S", "I", "R"]
    stages = [10000, 10, 0]
    SI = Flow(0, {1: 1}, 0.04, {1: 1})
    IR = Flow(1, {2: 1}, 0.01, {})
    flows = [SI, IR]
    model = Model(stages, flows, 400)
    model.start_model(stage_name, "result_3.csv")
    model.show_graphs("result_3.csv")





