"""
Potential additions:
Required weapon type (ex: slashing weapon, long weapon, etc) - requires more weapon attributes
Energy/Mana/Resource cost - requires more player attributes
Items spawn randomly, need to think about how new tricks are obtained - requires lots of stuff
"""

class Trick:
    def __init__(self, trick_function=None, targeting=False, targeting_message=None, **kwargs):
        self.trick_function = trick_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
