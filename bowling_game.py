#!/usr/local/bin/python3

MAX_NUMBER_PINS = 10
MAX_FRAME_NUMBER = 10
MAX_FRAME_COUNT_ERROR_MSG = \
    "No more than ten frames can be added to this game."
MAX_ROLLS_THREE_ERROR_MSG = \
    "No more than three rolls can be added to this frame."
MAX_ROLLS_TWO_ERROR_MSG = \
    "No more than two rolls can be added to this frame."
INSERT_FRAME_ERROR_MSG = \
    "You cannot insert a frame into the middle of the game."
MAX_COUNT_PINS_ERROR_MSG = \
    "No more than 10 pins can be rolled"


class Roll:
    """A roll is one roll of the ball in a bowling match."""
    def __init__(self, pins=0):
        self._pins = pins

    @property
    def pins(self):
        return self._pins

    @pins.setter
    def pins(self, pins):
        self._pins = pins


class Frame:
    """A frame is a round in a bowling match,
    usually consisting of two rolls but at times one or three rolls."""
    def __init__(self, previous_frame=None, next_frame=None, rolls=None):
        self.rolls = rolls if rolls else []
        self._previous_frame = previous_frame
        self._next_frame = next_frame
        self.assign_to_previous_of_next()
        self.validate_rolls()

    @property
    def next_frame(self):
        return self._next_frame

    @next_frame.setter
    def next_frame(self, next_frame):
        self.validate_frame_count(self.last())
        self._next_frame = next_frame
        self.assign_to_previous_of_next()

    @property
    def previous_frame(self):
        return self._previous_frame

    @previous_frame.setter
    def previous_frame(self, previous_frame):
        self._previous_frame = previous_frame

    def add_frame(self, next_frame):
        """Append a frame if this is the last frame."""
        self.validate_frame_count(self)
        if self != self.last():
            raise ValueError(INSERT_FRAME_ERROR_MSG)
        self.next_frame = next_frame
        next_frame.previous_frame = self

    def add_roll(self, pins):
        """Add a roll to the frame."""
        self.rolls.append(Roll(pins))
        self.validate_rolls()

    def assign_to_previous_of_next(self):
        """Assign the value of previous_frame
        to match the order applied by assigning
        to next_frame."""
        if self.next_frame is not None:
            self.next_frame.previous_frame = self

    def frame_number(self):
        """Get the frame number in the sequence of frames."""
        number = 1
        frame = self
        while getattr(frame, 'previous_frame') is not None:
            number += 1
            frame = frame.previous_frame
        return number

    def first_roll(self):
        """Get the number of pins rolls on the first roll."""
        if len(self.rolls) >= 1:
            return self.rolls[0].pins
        return 0

    def last(self):
        """get the last frame of the sequence of frames."""
        last = self
        while getattr(last, 'next_frame') is not None:
            last = last.next_frame
        return last

    def second_roll(self):
        """Get the number of pins rolls on the second roll."""
        if len(self.rolls) >= 2:
            return self.rolls[1].pins
        return 0

    def third_roll(self):
        """Get the number of pins rolls on the third roll."""
        if len(self.rolls) == 3:
            return self.rolls[2].pins
        return 0

    def is_last_frame(self):
        """Return True if this is the last frame of the
        game, and False otherwise"""
        if self.frame_number() == MAX_FRAME_NUMBER:
            return True
        return False

    def frame_score(self):
        """Get the score for the current frame,
        not counting any previous frames in the sequence."""
        first_roll = self.first_roll()
        third_roll = self.third_roll()
        total_pins = first_roll + self.second_roll()

        if total_pins < MAX_NUMBER_PINS:
            return total_pins

        try:
            next_first_roll = self.next_frame.first_roll()
        except AttributeError:
            next_first_roll = 0
        try:
            next_second_roll = self.next_frame.second_roll()
        except AttributeError:
            next_second_roll = 0
        try:
            twice_next_first_roll = self.next_frame.next_frame.first_roll()
        except AttributeError:
            twice_next_first_roll = 0

        if MAX_NUMBER_PINS in (first_roll, total_pins):
            # score_type is a strike or a spare
            if self.is_last_frame():
                # if it's the last frame, allow for a 2nd and 3rd roll
                return total_pins + third_roll

        if first_roll == MAX_NUMBER_PINS:
            # score type is a strike and it is not the last frame
            if next_first_roll == MAX_NUMBER_PINS:
                # score type of next frame is a strike, too
                if self.next_frame.frame_number() == MAX_FRAME_NUMBER:
                    # if the next frame is the last, count its second roll
                    return (first_roll +
                            next_first_roll + next_second_roll)
                # count the next two frames with 1 roll each if two
                # consecutive strikes are rolled but it's not the
                # second to last frame
                return (first_roll +
                        next_first_roll + twice_next_first_roll)
            # count the two rolls of the next frame for a strike
            return first_roll + next_first_roll + next_second_roll

        if total_pins == MAX_NUMBER_PINS:
            # score_type is a spare and it is not the
            # last frame
            return total_pins + next_first_roll

        return 0

    def total_score(self):
        """Get the total score for the current frame inclusive
        of the previous frame's scores."""
        total_score = self.frame_score()
        current_frame = self
        while getattr(current_frame, 'previous_frame') is not None:
            current_frame = current_frame.previous_frame
            total_score += current_frame.frame_score()
        return total_score

    def validate_rolls(self):
        """Validate the number of rolls that were added to the frame,
        and validates the sum of those rolls."""
        if (self.frame_number() == MAX_FRAME_NUMBER and
                self.frame_score() >= MAX_NUMBER_PINS):
            # ensure no more than three rolls are allowed
            # but only for the last frame with rolls
            # at or more than the number of pins
            if len(self.rolls) > 3:
                raise ValueError(MAX_ROLLS_THREE_ERROR_MSG)
        elif self.previous_frame is None:
            # allow the ability to create a free-standing frame
            # of three to append to a game in a later step
            if len(self.rolls) > 3:
                raise ValueError(MAX_ROLLS_THREE_ERROR_MSG)
        elif len(self.rolls) > 2:
            raise ValueError(MAX_ROLLS_TWO_ERROR_MSG)
        # you can only roll more than 10 pins if the first roll is a strike
        if (self.first_roll() + self.second_roll() > MAX_NUMBER_PINS
                and self.first_roll() != MAX_NUMBER_PINS):
            raise ValueError(MAX_COUNT_PINS_ERROR_MSG)

    @staticmethod
    def validate_frame_count(frame):
        """Validate that the number of frames does not exceed
        the maximum."""
        if frame.frame_number() >= MAX_FRAME_NUMBER:
            raise ValueError(MAX_FRAME_COUNT_ERROR_MSG)

    @classmethod
    def create_frames(cls, rolls_list):
        """Generate a sequence of frames given a list
        of lists of rolls."""
        def create_frame(rolls_list):
            rolls = rolls_list[0]
            del rolls_list[0]
            while rolls_list:
                return cls(
                    next_frame=create_frame(rolls_list),
                    rolls=rolls)
            return cls(rolls=rolls)

        if rolls_list:
            return create_frame(rolls_list)


class BowlingMatch:
    """A bowling match consist of up to ten frames or rounds."""
    def __init__(self, frame=None):
        if frame is not None:
            self.validate_frame_count(frame)
        self._frame = frame

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, frame):
        self.validate_frame_count(frame)
        self._frame = frame

    def add_frame(self, next_frame):
        """Append a frame to the game."""
        self.validate_frame_count(next_frame)
        last_frame = self.last_frame()
        last_frame.next_frame = next_frame
        next_frame.previous_frame = last_frame

    def last_frame(self):
        """Get the last frame of the game."""
        return self.frame.last()

    def score(self):
        """Get the final score of the game."""
        current_frame = self.frame
        total_score = 0
        while current_frame is not None:
            total_score += current_frame.frame_score()
            current_frame = current_frame.next_frame
        return total_score

    @staticmethod
    def validate_frame_count(frame):
        """Validate that the number of frames in the game
        does not exceed 10"""
        if frame.last().frame_number() > MAX_FRAME_NUMBER:
            raise ValueError(MAX_FRAME_COUNT_ERROR_MSG)

    @classmethod
    def create_game(cls, rolls_list):
        """Generate a game given a list of lists of rolls."""
        return cls(Frame.create_frames(rolls_list))
