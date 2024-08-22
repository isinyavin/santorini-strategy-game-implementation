import tkinter as tk
from strategy import PlayerStrategy
from tkinter import messagebox, PhotoImage
from game import Game
import time
import copy

class BoardFrame(tk.Frame):
    def __init__(self, parent, game, gui, type1, type2, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, bg="white")
        self.game = game
        self.temp_copy_game = copy.deepcopy(self.game)
        self.type1 = type1
        self.gui = gui
        self.type2 = type2
        self.buttons = {}
        self.selected_worker = None
        self.selected_move = None
        self.selected_move_coord = None
        self.selected_build = None
        self._move_retrieve_state = "select_player"

        m=5
        n=5

        self.image_0_temp = PhotoImage(file = '0.png')
        self.image_0 = self.image_0_temp.subsample(m,n)

        self.image_0A_temp = PhotoImage(file = '0A.png')
        self.image_0A = self.image_0A_temp.subsample(m,n)

        self.image_0B_temp = PhotoImage(file = '0B.png')
        self.image_0B = self.image_0B_temp.subsample(m,n)

        self.image_0Y_temp = PhotoImage(file = '0Y.png')
        self.image_0Y = self.image_0Y_temp.subsample(m,n)

        self.image_0Z_temp = PhotoImage(file = '0Z.png')
        self.image_0Z = self.image_0Z_temp.subsample(m,n)

        self.image_1_temp = PhotoImage(file = '1.png')
        self.image_1 = self.image_1_temp.subsample(m,n)

        self.image_1A_temp = PhotoImage(file = '1A.png')
        self.image_1A = self.image_1A_temp.subsample(m,n)

        self.image_1B_temp = PhotoImage(file = '1B.png')
        self.image_1B = self.image_1B_temp.subsample(m,n)

        self.image_1Y_temp = PhotoImage(file = '1Y.png')
        self.image_1Y = self.image_1Y_temp.subsample(m,n)

        self.image_1Z_temp = PhotoImage(file = '1Z.png')
        self.image_1Z = self.image_1Z_temp.subsample(m,n)

        self.image_2_temp = PhotoImage(file = '2.png')
        self.image_2 = self.image_2_temp.subsample(m,n)

        self.image_2A_temp = PhotoImage(file = '2A.png')
        self.image_2A = self.image_2A_temp.subsample(m,n)

        self.image_2B_temp = PhotoImage(file = '2B.png')
        self.image_2B = self.image_2B_temp.subsample(m,n)

        self.image_2Y_temp = PhotoImage(file = '2Y.png')
        self.image_2Y = self.image_2Y_temp.subsample(m,n)

        self.image_2Z_temp = PhotoImage(file = '2Z.png')
        self.image_2Z = self.image_2Z_temp.subsample(m,n)

        self.image_3_temp = PhotoImage(file = '3.png')
        self.image_3 = self.image_3_temp.subsample(m,n)

        self.image_3A_temp = PhotoImage(file = '3A.png')
        self.image_3A = self.image_3A_temp.subsample(m,n)

        self.image_3B_temp = PhotoImage(file = '3B.png')
        self.image_3B = self.image_3B_temp.subsample(m,n)

        self.image_3Y_temp = PhotoImage(file = '3Y.png')
        self.image_3Y = self.image_3Y_temp.subsample(m,n)

        self.image_3Z_temp = PhotoImage(file = '3Z.png')
        self.image_3Z = self.image_3Z_temp.subsample(m,n)

        self.image_4_temp = PhotoImage(file = '4.png')
        self.image_4 = self.image_4_temp.subsample(m,n)

        self.repr_to_img = {'0 ': self.image_0, '0A': self.image_0A, '0B': self.image_0B, '0Y': self.image_0Y, '0Z': self.image_0Z, 
                               '1 ': self.image_1, '1A': self.image_1A, '1B': self.image_1B, '1Y': self.image_1Y, '1Z': self.image_1Z, 
                               '2 ': self.image_2, '2A': self.image_2A, '2B': self.image_2B, '2Y': self.image_2Y, '2Z': self.image_2Z, 
                               '3 ': self.image_3, '3A': self.image_3A, '3B': self.image_3B, '3Y': self.image_3Y, '3Z': self.image_3Z, 
                               '4 ': self.image_4}

        if type1 != "human" and type2 != "human":
            self.create_grid(True)
        else:
            self.create_grid_gui()
        

    def create_grid_gui(self, var = False):
        self.game = self.gui.game
        for i in range(5):
            for j in range(5):
                square = self.game.board.squares[j][i]

                
                button = tk.Button(self, text=repr(square), image = self.repr_to_img[repr(square)],
                                   command=lambda i=i, j=j: self.handle_click(i, j),
                                   bg='black', width=100, height=100)
                button.grid(row=i, column=j, sticky='nsew')
                self.buttons[(i, j)] = button
        if var == False:
            self.update_button_highlights()
        else:
            for button in self.buttons.values():
                button.config(highlightbackground='light grey')

    def create_grid(self, var = False):
        winner_detected = False
        for i in range(5):
            for j in range(5):
                square = self.game.board.squares[i][j]
                square_repr = repr(square)
                
                if square_repr in ['3A', '3B', '3Y', '3Z']:
                    winner_detected = True
                
                button = tk.Button(self, text=square_repr, image=self.repr_to_img[square_repr],
                                command=lambda i=i, j=j: self.handle_click(i, j),
                                bg='black', width=100, height=100)
                button.grid(row=i, column=j, sticky='nsew')
                self.buttons[(i, j)] = button
        if var == False:
            self.update_button_highlights()
        else:
            for button in self.buttons.values():
                button.config(highlightbackground='light grey')

        if winner_detected:
            #winner = self.game.check_win()
            #if winner:
               # messagebox.showinfo("Game Over", f"{winner} wins!")
               # self.gui._window.quit()
            pass

    def update_button_highlights(self):
        if self._move_retrieve_state == "select_player":
            possible_moves = self.game.board.enumerate_all_available_moves(self.game.curr_player_to_move)
            active_workers = {move[0] for move in possible_moves}
            for (x, y), button in self.buttons.items():
                button.config(highlightbackground='dark blue' if str(self.game.board.squares[x][y].worker) in active_workers else 'light gray')
        elif self._move_retrieve_state == "select_move":
            for button in self.buttons.values():
                button.config(highlightbackground='light grey')
            x, y = self.game.board.find_worker_coords(str(self.selected_worker))
            self.buttons[(x, y)].config(highlightbackground='dark blue')
            possible_moves = []
            for move in self.game.board.enumerate_all_available_moves(self.game.curr_player_to_move):
                if str(move[0]) == str(self.selected_worker):
                    possible_moves.append(move)
            if not possible_moves:
                messagebox.showerror("No Possible Moves", "There are no available moves for the selected worker.")
                return
            possible_directions = {move[1] for move in possible_moves}

            for direction in possible_directions:
                x, y = self.game.board.find_worker_coords(str(self.selected_worker))  
                #print(self.selected_worker)
                new_x, new_y = self.game.board.find_new_coords2(y, x, direction) 
                if 0 <= new_x < 5 and 0 <= new_y < 5:  
                    self.buttons[(new_y, new_x)].config(highlightbackground='light blue')

        elif self._move_retrieve_state == "select_build":
            #print("SELECT BUILD")
            #print(self.selected_worker)
            for button in self.buttons.values():
                button.config(highlightbackground='light grey')
            x, y = self.game.board.find_worker_coords(str(self.selected_worker))
            self.buttons[(x, y)].config(highlightbackground='dark blue')
            possible_builds = []
            #print(self.temp_copy_game.curr_player_to_move)
            self.temp_copy_game.board.enumerate_all_available_moves(self.temp_copy_game.curr_player_to_move)
            for move in self.temp_copy_game.board.enumerate_all_available_moves(self.temp_copy_game.curr_player_to_move):
                #print(self.selected_worker)
                #print(self.selected_move)
                #print(move)
                #print(self.game.board)
                #print(self.temp_copy_game.board)
                if str(move[0]) == str(self.selected_worker) and str(move[1]) == str(self.selected_move):
                    possible_builds.append(move)
           # print(possible_builds)
            possible_build_directions = {move[2] for move in possible_builds}
            for direction in possible_build_directions:
                new_x, new_y = self.temp_copy_game.board.find_new_coords(self.selected_move_coord[0], self.selected_move_coord[1], direction) 
                if 0 <= new_x < 5 and 0 <= new_y < 5:  
                    self.buttons[(new_x, new_y)].config(highlightbackground='light blue')
        elif self._move_retrieve_state == "comp_build":
            self.clear_highlights()

    def clear_highlights(self):
        """Clears all highlights on the board."""
        for button in self.buttons.values():
            button.config(highlightbackground='light grey')

    
    def handle_click(self, i, j):
        square = self.game.board.squares[i][j]
        if self._move_retrieve_state == "select_player":
            if str(square.worker) in [worker for worker in self.current_possible_workers()]:
                self.selected_worker = square.worker
                self._move_retrieve_state = "select_move"
                self.update_button_highlights() 
                self.gui._move_retrieve_updates.update_label(f"You selected: {str(square.worker)}")
            else:
                self.gui._move_retrieve_updates.update_label("Invalid selection. For your convinience, players that you can move are highlighted in blue.")

        elif self._move_retrieve_state == "select_move":
            possible_moves = []
            for move in self.game.board.enumerate_all_available_moves(self.game.curr_player_to_move):
                if str(move[0]) == str(self.selected_worker):
                    possible_moves.append(move)
            possible_directions = list({move[1] for move in possible_moves})
            possible_new_coords = []
            for direction in possible_directions:
                x, y = self.game.board.find_worker_coords(str(self.selected_worker))  
                new_x, new_y = self.game.board.find_new_coords(x, y, direction) 
                possible_new_coords.append((new_x,new_y))
            #print(possible_directions)
            #print(possible_new_coords)
            if (i,j) in possible_new_coords:
                index = possible_new_coords.index((i,j))
                #print(possible_directions[index])
                self.selected_move = possible_directions[index]
                self.selected_move_coord = possible_new_coords[index]
                self._move_retrieve_state = "select_build"
                self.update_button_highlights()
                self.gui._move_retrieve_updates.update_label(f"You moved: {possible_directions[index]}")
                self.temp_copy_game = copy.deepcopy(self.game)
                self.game.move_worker(str(self.selected_worker), self.selected_move)


                self._move_retrieve_state = "select_build"
                self.create_grid() 
            else:
                self.gui._move_retrieve_updates.update_label("Invalid move. For your convinience, directions where you can build are highlighted in light blue.")

        elif self._move_retrieve_state == "select_build":
            possible_builds = []
            for move in self.temp_copy_game.board.enumerate_all_available_moves(self.temp_copy_game.curr_player_to_move):
                if str(move[0]) == str(self.selected_worker) and str(move[1]) == str(self.selected_move):
                    possible_builds.append(move)
            possible_directions = list({move[2] for move in possible_builds})
            possible_new_coords = []
            for direction in possible_directions:
                new_x, new_y = self.temp_copy_game.board.find_new_coords(self.selected_move_coord[0], self.selected_move_coord[1], direction) 
                possible_new_coords.append((new_x,new_y))
            if (i,j) in possible_new_coords:
                index = possible_new_coords.index((i,j))
                self.selected_build = possible_directions[index]
                #print(self.selected_build)

                self.game.build(str(self.selected_worker), self.selected_build)
                if self.game.check_win():
                    winner = self.game.check_win()
                    #self._disable_buttons()  
                    messagebox.showinfo("Game Over", f"{winner} wins!")
                    self.gui._window.quit() 
                    return 
                self.game.next_turn()
                #print(self.game.cur_player_object.type)
                self._move_retrieve_state = "select_player"
                if self.game.cur_player_object.type != "human": 
                    self._move_retrieve_state = "comp_build"
                    self.clear_highlights()
                    self.game.cur_player_object.play_turn(self.game, self)
                    #time.sleep(1)
                    self.game.next_turn()
                self.gui._game_info_frame.update_info()
                self._move_retrieve_state = "select_player"
                self.temp_copy_game = copy.deepcopy(self.game)
                self.gui._move_retrieve_updates.update_label(f"Select worker to move. Your available workers are highlighted in yellow.")
                self.create_grid()
                self.update_button_highlights()
            else:
                self.gui._move_retrieve_updates.update_label(f"Invalid selection. For your convinience, directions where you can build are highlighted in light blue.")

    def current_possible_workers(self):
        """Retrieve a list of the current player's workers that can legally move."""
        return {str(move[0]) for move in self.game.board.enumerate_all_available_moves(self.game.curr_player_to_move)}

class GameInfoFrame(tk.Frame):
    def __init__(self, parent, game, gui, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.game = game
        self.gui = gui
        self.configure(bg='white', relief=tk.RAISED, borderwidth=2)
        
        self.move_label = tk.Label(self, text="Move: 0", bg='white', font=('Helvetica', 12))
        self.move_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.player_label = tk.Label(self, text="Player: ", bg='white', font=('Helvetica', 12))
        self.player_label.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.update_info()

    def update_info(self):
        """Update the information displayed in the frame."""
        #print("UPDATING")
        self.game = self.gui.game
        self.move_label.config(text=f"Move: {self.game.turn_amount}")
        self.player_label.config(text=f"Player: {self.game.curr_player_to_move}")

class GameMoveUpdates(tk.Frame):
    def __init__(self, parent, game, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.game = game
        self.configure(bg='white', relief=tk.RAISED, borderwidth=0)
        self._update_label = tk.Label(self, text="Select worker to move. Your available workers are highlighted in blue.", bg='white', font=('Helvetica', 12))
        self._update_label.pack(side=tk.LEFT, padx=10, pady=10)

    def update_label(self, message):
        self._update_label.config(text=message)


class GameOverFrame(tk.Frame):
    def __init__(self, parent, game, type1, type2, gui, bg="white"):
        super().__init__(parent, bg=bg)
        self.game = game
        self.gui = gui
        self.parent = parent
        self.hidden = True
        self.is_built = False 
        self.type1 = type1
        self.type2 = type2

    def build_frame(self):
        if not self.is_built:
            self.pack(fill=tk.BOTH, expand=True)
            self.label = tk.Label(self, text="", font=("MS Reference Specialty", 16), bg=self["background"])
            self.label.pack(pady=20)

            self.play_again_button = tk.Button(self, text="MS Reference Specialty", command=self.reset_game, font=("MS Reference Specialty", 14))
            self.play_again_button.pack(pady=10)

            self.quit_button = tk.Button(self, text="Quit", command=self.parent.quit, font=("Helvetica", 14))
            self.quit_button.pack(pady=10)

            self.is_built = True
        self.hide()

    def display_winner(self, winner_name):
        if not self.is_built:
            self.build_frame()
        self.label.config(text=f"Congratulations, {winner_name} wins!")
        self.show()

    def reset_game(self):
        self.hide()
        self.gui.game = Game(self.type1, self.type2)
        self.gui._game_info_frame.update_info()
        self.gui._board.create_grid_gui()     

    def show(self):
        if self.hidden:
            self.pack(fill=tk.BOTH, expand=True)
            self.hidden = False

    def hide(self):
        if not self.hidden:
            self.pack_forget()
            self.hidden = True
