from game import Game
from strategy import Player, HumanInput, RandomStrategy, HeuristicStrategy, MLStrategy
import tkinter as tk
from tkinter import messagebox, font, ttk, PhotoImage
from PIL import Image, ImageTk
import sys
from megawidgets import BoardFrame, GameInfoFrame, GameMoveUpdates, GameOverFrame
import time


class SantoriniGUI:
    def __init__(self, type1, type2, rank, ml_model_path=None):
        """Initializes the GameCLI"""
        human_strategy = HumanInput()
        random_strategy = RandomStrategy()
        heuristic_strategy = HeuristicStrategy()

        ml_model_path = "santorini_cnn_win_predictor_varied_denser.h5"
        ml_strategy = MLStrategy(ml_model_path)

        if str(type1) == "human":
            player1 = Player(human_strategy, "human")
        elif str(type1) == "heuristic":
            player1 = Player(heuristic_strategy, "heuristic")
        elif str(type1) == "random":
            player1 = Player(random_strategy, "random")
        elif str(type1) == "ml" and ml_model_path:
            player1 = Player(ml_strategy, "ml")

        if str(type2) == "human":
            player2 = Player(human_strategy, "human")
        elif str(type2) == "heuristic":
            player2 = Player(heuristic_strategy, "heuristic")
        elif str(type2) == "random":
            player2 = Player(random_strategy, "random")
        elif str(type2) == "ml" and ml_model_path:
            player2 = Player(ml_strategy, "ml")

        self.game = Game(player1, player2, "gui", self)

        self._window = tk.Tk()
        self._window.title("SantoriniGame")
        self._window.geometry("540x680") 
        self._style = ttk.Style(self._window)
        self._style.theme_use('clam')
        self._window.configure(bg='#f0f0f0')
        self._top_frame = tk.Frame(self._window, bg='#f0f0f0')
        self._top_frame.pack(side=tk.TOP, fill=tk.X)
        background_image = Image.open("santorini_background.jpg")
        width, height = background_image.size
        bottom_crop = (325, 200, width, height)
        cropped_image = background_image.crop(bottom_crop)
        background_photo = ImageTk.PhotoImage(cropped_image)
        canvas = tk.Canvas(self._top_frame, width=600, height=50)
        canvas.pack()
        canvas.create_image(0, 0, image=background_photo, anchor='nw')
        my_font = font.Font(family="MS Reference Specialty", size=30, weight="bold")
        canvas.create_text(70, 25, text="Santorini", font=my_font, fill='black')

        self._move_retrieve_updates = GameMoveUpdates(self._window, self.game, bg='#f0f0f0')
        self._move_retrieve_updates.pack(side=tk.TOP, fill=tk.BOTH)

        self._board = BoardFrame(self._window, self.game, self, type1, type2)
        self._board.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._game_info_frame = GameInfoFrame(self._window, self.game, self, bg='#f0f0f0')
        self._game_info_frame.pack(side=tk.TOP, fill=tk.X)

        self._game_over_frame = GameOverFrame(self._window, self.game, type1, type2, self, bg="#f0f0f0")
        self._in_winning_state = False

        if type1 != "human" and type2 != "human":
            self._play_ai_vs_ai()

        elif self.game.cur_player_object.type != "human": 
            self._play_ai_turn()


        self._window.mainloop()

    def _play_ai_vs_ai(self):
        """Handles the game loop for AI vs AI with a delay between moves."""
        if self.game.check_win():
            self._end_game()
        else:
            self._game_info_frame.update_info()
            self.game.cur_player_object.play_turn(self.game, self)
            self._window.after(0, self._play_next_turn)

    def _play_ai_turn(self):
        """Plays the AI turn and schedules the next turn."""
        if self.game.check_win():
            self._end_game()
        self.game.cur_player_object.play_turn(self.game, self)
        self._window.after(0, self._play_next_turn)

    def _play_next_turn(self):
        """Advances to the next turn and checks if it's AI's turn again."""
        if self.game.check_win():
            self._end_game()
        self.game.next_turn()
        if self.game.cur_player_object.type != "human":
            self._play_ai_vs_ai()

    def _end_game(self):
        """Handles the end of the game by showing a pop-up with the winner and an option to quit."""
        winner = self.game.check_win()
        if winner:
            self._disable_buttons()
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self._window.quit()
        
    def _disable_buttons(self):
        """Disables all buttons on the board."""
        for button in self._board.buttons.values():
            button.config(state=tk.DISABLED)
    
    def refresh_board(self):
        """Refreshes the board."""
        self._board.create_grid(True)



if __name__ == "__main__":
    white_player_type = 'human'
    blue_player_type = 'human'
    undo_redo_enabled = 'off'
    score_display_enabled = 'on'
    
    if len(sys.argv) > 1:
        white_player_type = sys.argv[1]
    if len(sys.argv) > 2:
        blue_player_type = sys.argv[2]
    if len(sys.argv) > 3:
        undo_redo_enabled = sys.argv[3]
    if len(sys.argv) > 4:
        score_display_enabled = sys.argv[4]

    undo_redo_bool = undo_redo_enabled.lower() == 'on'
    score_display_bool = score_display_enabled.lower() == 'on'

    game_cli = SantoriniGUI(white_player_type, blue_player_type,score_display_bool)