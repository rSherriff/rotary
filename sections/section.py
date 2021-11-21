import gzip
import os
import random

import numpy as np
import tile_types
import xp_loader


class Section:
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = ""):
        self.engine = engine

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        tile = tile_types.background_tile
        tile["graphic"]["bg"] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.tiles =  np.full((self.width, self.height), fill_value=tile, order="F")
        self.ui = None

        xp_data = self.load_xp_data(xp_filepath)
        self.load_tiles(xp_filepath, xp_data)

        self.invisible = False

    def load_xp_data(self, filepath):
        if os.path.isfile(filepath):
            xp_file = gzip.open("images/" + filepath)
            raw_data = xp_file.read()
            xp_file.close()
            return xp_loader.load_xp_string(raw_data)

    def load_tiles(self, data_name, xp_data):
        if xp_data is not None:
            self.loaded_tiles = data_name
            for h in range(0, self.height):
                if h < xp_data['height']:
                    for w in range(0, self.width):
                        if w < xp_data['width']:
                            self.tiles[w, h]['graphic'] = xp_data['layer_data'][0]['cells'][w][h]
                        else:
                            break
                else:
                    break
            return True
        return False

    def load_xp_and_tiles(self, filepath):
        xp_data = self.load_xp_data(filepath)
        return self.load_tiles(filepath, xp_data)


    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                console.tiles_rgb[self.x : self.x + self.width, self.y: self.y + self.height] = self.tiles["graphic"]

            if self.ui is not None:
                self.ui.render(console)

    def update(self):
        pass
