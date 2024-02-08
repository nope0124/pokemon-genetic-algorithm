from enum import Enum
import random

class Style(Enum):
    ノーマル = 0
    ほのお = 1
    みず = 2
    でんき = 3
    くさ = 4
    こおり = 5
    かくとう = 6
    どく = 7
    じめん = 8
    ひこう = 9
    エスパー = 10
    むし = 11
    いわ = 12
    ゴースト = 13
    ドラゴン = 14
    あく = 15
    はがね = 16
    フェアリー = 17

class Pokemon():
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

compatibility = [
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

def Battle(attacker, defender):
    def calculate(move):
        if move[0] == 0:
            return 0
        elif len(move) == 1:
            return sum(move) + 10
        elif len(move) == 2:
            return sum(move) - 10

    def get_attacker_score(attacker, defender):
        # タイプ1の技で攻撃
        move = []
        move.append(compatibility[attacker.style1][defender.style1] * 10)
        if not defender.is_single:
            move.append(compatibility[attacker.style1][defender.style2] * 10)
        move.sort()
        attacker_score = calculate(move)

        if not attacker.is_single:
            # タイプ2の技で攻撃
            move = []
            move.append(compatibility[attacker.style1][defender.style1] * 10)
            if not defender.is_single:
                move.append(compatibility[attacker.style1][defender.style2] * 10)
            move.sort()
            # より相性がいい技を採用
            return max(attacker_score, calculate(move))
        else:
            return attacker_score

    attacker_score = get_attacker_score(attacker, defender)
    defender_score = 50 - get_attacker_score(defender, attacker)

    return (attacker_score + defender_score)



# ポケモンを返す
def Crossover(pokemon1, pokemon2):
    random_number1 = random.randint(0, 1)
    random_number2 = random.randint(0, 1)
    style1 = -1
    style2 = -1
    if random_number1 == 0:
        style1 = pokemon1.style1
    elif random_number1 == 1:
        style1 = pokemon1.style2

    if random_number2 == 0:
        style2 = pokemon2.style1
    elif random_number2 == 1:
        style2 = pokemon2.style2

    return Pokemon(style1, style2)

def style_complex_display(gen, stylestyle):
    grass_dict = dict()
    for i in range(num_style):
        grass_dict[i] = 0
    for pokemon in gen:
        if pokemon.style1 == stylestyle:
            grass_dict[pokemon.style2] += 1
        elif pokemon.style2 == stylestyle:
            grass_dict[pokemon.style1] += 1
    
    sorted_style_items = sorted(grass_dict.items(), key=lambda item: item[1])

    for key, value in sorted_style_items:
        print(f"Style: {Style(key).name}, Count: {value}")





max_iteration = 1
population = 1000
num_style = 18

if __name__ == "__main__":
    random.seed(0)
    # init
    gen = []
    for i in range(num_style):
        for j in range(population):
            gen.append(Pokemon(i))

    # 数世代回す
    for _ in range(max_iteration):
        print("iteration: ", _)
        living_gen = []
        next_gen = []

        # 全てのポケモンを適当に戦わせる
        for i in range(num_style*population//2):
            while True:
                random_number1 = 0
                random_number2 = random.randint(0, len(gen) - 1)
                if random_number1 != random_number2:
                    break
            pokemon2 = gen.pop(random_number2)
            pokemon1 = gen.pop(random_number1)
            prob = Battle(pokemon1, pokemon2)
            print(f"{pokemon1}, {pokemon2}, point: {prob}")
            if prob > random.randint(0, 99):
                living_gen.append(pokemon1)
            else:
                living_gen.append(pokemon2)


        # 交叉
        for pokemon in living_gen:
            while True:
                random_number = random.randint(0, len(living_gen) - 1)
                if pokemon != living_gen[random_number]:
                    break
            tmp_pokemon = living_gen[random_number]
            new_pokemon = Crossover(pokemon, tmp_pokemon)
            next_gen.append(new_pokemon)

        # 余った枠はランダムに交叉させる
        num_next_gen = len(next_gen)
        for i in range(num_style*population - num_next_gen):
            while True:
                random_number1 = random.randint(0, len(living_gen) - 1)
                random_number2 = random.randint(0, len(living_gen) - 1)
                if random_number1 != random_number2:
                    break
            pokemon1 = living_gen[random_number1]
            pokemon2 = living_gen[random_number2]
            new_pokemon = Crossover(pokemon1, pokemon2)
            next_gen.append(new_pokemon)

        gen = next_gen[:]
        style_dict = dict()
        for i in range(num_style):
            style_dict[i] = 0
        for pokemon in gen:
            if pokemon.is_single:
                style_dict[pokemon.style1] += 1
            else:
                style_dict[pokemon.style1] += 1
                style_dict[pokemon.style2] += 1
        
        sorted_style_items = sorted(style_dict.items(), key=lambda item: item[1])

        for key, value in sorted_style_items:
            print(f"Style: {Style(key).name}, Count: {value}")
        # style_complex_display(gen, Style.Bug.value)
                
                



    dict = dict()
    for pokemon in gen:
        if pokemon not in dict:
            dict[pokemon] = 0
        dict[pokemon] += 1
    sorted_items = sorted(dict.items(), key=lambda item: item[1])

    for key, value in sorted_items:
        print(f"Pokemon: {key}, Count: {value}")
