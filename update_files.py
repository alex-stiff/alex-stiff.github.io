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

class CheckoutDartsEnum(str, Enum):
    x1 = 'x1'
    x2 = 'x2'
    x3 = 'x3'

    def __str__(self):
        return str(self.value)


class Game(BaseModel):
    score: list[int | CheckoutDartsEnum] = []
    total_score: int = 0
    avg: int = 0
    darts: int = 0
    winner: bool = False
    player: str = ""
    
    def set_darts_and_avg(self):
        for s in self.score:
            if type(s) == int:
                self.darts += 3
                self.total_score += s
            else:
                self.darts += int(s.replace('x', ''))
                self.winner = True
                self.total_score = 501
                
        self.avg = self.total_score / self.darts * 3

    def print_game(self):
        score = 501

        remaining = [501]

        for throw_score in self.score:
            try:
                score -= throw_score
            except TypeError:
                score -= score

            remaining.append(score)


        print(f"| {self.home_player: <7} |     |")
        print("| ------- | --- |")
        print("|         | 501 |")

        game_over = False

        for i in range(100):
            try:
                home = self.home_score[i]
            except IndexError:
                home = ''
            
            try:
                home_left = remaining[i+1]
            except IndexError:
                game_over = True

            print(f"| {home: <7} | {home_left: <3} |")

            if game_over:
                print()
                break

class Match(BaseModel):
    player: str
    legs_for: int = 0
    legs_against: int = 0
    games: list[Game] = []
    avg: float = 0

    def add_game(self, score: list[str]):
        game = Game(home_score=score, player=self.player)
        self.games.append(game)

        if game.winner:
            self.legs_for += 1
        else:
            self.legs_against += 1
    
    def is_won(self) -> bool:
        return self.legs_for == 2
    # def print_stats():

def get_match_from_file(filename: str) -> Match:
    _, player, _ = filename.split('/')[-1].replace('.csv', '').split('-')
    match = Match(player=player.capitalize())

    with open(filename) as f:      
        for game in f.readlines():
            score = game.rstrip().split(' ')
            
            game = Game(
                score=score,
                player=player.capitalize(),
            )

            game.set_darts_and_avg()

            match.games.append(game)
    
    # Set match stats
    match.legs_for = len([game for game in match.games if game.winner])
    match.legs_against = 2 - match.legs_for

    # Calculate the average weighted by num darts per game
    total_score = sum([game.darts * game.avg for game in match.games])
    match.avg = total_score / sum([game.darts for game in match.games])

    return match


class Player(BaseModel):
    name: str
    num_games: int = 0
    games: list[Game] = []


players: dict[str, Player] = {
    player: Player(name=player) for player in [
        'Adam',
        'Alex',
        'Carl',
        'Dave',
        'Debbie',
        'Iain',
        'Karen',
        'Lee',
        'Linda',
        'Ray',
        'Steve'
    ]
}

for week in glob.glob('_python_source/*'):
    date = week.split('/')[-1]

    # Start writing to csv file in _data
    with open(f'_data/{date}.csv', 'w') as f:
        f.write("name,average\n")

        for filename in glob.glob(f'{week}/*.csv'):
            match = get_match_from_file(filename)
            weekly_avg = sum([game.total_score for game in match.games])/sum([game.darts for game in match.games]) * 3
            f.write(f"{match.player},{weekly_avg:.2f}\n")

            players[match.player].games += match.games

for name, player in players.items():
    print(name)
    for game in player.games:
        print(game.avg, game.darts, game.score)
    print()

with open('_data/season.csv', 'w') as f:
    f.write("name,games,average\n")
    for name, player in players.items():
        player.num_games = len(player.games)
        if player.num_games == 0:
            season_average = 0
        else:
            season_average = sum([game.total_score for game in player.games])/sum([game.darts for game in player.games]) * 3
        f.write(f"{name},{player.num_games},{season_average:.2f}\n")