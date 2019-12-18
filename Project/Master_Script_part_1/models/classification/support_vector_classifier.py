from sklearn.svm import SVC
from cross_validation import Cross_validation

from sklearn.metrics import accuracy_score, recall_score, precision_score


class Support_vector_classifier(Cross_validation):
    __svc = None
    __param = {}

    def __init__(self, x_train=None, y_train=None, cv=3, n_iter=10, n_jobs=None,scoring=None,
                 C=(1.0,), kernel=('rbf',), gamma=('auto',), coef0=(0.0,),
                 grid_search=False, random_search=False, class_weight=(None,)):

        self.__svc = SVC(random_state=0)

        self.__param = {
            'C': C,
            'kernel': kernel,
            'gamma': gamma,
            'coef0': coef0,
            'class_weight': class_weight
        }
        if grid_search and random_search:
#                 print('only one of GridSearch and RandomSearch can be used.')
            raise Exception
        else:
            if grid_search:
                # apply GridSearchCV and get the best estimator
                self.__svc = super().grid_search_cv(self.__svc,
                                                    self.__param, cv, n_jobs, x_train, y_train,scoring = scoring)
            elif random_search:
                # apply RandomSearchCV and get the best estimator
                self.__svc = super().random_search_cv(self.__svc,
                                                      self.__param, cv, n_iter, n_jobs, x_train, y_train ,scoring = scoring)
            else:
                # fit data directly
                self.__svc.fit(x_train, y_train)

    def accuracy_score(self, x_test=None, y_test=None):
        """
        get classification accuracy score

        :param x_test: test data
        :param y_test: test targets
        :return: the accuracy score
        """
        return accuracy_score(
            y_true=y_test,
            y_pred=self.__svc.predict(x_test))

    def recall(self, x_test=None, y_test=None, average='binary'):
        """
        get classification recall score

        :param average: multi-class or not
        :param x_test: test data
        :param y_test: test targets
        :return: the recall score
        """
        return recall_score(
            y_true=y_test,
            y_pred=self.__svc.predict(x_test),average = average)

    def precision(self, x_test=None, y_test=None,average='binary'):
        """
        get classification precision score

        :param average: multi-class or not
        :param x_test: test data
        :param y_test: test targets
        :return: the precision score
        """
        return precision_score(
            y_true=y_test,
            y_pred=self.__svc.predict(x_test),average = average)

    def evaluate(self, data=None, targets=None, average='binary'):
        """
        evaluate the model

        :param average: multi-class or not
        :param data: training or testing data
        :param targets: targets
        :return: return (accuracy_score, recall, precision)
        """
        return (self.accuracy_score(data, targets),
                self.recall(data, targets, average),
                self.precision(data, targets, average))
    
    def predict(self, data = None):
        """
        get the prediction

        :param data: training or testing data
        :return: return prediction
        """
        
        return (self.__svc.predict(data))

    def print_parameter_candidates(self):
        """
        print all possible parameter combinations
        """
        print('Parameter range: ', self.__param)

    def print_best_estimator(self):
        """
        print the best hyper-parameters
        """
        try:
            print('Best estimator : ', self.__svc.best_estimator_)
        except:
            print("Support_vector_classifier: __svc didn't use GridSearchCV "
                  "or RandomSearchCV.")
