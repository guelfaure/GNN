import ignnition
import numpy as np

def main(iter):
    results=[]
    model = ignnition.create_model(model_dir='./')
    model.computational_graph()
    all_predictions = np.array(model.predict(num_predictions = iter, verbose=True))
    for e in all_predictions:
        results.append(e.tolist())
    return results
    
