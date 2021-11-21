import tcod
from actions.actions import NumberInputAction

from ui.ui import UI, get_key_character


class GameSectionUI (UI):
    def keydown(self, event: tcod.event.KeyDown):
        key = event.sym

        if key >= tcod.event.K_0 and key <= tcod.event.K_9:
            NumberInputAction(self.section.engine, get_key_character(key)).perform()