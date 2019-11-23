#!/usr/local/bin/python3

import unittest

from bowling_game import BowlingMatch, Frame


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
        frame_class = Frame(rolls=[first_roll, second_roll])
        return frame_class

    def build_two_consecutive_frames(
            self, first_roll=0, second_roll=0, third_roll=0, fourth_roll=0):
        frame_1 = self.build_frame(first_roll, second_roll)
        frame_2 = self.build_frame(third_roll, fourth_roll)
        match = BowlingMatch()
        match.add_frame(frame_1)
        match.add_frame(frame_2)
        return match

    def test_frames_score(self):
        frame_class = self.build_frame(3, 1)
        self.assertEqual(
            frame_class.frame_score(), 4,
            msg="The frame score should be the sum of its two rolls")

    def test_frames_spare(self):
        match_class = self.build_two_consecutive_frames(0, 10, 8, 1)
        self.assertEqual(
            match_class.frames[0].frame_score(next_frame=match_class.frames[1]), 18,
            msg="A first roll of 0 and second roll of 10 should be considered"
            " a spare, not a strike, when scores are counted")

        match_class = self.build_two_consecutive_frames(5, 5, 3)
        self.assertEqual(
            match_class.frames[0].frame_score(next_frame=match_class.frames[1]), 13,
            msg="The frame score for a spare should count "
            "the next frames first roll")

    def test_frames_strike(self):
        match_class = self.build_two_consecutive_frames(10, 0, 3, 5)
        self.assertEqual(
            match_class.frames[0].frame_score(next_frame=match_class.frames[1]), 18,
            msg="The frame score for a strike should count the "
            "two rolls of the next frame")

    def test_frames_game_score(self):
        match_class = self.build_two_consecutive_frames(5, 4, 3, 5)
        self.assertEqual(
            match_class.score(),
            match_class.frames[0].frame_score() + match_class.frames[1].frame_score(),
            msg="The score of the game should equal "
            "the sum of the frame scores.")

    def test_pin_count_validation_error(self):
        frame = Frame()
        frame.add_roll(7)
        msg = "The total of the first and second roll can't exceed 10"
        with self.assertRaises(ValueError, msg=msg):
            frame.add_roll(5)

    def test_roll_validation_error(self):
        frame = Frame()
        msg = "The total number of pins rolled can't exceed 10"
        with self.assertRaises(ValueError, msg=msg):
            frame.add_roll(11)

    def test_add_third_roll_validation_error(self):
        frame = Frame()
        frame.add_roll(4)
        frame.add_roll(3)
        msg = ("Adding a third roll to a frame raises a validation error")
        with self.assertRaises(ValueError, msg=msg):
            frame.add_roll(1)

    @staticmethod
    def build_rolls_list():
        """Return a list of rolls that can be used to create valid frames."""
        return [[1, 3], [6, 2], [4, 5]]

    def test_game_score(self):
        rolls_list = self.build_rolls_list()
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 21,
            msg="A game created with a list of rolls returns a valid "
            "game score")

    def test_game_frame_score(self):
        rolls_list = self.build_rolls_list()
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.frames[0].frame_score(), 4,
            msg="A game created with a list of rolls returns a valid first "
            "frame score")

    def test_game_strike(self):
        perfect_roll = [[10]]
        rolls_list = perfect_roll * 5
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 120,
            msg="A game with 5 strikes so far returns a valid game score")

    def test_game_spares(self):
        perfect_roll = [[0, 10]]
        rolls_list = perfect_roll * 5
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 50,
            msg="A game with 5 spares so far returns a valid game score")

    def test_empty_game(self):
        rolls_list = [[]]
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 0,
            msg="A game with no rolls in it returns a valid game score")

    def test_perfect_game(self):
        perfect_roll = [[10]]
        rolls_list = perfect_roll * 11
        match = BowlingMatch.create_game(rolls_list)
        self.assertEqual(
            match.score(), 300,
            msg="A perfect game of only strikes returns a valid game score")


if __name__ == '__main__':
    unittest.main()
