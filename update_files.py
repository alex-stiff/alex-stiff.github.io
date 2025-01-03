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
    score: list[int] = []
    total_score: int = 0
    avg: int = 0
    darts: int = 0
    winner: bool = False
    player: str = ""
    
    def set_stats(self):
        self.total_score = sum(self.score)
        self.winner = self.total_score == 501
        self.avg = self.total_score / self.darts * 3

    def print_game(self):
        remaining = 501

        print(f"| {self.player: <7} |     |")
        print("| ------- | --- | --- |")
        print("|         | 501 |     |")

        game_over = False

        # in 49 darts 49 % 3 == 1 (x1)
        # in 50 darts 50 % 3 == 2 (x2)
        # in 51 darts 51 % 3 == 0 (x3)

        for i, score in enumerate(self.score):
            if score == remaining:
                score = f"x{(self.darts-1) % 3 + 1}"
                game_over = True
                remaining = 0
            else:
                remaining -= score

            print(f"| {score: <7} | {remaining: <3} | {(i+1) * 3: <3} |")

            if game_over:
                print()
                break

class Match(BaseModel):
    player: str
    legs_for: int = 0
    legs_against: int = 0
    games: list[Game] = []
    avg: float = 0

    def add_game(self, score: list[int]):
        game = Game(score=score)
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

            game_score: list[int] = []
            darts: int = 0

            for s in score:
                try:
                    game_score.append(int(s))
                    darts += 3
                except Exception:
                    game_score.append(501 - sum(game_score))
                    darts += int(s.replace('x', ''))
            
            game = Game(
                score=game_score,
                darts=darts,
                player=player.capitalize(),
            )

            game.set_stats()

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

# for name, player in players.items():
#     print(name)
#     for game in player.games:
#         print(game.avg, game.darts, game.score)
#     print()

with open('_data/season.csv', 'w') as f:
    f.write("name,games,average\n")
    for name, player in players.items():
        player.num_games = len(player.games)
        if player.num_games == 0:
            season_average = 0
        else:
            season_average = sum([game.total_score for game in player.games])/sum([game.darts for game in player.games]) * 3
        f.write(f"{name},{player.num_games},{season_average:.2f}\n")