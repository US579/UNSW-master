import csv
import json


def csv2json(file_path):
    lis2 = []
    lis3 = []
    lis5 = []
    dic1 = {}
    dic2 = {}
    inf = {}

    categories = ["civil", "continent", "district", "staff"]
    data = []
    #open file and read it
    with open(file_path,'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            dic = {}
            for j in range(0,len(categories)):
                par = line[j]
                buf = categories[j]
                dic[buf] = par
            data.append(dic)


    #find the relation betwween the district columns and staff colums and store it in a lis2

    flag = 0
    for i in range(len(data)):
        i = i+flag
        if i > len(data)-1:
            break
        if data[i]['district'] and data[i+1]['district'] :
            dic1[data[i]['district']] = data[i]['staff']
            flag = 0
        else:
            lis2.append(data[i]['staff'])
            for j in range(i+1,len(data)):
                if not data[j]['district']:
                    lis2.append(data[j]['staff'])
                flag+=1
                break
            dic1[data[i]['district']] = lis2
            lis2 = []

    continent = [i['continent'] for i in data if i['continent']]
    # find the relation betwween the continent columns and staff districe and store it in a lis3
    flag1 = 0
    for i in range(len(data)):
        i = i+flag1
        if i > len(data)-1:
            break
        if not data[i]['continent'] and not data[i]['district']:
            continue
        if data[i]['continent'] and data[i+1]['continent'] :
            dic2[data[i]['continent']] = data[i]['district']
        else:
            lis3.append(data[i]['district'])
            for j in range(i+1,len(data)):
                if not data[j]['continent'] and not data[j]['district']:
                    continue
                if not data[j]['continent']:
                    lis3.append(data[j]['district'])
                    if not data[j]['continent']:
                        continue
                    elif not data[j+1]['continent']:
                        break

                flag1+=1
                break

            dic2[data[i]['continent']] = lis3
            if (len(dic2)) == len(continent):
                break
            lis3 = []


    #find the relation in the conjection of the district and merge it

    for i, j in dic2.items():
        if isinstance(j,list):
            for k in j:
                if k in dic1:
                    if k in dic2[i]:
                        lis5.append({k:dic1[k]})
            dic2[i] = lis5
            lis5 = []
        else:
            dic2[i] = [{j:dic1[j]}]

    for i in data:
        if i["civil"]:
            inf[i['civil']] = [{i:j} for i,j in dic2.items()]

    return inf




def pathSearch(data,suffix,path):
    #check wether data format is dict
    if isinstance(data,dict):
        #iterate
        for key,value in data.items():
            pathSearch(value, suffix, path+'.'+ key)
    elif isinstance(data,list):
        for i in data:
            if not isinstance(i ,str):
                pathSearch(i,suffix,path)
    elif isinstance(data,str):
        if data == suffix:
            print(path[1:]+'.'+suffix)
            return False
        return False



if __name__ == "__main__":
    file_path = 'history.csv'
    data = csv2json(file_path)
    print(json.dumps(data, indent=3, ensure_ascii=False))
    suffix = '汉谟拉比法典'
    path = ''
    pathSearch(data,suffix,path)


