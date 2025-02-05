import json
import predict
#faire du predict en modelant le graph
# Ouvrir le fichier JSON
with open('./data_light/data/test/test.json', 'r') as fichier:
    # Charger les données JSON
    datas = json.load(fichier)
databis=datas   
# results = predict.main(29)
results=[[0.31064302, 0.5700141, 0.19091764], [0.056569993, 0.9043529, 0.18179044, 0.038161308], [0.39550745, 0.5432274, 0.17317069], [0.04581064, 0.081302136, 0.95463747, 0.019175142], [0.2851317, 0.6262225, 0.16747653], [0.17099383, 0.011018962, 0.708846], [0.013346791, 0.045996666, 0.9306798, 0.045843065], [0.03254327, 0.09666431, 0.014038056, 0.96502686], [0.93618727, 0.20970741, 0.02121064, 0.05196151, 0.034480363], [0.42849904, 0.15773544, 0.05808723, 0.076832354, 0.06403458], [0.6097696, 0.011471003, 0.009050727, 0.053668946, 0.39856476], [0.16334417, 0.026182622, 0.021174759, 0.22335139, 0.038098782, 0.87494826], [0.36508235, 0.06727812, 0.04110548, 0.52112275, 0.0765312, 0.064058125], [0.04337433, 0.016182572, 0.2891661, 0.0362598, 0.031242877, 0.80627817], [0.09087533, 0.056175858, 0.4513467, 0.04833302, 0.09765801, 0.569978], [0.056301266, 0.03200832, 0.052413017, 0.091718435, 0.8724107], [0.020919412, 0.6312095, 0.015500158, 0.48828703], [0.025072604, 0.14588892, 0.036259323, 0.94169575], [0.309303, 0.6650728, 0.3007995], [0.6319334, 0.5263404, 0.044828206, 0.01828754], [0.582218, 0.066284, 0.59306514, 0.02161178], [0.07532781, 0.58872306, 0.084916115, 0.044429183], [0.60651135, 0.50962245, 0.037216514, 0.039200306], [0.019770175, 0.9830204, 0.04809761, 0.08541551], [0.4217912, 0.09930158, 0.6088515, 0.11035901], [0.4753107, 0.7291839, 0.15090215], [0.8832884, 0.30533922, 0.1396431], [0.6321156, 0.13079292, 0.48268706], [0.8238199, 0.48303938]]
nodes_list = [u for u in range(1, 32)]
frontier=[[] for u in range(29)]
time=[]
solutions_GNN=[]
solutions_opti=[]   
for i in range(29):
    nodes = datas[i]["nodes"]
    break_time=0
    for v in range(len(nodes)):
        if nodes[v]["entity"]=="frontier":
            frontier[i].append(int(nodes[v]["id"]))
            if nodes[v]["solution"]==1:
                solutions_opti.append(int(nodes[v]["id"]))
        elif nodes[v]["entity"]=="time" and break_time==0:
            time.append(int(nodes[v]["id"].split("time")[1]))
            break_time=1            
    solution_index = results[i].index(max(results[i]))
    solutions_GNN.append(int(frontier[i][solution_index]))


print(solutions_GNN)
print(solutions_opti)
print(time)
real_accuracy=0
for i in range(29):
    if solutions_opti[i] in solutions_GNN:
        ind=solutions_GNN.index(solutions_opti[i])
        t_GNN=time[ind]
        if t_GNN==time[i]:
            real_accuracy+=1
print("good predict:"+ str(round(real_accuracy/29, 3))+"%")

