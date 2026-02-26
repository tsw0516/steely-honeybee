# Board Game Shelf Organizer
# This program reads board game dimensions from an Excel file,
# allocates them onto shelves while maximizing space utilization, and visualizes the arrangement
# Tyler Walker - 2026-02-25

import pandas as pd
import matplotlib.pyplot as plt
import random

from models import BoardGame, Stack, Shelf

# -------------------
# Load games from Excel
# -------------------
def load_games_from_excel(filepath):
    df = pd.read_excel(filepath).dropna() # Read the file and drop any rows with missing values
    games = [] 

    for _, row in df.iterrows():
        game = BoardGame(
            name=row["Name"],
            width=row["Width"],
            height=row["Height"]
        )
        games.append(game)
    return games


# -------------------
# Allocation Logic
# -------------------
def allocate_games_to_shelves(games, shelves):
    unplaced = []

    for game in games:
        placed = False

        # Try existing stacks first
        for shelf in shelves:
            for stack in shelf.stacks:
                if stack.can_fit(game):
                    stack.add_game(game)
                    placed = True
                    break
            if placed:
                break

        # Try starting a new stack
        if not placed:
            for shelf in shelves:
                if shelf.can_start_new_stack(game):
                    shelf.start_new_stack(game)
                    placed = True
                    break

        # If still not placed
        if not placed:
            unplaced.append(game)

    return shelves, unplaced

# -------------------
# Visualization
# -------------------
def visualize_shelves(shelves):
    fig, ax = plt.subplots(figsize=(12, 6))

    shelf_gap = 5       # vertical gap between shelves
    stack_gap = 1       # horizontal gap between stacks
    y_offset = 0        # starting y for first shelf

    for shelf_idx, shelf in enumerate(shelves):
        x_offset = 0

        # Draw shelf baseline slightly below first stack
        ax.hlines(y=y_offset - 1.5, xmin=0, xmax=shelf.max_length, color='black', linewidth=2)

        for stack in shelf.stacks:
            stack_bottom = y_offset
            for game in stack.games:
                color = (random.random(), random.random(), random.random())

                # Draw the game as a horizontal bar
                ax.barh(
                    y=stack_bottom,
                    width=game.width,
                    height=game.height,
                    left=x_offset,
                    color=color,
                    edgecolor='black'
                )

                ax.text(
                    x=x_offset + game.width / 2,
                    y=stack_bottom + game.height / 2,
                    s=game.name,
                    fontsize=12,
                    color='black'
                )

                stack_bottom += game.height

            x_offset += stack.base_width + stack_gap

        y_offset += shelf.max_height + shelf_gap

    ax.set_xlabel("Shelf Length")
    ax.set_ylabel("Height")
    ax.set_title("Board Game Shelf Visualization")
    ax.set_xlim(0, max(s.max_length for s in shelves) + 5)
    ax.set_ylim(0, y_offset + 5)
    plt.show()


# -------------------
# Main Execution
# -------------------
def main():
    # Load games
    filepath = "data/games.xlsx"
    games = load_games_from_excel(filepath)

    # Sort by width descending, then height descending
    games.sort(key=lambda g: (g.width, g.height), reverse=True)

    # Shelf configuration
    NUM_SHELVES = 14
    SHELF_LENGTH = 13.125
    SHELF_HEIGHT = 13.125
    shelves = [Shelf(SHELF_LENGTH, SHELF_HEIGHT) for _ in range(NUM_SHELVES)]

    # Allocation
    shelves, unplaced = allocate_games_to_shelves(games, shelves)

    # Metrics
    print("\n=== Shelf & Stack Metrics ===")
    for i, shelf in enumerate(shelves, start=1):
        shelf_utilization = (shelf.max_length - shelf.remaining_length) / shelf.max_length
        print(f"\nShelf {i} utilization (horizontal): {shelf_utilization:.0%}")

        for j, stack in enumerate(shelf.stacks, start=1):
            stack_utilization = (shelf.max_height - stack.remaining_height) / shelf.max_height
            print(f"  Stack {j} utilization (vertical): {stack_utilization:.0%}")

    # Print structured allocation results
    for i, shelf in enumerate(shelves, start=1):
        print(f"\n=== Shelf {i} ===")
        print(f"Remaining horizontal length: {shelf.remaining_length}")
        for j, stack in enumerate(shelf.stacks, start=1):
            print(f"  Stack {j} (base width {stack.base_width})")
            for game in stack.games:
                print(f"     - {game.name} (W:{game.width}, H:{game.height})")
            print(f"     Remaining stack height: {stack.remaining_height}")

    if unplaced:
        print("\n=== Unplaced Games ===")
        for game in unplaced:
            print(f" - {game.name}")

    # Visualization
    visualize_shelves(shelves)


if __name__ == "__main__":
    main()