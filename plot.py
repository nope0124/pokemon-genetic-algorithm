import json
from enum import Enum

num_of_generations = 1000
population_size = 1000
num_of_styles = 18

class Style(Enum):
    Normal = 0 # ノーマル
    Fire = 1 # ほのお
    Water = 2 # みず
    Electric = 3 # でんき
    Grass = 4 # くさ
    Ice = 5 # こおり
    Fighting = 6 # かくとう
    Poison = 7 # どく
    Ground = 8 # じめん
    Flying = 9 # ひこう
    Psychic = 10 # エスパー
    Bug = 11 # むし
    Rock = 12 # いわ
    Ghost = 13 # ゴースト
    Dragon = 14 # ドラゴン
    Dark = 15 # あく
    Steel = 16 # はがね
    Fairy = 17 # フェアリー

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

dominant_style_ids = [2, 1, 3, 4, 5]
labels = [Style(dominant_style_ids[i]).name for i in range(len(dominant_style_ids))]
colors = [style_colors[dominant_style_ids[i]] for i in range(len(dominant_style_ids))]

def tyuusyutu(styles, style_ids):
    ret = []
    for i in range(len(style_ids)):
        ret.append(styles[style_ids[i]])
    return ret
print(styles)
    

import matplotlib.pyplot as plt

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
plt.xlabel("Generation")
plt.ylabel("Count By Type")

# 凡例の表示
plt.legend(loc='upper left')

# グラフの表示
plt.show()
