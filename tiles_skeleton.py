import numpy as np
import cv2
import os




TILE_SIZE = 32

MARKET = """
##################
##..............##
##..q#..A#..#b..##
##..w#..S#..#s..##
##..e#..D#..#m..##
##..r#..F#..#g..##
##..t#..H#..#p..##
##...............d
##..C#..C#..C#...d
##..##..##..##...d
##...............#
##############GG##
""".strip()


class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        self.tiles = tiles
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in layout.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*TILE_SIZE, self.ncols*TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        
        y = row*TILE_SIZE
        x = col*TILE_SIZE

        return self.tiles[y:y+TILE_SIZE, x:x+TILE_SIZE]

    
    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "G":
            return self.extract_tile(7, 3)
        elif char == "C":
            return self.extract_tile(2, 8)
        ## Fruit
        elif char == "b":
            return self.extract_tile(0, 4)
        elif char == "m":
            return self.extract_tile(3, 4)
        elif char == "s":
            return self.extract_tile(0, 6)
        elif char == "g":
            return self.extract_tile(4, 4)
        elif char == "p":
            return self.extract_tile(5, 4)
        ## Fish
        elif char == "q":
            return self.extract_tile(4, 15)
        elif char == "w":
            return self.extract_tile(5, 15)
        elif char == "e":
            return self.extract_tile(6, 15)
        elif char == "r":
            return self.extract_tile(7, 15)
        elif char == "t":
            return self.extract_tile(8, 15)
        ## Spices
        elif char == "A":
            return self.extract_tile(0,3)
        elif char == "S":
            return self.extract_tile(1,3)
        elif char == "D":
            return self.extract_tile(2,3)
        elif char == "F":
            return self.extract_tile(3,3)
        elif char == "g":
            return self.extract_tile(4,9)
        elif char == "H":
            return self.extract_tile(5,9)
        ## Drinks
        elif char == "d":
            return self.extract_tile(6,9)
        ## Avatars
        elif char == "1":
            return self.extract_tile(3, 0)
        elif char == "2":
            return self.extract_tile(3, 1)
        elif char == "3":
            return self.extract_tile(3, 2)
        elif char == "4":
            return self.extract_tile(4, 0)
        elif char == "5":
            return self.extract_tile(4, 1)
        elif char == "6":
            return self.extract_tile(4, 2)
        elif char == "7":
            return self.extract_tile(5, 0)
        elif char == "8":
            return self.extract_tile(5, 1)
        elif char == "9":
            return self.extract_tile(5, 2)
        elif char == "10":
            return self.extract_tile(6, 0)
        elif char == "11":
            return self.extract_tile(6, 1)
        elif char == "12":
            return self.extract_tile(6, 2)
        elif char == "13":
            return self.extract_tile(7, 0)
        elif char == "14":
            return self.extract_tile(7, 1)
        elif char == "15":
            return self.extract_tile(7, 2)
        elif char == "16":
            return self.extract_tile(8, 1)
        elif char == "17":
            return self.extract_tile(8, 2)
        else:
            return self.extract_tile(1, 2)

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            # print('row', row, 'line', line)
            for col, char in enumerate(line):
                # print('col', col, 'char', char)
                bm = self.get_tile(char)
                y = row*TILE_SIZE
                x = col*TILE_SIZE

                self.image[y:y+TILE_SIZE, x:x+TILE_SIZE] = bm

    def draw(self, frame):
        """
        draws the image into a frame
        """
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image
        
        return frame

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


if __name__ == "__main__":
    dir = os.path.dirname(os.path.realpath(__file__))

    tiles = cv2.imread(f"{dir}/tiles.png")

    background = np.zeros((500, 700, 3), np.uint8)
    
    market = SupermarketMap(MARKET, tiles)

    while True:
        frame = background.copy()
        market.draw(frame)

        # https://www.ascii-code.com/
        key = cv2.waitKey(1)
       
        if key == 113: # 'q' key
            break
    
        cv2.imshow("frame", frame)


    cv2.destroyAllWindows()

    market.write_image("supermarket.png")
