#!/usr/local/bin/python3

"""A bowling game is a series of frames that represent the number of pins
knocked down by a player.
"""

MAX_NUMBER_ROLLS = 2
MAX_NUMBER_PINS = 10
MAX_FRAME_NUMBER = 11
MAX_FRAME_COUNT_ERROR_MSG = \
    "No more than eleven frames can be added to this game."
MAX_ROLLS_TWO_ERROR_MSG = \
    "No more than two rolls can be added to this frame."
MAX_COUNT_PINS_ERROR_MSG = \
    "No more than 10 pins can be rolled"


class Frame:
    """A frame is a round in a bowling match"""
    def __init__(self, rolls=None):
        self.rolls = rolls or []
        self.validate_rolls()

    def add_roll(self, pins):
        """Add a roll to the frame."""
        self.rolls.append(pins)
        self.validate_rolls()

    def frame_score(self, next_frame=None, second_next=None):
        """Get the score for the current frame,
        not counting any previous frames in the sequence."""
        total_score = sum(self.rolls)
        if not next_frame:
            return total_score

        if total_score < MAX_NUMBER_PINS:
            return total_score

        total_score += next_frame.rolls[0]
        if self.rolls[0] == MAX_NUMBER_PINS:
            try:
                total_score += next_frame.rolls[1]
            except IndexError:
                if second_next:
                    total_score += second_next.rolls[0]

        return total_score

    def validate_rolls(self):
        """Validate the number of rolls that were added to the frame,
        and validates the sum of those rolls."""
        if self.frame_score() > MAX_NUMBER_PINS:
            raise ValueError(MAX_COUNT_PINS_ERROR_MSG)
        if len(self.rolls) > MAX_NUMBER_ROLLS:
            raise ValueError(MAX_ROLLS_TWO_ERROR_MSG)
        if sum(self.rolls) > MAX_NUMBER_PINS:
            raise ValueError(MAX_COUNT_PINS_ERROR_MSG)


class BowlingMatch:
    """A bowling match consists of up to eleven frames."""
    def __init__(self, frames=None):
        if frames is not None:
            self.validate_frame_count(frames)
            self.frames = frames
        else:
            self.frames = []

    def add_frame(self, frame):
        """Append a frame to the game."""
        if len(self.frames) == MAX_FRAME_NUMBER - 1:
            raise ValueError(MAX_FRAME_COUNT_ERROR_MSG)
        self.frames.append(frame)

    def last_frame(self):
        """Get the last frame of the game."""
        return self.frames.pop()

    def score(self):
        """Get the score of the game."""
        current_frame = self.frames[0] if self.frames else None
        total_score = 0
        frame_index = 0

        while current_frame:
            next_frame = None
            if len(self.frames) > frame_index + 1:
                next_frame = self.frames[frame_index + 1]

            second_next = None
            if len(self.frames) > frame_index + 2:
                second_next = self.frames[frame_index + 2]
            total_score += current_frame.frame_score(
                next_frame=next_frame, second_next=second_next)
            current_frame = next_frame
            frame_index += 1

        return total_score

    @staticmethod
    def validate_frame_count(frames):
        """Validate that the number of frames in the game
        does not exceed 11"""
        if len(frames) > MAX_FRAME_NUMBER:
            raise ValueError(MAX_FRAME_COUNT_ERROR_MSG)

    @classmethod
    def create_game(cls, rolls_list):
        """Generate a game given a list of lists of rolls."""
        frames = []
        for rolls in rolls_list:
            frames.append(Frame(rolls))
        return cls(frames)
