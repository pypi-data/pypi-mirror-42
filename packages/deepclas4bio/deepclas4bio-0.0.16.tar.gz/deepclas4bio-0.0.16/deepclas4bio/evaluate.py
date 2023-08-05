import argparse
import json
from deepclas4bio import Evaluator
from deepclas4bio.PredictorFactory import PredictorFactory
import importlib

def evaluate(readDataset,path,pathLabels,measures,predictors):
    # with open(config) as file:
    #     data=json.load(file)
    #
    #
    # readDataset=data['readDataset']
    # path = data['pathDataset']
    # pathLabels = data['pathLabels']

    classReadDataset__ = getattr(importlib.import_module('deepclas4bio.'+readDataset), readDataset)
    rd=classReadDataset__()

    evaluator = Evaluator.Evaluator(rd, path,
                                    pathLabels)

    # Anadimos las medidas
    # measures=data['measures']
    for measure in measures:
        evaluator.addMeasure(measure)

    # Anadimos los constructores
    m = PredictorFactory()
    # predictors=data['predictors']
    for predictor in predictors:

        model = m.getPredictor(predictor['framework'], predictor['model'])
        evaluator.addPredictor(model)

    return evaluator.evaluate()



# if __name__=="__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-c", "--config", required=True, help="Configuration file")
#     args=vars(parser.parse_args())
#     evaluate(args["config"])
