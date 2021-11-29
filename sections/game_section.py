import json
from threading import Timer

from tcod import Console, CENTER
from ui.game_section_ui import GameSectionUI

from sections.section import Section


class GameSection(Section):
    def __init__(self, engine, x: int, y: int, width: int, height: int, xp_filepath: str = ""):
        super().__init__(engine,x,y,width,height,xp_filepath)
        self.indexIntoRender = 0
        self.numTiles = width * height
        self.renderSpeed = 2000
        self.ui = GameSectionUI(self, 0,0)

        self.blink = False
        self.blink_key = ''
        self.blink_interval = 0.15

        self.currentPage = xp_filepath
        self.changing_page = False
        self.next_page_name = ''
        self.next_page_image = ''
        self.next_page_timer = 0.5

        with open ( "data/pages.json" ) as f:
            self.pages = json.load(f)
        self.change_page( page_name="start", page_image="blank")
        

    def render(self, console):
        if len(self.tiles) > 0:
            if self.invisible == False:
                temp_console = Console(width=self.width, height=self.height, order="F")
                for x in range(0,self.width):
                    for y in range(0, self.height):
                        temp_console.tiles_rgb[x,y] = self.tiles[x,y]["graphic"]

                current_page = self.pages["data"][self.currentPage]
                temp_console.print_box(x=10, y=12,width=49,height=1, string=current_page["title"], fg=(0,255,0), bg=(0,0,0), alignment=CENTER)

                for number, link in current_page["links"].items():
                    if link:
                        bg = (0,0,0)
                        fg = (0,255,0)
                        if self.blink == True and self.blink_key == number:
                            bg = (0,255,0)
                            fg = (0,0,0)

                        temp_console.print(x=link["x"], y=link["y"], string=link["title"], fg=fg, bg=bg)
                        

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
        if number in self.pages["data"][self.currentPage]["links"]:
            page_link = self.pages["data"][self.currentPage]["links"][number]
            if page_link and page_link["name"] in self.pages["data"]:

                self.next_page_name = page_link["name"]
                self.next_page_image = page_link["image"]

                self.blink_key = number
                self.changing_page = True
                Timer(self.next_page_timer, self.change_page_timer_end).start()
                self.blink_on()

            else:
                print("Tried to go to page '" + page_link["name"] +"' but it doesn't exist!")

    def change_page_timer_end(self):
        self.changing_page = False
        self.blink = False  
        self.blink_key = ''
        self.change_page(self.next_page_name, self.next_page_image)

    def change_page(self, page_name, page_image):
        if page_name != "":
            print("Changing to page '" + page_name +"'")
            self.load_xp_and_tiles(page_image)
            self.currentPage = page_name
            self.indexIntoRender = 0 

    def blink_on(self):
        self.blink = True
        if self.changing_page:
            Timer(self.blink_interval, self.blink_off).start()
    
    def blink_off(self):
        self.blink = False
        if self.changing_page:
            Timer(self.blink_interval, self.blink_on).start()

