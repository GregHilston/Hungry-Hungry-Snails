import sys
import requests

base = "http://127.0.0.1:5000"
name = "Example"
food_value = "f"
player_value = "w"

def calculate_manhattan_distance(point_one, point_two):
    print(f"point_one {point_one}")
    print(f"point_two {point_two}")
    row_difference = point_two[0] - point_one[0]
    column_difference = point_two[1] - point_one[1]

    print(f"row_difference {row_difference} column_difference {column_difference}")

    return row_difference, column_difference

def calculate_manhattan_distance_to_cardinal_direction(row_difference, column_difference):
    print(f"row_difference {row_difference} column_difference {column_difference}")
    if row_difference > 0:
        print('n')
        return 'n'
    elif row_difference < 0:
        print('s')
        return 's'

    if column_difference > 0:
        print('e')

        return 'e'
    elif column_difference < 0:
        print('w')

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

    print(f"player_point: {player_point}")

    for row_index, row in enumerate(board):
        for column_index, column in enumerate(board[row_index]):
            if board[row_index][column_index] == food_value:
                print(f"found food: {row_index} {column_index}")

                manhattan_distance = calculate_manhattan_distance((row_index, column_index), player_point)
                manhattan_distance_point_sum = abs(manhattan_distance[0]) + abs(manhattan_distance[1])

                if manhattan_distance_point_sum < closest_food_distance:
                    print(f"\tfound closest food: {row_index} {column_index}")

                    closest_food_distance = manhattan_distance_point_sum

                closest_food_point = manhattan_distance[0], manhattan_distance[1]

    return closest_food_point

def step(unique_token, board, name=name):
    endpoint = base + "/api/step"

    closest_food_point = calculate_closet_food_point(board)
    cardinal_direction = calculate_manhattan_distance_to_cardinal_direction(closest_food_point[0], closest_food_point[1])

    print(f"board: {board}")
    print(f"cardinal_direction: {cardinal_direction}")

    json = {"name": name, "unique_token": unique_token, "step_direction": cardinal_direction}

    print(json)

    response = requests.post(endpoint, json=json)

    print(response)

    return response

start_response = start_game()
step_response = step(start_response.json()["unique_token"], start_response.json()["board"])

while step_response.status_code != 400:
    print(f"HERE {step_response.json()}")
    step_response = step(step_response.json()["unique_token"], step_response.json()["board"])

print(f"Score: {step_response.json()['score']}")