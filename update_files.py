#!/usr/env python3

import csv
import glob
from pydantic import BaseModel
from enum import Enum

def get_avg_from_score(score: list[str]) -> int:
    darts: int = 0

    for s in score:
        if 'x' in s:
            darts += int(s.replace('x', ''))
        else:
            darts += 3

    return 501 / darts * 3

class PlayersEnum(str, Enum):
    home = 'home'
    away = 'away'


class CheckoutDartsEnum(str, Enum):
    x1 = 'x1'
    x2 = 'x2'
    x3 = 'x3'

    def __str__(self):
        return str(self.value)


class Game(BaseModel):
    home_score: list[int | CheckoutDartsEnum] = []
    away_score: list[int | CheckoutDartsEnum] = []
    home_total_score: int = 0
    away_total_score: int = 0
    home_avg: int = 0
    away_avg: int = 0
    home_darts: int = 0
    away_darts: int = 0
    winner: PlayersEnum = None
    home_player: str = ""
    away_player: str = ""

    def set_darts_and_avg(self):
        for s in self.home_score:
            if type(s) == int:
                self.home_darts += 3
                self.home_total_score += s
            else:
                self.home_darts += int(s.replace('x', ''))
                self.winner = PlayersEnum.home
                self.home_total_score = 501
        
        for s in self.away_score:
            if type(s) == int:
                self.away_darts += 3
                self.away_total_score += s
            else:
                self.away_darts += int(s.replace('x', ''))
                self.winner = PlayersEnum.away
                self.away_total_score = 501
        
        self.home_avg = self.home_total_score / self.home_darts * 3
        self.away_avg = self.away_total_score / self.away_darts * 3

    def print_game(self):
        home_score = 501
        away_score = 501

        home_remaining = [501]
        away_remaining = [501]

        for score in self.home_score:
            try:
                home_score -= score
            except TypeError:
                home_score -= home_score

            home_remaining.append(home_score)

        for score in self.away_score:
            try:
                away_score -= score
            except TypeError:
                away_score -= away_score

            away_remaining.append(away_score)

        print(f"| {self.home_player: <7} |     | - | {self.away_player: <7} |     |")
        print(f"| ------- | --- | - | ------- | --- |")
        print(f"|         | 501 | - |         | 501 |")

        game_over = False

        for i in range(100):
            try:
                home = self.home_score[i]
            except IndexError:
                home = ''
            
            try:
                home_left = home_remaining[i+1]
            except IndexError:
                game_over = True
            
            try:
                away = self.away_score[i]
            except IndexError:
                away = ''
            
            try:
                away_left = away_remaining[i+1]
            except IndexError:
                game_over = True


            print(f"| {home: <7} | {home_left: <3} | - | {away: <7} | {away_left: <3} |")

            if game_over:
                print()
                break

class Match(BaseModel):
    home: str
    away: str
    home_score: int = 0
    away_score: int = 0
    home_avg: int = 0
    away_avg: int = 0
    games: list[Game] = []
    winner: PlayersEnum = None

    def add_game(self, home_score: list[str], away_score: list[str]):
        game = Game(home_score=home_score, away_score=away_score, home_player=self.home, away_player=self.away)
        self.games.append(game)

        if game.winner == PlayersEnum.home:
            self.home_score += 1
        else:
            self.away_score += 1
        
        if self.home_score == 2:
            self.winner = PlayersEnum.home
        elif self.away_score == 2:
            self.winner = PlayersEnum.away
    
    # def print_stats():

def get_match_from_file(filename: str) -> Match:
    _, home, away = filename.split('/')[-1].replace('.csv', '').split('-')
    match = Match(home=home.capitalize(), away=away.capitalize())

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            player, scores = row

            if player == PlayersEnum.home:
                home_score = scores.split(' ')
                continue
            else:
                away_score = scores.split(' ')
            
            game = Game(
                home_score=home_score,
                away_score=away_score,
                home_player=home.capitalize(),
                away_player=away.capitalize()
            )

            game.set_darts_and_avg()

            match.games.append(game)
    
    # Set match stats
    match.home_score = len([game for game in match.games if game.winner == PlayersEnum.home])
    match.away_score = len([game for game in match.games if game.winner == PlayersEnum.away])

    # Calculate the average weighted by num darts per game
    total_home_score = sum([game.home_darts * game.home_avg for game in match.games])
    match.home_avg = total_home_score / sum([game.home_darts for game in match.games])


    return match

for week in glob.glob('_source/*'):
    date = week.split('/')[-1]

    # Start writing to csv file in _data
    with open(f'_data/{date}.csv', 'w') as f:
        f.write("Name,Games,Average\n")

        for filename in glob.glob(f'{week}/*.csv'):
            match = get_match_from_file(filename)
            f.write(f"{match.home},{match.home_score + match.away_score},{match.home_avg:.2f}\n")
