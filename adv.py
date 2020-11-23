from room import Room
from player import Player
from world import World

from collections import deque

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []
# traversal_path = ['n', 'n']
# traversal_path = ['n', 'w']
# traversal_path = ['w', 'w']
# traversal_path = ['s', 's']
graph = {

}

directions = {"n": "s", "e": "w", "s": "n", "w": "e"}

current_room = player.current_room.id

exit_room = player.current_room.get_exits()

graph[current_room] = {e: "?" for e in exit_room}

# dft
while "?" in graph[current_room].values():
    t = random.choice([k for k, v in graph[current_room].items() if v == "?"])

    prev_room = current_room
    player.travel(t)
    traversal_path.append(t)
    current_room = player.current_room.id

    if current_room not in graph:
        graph[current_room] = {e: "?" for e in player.current_room.get_exits()}

    graph[prev_room][t] = current_room
    graph[current_room][directions[t]] = prev_room

    if "?" not in graph[current_room].values():
        # check which room youve visited
        if len(graph) == 500:
            print("End of the line")
            break

        # BFS shortest path to unexplored exit
        queue = deque()
        visited = set()
        queue.append([current_room])

        while len(queue) > 0:
            currPath = queue.popleft()
            currRoom = currPath[-1]

            if "?" in graph[currRoom].values():
                break
            if currRoom not in visited:
                visited.add(currRoom)

                for e in graph[currRoom]:
                    newPath = list(currPath)
                    newPath.append(graph[currRoom][e])
                    queue.append(newPath)

            # after you hit dead end
        for i in range(1, len(currPath)):
            t = [k for k, v in graph[current_room].items() if v ==
                 currPath[i]][0]
            player.travel(t)
            traversal_path.append(t)
            current_room = player.current_room.id

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
