from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# set up Queue 
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
# set up empty Queue
q = Queue()
pathways = {}
count = 0

# look for available exits in the room for player
next_room = {}
for exit_options in player.current_room.get_exits():
    next_room[exit_options] = '?'

pathways[world.starting_room.id] = next_room
# You may find the commands `player.current_room.id`, `player.current_room.get_exits()` and `player.travel(direction)` useful.

# set visited
visited = set()

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
        curr = d[count - 1]

        # if current is not in visited
        if curr not in visited:
            # add it in to visited
            visited.add(curr)

            # set up for loop
            for neighbor in pathways[curr]:
                if '?' == pathways[curr][neighbor]:
                    # print(f"Pathways: ", pathways[curr])
                    return d
                else:
                    # make a copy of the path
                    neighbors = d.copy()
                    neighbors.append(pathways[curr][neighbor])
                    q.enqueue(neighbors)     
        else:
            continue

    return []


def explore(player, direction):
    # create a new empty array of unexplored rooms
    unexplored = []
    
    # set the current player room
    explore_room = pathways[player.current_room.id]
    # set count to zero
    count = 0

    for node in explore_room:
        if '?' == explore_room[node]:
            unexplored.append(node)

    # if length of unexplored is equal to zero  
    if len(unexplored) == count:
        # set the traverse to move_player
        traverse = move_player(player, direction)
        
        # rooms the player has been to and is in currently
        player_room = player.current_room.id
        # print the rooms the player has been in
        print(f"Room entered: ", player_room)

        for node in traverse:
            for r in pathways[player_room]:

                if node == pathways[player_room][r]:
                    player_room = node
                    q.enqueue(r)
                    # print(f"Room: ", player_room)
                    break
    else:
        un = unexplored[random.randint(0, len(unexplored) -1)]
        # algorithm to find the nearest random room that has been unexplored
        random_room = direction.enqueue(un)

        return random_room

explore(player, q)


def direct_player(player, q):
    # add direction options for player to move
    directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    count = 0

    while q.size() > 0:
        d = q.dequeue()

        updated = player.current_room.id
        # You know you are done when you have exactly 500 entries (0-499) in your graph and no `'?'` in the adjacency dictionaries. To do this, you will need to write a traversal algorithm that logs the path into `traversal_path` as it walks. - (part of this is in the method above)
        traversal_path.append(d)
        
        # use the travel() function from `player.py`
        player.travel(d)

        r = player.current_room.id
        pathways[updated][d] = r

        if r not in pathways:
            pathways[r] = {}
            # player looks for exits
            for node in player.current_room.get_exits():
                pathways[r][node] = '?'

        pathways[r][directions[d]] = updated

        if q.size() == count:
            # use explore method
            explore(player, q)
        else:
            continue
        # prints all the directions
        # print(f"Directions: ", directions)

direct_player(player, q)



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
