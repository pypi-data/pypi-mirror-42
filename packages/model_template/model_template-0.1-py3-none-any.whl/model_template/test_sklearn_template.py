from sklearn import datasets
from model_template import ModelTemplate, logger
import pickle
from sklearn import svm 
import logging

logger.setLevel(logging.DEBUG)

iris = datasets.load_iris()

class SVMTemplate(ModelTemplate):
    
    def _load_model(self):

        model = svm.SVC(gamma='scale')
        iris = datasets.load_iris()

        x, y = iris.data, iris.target

        model.fit(x,y)

        return model
        
    def _parse_data(self, data):
        return data

    def _model_output(self, data):
        return self._model.predict(data)

    def _recover_label(self, model_output):
        return model_output 

if __name__ == '__main__':
    svm = SVMTemplate()

    print(svm.predict(iris.data[0:1]))
