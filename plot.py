import json
from enum import Enum

num_of_generations = 1000
population_size = 1000
num_of_styles = 18

class Style(Enum):
    ノーマル = 0 # Normal
    ほのお = 1 # Fire
    みず = 2 # Water
    でんき = 3 # Electric
    くさ = 4 # Grass
    こおり = 5 # Ice
    かくとう = 6 # Fighting
    どく = 7 # Poison
    じめん = 8 # Ground
    ひこう = 9 # Flying
    エスパー = 10 # Psychic
    むし = 11 # Bug
    いわ = 12 # Rock
    ゴースト = 13 # Ghost
    ドラゴン = 14 # Dragon
    あく = 15 # Drak
    はがね = 16 # Steel
    フェアリー = 17 # Fairy

style_colors = [
    "#aea886", # Normal
    "#f45c19", # Fire
    "#4a96d6", # Water
    "#eaa317", # Electric
    "#28b25c", # Grass
    "#45a9c0", # Ice
    "#9a3d3e", # Fighting
    "#8f5b98", # Poison
    "#916d3c", # Ground
    "#7e9ecf", # Flying
    "#d56d8b", # Psychic
    "#989001", # Bug
    "#878052", # Rock
    "#555fa4", # Ghost
    "#454ba6", # Dragon
    "#7a0049", # Dark
    "#9b9b9b", # Steel
    "#ffbbff" # Fairy
]

import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "MS Gothic"
plt.figure(figsize=(10, 6))


plt.title("第1000世代の複合タイプ含めたタイプ別個体数")
# plt.xlabel("世代数")
# plt.ylabel("タイプ別個体数")
# タイプ
styles = [[] for i in range(num_of_styles)]

for generation in range(num_of_generations + 1):
    styles2 = [0 for i in range(num_of_styles)]
    with open(f"results/genetic_algorithm_data_{generation}.json", "r") as file:
        data = json.load(file)
        for i in range(num_of_styles*population_size):
            style1 = data["population"][i]["style1"]
            style2 = data["population"][i]["style2"]
            if style1 == style2:
                styles2[style1] += 1
            else:
                styles2[style1] += 1
                styles2[style2] += 1
    
    for i in range(num_of_styles):
        styles[i].append(styles2[i])
    print(generation)
    if False:
        # 各要素とそのインデックスをタプルにする
        indexed_arr = list(enumerate(styles2))

        # タプルの2番目の要素（配列の値）に基づいてソートする
        sorted_indexed_arr = sorted(indexed_arr, key=lambda x: x[1])

        # ソートされた配列と元のインデックスを表示
        for index, value in sorted_indexed_arr:
            print(f"Value: {value}, Original Index: {index}")
        
        sorted_values = [value for index, value in sorted_indexed_arr]
        categorys = [Style(index).name for index, value in sorted_indexed_arr]
        sorted_colors = [style_colors[index] for index, value in sorted_indexed_arr]
        bars = plt.barh(categorys, sorted_values, color=sorted_colors)
        # bars = plt.bar(categories, values, color=colors)

        # 各棒に値を表示
        for bar in bars:
            xval = bar.get_width()
            plt.text(xval + 20, bar.get_y() + bar.get_height()/2, round(xval, 2), ha='left', va='center')
    if generation == num_of_generations:
        complex_dict = dict()
        for i in range(num_of_styles*population_size):
            style1 = data["population"][i]["style1"]
            style2 = data["population"][i]["style2"]
            if (style1, style2) not in complex_dict:
                complex_dict[(style1, style2)] = 0
            complex_dict[(style1, style2)] += 1
        sorted_style_items = sorted(complex_dict.items(), key=lambda item: item[1])
        sorted_style_items_10 = sorted_style_items[-15:]
        categorys = [f"{Style(index[0]).name}・{Style(index[1]).name}" for index, value in sorted_style_items_10]
        sorted_values = [value for index, value in sorted_style_items_10]
        for index, value in sorted_style_items_10:
            category = f"{Style(index[0]).name}・{Style(index[1]).name}"
            if index[0] == index[1]:
                category = f"{Style(index[0]).name}"
            plt.barh(category, value / 2, color=style_colors[index[0]])
            bars = plt.barh(category, value / 2, left=value / 2, color=style_colors[index[1]])
            for bar in bars:
                xval = bar.get_width()*2
                plt.text(xval + 5, bar.get_y() + bar.get_height()/2, round(value, 2), ha='left', va='center')


dominant_style_ids = [2, 1, 3, 4, 5]
labels = [Style(dominant_style_ids[i]).name for i in range(len(dominant_style_ids))]
colors = [style_colors[dominant_style_ids[i]] for i in range(len(dominant_style_ids))]

def tyuusyutu(styles, style_ids):
    ret = []
    for i in range(len(style_ids)):
        ret.append(styles[style_ids[i]])
    return ret
print(styles)


plt.figure(figsize=(10, 6))

# 遺伝的アルゴリズムの結果を模擬するデータ
# 例: 18項目の進化を10世代にわたって表す
# 各項目はリストのリストで表現される
ga_results = [[i + j for j in range(10)] for i in range(18)]

# 世代数（例として0から9までの10世代を仮定）
generations = list(range(num_of_generations + 1))

# 各項目のデータをプロット
for i in range(18):
    plt.plot(generations, styles[i], label=Style(i).name, color=style_colors[i])

# グラフのタイトルと軸ラベルの設定
plt.title("")
plt.xlabel("世代数")
plt.ylabel("タイプ別個体数")

# 凡例の表示
plt.legend(loc='upper left')

# グラフの表示
plt.show()
