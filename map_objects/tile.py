"""
Map tile. Can block pathing (blocked) or sight (block sight)
"""
class Tile:

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        #If a tile is blocked, it blocks sight by default
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False