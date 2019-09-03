"""
Pretty empty right now but will probably be the place that we
take care of modding your moves (allowing the player to select
and rebind tricks)
"""
from components.trick import Trick

class Trick_List:
    def __init__(self, active_tricks=None, tricks_known=None):
        self.active_tricks = active_tricks
        self.tricks_known = tricks_known


    def use(self, trick, **kwargs):
        results = []



        if trick.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
            results.append({'targeting': trick})
        else:
            kwargs = {**trick.function_kwargs, **kwargs}
            trick_use_results = trick.trick_function(self.owner, **kwargs)

            results.extend(trick_use_results)

        return results