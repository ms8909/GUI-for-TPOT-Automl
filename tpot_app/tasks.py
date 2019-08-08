from tpot import TPOTClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np
import dramatiq

from .models import Training, Dataset
import pickle


production_model={} # model_id: model




@dramatiq.actor
def train(train_id, dataset_address, y_variable, problem_type):
    # make a new dataset object
    dataset_obj= Dataset.objects.create(address= dataset_address, y_variable= y_variable)
    dataset_obj.save()

    # make a new training object
    training_obj= Training.objects.create(training_id= train_id, status="ABOUTTOSTART", dataset= dataset_obj)
    training_obj.save()


    # pull datafrom AWS s3. for now just pull from a local directory (CSV FOR NOW)
    # strat training based on problem type

    try:
        if problem_type=="CLASSIFICATION":

            training_obj.status= "TRAINING"
            training_obj.save()

            iris = load_iris()
            X_train, X_test, y_train, y_test = train_test_split(iris.data.astype(np.float64),
            iris.target.astype(np.float64), train_size=0.95, test_size=0.05)
            tpot = TPOTClassifier(generations=5, population_size=50, verbosity=2, use_dask=True)
            tpot.fit(X_train, y_train)
            print(tpot.score(X_test, y_test))


        if problem_type== "REGRESSION":
            training_obj.status= "TRAINING"
            training_obj.save()

            iris = load_iris()
            X_train, X_test, y_train, y_test = train_test_split(iris.data.astype(np.float64),
            iris.target.astype(np.float64), train_size=0.95, test_size=0.05)
            tpot = TPOTClassifier(generations=5, population_size=50, verbosity=2, use_dask=True)
            tpot.fit(X_train, y_train)
            print(tpot.score(X_test, y_test))


        # make a model object


        # save the model on locally and transfer it to s3

        #let train id be 1 for now
        with open('tpot_app/fitted_models/'+str(train_id)+'.pickle', 'wb') as handle:
            pickle.dump(tpot.fitted_pipeline_, handle, protocol=pickle.HIGHEST_PROTOCOL)


        # put the model in production

        with open('tpot_app/fitted_models/'+str(train_id)+'.pickle', 'rb') as handle:
            tpot_model = pickle.load(handle)

        production_model[str(train_id)]= tpot_model
        training_obj.status= "COMPLETED"
        training_obj.save()

    except:

        # update the training object. Change the status
        training_obj.status= "FAILED"
        training_obj.save()

        return True






def predict(train_id, data_set):
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data.astype(np.float64),
    iris.target.astype(np.float64), train_size=0.75, test_size=0.25)

    try:

        pred= production_model[str(train_id)].predict(X_test)
    except:


        with open('tpot_app/fitted_models/' + str(train_id)+'.pickle', 'rb') as handle:
            tpot_model = pickle.load(handle)
        production_model[str(train_id)]= tpot_model

        pred= production_model[str(train_id)].predict(X_test)

    return pred








