#!/usr/local/bin/python3

import unittest
from unittest import mock

from bowling_game import BowlingMatch, Frame, Roll


class TestFrame(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.expected_score = 0
        super().__init__(*args, **kwargs)

    def test_empty_frame_score(self):
        frame_class = Frame()
        self.assertEqual(
            frame_class.frame_score(), 0,
            msg="An empty frame with no rolls should have a score of 0")

    @staticmethod
    def build_frame(first_roll=0, second_roll=0):
        frame_class = Frame()
        frame_class.first_roll = mock.MagicMock(return_value=first_roll)
        frame_class.second_roll = mock.MagicMock(return_value=second_roll)
        return frame_class

    def build_two_consecutive_frames(
            self, first_roll=0, second_roll=0, third_roll=0, fourth_roll=0):
        frame_class = self.build_frame(first_roll, second_roll)
        next_class = self.build_frame(third_roll, fourth_roll)
        frame_class.next_frame = next_class
        next_class.previous_frame = frame_class
        return frame_class

    def test_frame_score_sums_rolls(self):
        frame_class = self.build_frame(3, 1)
        self.assertEqual(
            frame_class.frame_score(), 4,
            msg="The frame score should be the sum of its two rolls")

    def test_frame_score_for_spare_counts_next_roll(self):
        frame_class = self.build_two_consecutive_frames(5, 5, 3)
        self.assertEqual(
            frame_class.frame_score(), 13,
            msg="The frame score for a spare should count "
            "the next frames first roll")

    def test_second_roll_of_ten_is_spare_not_strike(self):
        frame_class = self.build_two_consecutive_frames(0, 10, 8, 1)
        self.assertEqual(
            frame_class.frame_score(), 18,
            msg="A firt roll of 0 and second roll of 10 should be considered"
            " a spare, not a strike, when scores are counted")

    def test_frame_score_for_strike_counts_next_two_rolls(self):
        frame_class = self.build_two_consecutive_frames(10, 0, 3, 5)
        self.assertEqual(
            frame_class.frame_score(), 18,
            msg="The frame score for a strike should count the "
            "two rolls of the next frame")

    def test_last_frame_total_score_equals_game_score(self):
        frame_class = self.build_two_consecutive_frames(5, 4, 3, 5)
        match = BowlingMatch(frame=frame_class)
        self.assertEqual(
            match.score(),
            match.last_frame().total_score(),
            msg="The total score of the last frame should equal "
            "the game score.")

    def test_last_frame(self):
        frame_class = self.build_two_consecutive_frames(0, 10, 8, 1)
        self.assertTrue(
            frame_class.next_frame is frame_class.last(),
            msg="The last frame method should return the last in a sequence "
            "of frames")

    @staticmethod
    def build_frames(last_rolls=None):
        """Return a sequnce of 5 frames."""
        if not last_rolls:
            last_rolls = [Roll(5), Roll(3)]
        frame = Frame(
            next_frame=Frame(
                next_frame=Frame(
                    next_frame=Frame(
                        next_frame=Frame(
                            rolls=last_rolls),
                        rolls=[Roll(4), Roll(1)]),
                    rolls=[Roll(0), Roll(10)]),
                rolls=[Roll(3), Roll(3)]),
            rolls=[Roll(2), Roll(4)])
        return frame

    def build_match(self):
        """Return a game that has 5 frames and set the expected socre."""
        self.expected_score = 39
        frame = self.build_frames()
        match = BowlingMatch(frame)
        return match

    def build_match_ten_frames(self, roll_type=None):
        """Return a game that has 10 frames and set the expected score."""
        match = self.build_match()
        if roll_type == 'strike':
            last_rolls = [Roll(10)]
            self.expected_score = self.expected_score * 2 - 8 + 10
        elif roll_type == 'spare':
            last_rolls = [Roll(5), Roll(5)]
            self.expected_score = self.expected_score * 2 - 8 + 10
        else:
            last_rolls = [Roll(5), Roll(3)]
            self.expected_score = self.expected_score * 2
        match.add_frame(self.build_frames(last_rolls))
        return match

    def add_frame_to_game(self, first_roll=0, second_roll=0):
        """Add two additional rolls to a game of 5 frames."""
        match = self.build_match()
        match.add_frame(Frame(
            rolls=[Roll(first_roll), Roll(second_roll)]))
        self.expected_score = self.expected_score + first_roll + second_roll
        return match

    def test_build_match_game_score(self):
        match = self.build_match()
        self.assertEqual(
            match.score(), self.expected_score,
            msg="The score for a match is the sum of the rolls of its frames")

    def test_build_match_last_frame_score(self):
        match = self.build_match()
        self.assertEqual(
            match.last_frame().total_score(), self.expected_score,
            msg="The score for the last frame in a sequence "
            "is the sum of the rolls of its previous frames")

    def test_build_match_frame_number(self):
        match = self.build_match()
        self.assertEqual(
            match.frame.next_frame.frame_number(), 2,
            msg="The frame number shows the position of a frame in "
            "its sequence of frames")

    def test_build_match_last_frame_number(self):
        match = self.build_match()
        self.assertEqual(
            match.last_frame().frame_number(), 5,
            msg="The frame number shows the position of a frame in "
            "its sequence of frames")

    def test_add_frame_to_game_frame_number(self):
        match = self.add_frame_to_game(1, 1)
        self.assertEqual(
            match.last_frame().frame_number(), 6,
            msg="Adding a frame to a game increases the frame number "
            "of the last frame in the game by 1")

    def test_add_frame_to_game_match_score(self):
        match = self.add_frame_to_game(1, 1)
        self.assertEqual(
            match.score(), self.expected_score,
            msg="Adding a frame to game increases the score of the game")

    def test_add_frame_to_game_last_frame_score(self):
        match = self.add_frame_to_game(1, 1)
        self.assertEqual(
            match.last_frame().total_score(), self.expected_score,
            msg="Adding a frame to a game increases the frame score "
            "of the last frame in the game")

    def test_add_frame_to_game_frame_score(self):
        match = self.add_frame_to_game(1, 1)
        self.assertEqual(
            match.last_frame().frame_score(), 2,
            msg="A frame in a sequence within a game has a "
            "score that is the sum of its two rolls")

    def test_last_frame_of_match(self):
        match = self.build_match()
        last_frame = Frame(rolls=[Roll(2), Roll(3)])
        match.add_frame(last_frame)
        self.assertTrue(
            last_frame is match.last_frame(),
            "The last frame of a game is the most recently appended frame")

    def test_add_roll_updates_score(self):
        frame = Frame()
        frame.add_roll(4)
        self.assertEqual(
            frame.frame_score(), 4,
            msg="Adding a roll to a frame increases the frame score by "
            "that amount")

    def test_add_first_roll(self):
        frame = Frame()
        frame.add_roll(4)
        self.assertEqual(
            frame.first_roll(), 4,
            msg="The first roll of a frame returns the value of the first "
            "added roll")

    def test_add_second_roll(self):
        frame = Frame()
        frame.add_roll(4)
        frame.add_roll(3)
        self.assertEqual(
            frame.second_roll(), 3,
            msg="The second roll of a frame returns the value of the second "
            "added roll")

    def test_add_second_roll_validation_error(self):
        frame = Frame()
        frame.add_roll(7)
        msg = "The total of the first and second roll can't exceed 10"
        with self.assertRaises(ValueError, msg=msg):
            frame.add_roll(5)

    def test_add_third_roll_validation_error(self):
        frame = Frame()
        frame.add_roll(4)
        frame.add_roll(3)
        frame.previous_frame = Frame()
        msg = ("Adding a third roll to a frame within a sequence of frames "
               "raises a validation error")
        with self.assertRaises(ValueError, msg=msg):
            frame.add_roll(1)

    def test_add_third_roll_tenth_frame_validation_error(self):
        match = self.build_match_ten_frames()
        msg = ("Adding a third roll to the 10th frame within a sequence of "
               "frames raises a validation error")
        with self.assertRaises(ValueError, msg=msg):
            match.last_frame().add_roll(1)

    def test_add_third_roll_tenth_frame_strike_allows_roll(self):
        match = self.build_match_ten_frames(roll_type='strike')
        match.last_frame().add_roll(1)
        self.assertEqual(
            match.score(), self.expected_score + 1,
            msg="Adding a second roll to the 10th frame within a sequence of "
            "frames is allowed when the frame is a strike and increased the "
            "score")

    def test_add_third_roll_tenth_frame_strike_allows_third_roll(self):
        match = self.build_match_ten_frames(roll_type='strike')
        match.last_frame().add_roll(1)
        match.last_frame().add_roll(3)
        self.assertEqual(
            match.score(), self.expected_score + 4,
            msg="Adding a third roll to the 10th frame within a sequence of "
            "frames is allowed if the frame is a strike and increases the "
            "score")

    def test_add_fourth_roll_tenth_frame_strike_validation_error(self):
        match = self.build_match_ten_frames(roll_type='strike')
        match.last_frame().add_roll(1)
        match.last_frame().add_roll(3)
        msg = ("Adding a fourth roll to the last frame when it's a strike "
               "raises a validation error")
        with self.assertRaises(ValueError, msg=msg):
            match.last_frame().add_roll(2)

    def test_add_third_roll_tenth_frame_spare_allows_roll(self):
        match = self.build_match_ten_frames(roll_type='spare')
        match.last_frame().add_roll(2)
        self.assertEqual(
            match.score(), self.expected_score + 2,
            msg="Adding a third roll to the last frame of the game that is a "
            "spare is allowed  and increases the score")

    def test_add_fourth_roll_tenth_frame_spare_validation_error(self):
        match = self.build_match_ten_frames(roll_type='spare')
        match.last_frame().add_roll(2)
        msg = ("Adding a fourth roll to a tenth frame that is a spare raises "
               "a validation error")
        with self.assertRaises(ValueError, msg=msg):
            match.last_frame().add_roll(2)

    def test_add_eleventh_frame_to_match_validation_error(self):
        match = self.build_match_ten_frames(roll_type='spare')
        msg = "Adding an eleventh frame to a match raises a validation error"
        with self.assertRaises(ValueError, msg=msg):
            match.add_frame(Frame())

    def test_add_eleventh_frame_to_last_frame_validation_error(self):
        match = self.build_match_ten_frames(roll_type='spare')
        msg = ("Adding an eleventh frame to the last frame in a sequence of "
               "frames raises a validation error")
        with self.assertRaises(ValueError, msg=msg):
            match.last_frame().add_frame(Frame())

    def test_insert_middle_frame_validation_error(self):
        match = self.build_match()
        msg = ("Inserting a frame in to the middle of a game raises a "
               "validation error")
        with self.assertRaises(ValueError, msg=msg):
            match.last_frame().previous_frame.add_frame(Frame())

    def test_get_first_roll(self):
        match = self.build_match()
        self.assertEqual(
            match.frame.first_roll(), 2,
            msg="The number of pins in the first roll of a frame is returned "
            "by the first_roll method")

    def test_get_second_roll(self):
        match = self.build_match()
        self.assertEqual(
            match.frame.second_roll(), 4,
            msg="The number of pins in the second roll of a frame is "
            "returned by the second_roll method")

    def test_get_third_roll(self):
        match = self.build_match_ten_frames(roll_type='spare')
        match.last_frame().add_roll(2)
        self.assertEqual(
            match.last_frame().third_roll(), 2,
            msg="The number of pins in the third roll of a frame is returned "
            "by the third_roll method")

    def build_three_frames_of_five(self):
        """Build three instances of five consecutive frames and return them
        as a tuple of three."""
        frame = self.build_frames()
        frame_two = self.build_frames()
        frame_three = self.build_frames()
        return (frame, frame_two, frame_three)

    def test_set_max_frame_count_validation_error(self):
        frame, frame_two, frame_three = self.build_three_frames_of_five()
        frame.last().next_frame = frame_two
        msg = ("Appending more than 10 frames to a sequence of frames raises "
               "a validation error")
        with self.assertRaises(ValueError, msg=msg):
            frame_two.last().next_frame = frame_three

    def test_set_game_max_frame_count_validation_error(self):
        frame, frame_two, frame_three = self.build_three_frames_of_five()
        frame_two.last().next_frame = frame_three
        frame.last().next_frame = frame_two
        msg = ("Appending more than 10 frames to a game raises a validation "
               "error")
        with self.assertRaises(ValueError, msg=msg):
            match = BowlingMatch()
            match.frame = frame

    def test_create_game_max_frame_count_validation_error(self):
        frame, frame_two, frame_three = self.build_three_frames_of_five()
        frame_two.last().next_frame = frame_three
        frame.last().next_frame = frame_two
        msg = ("Creating a game with a sequence of more than 10 frames "
               "raises a validation error")
        with self.assertRaises(ValueError, msg=msg):
            BowlingMatch(frame)

    @staticmethod
    def build_rolls_list():
        """Return a list of rolls that can be used to create valid frames."""
        return [[Roll(1), Roll(3)], [Roll(6), Roll(2)], [Roll(4), Roll(5)]]

    def test_build_match_score(self):
        rolls_list = self.build_rolls_list()
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 21,
            msg="A game created with a list of rolls returns a valid "
            "game score")

    def test_build_match_frame_score(self):
        rolls_list = self.build_rolls_list()
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.frame.frame_score(), 4,
            msg="A game created with a list of rolls returns a valid first "
            "frame score based on the order of the rolls in the provided list")

    def test_build_match_frame_roll_order_first_roll(self):
        rolls_list = self.build_rolls_list()
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.last_frame().first_roll(), 4,
            msg="A game created with a list of rolls returns a first roll "
            "based on the order of the rolls in the provided list")

    def test_build_match_frame_roll_order_second_roll(self):
        rolls_list = self.build_rolls_list()
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.last_frame().second_roll(), 5,
            msg="A game created with a list of rolls returns a valid second "
            "roll based on the order of the rolls in the provided list")

    def test_strike_game(self):
        perfect_roll = [[Roll(10)]]
        rolls_list = perfect_roll * 5
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 120,
            msg="A game with 5 strikes returns a valid game score")

    def test_empty_game(self):
        rolls_list = [[]]
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 0,
            msg="A game with no rolls in it returns a valid game score")

    def test_perfect_game(self):
        perfect_roll = [[Roll(10)]]
        rolls_list = perfect_roll * 9
        match = BowlingMatch.create_game(rolls_list)
        match.add_frame(Frame(rolls=[Roll(10), Roll(10), Roll(10)]))
        self.assertEqual(
            match.score(), 300,
            msg="A perfect game of only strikes returns a valid game score")


if __name__ == '__main__':
    unittest.main()
