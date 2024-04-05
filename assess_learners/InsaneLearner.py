import BagLearner as bl
import LinRegLearner as lrl
import numpy as np
class InsaneLearner(object):
    def __init__(self, verbose = False):
        self._learners = [bl.BagLearner(learner = lrl.LinRegLearner, kwargs = {}, bags = 20, boost = False, verbose = False)] * 20
    def author(self):
        return "szhou401"
    def add_evidence(self, data_x, data_y):
        for l in self._learners:
            l.add_evidence(data_x, data_y)
    def query(self, points):
        results = [learner.query(points) for learner in self._learners]
        return np.mean(results, axis=0)

    if __name__ == "__main__":
        print("InsaneLearner")