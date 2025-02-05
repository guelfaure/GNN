import ignnition
import numpy as np

def main():
    model = ignnition.create_model(model_dir='./')
    model.computational_graph()
    all_predictions = np.array(model.evaluate())
    print(all_predictions)
    
if __name__ == "__main__":
    main()