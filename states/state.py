class State():
    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.prev_state = None

    def update(self, delta_time, actions):
        pass
    def render(self,surface):
        pass

    def enter_state(self):
        if len(self.visualizer.state_stack) > 1:
            self.prev_state = self.visualizer.state_stack[-1]
        self.visualizer.state_stack.append(self)

    def exit_state(self):
        self.visualizer.state_stack.pop()
        