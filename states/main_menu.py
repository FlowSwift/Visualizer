from states.state import State
from states.sorting_visualizer import SortingVisualizer



class MainMenu(State):
    def __init__(self, visualizer):
        super().__init__(visualizer)

    def update(self, delta_time, actions):
        if actions["space"]:
            new_state = SortingVisualizer(self.visualizer)
            new_state.enter_state()
        self.visualizer.reset_keys()

    def render(self, display):
        display.fill((255,255,255))
        self.visualizer.draw_text(display, "Game States", (0,0,0), self.visualizer.CANVAS_W/2, self.visualizer.CANVAS_H/2)