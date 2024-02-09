from enum import Enum
import random
import json
import os

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
    あく = 15 # Dark
    はがね = 16 # Steel
    フェアリー = 17 # Fairy

compatibility_table = [
    #N  F  W  E  G  I  F  P  G  F  P  B  R  G  D  D  S  F
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 1, 2], # Normal->
    [2, 1, 1, 2, 3, 3, 2, 2, 2, 2, 2, 3, 1, 2, 1, 2, 3, 2], # Fire->
    [2, 3, 1, 2, 1, 2, 2, 2, 3, 2, 2, 2, 3, 2, 1, 2, 2, 2], # Water->
    [2, 2, 3, 1, 1, 2, 2, 2, 0, 3, 2, 2, 2, 2, 1, 2, 2, 2], # Electric->
    [2, 1, 3, 2, 1, 2, 2, 1, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2], # Grass->
    [2, 1, 1, 2, 3, 1, 2, 2, 3, 3, 2, 2, 2, 2, 3, 2, 1, 2], # Ice->
    [3, 2, 2, 2, 2, 3, 2, 1, 2, 1, 1, 1, 3, 0, 2, 3, 3, 1], # Fighting->
    [2, 2, 2, 2, 3, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 0, 3], # Poison->
    [2, 3, 2, 3, 1, 2, 2, 3, 2, 0, 2, 1, 3, 2, 2, 2, 3, 2], # Ground->
    [2, 2, 2, 1, 3, 2, 3, 2, 2, 2, 2, 3, 1, 2, 2, 2, 1, 2], # Flying->
    [2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 1, 2, 2, 2, 2, 0, 1, 2], # Psychic->
    [2, 1, 2, 2, 3, 2, 1, 1, 2, 1, 3, 2, 2, 1, 2, 3, 1, 1], # Bug->
    [2, 3, 2, 2, 2, 3, 1, 2, 1, 3, 2, 3, 2, 2, 2, 2, 1, 2], # Rock->
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 2, 1, 2, 2], # Ghost->
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 0], # Dragon->
    [2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 3, 2, 2, 3, 2, 1, 2, 1], # Dark->
    [2, 1, 1, 1, 2, 3, 1, 2, 2, 2, 2, 2, 3, 2, 2, 2, 1, 3], # Steel->
    [2, 1, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 2, 2, 3, 3, 1, 2], # Fairy->
]

class Pokemon(Object):
    def __init__(self, style1, style2=None):
        if style2 == None:
            self.style1 = self.style2 = style1
        else:
            self.style1 = min(style1, style2)
            self.style2 = max(style1, style2)

    @property
    def is_single(self):
        return self.style1 == self.style2

    def __repr__(self):
        if self.is_single:
            return f"タイプ: {Style(self.style1).name}"
        else:
            return f"タイプ1: {Style(self.style1).name}, タイプ2: {Style(self.style2).name}"
        
    def __str__(self):
        if self.is_single:
            return f"タイプ: {Style(self.style1).name}"
        else:
            return f"タイプ1: {Style(self.style1).name}, タイプ2: {Style(self.style2).name}"
        
    def __hash__(self):
        if self.style1 == self.style2:
            return hash(f"Style: {Style(self.style1).name}")
        else:
            return hash(f"Style1: {Style(self.style1).name}, Style2: {Style(self.style2).name}")
        
    def __eq__(self, other):
        if self.style1 < self.style2 and other.style1 < other.style2:
            return (self.style1 == other.style1 and self.style2 == other.style2)
        elif self.style1 >= self.style2 and other.style1 < other.style2:
            return (self.style2 == other.style1 and self.style1 == other.style2)
        elif self.style1 < self.style2 and other.style1 >= other.style2:
            return (self.style1 == other.style2 and self.style2 == other.style1)
        elif self.style1 >= self.style2 and other.style1 >= other.style2:
            return (self.style2 == other.style2 and self.style1 == other.style1)
    
    def evaluate_battle(self, other):
        def get_attacker_score(attacker, defender):
            def calculate_score(moves):
                if moves[0] == 0:
                    return 0
                elif len(moves) == 1:
                    return sum(moves) + 10
                elif len(moves) == 2:
                    return sum(moves) - 10

            # タイプ1の技で攻撃
            moves = []
            moves.append(compatibility_table[attacker.style1][defender.style1] * 10)
            if not defender.is_single:
                moves.append(compatibility_table[attacker.style1][defender.style2] * 10)
            moves.sort()
            attacker_score = calculate_score(moves)

            if not attacker.is_single:
                # タイプ2の技で攻撃
                moves = []
                moves.append(compatibility_table[attacker.style2][defender.style1] * 10)
                if not defender.is_single:
                    moves.append(compatibility_table[attacker.style2][defender.style2] * 10)
                moves.sort()
                # より相性がいい技を採用
                return max(attacker_score, calculate_score(moves))
            else:
                return attacker_score

        attacker_score = get_attacker_score(self, other)
        defender_score = 50 - get_attacker_score(other, self)

        return (attacker_score + defender_score)

    def crossover(self, other):
        style1 = self.style1 if random.randint(0, 1) == 0 else self.style2
        style2 = other.style1 if random.randint(0, 1) == 0 else other.style2

        return Pokemon(style1, style2)

def style_complex_display(current_pokemons, stylestyle):
    grass_dict = dict()
    for i in range(num_of_styles):
        grass_dict[i] = 0
    for pokemon in current_pokemons:
        if pokemon.style1 == stylestyle:
            grass_dict[pokemon.style2] += 1
        elif pokemon.style2 == stylestyle:
            grass_dict[pokemon.style1] += 1
    
    sorted_style_items = sorted(grass_dict.items(), key=lambda item: item[1])

    for key, value in sorted_style_items:
        print(f"Style: {Style(key).name}, Count: {value}")





num_of_generations = 1000 # 世代数
population_size = 1000 # 個体数
num_of_styles = 18 # タイプ数

if __name__ == "__main__":
    random.seed(0)
    if not os.path.exists("results"):
        os.mkdir("results")
        
    # 1. 初期設定
    current_pokemons = []
    for style in range(num_of_styles):
        for _ in range(population_size):
            current_pokemons.append(Pokemon(style))
    data = {
        "generation": 0,
        "population": [{"style1": pokemon.style1, "style2": pokemon.style2} for pokemon in current_pokemons]
    }

    with open(f"results/genetic_algorithm_data_0.json", "w") as file:
        json.dump(data, file)

    # 2. 数世代回す
    for generation in range(1, num_of_generations + 1):
        print("Generation: ", generation)

        # 2.1. 全てのポケモンを戦わせる
        surviving_pokemons = []
        for i in range(num_of_styles*population//2):
            pokemon1 = current_pokemons.pop(random.randint(1, len(current_pokemons) - 1))
            pokemon2 = current_pokemons.pop(0)
            prob = pokemon1.evaluate_battle(pokemon2)
            if _ == 1:
                print(f"{pokemon1}, {pokemon2}, point: {prob}")
            if prob > random.randint(0, 99):
                surviving_pokemons.append(pokemon1)
            else:
                surviving_pokemons.append(pokemon2)

        # 2.2. 交叉して次世代に繋げる
        next_pokemons = []
        for pokemon in surviving_pokemons:
            while True:
                random_number1 = random.randint(0, num_of_styles*population//2 - 1)
                random_number2 = random.randint(0, num_of_styles*population//2 - 1)
                if pokemon != surviving_pokemons[random_number1] and pokemon != surviving_pokemons[random_number2] and random_number1 != random_number2:
                    break
            other_pokemon1 = surviving_pokemons[random_number1]
            other_pokemon2 = surviving_pokemons[random_number2]
            next_pokemons.append(pokemon.crossover(other_pokemon1))
            next_pokemons.append(pokemon.crossover(other_pokemon2))
        current_pokemons = next_pokemons[:]            

        # 3. データをjsonで出力
        data = {
            "generation": generation,
            "population": [{"style1": pokemon.style1, "style2": pokemon.style2} for pokemon in current_pokemons]
        }
        with open(f"results/genetic_algorithm_data_{generation}.json", "w") as file:
            json.dump(data, file)

        # 上位5位までのタイプを出力
        dominant_styles_dict = dict()
        for i in range(num_of_styles):
            dominant_styles_dict[i] = 0
        for pokemon in current_pokemons:
            if pokemon.is_single:
                dominant_styles_dict[pokemon.style1] += 1
            else:
                dominant_styles_dict[pokemon.style1] += 1
                dominant_styles_dict[pokemon.style2] += 1
        
        sorted_styles = reverse(sorted(dominant_styles_dict.items(), key=lambda item: item[1]))
        top5_styles = sorted_styles[:5]

        for style, value in top5_styles:
            print(f"タイプ: {Style(style).name}, {value}匹")

    styles_dict = dict()
    for pokemon in current_pokemons:
        if pokemon not in styles_dict:
            styles_dict[pokemon] = 0
        styles_dict[pokemon] += 1
    sorted_styles = reverse(sorted(dict.items(), key=lambda item: item[1]))

    for pokemon, value in sorted_styles:
        if pokemon.is_single:
            print(f"タイプ: {Style(pokemon.style1).name}, {value}匹")
        else:
            print(f"タイプ1: {Style(pokemon.style1).name}, タイプ2: {Style(pokemon.style2).name}, {value}匹")
