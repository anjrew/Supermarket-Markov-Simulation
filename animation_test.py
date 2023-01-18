import time
from tiles_skeleton import SupermarketMap, MARKET
import os
import numpy as np
import cv2
import random

dir = os.path.dirname(os.path.realpath(__file__))

tiles = cv2.imread(f"{dir}/tiles.png")

TILE_SIZE = 32


class Customer:

    def __init__(self, supermarket, avatar, row=5, col=5):
      """
      supermarket: A SuperMarketMap object
      avatar : a numpy array containing a 32x32 tile image
      row: the starting row
      col: the starting column
      """
      self.supermarket = supermarket
      self.avatar = avatar
      self.row = row
      self.col = col

    def draw(self, frame):

        y = self.row * TILE_SIZE
        x = self.col * TILE_SIZE

        one = y + self.avatar.shape[0]
        two = x + self.avatar.shape[1]

        frame[y:one, x:two] = self.avatar

        return frame
    
    def move(self, direction):
        new_row = self.row
        new_col = self.col

        if direction == 'up':
            new_row -= 1

        if self.supermarket.contents[new_row][new_col] == '.':
            self.col = new_col
            self.row = new_row

# Do tests here
supermarket = SupermarketMap(MARKET, tiles)

get_avatar_id = str(random.randint(1,12))
print('get_avatar_id', get_avatar_id)
customer = Customer(supermarket, supermarket.get_tile(get_avatar_id), 8, 10)

background = np.zeros((500, 700, 3), np.uint8)

while True:
    frame = background.copy()
  
    frame = supermarket.draw(frame)
    
    frame = customer.draw(frame)

    # https://www.ascii-code.com/
    key = cv2.waitKey(1)
    
    if key == 113: # 'q' key
        break
    
    customer.move('up')

    cv2.imshow("frame", frame)
    
    time.sleep(1)


cv2.destroyAllWindows()

supermarket.write_image("supermarket.png")
