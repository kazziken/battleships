#!/usr/bin/env python3

def render(board_width, board_height, shots):
    header = "+" + "-" * board_width + "+"
    print(header)
    
    #using a set is faster than a list of tuples b/c it's unique
    shot_sets = set(shots)
    for y in range(board_height):
        row = []
        for x in range(board_width):
            if (x,y) in shot_sets:
                ch = "X"
            else:
                ch = " "
            row.append(ch)
        print("|" + "".join(row) + "|")
    # print("|" + " " * board_width + "|")

    print(header)
    

if __name__ == '__main__':
    # render(10,10, [(3,1), (4,5), (8,1)])
    shots = []
    
    while True:
        inp = input("Where do you want to shoot?\n")
        #TODO: DEAL WITH INVALID INPUTS
        #assign first num to be x and second to y
        xstr, ystr = inp.split(",") 
        x = int(xstr)
        y = int(ystr)
        
        shots.append((x,y))
        render(10,10, shots)
