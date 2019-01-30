import sys
import requests

base = "http://127.0.0.1:5000"
name = "Example"
food_value = "f"
player_value = "w"

def calculate_manhattan_distance(point_one, point_two):
    row_difference = point_one[0] - point_two[0]
    column_difference = point_one[1] - point_two[1]

    return row_difference, column_difference

def calculate_manhattan_distance_to_cardinal_direction(row_difference, column_difference):
    if column_difference == 0 or row_difference <= column_difference:
        if row_difference < 0:
            return 'n'
        elif row_difference > 0:
            return 's'
    else:
        if column_difference < 0:
            return 'e'
        elif column_difference > 0:
            return 'w'

def start_game(name=name, board_number=0):
    endpoint = base + "/api/game"
    json = {"name": name, "board_number": board_number}

    response = requests.post(endpoint, json=json)

    return response

def find_player_point(board):
    for row_index, row in enumerate(board):
        for column_index, column in enumerate(board[row_index]):
            if board[row_index][column_index] == player_value:
                return row_index, column_index

def calculate_closet_food_point(board):
    player_point = find_player_point(board)
    closest_food_distance = sys.maxsize

    for row_index, row in enumerate(board):
        for column_index, column in enumerate(board[row_index]):
            if board[row_index][column_index] == food_value:
                manhattan_distance = calculate_manhattan_distance((row_index, column_index), player_point)
                manhattan_distance_point_sum = abs(manhattan_distance[0]) + abs(manhattan_distance[1])

                if manhattan_distance_point_sum < closest_food_distance:
                    closest_food_distance = manhattan_distance_point_sum
                    closest_food_point = manhattan_distance[0], manhattan_distance[1]

    return closest_food_point

def step(unique_token, board, name=name):
    endpoint = base + "/api/step"

    closest_food_point = calculate_closet_food_point(board)
    cardinal_direction = calculate_manhattan_distance_to_cardinal_direction(closest_food_point[0], closest_food_point[1])

    json = {"name": name, "unique_token": unique_token, "step_direction": cardinal_direction}

    response = requests.post(endpoint, json=json)

    return response

start_response = start_game()
step_response = step(start_response.json()["unique_token"], start_response.json()["board"])

while step_response.status_code != 400:
    step_response = step(step_response.json()["unique_token"], step_response.json()["board"])

print(f"Score: {step_response.json()['score']}")