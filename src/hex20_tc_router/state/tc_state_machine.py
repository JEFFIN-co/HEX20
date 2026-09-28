from enum import Enum, auto

class TCState(Enum):
    IDLE = auto()
    RECEIVING = auto()
    DECODING = auto()
    ROUTING = auto()
    HANDLING = auto()
    COMPLETE = auto()
    REJECTED = auto()

class TCStateMachine:
    def __init__(self):
        self.state = TCState.IDLE

    def transition(self, new_state: TCState):
        self.state = new_state
        return self.state
