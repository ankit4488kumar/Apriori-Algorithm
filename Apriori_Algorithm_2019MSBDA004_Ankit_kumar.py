#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import itertools


# In[2]:


data = pd.read_csv('/home/akki/Documents/3rd Sem books/Data Mining/Assignments/GroceryStoreDataSet.csv')


# In[3]:


data


# In[4]:


data.shape


# In[5]:


data_arr = data.to_numpy()
data_arr


# In[6]:


items_list=[]

order = []
for i in data_arr:
    t = i[0].split(',')
    
    items_list.append(t)

print("Given Item list: ",items_list)
print('')

for i in data_arr:
    t = i[0].split(',')
    for j in t:
        order.append(j)


seq = list(set(order))
print("Order of Items: ",seq)


# In[7]:


num_items_list = len(items_list)
num_items_list


# In[8]:


support_min = 2/19
C = {}
L = {}
itemset_size = 1
Discarded = {itemset_size : []}
C.update({itemset_size : [ [f] for f in seq ]})


# In[9]:


C


# In[10]:


def numbers_of_occurences(itemset , items_list):
    count = 0
    for i in range(len(items_list)):
        if set(itemset).issubset(set(items_list[i])):
            count +=1
    return count


# In[11]:


def item_frequency(itemsets , items_list , support_min , pre_discarded):
    L = []
    sup_count = []
    latest_discarded = []
   
    
    k = len(pre_discarded.keys())
    
    for i in range(len(itemsets)):
        discarded_before = False
        if k > 0:
            for it in pre_discarded[k]:
                if set(it).issubset(set(itemsets[i])):
                    discarded_before = True
                    break
        
        if not discarded_before:
            count = numbers_of_occurences(itemsets[i], items_list)
            if count/len(items_list) >= support_min:
                L.append(itemsets[i])
                sup_count.append(count)
            else:
                latest_discarded.append(itemsets[i])
                
    return L , sup_count , latest_discarded


# In[12]:


sup_count_L = {}
f, supp , latest_discarded = item_frequency(C[itemset_size], items_list , support_min , Discarded)
Discarded.update({itemset_size : latest_discarded})
L.update({itemset_size : f})
sup_count_L.update({itemset_size :supp})


# In[13]:


def print_table(T, sup_count):
    print("Itemset ==> Frequency")
    for k in range(len(T)):
        print("{} ==> {}".format(T[k], sup_count[k]))
    print("\n\n")


# In[14]:


print("L1 : \n")
print_table(L[1] , sup_count_L[1])


# In[15]:


def joining_of_itemsets(set_of_items, seq):
    C =[]
    for i in range(len(set_of_items)):
        for j in range(i+1, len(set_of_items)):
            item_out = joining_two_itemsets(set_of_items[i], set_of_items[j], seq)
            if len(item_out) > 0:
                C.append(item_out)
    return C

def joining_two_itemsets(item1, item2, seq):
    item1.sort(key= lambda x: seq.index(x))
    item2.sort(key= lambda x: seq.index(x))
    
    for i in range(len(item1)-1):
        if item1[i] != item2[i]:
            return []
    
    if seq.index(item1[-1]) < seq.index(item2[-1]):
        return item1 + [item2[-1]]
    
    return []


# In[16]:


k = itemset_size + 1
convergence = False
while convergence == 0:
    C.update({k : joining_of_itemsets(L[k-1], seq)})
    print("Table C{}: \n".format(k))
    print_table(C[k], [numbers_of_occurences(it, items_list) for it in C[k]])
    f, supp, latest_discarded = item_frequency(C[k], items_list , support_min , Discarded)
    Discarded.update({k : latest_discarded})
    L.update({k : f})
    sup_count_L.update({k : supp})
    if len(L[k]) == 0:
        convergence = True
    else:
        print("Table L{}: \n".format(k))
        print_table(L[k], sup_count_L[k])
    k +=1


# In[17]:


from itertools import combinations, chain

def powerset(s):
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))


# In[18]:


def write_rules(X, X_S, S, conf, supp, num_items_list):
    out_rules = ""
    out_rules += " Frequent Itemset : {} \n ".format(X)
    out_rules += "    Rule : {} -> {} \n".format(list(S),list(X_S))
    out_rules += "    Conf : {0:2.3f} ".format(conf)
    out_rules += "    Support : {0:2.3f} ".format(supp / num_items_list)
    
    return out_rules


# In[23]:


conf_min = 0.3
apriori_str =""
for i in range(1, len(L)):
    for j in range(len(L[i])):
        s = powerset(L[i][j])
        s.pop()
        for z in s:
            S = set(z)
            X = set(L[i][j])
            X_S = set(X-S)
            sup_x = numbers_of_occurences(X, items_list)
            sup_x_s = numbers_of_occurences(X_S, items_list)
            conf = sup_x / numbers_of_occurences(S, items_list) 
            
            if conf >= conf_min and sup_x >= support_min:
                apriori_str += write_rules(X, X_S, S, conf, sup_x, num_items_list)
                


# In[24]:


print(apriori_str)


# In[ ]:




