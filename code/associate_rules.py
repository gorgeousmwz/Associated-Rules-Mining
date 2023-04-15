# date : 2023-3-26
# language : python
# version : 3.7.16
# coder : mwz
# email : mawenzhuogorgeous@gmail.com
# topic : association rules
# details : From the keywords of 16,071 articles, the keyword combination with correlation was found,
#           and the validity of the correlation was evaluated
# tips : apriori algorithm, support degree, confidence degree, lift degree
# links : https://www.cnblogs.com/pinard/p/6293298.html (a good instruction to Apriori algorithm)

import pandas as pd
import os
import itertools
from tqdm import tqdm
import prettytable as pt

def readFile(path,constraint=None,no_values=''):
    '''读取数据文件,返回list'''
    files=os.listdir(path)
    data_sum=[]
    for filename in files:
        file=os.path.join(path,filename)
        data=pd.read_excel(io=file,usecols=constraint) # 读取文件
        data.fillna(no_values,inplace=True) # 填写空缺值
        data=data.values.tolist() # 转为list
        data_sum+=data
    return data_sum

def dataPrepoccess(data):
    '''数据预处理:将两个字段中的值全部分割,组成database'''
    database=[]
    for i in range(len(data)):
        database.append([]) # 添加Article Title字段
        a=data[i][0].split('; ') # 分割Author Keywords字段
        b=data[i][1].split('; ') # 分割Keywords Plus字段
        for j in range(len(a)): # 全部转小写
            a[j]=a[j].lower()
        for j in range(len(b)):
            b[j]=b[j].lower()
        if a!=['']:
            database[i]+=a
        if b!=['']:
            database[i]+=b
    return database

def get_subsets(lst, k):
    """
    将一个列表转换为set,获取其所有长度为k的子集并转换为元组列表返回
    """
    s = set(lst)
    subsets = list(itertools.combinations(s, k))
    return [tuple(subset) for subset in subsets]

def createKSet(items,k):
    '''
    生成K项候选集
    params:
        items:k-1项集筛选过后的剩余项列表
        k:k项候选集看k>1
    '''
    keywords=[]
    for item in items:
        for i in list(item):
            if i not in keywords:
                keywords.append(i)
    Ck=get_subsets(keywords,k)
    return Ck
    
def Apriori(database,support_threshold):
    '''
    Aprioris算法
    params:
        database:事务数据库
        support_threshold:支持度阈值[0,1]
    returns:
        返回一个包含频繁集和其支持度的字典
    '''
    k=1
    prekeywords={}
    keywords={}
    while True:
        print(f'====================================频繁{k}-项集挖掘====================================')
        # 计算每个keyword组合的出现次数
        for paper in tqdm(database, desc=f"Processing k={k}"): # 遍历database中的所有paper
            for keyword in get_subsets(paper,k): # 遍历每个paper中的所有keyword组合
                if keyword not in list(keywords.keys()): # keyword组合没出现过
                    keywords[keyword]=1 
                else: # keyword组合出现过
                    keywords[keyword]+=1
        # 计算每个组合的支持度
        for key in list(keywords.keys()):
            support=keywords[key]/len(database) # 支持度=出现频次/事务总数
            keywords[key]=support
            if support < support_threshold:
                keywords.pop(key) # 如果小于支持度阈值就删除相应的组合
        # 数据可视化
        for index,value in keywords.items():
            print(f'{index}组合支持度为: {value:5f}')
        # 算法结束判断
        if len(keywords)==1:
            print(f'Apriori算法结束,在{k}-项集终止\n频繁集为: {list(keywords.keys())[0]}, 支持度为: {list(keywords.values())[0]:5f}')
            print(f'================================================================================')
            return keywords
        if len(keywords)==0:
            print(f'Apriori算法结束,在{k-1}-项集终止\n频繁集为:\n{list(prekeywords.keys())}\n支持度为:\n{list(prekeywords.values())}')
            print(f'================================================================================')
            return prekeywords
        k+=1 # 增加频繁集层数
        prekeywords=keywords # 存储k-1层的结果
        keywords=createKSet(list(keywords.keys()),k) # 创建下一层的候选集
        # Prune: 任何非频繁项集都不可能是频繁项集的子集
        # 剪枝1：减掉k-项候选集中的子集不在频繁k-1项集中的候选组合
        pruned_candidates = []
        for candidate in keywords: # 遍历生成的k-项集关键字组合
            subsets = get_subsets(candidate, k-1) # 取其k-1项子集
            if all(subset in prekeywords for subset in subsets): # 如果其所有的k-1项子集都被k-1项频繁集所包含
                pruned_candidates.append(candidate) # 则被纳入剪枝后的k-项候选集
        keywords = dict(zip(pruned_candidates,[0]*len(pruned_candidates)))
        # 剪枝2：由于k-1项频繁集中所有的1项子集都是频繁集，所以删掉每个事务中的非频繁1项集
        preset=[]
        for key in list(prekeywords.keys()):
            for a in key:
                if a not in preset:
                    preset.append(a)
        for i in range(len(database)):
            j=0
            while j<len(database[i]):
                if database[i][j] not in preset:
                    database[i].remove(database[i][j])
                else:
                    j+=1
        
def get_associate_rules(data_floder,object_col,threshold_support,threshold_confidence):
    '''
    获取关联规则
    params:
        data_floder:数据文件夹
        object_col:挖掘对象
        support_threshold:支持度阈值[0,1]
        confidence_threshold:置信度阈值[0,1]
    returns:
        useful_rules:获取的有效的强关联规则
    '''
    data=readFile(data_floder,object_col) # 读取文件
    database=dataPrepoccess(data) # 数据预处理
    keywords=Apriori(database,threshold_support) # Apriori算法计算频繁项集
    frequent_sets=list(keywords.keys()) # 找出的所有频繁项集
    print('频繁项集: ',frequent_sets)
    # 找关联规则
    rules=[]
    for frequent_set in frequent_sets: # 遍历每一个频繁项集
        frequent_set=set(frequent_set)
        for i in range(1, len(frequent_set)):
            for itemset in itertools.combinations(frequent_set, i): # 寻找每一个位数的子频繁项集
                itemset = set(itemset)
                complement = frequent_set - itemset
                for j in range(1, len(complement) + 1):
                    for consequent in itertools.combinations(complement, j):
                        rule = (tuple(itemset), tuple(consequent))
                        rules.append(rule)
    print('关联规则: ',rules)
    # 计算每个关联规则的置信度
    strong_rules=[] # 筛选后置信度达标的规则
    confidences={} # 计算的强关联规则的置信度
    for antecedent, consequent in rules: # 遍历所有关联规则
        antecedent = set(antecedent) # 起因
        consequent = set(consequent) # 后果
        support_antecedent = 0
        support_rule = 0
        for transaction in database: # 遍历所有事务
            if antecedent.issubset(set(transaction)): # 如果包含起因
                support_antecedent += 1
                if consequent.issubset(set(transaction)): # 包含起因的同时做了结果
                    support_rule += 1
        confidence = support_rule / support_antecedent # 计算置信度
        print(f"规则 {antecedent} => {consequent} 的置信度为: {confidence:5f}")
        if confidence > threshold_confidence:  # 大于置信度阈值的才是有意义的规则
            strong_rules.append((antecedent,consequent))
            confidences[(list(antecedent)[0],list(consequent)[0])]=confidence
    print('强关联规则: ',strong_rules)
    # 计算每个强关联规则的提升度
    useful_rules=[] # 有效的强关联规则
    lifts={} # 有效的强关联规则的提升度
    for antecedent,consequent in strong_rules: # 遍历所有强关联规则
        confidence=confidences[(list(antecedent)[0],list(consequent)[0])] # 获取置信度
        support_consequent=0
        for transaction in database: # 遍历所有事务
            if consequent.issubset(set(transaction)): # 如果包含结果
                support_consequent += 1
        support_consequent/=len(database) # 计算P（结果）
        lift=confidence/support_consequent # 计算提升度
        print(f"规则 {antecedent} => {consequent} 的提升度为: {lift:5f}")
        if lift > 1: # 是有效的强关联规则
            useful_rules.append((antecedent,consequent))
            lifts[(list(antecedent)[0],list(consequent)[0])]=lift
    print('有用的强关联规则: ',useful_rules)
    # 输出最终结果
    tb=pt.PrettyTable() # 创建表格
    tb.field_names=['index','antecedence','consequence','confidence','lift'] # 添加表头
    index=0
    for antecedent,consequent in useful_rules: # 遍历所有有用的强关联规则
        index+=1 # 序号
        antecedent=list(antecedent)[0] # 起因
        consequent=list(consequent)[0] # 结果
        confidence=confidences[(antecedent,consequent)] # 置信度
        lift=lifts[(antecedent,consequent)] # 提升度
        tb.add_row([index,antecedent,consequent,confidence,lift]) # 添加行
    print(tb) # 输出表格
    return useful_rules,tb

if __name__=='__main__':
    useful_rules,tb=get_associate_rules('/home/ubuntu/mwz/Spatio-temporal_data_mining_and_analysis/data',['Author Keywords','Keywords Plus'],0.025,0.85)

    



    