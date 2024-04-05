import numpy as np
class BagLearner(object):
    def __init__(self, learner=None, kwargs={}, bags=20, boost=False, verbose=False):
        self._boost = boost
        self._verbose = verbose
        self._learners = []
        for i in range(bags):
            self._learners.append(learner(**kwargs))
    def author(self):
        return "szhou401"
    def add_evidence(self, data_x, data_y):
        for l in self._learners:
            i = np.random.choice(range(data_x.shape[0]), data_x.shape[0], replace=True)
            train_x = data_x[i]
            train_y = data_y[i]
            l.add_evidence(train_x, train_y)
    def query(self, points):
        results = [learner.query(points) for learner in self._learners]
        return np.mean(results, axis=0)

    if __name__ == "__main__":
        print("BagLearner")