import json
import re
import os
import draw_chickens


chicken_positions = list()
last_tick = 0
last_id = 0
new_tick = False

i = 0
new_chicken = False
chicken_i = 0

if not os.path.isfile("chickendict"):
    with open("all.file") as data:
        for line in data:
            if "tick: " in line:
                last_tick = int(line.split(' ')[1])
                new_tick = True

            if "Entity Delta update:" in line:
                numbers = re.findall("\d+", line)
                if len(numbers) > 0:
                    last_id = numbers[0]

            if "DT_CChicken" in line:
                new_chicken = True
                new_chicken_i = i + 2
            if new_chicken and i == new_chicken_i:
                chicken_coords = re.findall("\d+\.\d+", line)
                chicken_coords = [ float(v) for v in chicken_coords ]
                if len(chicken_coords) > 0:
                    if new_tick:
                        chicken_positions.append({})
                        new_tick = False
                    chicken_positions[-1][last_id] = chicken_coords
                new_chicken = False
            i += 1


    with open("chickendict", "w") as f:
        json.dump(chicken_positions, f)
else:
    with open("chickendict") as f:
        chicken_positions = json.load(f)

draw_chickens.make_gif(chicken_positions)
