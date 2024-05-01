from game import Game
from strategy import Player, HumanInput, RandomStrategy, HeuristicStrategy
import tkinter as tk
from tkinter import messagebox, font, ttk
from PIL import Image, ImageTk
import sys
from megawidgets import BoardFrame, GameInfoFrame, GameMoveUpdates, GameOverFrame


class SantoriniGUI:
    def __init__(self, type1, type2, rank):
        """Initializes the GameCLI"""
        human_strategy = HumanInput()
        random_strategy = RandomStrategy()
        heuristic_strategy = HeuristicStrategy()


        if str(type1) == "human": player1 = Player(human_strategy, "human")
        if str(type1) == "heuristic": player1 = Player(heuristic_strategy, "heuristic")
        if str(type1) == "random": player1 = Player(random_strategy, "random")
        
        if str(type2) == "human": player2 = Player(human_strategy, "human")
        if str(type2) == "heuristic":player2 = Player(heuristic_strategy, "heuristic")
        if str(type2) == "random":player2 = Player(random_strategy, "random")

        if rank == True: 
            self.score_output = True
        else:
            self.score_output = False
    
        self.game = Game(player1, player2, "gui")


        self._window = tk.Tk()
        self._window.title("SantoriniGame")
        self._window.geometry("600x600") 
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
        my_font = font.Font(family="Times New Roman", size=30, weight="bold")
        canvas.create_text(70, 25, text="Santorini", font=my_font, fill='black')

        self._move_retrieve_updates = GameMoveUpdates(self._window, self.game, bg='#f0f0f0')
        self._move_retrieve_updates.pack(side=tk.TOP, fill=tk.BOTH)

        self._board = BoardFrame(self._window, self.game, self, type1, type2)
        self._board.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._game_info_frame = GameInfoFrame(self._window, self.game, self, bg='#f0f0f0')
        self._game_info_frame.pack(side=tk.TOP, fill=tk.X)

        self._game_over_frame = GameOverFrame(self._window, self.game, type1, type2, self, bg="#f0f0f0")

        if type1 != "human" and type2 != "human":
            var = True
            while var:
                self._game_info_frame.update_info()
                if self.game.check_win():
                    self._board.create_grid()
                    self._game_over_frame.build_frame()
                    self._game_over_frame.show()
                    self._game_over_frame.display_winner(self.game.check_win())
                    var = False
                else:
                    self.game.cur_player_object.play_turn(self.game, self)
                    self.game.next_turn()
        elif self.game.cur_player_object.type != "human": 
            self.game.cur_player_object.play_turn(self.game, self)
            self.game.next_turn()
            print(self.game.cur_player_object.type)

        self._window.mainloop()


    def run(self):
        """Initiates the game input loop."""
        while True:
            self._retrieve_all_possible_moves()
            print("hello")
            self._print_game_state()
            self._winner_winner_chicken_dinner()
            self.game.cur_player_object.play_turn(self.game, self)
            self.game.next_turn()


if __name__ == "__main__":
    white_player_type = 'human'
    blue_player_type = 'human'
    undo_redo_enabled = 'off'
    score_display_enabled = 'off'
    

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



