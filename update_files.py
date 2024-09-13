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


class Game(BaseModel):
    home_score: list[int | CheckoutDartsEnum] = []
    away_score: list[int | CheckoutDartsEnum] = []
    home_avg: int = 0
    away_avg: int = 0
    winner: PlayersEnum = None

    def set_winner(self):
        for score in self.home_score:
            if 'x' in score:
                self.winner = PlayersEnum.home
        
        if not self.winner:
            self.winner = PlayersEnum.away
        
        self.home_avg = get_avg_from_score(self.home_score)
        self.away_avg = get_avg_from_score(self.away_score)
    
    def print_game(self):
        home_score = 501
        away_score = 501

        home_remaining = [501]
        away_remaining = [501]

        for score in self.home_score:
            if 'x' in score:
                home_score -= home_score
            else:
                home_score -= int(score)

            home_remaining.append(home_score)

        for score in self.away_score:
            if 'x' in score:
                away_score -= away_score
            else:
                away_score -= int(score)

            away_remaining.append(away_score)

        print(f"| Home  |     | - | Away |     |")
        print(f"| ----- | --- | - | ---- | --- |")
        print(f"|       | 501 | - |      | 501 |")

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

            if game_over:
                print()
                break

            print(f"| {home: <5} | {home_left: <3} | - | {away: <5} | {away_left: <3} |")



        # print(f"| Home |     | - | Away |     |")
        # print(f"|      | 501 | - |      | 501 |")
        # for i in range(max(len(self.home_score), len(self.away_score))):
        #     home_throw = self.home_score[i] if i < len(self.home_score) else ''
        #     away_throw = self.away_score[i] if i < len(self.away_score) else ''

        #     home_score -= self.home_score[i] if i < len(self.home_score) else ''
        #     away_score -= self.away_score[i] if i < len(self.away_score) else ''
        #     print(f"|  {self.home_score[i]}    | {home_score} | - |  {self.away_score[i]}    | {away_score} |")
            
        #     print(f"| {home_score} | {501 - sum(self.home_score[:i])} | - | {away_score} | {501 - sum(self.away_score[:i])} |")
        # | 100  | 401 | - | 90   | 411 |


class Match(BaseModel):
    home: str
    away: str
    home_score: int = 0
    away_score: int = 0
    games: list[Game] = []
    winner: PlayersEnum = None

    def add_game(self, game: Game):
        self.games.append(game)

        if game.winner == PlayersEnum.home:
            self.home_score += 1
        else:
            self.away_score += 1
        
        if self.home_score == 2:
            self.winner = PlayersEnum.home
        elif self.away_score == 2:
            self.winner = PlayersEnum.away


# Home,Scores
# Alex,100 121 95 85 60 x1
# John, 90 100 26 55 30

# Want to generate markdown like this:
# | Alex |     | - | John |     |
# |      | 501 | - |      | 501 |
# | 100  | 401 | - | 90   | 411 |

for week in glob.glob('_source/*'):
    date = week.split('/')[-1]
    for filename in glob.glob(f'{week}/*.csv'):
        match_number, home, away = filename.split('/')[-1].replace('.csv', '').split('-')
        print(date, match_number, home, away)

        match = Match(home=home.capitalize(), away=away.capitalize())
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            
            game = Game()

            for row in reader:
                player, scores = row

                if player == PlayersEnum.home:
                    game.home_score = scores.split(' ')
                else:
                    game.away_score = scores.split(' ')
                
                if game.home_score and game.away_score:
                    game.set_winner()
                    match.add_game(game)
                    game = Game()

        for game in match.games:
            game.print_game()
            print(f"Home avg: {game.home_avg}")

if False:
    for filename in glob.glob('_source/*.csv'):
        home, away = filename.split('/')[-1].replace('.csv', '').split('-')

        match = Match(home=home.capitalize(), away=away.capitalize())
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            
            game = Game()

            for row in reader:
                player, scores = row

                if player == PlayersEnum.home:
                    game.home_score = scores.split(' ')
                else:
                    game.away_score = scores.split(' ')
                
                if game.home_score and game.away_score:
                    game.set_winner()
                    match.add_game(game)
                    game = Game()
        
        for game in match.games:
            game.print_game()