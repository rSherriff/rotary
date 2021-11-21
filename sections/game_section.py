import json

from tcod import Console
from ui.game_section_ui import GameSectionUI

from sections.section import Section


class GameSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = ""):
        super().__init__(engine,x,y,width,height,xp_filepath)
        self.indexIntoRender = 0
        self.numTiles = width * height
        self.renderSpeed = 800
        self.currentPage = xp_filepath
        self.ui = GameSectionUI(self, 0,0)
        with open ( "data/pages.json" ) as f:
            self.pages = json.load(f)

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                temp_console = Console(width=self.width, height=self.height, order="F")
                for x in range(0,self.width):
                    for y in range(0, self.height):
                        temp_console.tiles_rgb[x,y] = self.tiles[x,y]["graphic"]

                for link in self.pages["data"][self.currentPage].values():
                    if link:
                        temp_console.print(link["x"], link["y"], link["title"])
                        

                if self.indexIntoRender < self.numTiles:
                    #Completed Rows
                    numFullRows = int(self.indexIntoRender / self.width)
                    console.tiles_rgb[self.x: self.x + self.width, self.y: self.y + numFullRows] = temp_console.tiles_rgb[self.x: self.x + self.width, self.y: self.y + numFullRows]

                    #Uncompleted Row
                    numIntoFinalRow = self.indexIntoRender % self.width
                    console.tiles_rgb[self.x: self.x + numIntoFinalRow, numFullRows: numFullRows + 1] = temp_console.tiles_rgb[self.x: self.x + numIntoFinalRow, numFullRows: numFullRows+1]

                    self.indexIntoRender += int(self.renderSpeed * self.engine.get_delta_time())
                else:
                    #Full Render
                    console.tiles_rgb[self.x: self.x + self.width, self.y: self.y + self.height] = temp_console.tiles_rgb


            if self.ui is not None:
                self.ui.render(console)
        
        
    def update(self):
        pass

    def number_input(self, number):
        page_link = self.pages["data"][self.currentPage][number]
        if page_link and page_link["path"] in self.pages["data"]:
            page_to_load = page_link["image"]
            if page_to_load is not "":
                    self.load_xp_and_tiles(page_to_load)
                    print(page_link["path"])
                    self.currentPage = page_link["path"]
                    self.indexIntoRender = 0
        else:
            print("Tried to go to page '" + page_link["path"] +"' but it doesn't exist!")
            

