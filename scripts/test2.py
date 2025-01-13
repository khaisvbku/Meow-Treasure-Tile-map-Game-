tile_pos = [10, 10]
next_pos = {
            "front": str(tile_pos[0]) + ", " + str(tile_pos[1] + 1),
            "back": str(tile_pos[0]) + ", " + str(tile_pos[1] - 1),
            "left": str(tile_pos[0] - 1) + ", " + str(tile_pos[1]),
            "right": str(tile_pos[0] + 1) + ", " + str(tile_pos[1])
        }

        # Check collisions for each direction
for direction, pos in next_pos.items():
    print(direction, pos)