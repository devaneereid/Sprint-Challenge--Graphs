from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# setting up Stack and Queue utils
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

pathways = {}
queue = Queue()
directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# set up Queue and Stack utils - set up above
# visited = set()
# next_room = {}
# directions = {'n':'s', 's':'n', 'e':'w', 'w':'e'}

# look for available exits in the room
# for exit_options in player.current_room.get_exits():
#     next_room[exit_options] = '?'

# pathways[world.starting_room.id] = next_room

# add direction options

# def directions(room_id):
#     next_direction = {}
#     if 'n' in room_graph[room_id][1].keys():
#         next_direction['n'] = 's'
#     if 's' in room_graph[room_id][1].keys():
#         next_direction['s'] = 'n'
#     if 'e' in room_graph[room_id][1].keys():
#         next_direction['e'] = 'w'
#     if 'w' in room_graph[room_id][1].keys():
#         next_direction['w'] = 'e'

#     return next_direction


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
