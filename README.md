# minetest

## Usage
- Run using `python .\src\game.py`

## Save States
- States are saved in JSON format
- The board is represented by a three-dimensional grid, ordered by: `row` -> `column` -> `stack/board cell`.
- When saving the game state, the full file path of the save file must be provided, e.g `./save_state.json`
- The `type` of the player determines if it's a player or an AI. This can be changed without any problems.
- The difficulty at the bottom of the save file is encoded with the following values: `0` (easy), `1` (medium) and `2` (difficult).
- The `round` counter starts at `0` on the first turn (when the first player places a piece for their opponent) and is incremented at the end of each player's turn.
- The `owner` value of a piece on the board is the value of the `identifier` of the owning player.

If any of the values are out of bounds or invalid, the file may be interpreted as best it can (by defaulting to some value) or not loaded at all.