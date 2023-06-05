import copy
import random

class GameBoard(object):
    
    def __init__(self, battleships, width, height):
        self.battleships = battleships
        # empty list to store all the shots during the game - we can also save games and restart them later
        self.shots = []
        self.width = width
        self.height = height
    
    #1 update the battleship with any hits - health
    #2 save the fact that the shot was a hit or miss
    def take_shot(self, shot_location):
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:                
                #it is a hit
                is_hit = True
                b.hits[idx] = True
                
        
        self.shots.append(Shot(shot_location, is_hit))
    
    def is_game_over(self):
        #or list comprehension (kinda reable)
        return all([b.is_destroyed() for b in self.battleships])
        #for each battleship, is it destroyed?
        # for b in self.battleships:
        #     if not b.is_destroyed:
        #         return False
        # return True
        #if yes for all, return True, else return False
        
        pass
    
class Shot(object):
    
    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit

class Battleship(object):
    
    #TODO: which of these params do we need to create a better rendering?
    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
        #[False, False, False, True (when hit), False]
        self.hits = [False] * len(body)
    
    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None
    
    @staticmethod
    def build(head, length, direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i) # because 0,0 is the top left of the board, when we reduce the y coordinate, we're going closer to the top
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "E":
                el = (head[0] + i, head[1])
            elif direction == "W":
                el = (head[0] - i, head[1])
                
            body.append(el)
        return Battleship(body, direction)
    
    def is_destroyed(self):
        return all(self.hits)

# b = BattleShip.build((1,1), 5, "S")
# b2 = BattleShip([(1,2), (1,3), (1,4), (1,5)])
#these two are the same object but different initalization

class Player(object):
    
    def __init__(self, name, shot_f):
        self.name = name
        self.shot_f = shot_f
    
def render(game_board, show_battleships=False):
    header = "+" + "-" * game_board.width + "+"
    print(header)
    
    #Construct empty board
    board = []
    for _ in range(game_board.width):
        board.append([None for _ in range(game_board.height)])
    
    if show_battleships:
        #Add battleships to the board
        for b in game_board.battleships:
            # <-----> for horizontal
            # ^
            # |
            # |
            # v for vertical
            for i, (x, y) in enumerate(b.body):
                if b.direction == "N":
                    chs = ('v', '|', '^')
                elif b.direction == "S":
                    chs = ('^', '|', 'v')
                elif b.direction == "W":
                    chs = ('>', '-', '<')
                elif b.direction == "E":
                    chs = ('<', '-', '>')
                else:
                    raise "Unknown direction"
            
                if i == 0:
                    ch = chs[0]
                elif i == len(b.body) -1:
                    ch = chs[2]
                else:
                    ch = chs[1]
                board[x][y] = ch
        
    #Add Shots to the board
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            ch = "X"
        else:
            ch = "."
        board[x][y] = ch
        
    for y in range(game_board.height):
        row = []
        for x in range(game_board.width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")
    
    print(header)
    
def get_random_ai_shot(game_board):
    #random.randint(a,b)
    x = random.randint(0, game_board.width - 1) #we don't want 10 b/c its out of bounds (so -1)
    y = random.randint(0, game_board.height -1)
    return (x,y)

def get_human_shot(game_board):
    inp = input("Where do you want to shoot?\n")
    xstr, ystr = inp.split(",") 
    x = int(xstr)
    y = int(ystr)
    return (x,y)

    
if __name__ == '__main__':
    
    
    battleships = [
        Battleship.build((1,1), 2, "N"),
        Battleship.build((5,8), 5, "N"),
        Battleship.build((2,3), 4, "E")
    ]
    
    game_boards = [
        GameBoard(battleships, 10, 10),
        GameBoard(copy.deepcopy(battleships), 10, 10)
    ]
    
    player_names = [
        "Joji",
        "Frank"
    ]
    
    players = [
        Player("Joji", get_random_ai_shot),
        Player("Frank", get_human_shot)
    ]
    
    #index of the offensive player
    offensive_idx = 0

    while True:
        #defensive player is always opposite of 0 b/c we'll make it permanently 1
        defensive_idx = (offensive_idx + 1) % 2 #if 1 then its defensive idx turn
        
        defensive_board = game_boards[defensive_idx]
        offensive_player = players[offensive_idx]
        print("%s YOUR TURN!" % offensive_player.name)
        # shot_location = get_human_shot(defensive_board)
        shot_location = offensive_player.shot_f(defensive_board)
        defensive_board.take_shot(shot_location)
        render(defensive_board, True)
        
        if defensive_board.is_game_over():
            print("%s has won!" %offensive_player.name)
            break
        
        #offensive player becomes previous defensive player
        #idx keeps switching between 0 and 1 to swap between game_boards
        offensive_idx = defensive_idx
        