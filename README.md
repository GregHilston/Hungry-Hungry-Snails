# [Hungry Hungry Snails](https://github.com/GregHilston/Hungry-Hungry-Snails)

[![Heroku](https://heroku-badge.herokuapp.com/?app=heroku-badge)(https://hungry-hungry-snails.herokuapp.com/)]

Hungry Hungry Snails is a small API used to host a game, interacted with via scripts through an API.

## The Objective

The point of Hungry Hungry Snails is to write software to help guide your snail to the most amount of food on a 2d grid, in the least amount of steps. A leader board can be accessed to check the top score for each board. I was interested in playing a game like this, but I was unable to find a harness to run the server logic. See the section titled "Example Solution", so see a sample greedy implementation.

## Endpoints

Each endpoint uses the local development IP and Port. These may change in production.

### Home Page (Leader Board) Endpoint

**Path: `/`**

**HTTP Method** [GET]

The home page of our application. Returns the leader board standings per level, player and score.

**Example Curl**

```
curl http://0.0.0.0:5000
```

#### Successful Response

**Status Code** 200

**Body** HTML of the leader board, describing each player's best score for each level they've attempted.

**Example Response**

```
<!doctype html><title>Hungry Hungry Snails</title><body><h1>Hungry Hungry Snails</h1><p>Hungry Hungry Snails is a competitive game intended to be played by individuals writing their own scripts with logic to make decisions for them.</p><h2>Leader Board</h2><table><th>Level</th><th>Name</th><th>Highest Score</th><ul><tr><td>0</td><td>grehg</td><td>3</td></tr><tr><td>1</td><td>grehg</td><td>3</td></tr>
          
        
      </ul>
  </table></body>
```

### Start Game Endpoint

**Path: `/api/game`**

**HTTP Method** [POST]

**Required Body Parameters**

- `name` (`String`): The name of the player

**Optional Body Parameters**

- `board_number` (`Int`): Which board the player would like to play. Defaults to board 0.

Used to initialize a game for the player. A player may have multiple games active at once.

**Example Curl**

```
curl -X POST \
  http://127.0.0.1:5000/api/game \
  -d '{
	"name": "Grehg",
	"board_number": 0
}'
```

#### Successful Response

**Status Code** 200

**Body** JSON with the following:

- `max_steps` (`Int`): Describes how many steps the player can make before the game ends.
- `board` (`Array of Arrays`): Describes the current state of the field. The follow single character Strings can be used to describe a cell:
  - `_`: An empty space
  - `f`: A single piece of food. Stepping onto this cell will consume the food and award the player a single point.
  - `s`: The snail the player is controlling. This is your current location in the game.
- `unique_token` (`Str`): A unique token to represent your game id. This must be stored and sent in subsequent Step endpoint POSTs. This is used to signify to the server which game your attempting to make a move on.
- `score` (`Int`): The player's current score.
- `steps_taken` (`Int`): The number of steps the player has taken so far. When this counter equals `max_steps`, the game will end and no additional steps will be accepted.

**Example Response**

`json`
```
{
    "max_steps": 5,
    "board": [
        ["_", "_", "_", "_", "_"],
        ["_", "_", "f", "_", "_"],
        ["_", "_", "_", "_", "_"],
        ["_", "_", "s", "_", "_"],
        ["_", "f", "f", "f", "_"]
    ],
    "unique_token": "fc60c0b5-0a8d-48ee-93ea-19069836f913",
    "score": 0,
    "steps_taken": 0
}
```

#### Error Response

**Status Code** 422

Occurs when the required field `name` (`String`) is not passed.

**Example Response**

`json`
```
{"message": "Required parameter 'name' was not provided. How would we know who you are?"}
```

### Step Endpoint

**Path:** `/api/step`

**HTP Method:** [Post]

**Required Body Parameters**

- `name` (`String`): The name of the player
- `unique_token` (`String`): The unique token of the game we're making a move of
- `step_direction` (`String`): The cardinal direction that we're moving

**Example Curl**

```
curl -X POST \
  http://127.0.0.1:5000/api/step \
  -d '{
	"name": "Grehg",
	"unique_token": "e73f8275-fd01-4d07-aadf-877c16283dcc",
	"step_direction": "s"
}'
```
#### Successful Response 

**Status Code** 200

**Body** JSON with the following:

- `max_steps` (`Int`): Describes how many steps the player can make before the game ends.
- `board` (`Array of Arrays`): Describes the current state of the field. The follow single character Strings can be used to describe a cell:
  - `_`: An empty space
  - `f`: A single piece of food. Stepping onto this cell will consume the food and award the player a single point.
  - `s`: The snail the player is controlling. This is your current location in the game.
- `unique_token` (`Str`): A unique token to represent your game id. This must be stored and sent in subsequent Step endpoint POSTs. This is used to signify to the server which game your attempting to make a move on.
- `score` (`Int`): The player's current score.
- `steps_taken` (`Int`): The number of steps the player has taken so far. When this counter equals `max_steps`, the game will end and no additional steps will be accepted.

**Example Response**

`json`
```
{
    "max_steps": 5,
    "board": [
        ["_", "_", "_", "_", "_"],
        ["_", "_", "f", "_", "_"],
        ["_", "_", "_", "_", "_"],
        ["_", "_", "s", "_", "_"],
        ["_", "f", "f", "f", "_"]
    ],
    "unique_token": "f0a13b6d-e77c-4d45-ab1d-1febdec92a36",
    "score": 0,
    "steps_taken": 1
}
```

#### Error Response

**Status Code** 400

Occurs when you have no more moves left. You'll still receive the last state of the game.

**Example Response**

`json`
```
{
    "max_steps": 5,
    "board": [
        ["_", "_", "_", "_", "_"],
        ["_", "_", "f", "_", "_"],
        ["_", "_", "_", "_", "_"],
        ["_", "_", "s", "_", "_"],
        ["_", "f", "f", "f", "_"]
    ],
    "unique_token": "f0a13b6d-e77c-4d45-ab1d-1febdec92a36",
    "score": 0,
    "steps_taken": 5,
    "message": "Game has already ended and your newest move was not processed"
}
```

**Status Code** 422

Occurs when:

- The required field `name` (`String`) or `unique_token` (`String`) is not passed.
- Your move would have taken your worm off an edge.

**Example Response 1**

`json`
```
{"message": "Required parameter 'unique_token' was not provided. How would we know what game you are playing?"}
```

**Example Response 2**

`json`
```
{"message": "Invalid move. You would have gone off the edge"}
```

## Running

The following scripts must be run in order:

1. build.sh
2. clean.sh
3. run.sh OR run_watch.sh (for live reloading of code changes)

## Example Solution

A greedy python solution has been provided to ensure that the API access is clear, along with giving an idea on how one can approach this problem. While this greedy approach does solve the level `0.json` with the maximum value, it will fail on more complicated levels. This is because the algorithm is very short sighted and will step towards whatever food is closest to it at each moment in time.

## TODO

- ensure that the POSTs have a JSON body being sent and not form data
- return your best score
- return the best score
- could support walls
- Could productionify this by using -d on the docker run to run in detached mode
  - use docker logs -f Hungry-Hungry-Snails to look at the stdout/stderr logs
- create a Makefile for all my Docker scripts
- Use swagger for documentation