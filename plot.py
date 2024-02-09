import json
from style import Style
import matplotlib.pyplot as plt

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

num_of_generations = 1000 # 世代数
population_size = 1000 # 個体数
num_of_styles = 18 # タイプ数
plot_status = 0

if __name__ == "__main__":
    plt.rcParams["font.family"] = "MS Gothic"
    plt.figure(figsize=(10, 6))

    # 全世代のタイプ情報
    all_styles = [[] for i in range(num_of_styles)]

    for generation in range(num_of_generations + 1):
        if generation % 100 == 0:
            print(f"第{generation}世代")
        tmp_styles = [0 for i in range(num_of_styles)]
        with open(f"results/genetic_algorithm_data_{generation}.json", "r") as file:
            data = json.load(file)
            for i in range(num_of_styles*population_size):
                style1 = data["population"][i]["style1"]
                style2 = data["population"][i]["style2"]
                if style1 == style2:
                    tmp_styles[style1] += 1
                else:
                    tmp_styles[style1] += 1
                    tmp_styles[style2] += 1
        for i in range(num_of_styles):
            all_styles[i].append(tmp_styles[i])

        # 最終世代の各タイプごとの棒グラフ
        if plot_status == 1 and generation == num_of_generations:
            indexed_styles = list(enumerate(tmp_styles))
            sorted_indexed_styles = sorted(indexed_styles, key=lambda x: x[1])

            bars = plt.barh(
                [Style(index).name for index, value in sorted_indexed_styles],
                [value for index, value in sorted_indexed_styles],
                color=[style_colors[index] for index, value in sorted_indexed_styles]
            )

            # 各棒に値を表示
            for bar in bars:
                xval = bar.get_width()
                plt.text(xval + 20, bar.get_y() + bar.get_height()/2, round(xval, 2), ha="left", va="center")

        # 最終世代にいるポケモンのタイプごとの棒グラフ
        if plot_status == 2 and generation == num_of_generations:
            styles_dict = dict()
            for i in range(num_of_styles*population_size):
                style1 = data["population"][i]["style1"]
                style2 = data["population"][i]["style2"]
                if (style1, style2) not in styles_dict:
                    styles_dict[(style1, style2)] = 0
                styles_dict[(style1, style2)] += 1
            sorted_style_items = sorted(styles_dict.items(), key=lambda item: item[1])[-15:]
            # sorted_style_items_15 = sorted_style_items
            for index, value in sorted_style_items:
                category = f"{Style(index[0]).name}・{Style(index[1]).name}"
                if index[0] == index[1]:
                    category = f"{Style(index[0]).name}"
                bars = plt.barh(category, value / 2, color=style_colors[index[0]])
                bars = plt.barh(category, value / 2, left=value / 2, color=style_colors[index[1]])
                for bar in bars:
                    xval = bar.get_width()*2
                    plt.text(xval + 5, bar.get_y() + bar.get_height()/2, round(value, 2), ha="left", va="center")

    if plot_status == 0:
        # 各項目のデータをプロット
        for i in range(num_of_styles):
            plt.plot(list(range(num_of_generations + 1)), all_styles[i], label=Style(i).name, color=style_colors[i])

        plt.xlabel("世代数")
        plt.ylabel("タイプ別個体数")
        plt.legend(loc="upper left")

    # グラフの表示
    plt.show()
