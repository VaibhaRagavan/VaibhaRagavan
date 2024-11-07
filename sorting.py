#! /usr/bin/python3
data = {
    "VAIBHA": {
        "age": 25,
        "gender": "f",
        "weight": 91,
        "marital status": "married",
        "employment": "unemployed",
        "countrty": "Ireland",
        "marks": [90, 60, 70, 50],
    },
    "VIJAY": {
        "age": 34,
        "gender": "M",
        "weight": 92,
        "marital status": "married",
        "employment": "employed",
        "countrty": "Ireland",
        "marks": [80, 60, 50, 50],
    },
    "VIDHUN": {
        "age": 2,
        "gender": "M",
        "weight": 14,
        "marital status": "unmarried",
        "employment": "unemployed",
        "countrty": "Ireland",
        "marks": [70, 60, 70, 67],
    },
    "SUDHARSAN": {
        "age": 20,
        "gender": "M",
        "weight": 95,
        "marital status": "unmarried",
        "employment": "unemployed",
        "countrty": "India",
        "marks": [89, 78, 70, 50],
    },
    "VAISHNAVI": {
        "age": 30,
        "gender": "f",
        "weight": 64,
        "marital status": "married",
        "employment": "employed",
        "countrty": "India",
        "marks": [94, 67, 70, 59],
    },
    "VINU": {
        "age": 37,
        "gender": "m",
        "weight": 80,
        "marital status": "married",
        "employment": "employed",
        "countrty": "India",
        "marks": [93, 56, 80, 40],
    },
        "VINU": {
        "age": 37,
        "gender": "m",
        "weight": 80,
        "marital status": "married",
        "employment": "employed",
        "countrty": "India",
        "marks": [93, 56, 80, 40],
    },
        "ANIRUDH": {
        "age": 8,
        "gender": "m",
        "weight": 20,
        "marital status": "unmarried",
        "employment": "unemployed",
        "countrty": "India",
        "marks": [93, 88, 80, 40],
    },
        "ANANYAA": {
        "age": 8,
        "gender": "f",
        "weight": 20,
        "marital status": "unmarried",
        "employment": "unemployed",
        "countrty": "India",
        "marks": [93, 88, 80, 40],
    },
        "SRIRAM": {
        "age": 37,
        "gender": "m",
        "weight": 80,
        "marital status": "married",
        "employment": "employed",
        "countrty": "Bahrain",
        "marks": [93, 88, 80, 40],
    },
        "SRIDEVI": {
        "age": 37,
        "gender": "f",
        "weight": 80,
        "marital status": "unmarried",
        "employment": "unemployed",
        "countrty": "India",
        "marks": [93, 88, 80, 40],
    },
}
s_age =[]
for name, value in data.items():
    for v_name, v_property in value.items():
        if v_name == "age":
            s_age.append(v_property)

n_sorted_age=sorted(list(set(s_age)), reverse=True)
print(n_sorted_age)
'''
for items in sorted_age:
    if items not in n_sorted_age:
        n_sorted_age.append(items)
'''
print(data)
sorted_data=dict(sorted(data.items()))
print(sorted_data)
for age in n_sorted_age:
    for name, value in sorted_data.items():
        if age==value["age"]:
            print(name,value["age"],value["gender"],value["employment"])

temp_vijay = {}
for k, v in data.items():
    temp_vijay[v["age"]] = []

for age, name in temp_vijay.items():
    for k,v in data.items():
        if age == v["age"]:
            name.append(k)
temp_vijay_sorted=dict(sorted(temp_vijay.items()))

for age, person in temp_vijay_sorted.items():
    for k,v in data.items():
        for per in sorted(person):
            if age == v["age"] and per == k:
                print(k,age)
