class GameBoard(object):
    
    def __init__(self, battleships, board_width, board_height):
        self.battleships = battleships
        # empty list to store all the shots during the game - we can also save games and restart them later
        self.shots = []
        self.board_width = board_width
        self.board_height = board_height
    
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
                break
        
        self.shots.append(Shot(shot_location, is_hit))
    
class Shot(object):
    
    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit

class Battleship(object):
    
    def __init__(self, body):
        self.body = body
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
        return Battleship(body)

# b = BattleShip.build((1,1), 5, "S")
# b2 = BattleShip([(1,2), (1,3), (1,4), (1,5)])
#these two are the same object but different initalization

def render(board_width, board_height, shots):
    header = "+" + "-" * board_width + "+"
    print(header)
    
    #using a set is faster than a list of tuples b/c it's unique
    shot_sets = set(shots)
    #board height
    for y in range(board_height):
        row = []
        #board width
        for x in range(board_width):
            if (x,y) in shot_sets:
                ch = "X"
            else:
                ch = " "
            row.append(ch)
        print("|" + "".join(row) + "|") 

    print(header)
    
def render_battleships(board_width, board_height, battleships):
    header = "+" + "-" * board_width + "+"
    print(header)
    
    #Construct empty board
    board = []
    for _ in range(board_width):
        board.append([None for _ in range(board_height)])
    
    #Add battleships to the board
    for b in battleships:
        for x, y in b.body:
            board[x][y] = "O"
        
    for y in range(board_height):
        row = []
        for x in range(board_width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")
        
    print(header)
    

if __name__ == '__main__':
    battleships = [
        Battleship.build((1,1), 2, "N"),
        Battleship.build((5,8), 5, "N"),
        Battleship.build((2,3), 4, "E")
    ]
    
    for b in battleships:
        print(b.body)
        
    game_board = GameBoard(battleships, 10, 10)
    shots = [(1,1), (0,0), (5,7)]
    for sh in shots:
        game_board.take_shot(sh)
    
    for sh in game_board.shots:
        print(sh.location)
        print(sh.is_hit)
        print("===========")
    for b in game_board.battleships:
        print(b.body)
        print(b.hits)
        print("=============")

    
    
    # render_battleships(10,10, battleships)
    
    exit(0)
    
    while True:
        inp = input("Where do you want to shoot?\n")
        #TODO: DEAL WITH INVALID INPUTS
        #assign first num to be x and second to y
        xstr, ystr = inp.split(",") 
        x = int(xstr)
        y = int(ystr)
        
        shots.append((x,y))
        render(10,10, shots)
