from flask import Flask, Response, request, render_template
import uuid
import json
import pickle
import os

app = Flask(__name__)

EMPTY_SPACE_TOKEN = '_'
PLAYER_TOKEN = 'p'
FOOD_TOKEN = 'f'
game_history = {}
# game_rules_function = 

# def collect_most_food_in_least_steps():
#     pass

# def collest_most_food_in_n_steps():
#     pass

def create_folder_structure_for_player_if_not_exists(name, unique_token):
    player_folder = f"game_history/{name}"
    if not os.path.exists(player_folder):
        os.makedirs(player_folder)
    
    current_game_folder = f"game_history/{name}/{unique_token}"
    if not os.path.exists(current_game_folder):
        os.makedirs(current_game_folder)

def record_step(name, unique_token, board, score, max_steps, steps_taken):
    d = {}
    d["name"] = name
    d["unique_token"] = unique_token
    d["max_steps"] = max_steps
    d["board"] = board
    d["score"] = score
    d["steps_taken"] = steps_taken

    with open(f"game_history/{name}/{unique_token}/{steps_taken}.json", 'w') as fp:
        json.dump(d, fp)

def calculate_last_step_taken(name, unique_token):
    highest_step_taken = -1
    
    directory = f"game_history/{name}/{unique_token}"
    for filename in os.listdir(directory):
        steps_taken = int(filename.split(".json")[0])

        if steps_taken > highest_step_taken:
            highest_step_taken = steps_taken

    return highest_step_taken

def find_player_index(name, unique_token, last_step_taken):
    filepath = f"game_history/{name}/{unique_token}/{last_step_taken}.json"

    with open(filepath, 'r') as fp:
        data = json.load(fp)
        player_index = 0

        for row in data["board"]:
            for column in row:
                if column == "p":
                    return player_index

                player_index += 1

def parse_last_game_state(name, unique_token, last_step_taken):
    filepath = f"game_history/{name}/{unique_token}/{last_step_taken}.json"

    with open(filepath, 'r') as fp:
        data = json.load(fp)
        
        return data["max_steps"], data["board"], data["score"], data["steps_taken"], find_player_index(name, unique_token, last_step_taken)

def move_player(name, unique_token, last_step_taken, new_player_location_index_offset, score, steps_taken):
    filepath = f"game_history/{name}/{unique_token}/{last_step_taken}.json"
    player_index = find_player_index(name, unique_token, last_step_taken)
    new_player_index = player_index + new_player_location_index_offset

    with open(filepath, 'r') as fp:
        data = json.load(fp)
        index = 0

        for row_index, row in enumerate(data["board"]):
            for column_index, column in enumerate(row):
                if index == player_index:
                    data["board"][row_index][column_index] = "_"
                if index == new_player_index:
                    if column == "f":
                        score += 1
                    data["board"][row_index][column_index] = "p"
                index += 1

        return data["board"], score, steps_taken + 1

def get_players_highest_score(name):
    best_score = -1
    player_folder = f"game_history/{name}"

    if os.path.exists(player_folder):
        for game in os.listdir(player_folder):
            last_step_taken = calculate_last_step_taken(name, game)

            _, _, score, _, _ = parse_last_game_state(name, game, last_step_taken)

            if score > best_score:
                best_score = score
    
    return best_score

def get_players_names_and_best_scores():
    player_names = []
    best_scores = []

    game_history_folder = "game_history"
    if os.path.exists(game_history_folder):

        for player_name in os.listdir(game_history_folder):
            player_names.append(player_name)

            best_scores.append(get_players_highest_score(player_name))

    return player_names, best_scores

@app.route('/')
def index(name=None):
    player_names, player_scores  = get_players_names_and_best_scores()

    return render_template("index.html", zipped_player_names_and_scores=zip(player_names, player_scores))

@app.route('/game/start', methods=["POST"])
def init(board_number=0):
    if not request.form.get("name"):
        return Response(json.dumps({"message": "Required parameter 'name' was not provided. How would we know who you are?"}), 422)

    if request.form.get("board_number"):
        board_number = request.form.get("board_number")

    with open(f'levels/{board_number}.json', 'r') as fp:
        INITIAL = json.load(fp)

    initial_copy = {**INITIAL}

    unique_token = str(uuid.uuid4()) 

    initial_copy["unique_token"] = unique_token 

    initial_copy["score"] = 0

    initial_copy["steps_taken"] = 0

    game_history[request.form["name"] ] = unique_token

    create_folder_structure_for_player_if_not_exists(request.form["name"], unique_token)

    print(f"initial board \n {initial_copy['board']}")

    record_step(request.form["name"], unique_token, initial_copy["board"], 0, initial_copy["max_steps"], 0) 

    return Response(json.dumps(initial_copy), mimetype='text/json')

@app.route('/game/step', methods=["POST"])
def step():
    if not request.form.get("name"):
        return Response(json.dumps({"message": "Required parameter 'name' was not provided. How would we know who you are?"}), 422)
    
    if not request.form.get("unique_token"):
        return Response(json.dumps({"message": "Required parameter 'unique_token' was not provided. How would we know what game you are playing?"}), 422)

    if not request.form.get("step_direction"):        
        return Response(json.dumps({"message": "Required parameter 'step_direction' was not provided. How would we know where your snail intends to go?"}), 400)

    last_step_taken = calculate_last_step_taken(request.form["name"], request.form["unique_token"])

    max_steps, board, score, steps_taken, player_location_index = parse_last_game_state(request.form["name"], request.form["unique_token"], last_step_taken)

    if max_steps == steps_taken:
        d = {}

        d["max_steps"] = max_steps
        d["board"] = board
        d["unique_token"] = request.form["unique_token"]
        d["score"] = score
        d["steps_taken"] = steps_taken

        d["message"] = "Game has already ended and your newest move was not processed"

        # d["your best score"] = calculate_players_best_score(request.form["name"], request.form["unique_token"]) # TODO
        # d["best score"] = calculate_best_score() # TODO

        return Response(json.dumps(d), 400, mimetype='text/json')

    if request.form["step_direction"]  == "n":
        player_location_index_offset = -5 # going up a row
    elif request.form["step_direction"]  == "e":
        player_location_index_offset = 1 # going right a column
    elif request.form["step_direction"]  == "s":
        player_location_index_offset = 5 # going down a row 
    elif request.form["step_direction"]  == "w":
        player_location_index_offset = -1 # going left a column
    else:
        return Response(json.dumps({"message": "Required parameter 'step_direction' was not valid character. Accepted characters are ['n', 'e', 's', 'w']"}), 422)

    new_board, new_score, steps_taken = move_player(request.form["name"], request.form["unique_token"], last_step_taken, player_location_index_offset, score, steps_taken)    

    print(f"new board \n{new_board}")

    record_step(request.form["name"], request.form["unique_token"], new_board, new_score, max_steps, steps_taken)

    d = {}

    d["max_steps"] = max_steps
    d["board"] = board
    d["unique_token"] = request.form["unique_token"]
    d["score"] = new_score
    d["steps_taken"] = steps_taken

    if steps_taken == max_steps:
        d["message"] = "Game Over, max number of steps taken"
        # d["your best score"] = calculate_players_best_score(request.form["name"], request.form["unique_token"]) # TODO
        # d["best score"] = calculate_best_score() # TODO
        return Response(json.dumps(d), 400, mimetype='text/json')


    return Response(json.dumps(d), 200, mimetype='text/json')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')