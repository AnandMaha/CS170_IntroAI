## Feature Selection for Classification
#   Nearest Neighbor w/ a) Forward Selection ; b) Backward Elimination
#   Small Dataset -- 111
#   Large Dataset -- 14
 
from copy import deepcopy
import time
import math
import matplotlib.pyplot as plt # plot Runtime(s) v. Depth of Solution

def forward_select(data, def_rate):
    start_time = time.time()
    acc_y = []
    acc_x = []
    acc_y.append(round(def_rate*100,2))
    acc_x.append([])

    print("Nearest Neighbor Search begins with forward selection...\n")
    print("Feature set [] has an accuracy of",round(def_rate*100,2),"% (the default rate)\n")

    best_accuracy_total = def_rate
    best_features = []
    features_used = []
    total_features = [i for i in range(1,len(data[0]))]
    for z in range(len(data[0])-1): # add 1 of each feature
        if z >=20:
            break
        best_accuracy = -1
        best_feature_to_add = -1
        features_to_check = list(set(total_features).difference(features_used))
        for f in features_to_check: # check which feature to add
            num_crrct_clss = 0 # count correct classifications for accuracy calc.
            temp_features = features_used + [f]
            for i in range(len(data)): # check if each data point would get classified correctly
                close_class = -1 # no class label will ever be negative
                close_dist = float("inf")
                for j in range(len(data)): # the other data
                    if i != j:
                        check_data = [data[i][k] for k in temp_features]
                        test_data = [data[j][k] for k in temp_features]
                        curr_dist = math.sqrt(sum([(a - b)*(a - b) for (a,b) in zip(check_data, test_data)]))
                        if curr_dist < close_dist:
                            close_class = data[j][0]
                            close_dist = curr_dist
                if close_class == data[i][0]:
                    num_crrct_clss += 1
            accuracy =  num_crrct_clss / len(data)
            print("Feature set",temp_features,"has an accuracy of",round(accuracy*100,2),"%")
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_feature_to_add = f
        # add the best accuracy feature
        features_used.append(best_feature_to_add)
        acc_y.append(round(best_accuracy*100,2))
        acc_x.append(deepcopy(features_used))
        print("The best feature set is",features_used,"with an accuracy of",round(best_accuracy*100,2),"%\n")
        if best_accuracy > best_accuracy_total:
            best_accuracy_total = best_accuracy
            best_features = deepcopy(features_used)
    print("Nearest Neighbor Search with forward selection has finished.\n")
    print("The best feature set is",best_features,"with accuracy:",round(best_accuracy_total*100,2),"%\n")
    tot_time = time.time() - start_time
    return (tot_time, acc_y, acc_x)

def backward_elim(data, def_rate):
    start_time = time.time()
    acc_y = []
    acc_x = []

    print("Nearest Neighbor Search begins with backward elimination...\n")
    best_accuracy_total = def_rate
    best_features = []
    features_used = [i for i in range(1,len(data[0]))]
    for z in range(len(data[0])-2): # remove 1 of each feature
        best_accuracy = -1
        best_feature_to_remove = -1
        if z == 0: # print all features
            num_crrct_clss = 0 # count correct classifications for accuracy calc.
            temp_features = deepcopy(features_used)
            for i in range(len(data)): # check if each data point would get classified correctly
                close_class = -1 # no class label will ever be negative
                close_dist = float("inf")
                for j in range(len(data)): # the other data
                    if i != j:
                        check_data = [data[i][k] for k in temp_features]
                        test_data = [data[j][k] for k in temp_features]
                        curr_dist = math.sqrt(sum([(a - b) * (a - b) for (a,b) in zip(check_data, test_data)]))
                        if curr_dist < close_dist:
                            close_class = data[j][0]
                            close_dist = curr_dist
                if close_class == data[i][0]:
                    num_crrct_clss += 1
            accuracy =  num_crrct_clss / len(data)
            acc_y.append(round(accuracy*100,2))
            acc_x.append(temp_features)
            print("Feature set",temp_features,"has an accuracy of",round(accuracy*100,2),"%\n")
        for f in features_used: # check which feature to remove
            num_crrct_clss = 0 # count correct classifications for accuracy calc.
            temp_features = list(set(features_used).difference([f]))
            for i in range(len(data)): # check if each data point would get classified correctly
                close_class = -1 # no class label will ever be negative
                close_dist = float("inf")
                for j in range(len(data)): # the other data
                    if i != j:
                        check_data = [data[i][k] for k in temp_features]
                        test_data = [data[j][k] for k in temp_features]
                        curr_dist = math.sqrt(sum([(a - b) * (a - b) for (a,b) in zip(check_data, test_data)]))
                        if curr_dist < close_dist:
                            close_class = data[j][0]
                            close_dist = curr_dist
                if close_class == data[i][0]:
                    num_crrct_clss += 1
            accuracy =  num_crrct_clss / len(data)
            print("Feature set",temp_features,"has an accuracy of",round(accuracy*100,2),"%")
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_feature_to_remove = f
        # remove the feature that increases accuracy the most
        features_used = list(set(features_used).difference([best_feature_to_remove]))
        acc_y.append(round(best_accuracy*100,2))
        acc_x.append(deepcopy(features_used))
        print("The best feature set is",features_used,"with an accuracy of",round(best_accuracy*100,2),"%\n")
        if best_accuracy > best_accuracy_total:
            best_accuracy_total = best_accuracy
            best_features = deepcopy(features_used)
    acc_y.append(round(def_rate*100,2))
    acc_x.append([])
    print("Feature set [] has an accuracy of",round(def_rate*100,2),"% (the default rate)\n")
    print("Nearest Neighbor Search with backward elimination has finished.\n")
    print("The best feature set is",best_features,"with accuracy:",round(best_accuracy_total*100,2),"\n")
    tot_time = time.time() - start_time
    return (tot_time, acc_y, acc_x)

print("Feature Selection Algorithm using Nearest Neighbor")
# file to read
filename = input("Name of file with data -> ")
filename = "CS170_Large_Data__14.txt"
algo_choice = int(input("Type (1) for forward selection, or (2) for backward elimination -> "))
print()

data = []
for line in open(filename):
    data.append([float(n) for n in line.split()])

# normalize data for all features 
# (for nearest neighbor distance calculation)
for i in range(1,len(data[0])): # for each feature
    feat_col = []
    for j in range(len(data)): # through all data
        feat_col.append(data[j][i])
    min_col = min(feat_col)
    max_col = max(feat_col)
    for k in range(len(feat_col)):
        data[k][i] = (feat_col[k] - min_col) / (max_col  - min_col)

# no features accuracy == default rate (# most common class / total data)
class_dist = []
for i in range(len(data)):
    class_dist.append(data[i][0])
def_rate = class_dist.count(max(set(class_dist), key = class_dist.count)) / len(data)

print("There are",len(data),"data points and",len(data[0])-1,"features.\n")

runtime = -1 # run time 
acc_y = [] # y-axis plotting (accuracy)
acc_x = [] # x-axis plotting (Feature set)
if algo_choice == 1: # forward
    (runtime, acc_y, acc_x) = forward_select(data, def_rate)
elif algo_choice == 2: # backward
    (runtime, acc_y, acc_x) = backward_elim(data, def_rate)
else:
    print("You entered an invalid selection method choice -.-")

# Make acc_x lists into string
acc_x = [str(x) for x in acc_x]
# Print runtime
print("Runtime:",runtime,"seconds \n")
# Scatter Plot
plt.plot(acc_x, acc_y, marker="*",color="black",mfc="red")
plt.xlabel('Feature Set')
plt.ylabel('Accuracy of Classification (%)')
plt.xticks(rotation=45)
plt.title('Accuracy of Classification (%) vs. Feature Set')
plt.show()
