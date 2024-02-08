from enum import Enum
import random

class Type(Enum):
    Normal = 0
    Fire = 1
    Water = 2
    Electric = 3
    Grass = 4
    Ice = 5
    Fighting = 6
    Poison = 7
    Ground = 8
    Flying = 9
    Psychic = 10
    Bug = 11
    Rock = 12
    Ghost = 13
    Dragon = 14
    Dark = 15
    Steel = 16
    Fairy = 17

class Pokemon():
    def __init__(self, type1, type2=None):
        self.type1 = type1
        if type2 == None:
            self.type2 = type1
        else:
            self.type2 = type2
        self.is_dead = False

    def __repr__(self):
        if self.type1 == self.type2:
            return f"Type: {Type(self.type1).name}"
        elif self.type1 < self.type2:
            return f"Type1: {Type(self.type1).name}, Type2: {Type(self.type2).name}"
        elif self.type1 > self.type2:
            return f"Type1: {Type(self.type2).name}, Type2: {Type(self.type1).name}"
        
    def __str__(self):
        if self.type1 == self.type2:
            return f"Type: {Type(self.type1).name}"
        elif self.type1 < self.type2:
            return f"Type1: {Type(self.type1).name}, Type2: {Type(self.type2).name}"
        elif self.type1 > self.type2:
            return f"Type1: {Type(self.type2).name}, Type2: {Type(self.type1).name}"
        
    def __hash__(self):
        if self.type1 == self.type2:
            return hash(f"Type: {Type(self.type1).name}")
        elif self.type1 < self.type2:
            return hash(f"Type1: {Type(self.type1).name}, Type2: {Type(self.type2).name}")
        elif self.type1 > self.type2:
            return hash(f"Type1: {Type(self.type2).name}, Type2: {Type(self.type1).name}")
        
    def __eq__(self, other):
        if self.type1 < self.type2 and other.type1 < other.type2:
            return (self.type1 == other.type1 and self.type2 == other.type2)
        elif self.type1 >= self.type2 and other.type1 < other.type2:
            return (self.type2 == other.type1 and self.type1 == other.type2)
        elif self.type1 < self.type2 and other.type1 >= other.type2:
            return (self.type1 == other.type2 and self.type2 == other.type1)
        elif self.type1 >= self.type2 and other.type1 >= other.type2:
            return (self.type2 == other.type2 and self.type1 == other.type1)

compatibility = [
    #N  F  W  E  G  I  F  P  G  F  P  B  R  G  D  D  S  F
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 2, 1, 2], # Normal →
    [2, 1, 1, 2, 3, 3, 2, 2, 2, 2, 2, 3, 1, 2, 1, 2, 3, 2], # Fire →
    [2, 3, 1, 2, 1, 2, 2, 2, 3, 2, 2, 2, 3, 2, 1, 2, 2, 2], # Water →
    [2, 2, 3, 1, 1, 2, 2, 2, 0, 3, 2, 2, 2, 2, 1, 2, 2, 2], # Electric →
    [2, 1, 3, 2, 1, 2, 2, 1, 3, 1, 2, 1, 3, 2, 1, 2, 1, 2], # Grass →
    [2, 1, 1, 2, 3, 1, 2, 2, 3, 3, 2, 2, 2, 2, 3, 2, 1, 2], # Ice →
    [3, 2, 2, 2, 2, 3, 2, 1, 2, 1, 1, 1, 3, 0, 2, 3, 3, 1], # Fighting →
    [2, 2, 2, 2, 3, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 0, 3], # Poison →
    [2, 3, 2, 3, 1, 2, 2, 3, 2, 0, 2, 1, 3, 2, 2, 2, 3, 2], # Ground →
    [2, 2, 2, 1, 3, 2, 3, 2, 2, 2, 2, 3, 1, 2, 2, 2, 1, 2], # Flying →
    [2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 1, 2, 2, 2, 2, 0, 1, 2], # Psychic →
    [2, 1, 2, 2, 3, 2, 1, 1, 2, 1, 3, 2, 2, 1, 2, 3, 1, 1], # Bug →
    [2, 3, 2, 2, 2, 3, 1, 2, 1, 3, 2, 3, 2, 2, 2, 2, 1, 2], # Rock →
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 2, 1, 2, 2], # Ghost →
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 1, 0], # Dragon →
    [2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 3, 2, 2, 3, 2, 1, 2, 1], # Dark →
    [2, 1, 1, 1, 2, 3, 1, 2, 2, 2, 2, 2, 3, 2, 2, 2, 1, 3], # Steel →
    [2, 1, 2, 2, 2, 2, 3, 1, 2, 2, 2, 2, 2, 2, 3, 3, 1, 2], # Fairy →
]

def Battle(attacker, defender):
    point = 0

    attacker_score1 = 0
    attacker_score2 = 0
    move1 = []
    move1.append(compatibility[attacker.type1][defender.type1])
    if defender.type1 != defender.type2:
        move1.append(compatibility[attacker.type1][defender.type2])
    move1.sort()
    
    if move1[0] == 0:
        attacker_score1 = 0
    elif len(move1) == 1:
        attacker_score1 = sum(move1) + 1
    elif len(move1) == 2:
        attacker_score1 = sum(move1) - 1

    move1 = []
    move1.append(compatibility[attacker.type2][defender.type1])
    if defender.type1 != defender.type2:
        move1.append(compatibility[attacker.type2][defender.type2])
    move1.sort()
    if move1[0] == 0:
        attacker_score2 = 0
    elif len(move1) == 1:
        attacker_score2 = sum(move1) + 1
    elif len(move1) == 2:
        attacker_score2 = sum(move1) - 1

    point += max(attacker_score1, attacker_score2)

    defender_score1 = 0
    defender_score2 = 0
    move2 = []
    move2.append(compatibility[defender.type1][attacker.type1])
    if attacker.type1 != attacker.type2:
        move2.append(compatibility[defender.type1][attacker.type2])
    move2.sort()

    if move2[0] == 0:
        defender_score1 = 0
    elif len(move2) == 1:
        defender_score1 = sum(move2) + 1
    elif len(move2) == 2:
        defender_score1 = sum(move2) - 1

    move2 = []
    move2.append(compatibility[defender.type2][attacker.type1])
    if attacker.type1 != attacker.type2:
        move2.append(compatibility[defender.type2][attacker.type2])
    move2.sort()
    if move2[0] == 0:
        defender_score2 = 0
    elif len(move2) == 1:
        defender_score2 = sum(move2) + 1
    elif len(move2) == 2:
        defender_score2 = sum(move2) - 1

    point += min(5 - defender_score1, 5 - defender_score2)

    return point * 10



# ポケモンを返す
def Crossover(pokemon1, pokemon2):
    random_number1 = random.randint(0, 1)
    random_number2 = random.randint(0, 1)
    type1 = -1
    type2 = -1
    if random_number1 == 0:
        type1 = pokemon1.type1
    elif random_number1 == 1:
        type1 = pokemon1.type2

    if random_number2 == 0:
        type2 = pokemon2.type1
    elif random_number2 == 1:
        type2 = pokemon2.type2

    return Pokemon(type1, type2)

max_iteration = 100
population = 1000
num_type = 18

if __name__ == "__main__":
    random.seed(2)
    # init
    gen = []
    for i in range(num_type):
        for j in range(population):
            gen.append(Pokemon(i))

    # 数世代回す
    for _ in range(max_iteration):
        print("iteration: ", _)
        living_gen = []
        next_gen = []

        # 全てのポケモンを適当に戦わせる
        for pokemon in gen:
            random_number1 = random.randint(0, 17)
            random_number2 = random.randint(0, 17)
            tmp_pokemon = Pokemon(random_number1, random_number2)
            prob = Battle(pokemon, tmp_pokemon)
            # print(f"{pokemon}, {tmp_pokemon}, point: {prob}")
            if prob > random.randint(0, 99):
                living_gen.append(pokemon)
            else:
                pokemon.is_dead = True

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
        for i in range(num_type*population - num_next_gen):
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

    dict = dict()
    for pokemon in gen:
        if pokemon not in dict:
            dict[pokemon] = 0
        dict[pokemon] += 1
    sorted_items = sorted(dict.items(), key=lambda item: item[1])

    for key, value in sorted_items:
        print(f"Pokemon: {key}, Count: {value}")
