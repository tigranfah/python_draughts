#! /usr/local/bin/python3

import os
import re
import io
import json
import platform


def process_games():

    game_file_names = os.listdir("dataset_pgn/levon_dataset")
    print(game_file_names)

    if platform.system() == "Darwin":
        print("remove .DS_Store")
        if ".DS_Store" in game_file_names:
            game_file_names.remove(".DS_Store")

    games = {}
    id = "1"

    GAME_OUTCOMES = ("0-1", "1-0", "1/2-1/2")

    for name in game_file_names:
        # "master_games.pgn"
        print(name)
        try:
            with open(os.path.join("dataset_pgn/levon_dataset", name), "r") as file:
                content = file.read()
                content = re.sub(r'{.*?}', '', content)
                content = re.sub(r'\[Event.*?\]', '', content)
                content = re.sub(r'\[WhiteFideId.*?\]', '', content)
                content = re.sub(r'\[BlackFideId.*?\]', '', content)
                content = re.sub(r'\[WhiteElo.*?\]', '', content)
                content = re.sub(r'\[BlackElo.*?\]', '', content)
                content = re.sub(r'\[Result.*?\]', '', content)
                content = re.sub(r'\[Round.*?\]', '', content)
                content = re.sub(r'\[TimeControl.*?\]', '', content)
                content = re.sub(r'\[Date.*?\]', '', content)
                content = re.sub(r'\[WhiteClock.*?\]', '', content)
                content = re.sub(r'\[BlackClock.*?\]', '', content)
                content = re.sub(r'\[ECO.*?\]', '', content)
                content = content.replace("[", '')
                content = content.replace("]", '')
                content = content.replace("\"", '')
                content = content.replace(".", '. ')

                ind = 0

                split_line = content.split()

                for ind in range(len(split_line)):

                    if split_line[ind] in ("White", "Black"):
                        if games.get(id) == None:
                            games[id] = {}
                        games[id][split_line[ind]] = f"{split_line[ind+1]}"
                    elif split_line[ind] == "1.":
                        if games[id].get("moves") == None:
                            games[id]["moves"] = {}
                        exp_moves = []
                        for i in range(len(split_line)):
                            if split_line[ind + i] in GAME_OUTCOMES:
                                exp_moves.append(split_line[ind + i])
                                break
                            exp_moves.append(split_line[ind + i])
                        for i in range(len(exp_moves)):
                            if exp_moves[i] in GAME_OUTCOMES:
                                games[id]["moves"]["result"] = exp_moves[i]
                            elif exp_moves[i][-1] == ".":
                                games[id]["moves"][exp_moves[i][:-1]] = f"{exp_moves[i+1]}"
                                if len(exp_moves) <= i + 2:
                                    continue
                                if not exp_moves[i+2] in GAME_OUTCOMES:
                                    games[id]["moves"][exp_moves[i][:-1]] += f" {exp_moves[i+2]}"
                        id = str(int(id)+1)
        except Exception as ex:
            print(ex)

    with open(os.path.join("dataset", "levon_games.json"), "w") as write_file:
        json.dump(games, write_file, indent=4)
        print("Saved into dataset/levon_games.json")


if __name__ == "__main__":
    process_games()
