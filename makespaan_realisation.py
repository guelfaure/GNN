import json
import predict
#faire du predict en modelant le graph
# Ouvrir le fichier JSON
with open('./data_light/data/test/test.json', 'r') as fichier:
    # Charger les données JSON
    datas = json.load(fichier)


frontier=[[] for u in range(29)]
time=[]
solutions_opti=[]
solutions_GNN=[]
nodes_id=[]
update_json=[]
  
for i in range(29):
    nodes = datas[i]["nodes"]
    break_time=0
    for v in range(len(nodes)):
        if nodes[v]["entity"]=="frontier":
            frontier[i].append(int(nodes[v]["id"]))
            if i==0:
                nodes_id.append(int(nodes[v]["id"])) 
            if nodes[v]["solution"]==1:
                solutions_opti.append(int(nodes[v]["id"]))
                
        elif nodes[v]["entity"]=="other":
            if i==0:
                nodes_id.append(int(nodes[v]["id"]))
            
        elif nodes[v]["entity"]=="time" and break_time==0:
            time.append(int(nodes[v]["id"].split("time")[1]))
            break_time=1            

graphs=[]
graph_data=[{}]
frontier_update=frontier[0]
err=0
first_time=""
duration_sol_opti=0
duration_sol_gnn=0
ressource_sol_opti=[]
ressource_sol_gnn=[]

for i in range(29):
    results=predict.main(1)
    print(results)
    if type(results[0])==list:
        solution_index = results[0].index(max(results[0]))
    else:
        solution_index = 0
    print(frontier_update)
    solutions_GNN.append(int(frontier_update[solution_index]))
    nodes_id.remove(int(frontier_update[solution_index]))
    print(solutions_GNN[i])
    print(solutions_opti[i])
    
    graph_data[0]["directed"]=True
    graph_data[0]["multigraph"]=False
    graph_data[0]["graph"]={}
    graph_data[0]["nodes"]=[]
    graph_data[0]["links"]=[]
    # update frontier:
    if i!=28 and solutions_GNN[i]==solutions_opti[i]:
        frontier_update=frontier[i+1]
        err=0
    elif i!=28 and solutions_GNN[i]!=solutions_opti[i]:
        frontier_update.remove(frontier_update[solution_index])
        err=1
        for j in range(len(datas[i]["nodes"])):
            try:
                if int(datas[i]["nodes"][j]["id"])==solutions_GNN[i]:
                    duration_sol_gnn=datas[i]["nodes"][j]["duration"]
                    ressource_sol_gnn=datas[i]["nodes"][j]["ressources_needed"]
            except:
                pass
            
            try:
                if int(datas[i]["nodes"][j]["id"])==solutions_opti[i]:
                    duration_sol_opti=datas[i]["nodes"][j]["duration"]
                    ressource_sol_opti=datas[i]["nodes"][j]["ressources_needed"]
            except:
                pass
                
       
    if i<28:
        #modify the graph according to gnn decision
        
        #nodes
        if err==1:
            for j in range(len(datas[i]["nodes"])):
                try:
                    if int(datas[i]["nodes"][j]["id"]) in nodes_id:
                        graph_data[0]["nodes"].append(datas[i]["nodes"][j])
                except:
                    pass
        else:
            for j in range(len(datas[i+1]["nodes"])):
                try:
                    if int(datas[i+1]["nodes"][j]["id"]) in nodes_id:
                        graph_data[0]["nodes"].append(datas[i+1]["nodes"][j])
                except:
                    pass  
        
        #times nodes            
        breaker=0
        t=0
        for j in range(len(datas[i+1]["nodes"])):
            if datas[i+1]["nodes"][j]["entity"]=="time":
                if breaker==0:
                    breaker=1
                    first_time=datas[i+1]["nodes"][j]["id"]    
                if err==0:
                    graph_data[0]["nodes"].append({"entity": "time", "ressources_available": datas[i+1]["nodes"][j]["ressources_available"], "id": datas[i+1]["nodes"][j]["id"]})
                elif err==1:
                    graph_data[0]["nodes"].append({"entity": "time", "ressources_available": datas[i+1]["nodes"][j]["ressources_available"], "id": datas[i+1]["nodes"][j]["id"]})
                    if 0<=t<=duration_sol_opti:
                        graph_data[0]["nodes"][-1]["ressources_available"]=[x - y for x, y in zip(graph_data[0]["nodes"][-1]["ressources_available"], ressource_sol_opti)]
                        
                    if 0<=t<=duration_sol_gnn:
                        graph_data[0]["nodes"][-1]["ressources_available"]=[x - y for x, y in zip(graph_data[0]["nodes"][-1]["ressources_available"], ressource_sol_gnn)]   
                t+=1
        
        #links
        for j in range(len(datas[i]["links"])):
            try:          
                if int(datas[i]["links"][j]["source"]) in nodes_id and int(datas[i]["links"][j]["target"]) in nodes_id:
                    graph_data[0]["links"].append(datas[i]["links"][j])
            except:
                pass

        for j in range(len(datas[i+1]["links"])):
            try:
                if int(datas[i+1]["links"][j]["source"]) in nodes_id and "time" in datas[i+1]["links"][j]["target"]:
                    graph_data[0]["links"].append(datas[i+1]["links"][j])
            except:
                pass
            
            
            if "time" in datas[i+1]["links"][j]["target"] and "time" in datas[i+1]["links"][j]["source"]:
                graph_data[0]["links"].append(datas[i+1]["links"][j])
            
            try:
                if int(datas[i+1]["links"][j]["target"]) in nodes_id and "time" in datas[i+1]["links"][j]["source"]:
                    graph_data[0]["links"].append(datas[i+1]["links"][j])
            except:
                pass
            
            if err==1:
                graph_data[0]["links"].append({"edge_type":"min_start","source": str(solutions_opti[i]),"target":first_time})
                graph_data[0]["links"].append({"edge_type":"time_link","source":first_time,"target":str(solutions_opti[i])})
                
        with open('./data_saved/test/test.json', 'w') as fichier:
            json.dump(graph_data, fichier, indent=4)
            
        graphs.append(graph_data[0])
    
    
with open('./data_makespan_creation/test.json', 'w') as fichier2:
            json.dump(graphs, fichier2)    
    ##réecrire le json
    
print(solutions_GNN)
print(solutions_opti)
print(time)