# import matplotlib.pyplot as plt
# import pandas as pd
import csv
from collections import defaultdict

# plt.close("all")

# data = pd.read_csv("data.csv", index_col=0)

# print(data.to_string())
# print(data)

# data = defaultdict(list)
data = {}
n_answers = 0
with open('data.csv') as csvfile:
    # data = csv.DictReader(file)
    reader = csv.reader(csvfile)
    row_index = 0
    columns = []
    for row in reader:
        if row_index == 0:
            for i in range(len(row)):
                data[row[i]] = []
                columns.append(row[i])
        else:
            for i in range(len(row)):
                data[columns[i]].append(row[i])
            n_answers += 1
        row_index += 1

data.pop("Tidsmerke")
data.pop("Additional feedback")


# for k in data.keys():
#     print(k)

# for k, v in data.items():
#     print("-" * 30)
#     print(f"{k}:\n{v}")
options = ["Strongly Agree", "Agree", "Neither Agree nor Disagree", "Disagree", "Strongly Disagree", "Not tested"]
n_options = len(options)
results = {}

for key, val in data.items():
    # Count how many of each option
    count = [0 for _ in range(n_options)]
    avg = [0 for _ in range(n_options)]
    
    for answer in val:
        for i in range(n_options):
            if answer == options[i]:
                count[i] += 1
    summary = {}
    for i in range(n_options):
        # summary[options[i]] = {"count": count[i], "avg": f"{round((count[i] / n_answers) * 100, 0)}%"}
        summary[options[i]] = count[i]
    results[key] = summary


for key, val in results.items():
    print("-" * 30)
    print(f"{key}:")
    for k2, v2 in val.items():
        print(f"\t{k2}: {v2}")

print(f"n_answers = {n_answers}")
headers = ["Statements", "Strongly Agree", "Agree", "Neither Agree nor Disagree", "Disagree", "Strongly Disagree", "Not tested"]
with open('updated_data.csv', mode='w') as writefile:
    writer = csv.writer(writefile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    # write header
    writer.writerow(headers)
    for k, v in results.items():
        values = [x for x in v.values()]
        values.insert(0, k)
        print(f"values = {values}")
        writer.writerow(values)

print("finished writing to file")


