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
# set up empty Queue and Stack
q = Queue()
s = Stack()
pathways = {}

# look for available exits in the room for player
next_room = {}
for exit_options in player.current_room.get_exits():
    next_room[exit_options] = '?'

pathways[world.starting_room.id] = next_room

def move_player(player, direction):
    # add queue to method
    q = Queue()
    # set players current room
    q.enqueue([player.current_room.id])
    count = 0
    # create a set() - stores visited 
    visited = set()

    while q.size() > count:
        d = q.dequeue()
        curr = d[count -1]

        # if current is not in visited
        if curr not in visited:
            # add it in to visited
            visited.add(curr)

            for neighbor in pathways[curr]:
                if '?' == pathways[curr][neighbor]:
                    print(f"Pathways: ", pathways[curr])
                    return d
                else:
                    # make a copy of the path
                    neighbors = d.copy()
                    neighbors.append(pathways[curr][neighbor])
                    q.enqueue(neighbors)     
        else:
            continue




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
