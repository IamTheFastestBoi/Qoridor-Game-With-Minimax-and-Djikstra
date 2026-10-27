import copy
import random
import sys
import pygame
class Board:
    def initialize_board(self):
        self.board = []
        self.first_row = []
        self.last_row = []
        for z in range(1):
            for i in range(17):
                if i % 2 == 0:
                    self.first_row.append(3)
                if i % 2 == 1:
                    self.first_row.append(1)
        self.board.append(self.first_row)
        for k in range(15):
            self.row = []
            if k % 2 == 0:
                for i in range(17):
                    if i % 2 == 0:
                        self.row.append(0)
                    if i % 2 == 1:
                        self.row.append(1)
                self.board.append(self.row)
            if k % 2 == 1:
                for i in range(17):
                    self.row.append(1)
                self.board.append(self.row)
        for i in range(1):
            for l in range(17):
                if l % 2 == 0:
                    self.last_row.append(4)
                if l % 2 == 1:
                    self.last_row.append(1)
            self.board.append(self.last_row)
        self.board[1][8] = 6
        self.board[15][8] = 5
        return self.board

# pc = 5
# player = 6
# wall = 2
# empty non space = 1
# moveable space = 0
# target space for pc = 3
# target space for player = 4
    
class PC:
    def __init__(self , board  ,current_position = (8 , 0) , current_player_position = (8 , 16) , pc_walls = 10 , player_walls = 10):
        self.pc_walls = pc_walls
        self.player_walls = player_walls
        self.board = board
        self.current_position = current_position
        self.current_player_position = current_player_position
        self.previous_positions = []
    def virtual_djikstra(self , current_position , target_value=3):
        if target_value == 3:
            self.successfull_PC_routes = []
        else:
            self.successfull_player_routes = []
        explored_positions = set()
        last_pos = self.previous_positions[-1] if len(self.previous_positions) > 0 else None
        current_spys = [{"position" : current_position , "step" : 0 , "previous_position" : last_pos , "path" : []}]
        while current_spys:
            current_spy = current_spys.pop(0)
            current_position = current_spy["position"]
            current_step = current_spy["step"]
            current_path = current_spy["path"]
            if self.board[current_position[0]][current_position[1]] == target_value:
                clean_route = []
                for pos in current_path:
                    if self.board[pos[0]][pos[1]] in [0, 3, 4, 5, 6]:
                        clean_route.append(pos)
                if target_value == 3:
                    self.successfull_PC_routes.append(clean_route)
                if target_value == 4:
                    self.successfull_player_routes.append(clean_route)
                continue

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                if self.board[current_position[0]][current_position[1]] in [0,5,6]:
                    new_position = (current_position[0] + dx, current_position[1] + dy)
                    if 0 <= new_position[0] < len(self.board) and 0 <= new_position[1] < len(self.board[0]):
                        is_passable = (self.board[new_position[0]][new_position[1]] == 1 or self.board[new_position[0]][new_position[1]] == 3 or self.board[new_position[0]][new_position[1]] == 4 or self.board[new_position[0]][new_position[1]] == 5 or self.board[new_position[0]][new_position[1]] == 6)
                        if is_passable:
                            if new_position not in current_path and new_position != self.current_position and new_position != self.current_player_position and new_position not in explored_positions:
                                new_path = current_path + [new_position]
                                explored_positions.add(new_position)
                                current_spys.append({"position": new_position, "step": current_step + 1, "previous_position": current_spy["position"], "path": new_path})
                if self.board[current_position[0]][current_position[1]] in [1 , 5, 6]:
                    new_position = (current_position[0] + dx, current_position[1] + dy)
                    if 0 <= new_position[0] < len(self.board) and 0 <= new_position[1] < len(self.board[0]):
                        is_passable = (self.board[new_position[0]][new_position[1]] == 0 or self.board[new_position[0]][new_position[1]] == 3 or self.board[new_position[0]][new_position[1]] == 4 or self.board[new_position[0]][new_position[1]] == 5 or self.board[new_position[0]][new_position[1]] == 6)
                        if is_passable:
                            if new_position not in current_path:
                                new_path = current_path + [new_position]
                                explored_positions.add(new_position)
                                current_spys.append({"position": new_position, "step": current_step + 1, "previous_position": current_spy["position"], "path": new_path})
        target_routes = self.successfull_PC_routes if target_value == 3 else self.successfull_player_routes
        if not target_routes:
            return []
        target_routes.sort(key=len)
        return target_routes[0]
    def virtual_find_anchors(self , pc = True , player = False):
        self.virtual_zero_positions = []
        if pc:
            for route in self.virtual_djikstra(self.current_player_position , target_value=4):
                if self.board[route[0]][route[1]] == 0:
                    self.virtual_zero_positions.append(route)
        if player:
            for route in self.virtual_djikstra(self.current_position , target_value=3):
                if self.board[route[0]][route[1]] == 0:
                    self.virtual_zero_positions.append(route)
        self.anchors = set()
        for zero in self.virtual_zero_positions:
            if  0 <= zero[0] - 1 < len(self.board) and 0 <= zero[1] -1 < len(self.board[0]):
                self.anchors.add( (zero[0] - 1, zero[1] - 1) )
            if 0 <= zero[0] - 1 < len(self.board) and 0 <= zero[1] + 1 < len(self.board[0]):
                self.anchors.add( (zero[0] - 1, zero[1] + 1) )
            if 0 <= zero[0] + 1 < len(self.board) and 0 <= zero[1] - 1 < len(self.board[0]):
                self.anchors.add( (zero[0] + 1, zero[1] - 1) )
            if 0 <= zero[0] + 1 < len(self.board) and 0 <= zero[1] + 1 < len(self.board[0]):
                self.anchors.add( (zero[0] + 1, zero[1] + 1) )
    def minimax(self, depth = 0 , alpha = float('-inf') , beta = float('inf') , turn = "PC" , original_way = None , original_number_of_pc_walls = None):
        best_action= None
        if depth == 0:
            original_route = self.virtual_djikstra(self.current_player_position , target_value=4)
            original_way = len(original_route) if original_route else 999
            original_number_of_pc_walls = self.pc_walls

        if depth == 4:
            route_pc = self.virtual_djikstra(self.current_position , target_value=3)
            pc_route_len = len(route_pc) if self.successfull_PC_routes else float('inf')
            route_player = self.virtual_djikstra(self.current_player_position , target_value=4)
            player_route_len = len(route_player) if self.successfull_player_routes else float('inf')
            delta_way = player_route_len - original_way
            spent_walls = original_number_of_pc_walls - self.pc_walls
            expected_increase = spent_walls * 2
            extra_bonus = max(0 , delta_way - expected_increase)
            trap_bonus = extra_bonus * 10
            return (player_route_len - pc_route_len) + (self.pc_walls * 2.5) + trap_bonus

            
            
        if turn == "PC":
            best_score = float('-inf')
            pc_moves = [["move"] ]
            prunned = False
            if self.pc_walls > 0:
                pc_moves.extend([["wall" , "h"] , ["wall" , "v"]])
            for pc_move in pc_moves:
                if prunned:
                    break
                if pc_move[0] == "move":
                    route_pc = self.virtual_djikstra(self.current_position  , target_value=3)

                    route = route_pc if route_pc else None
                    if route:
                        move = route[0] 
                        old_pos = self.current_position
                        self.board[old_pos[0]][old_pos[1]] = 0
                        self.board[move[0]][move[1]] = 5
                        self.current_position = move
                        score = self.minimax(depth + 1, alpha , beta , turn="player" , original_way = original_way , original_number_of_pc_walls = original_number_of_pc_walls)
                        self.board[move[0]][move[1]] = 0
                        self.board[old_pos[0]][old_pos[1]] = 5
                        self.current_position = old_pos
                        if score > best_score:
                            best_score = score
                            alpha = max(alpha, best_score)
                            if alpha >= beta:
                                prunned = True
                                break
                            best_action= ( "move" , move)
                elif pc_move[0] == "wall":
                    orientation = pc_move[1]
                    self.virtual_find_anchors(pc=True, player=False)
                    for anchor in list(self.anchors):
                        y, x = anchor
                            
                        if orientation == "h":
                            if 0 <= x-1 and x+1 < len(self.board[0]):
                                if self.board[y][x] == 1 and self.board[y][x-1] == 1 and self.board[y][x+1] == 1:
                                    self.board[y][x] = 2
                                    self.board[y][x-1] = 2
                                    self.board[y][x+1] = 2
                                    route_pc = self.virtual_djikstra(self.current_player_position , target_value=4)
                                    if not route_pc:
                                        self.board[y][x] = 1
                                        self.board[y][x-1] = 1
                                        self.board[y][x+1] = 1
                                        continue
                                    self.pc_walls -= 1
                                    score = self.minimax(depth + 1, alpha , beta , turn="player" , original_way = original_way , original_number_of_pc_walls = original_number_of_pc_walls)

                                    self.board[y][x] = 1
                                    self.board[y][x-1] = 1
                                    self.board[y][x+1] = 1
                                    self.pc_walls += 1
                                    if score >= best_score:
                                        best_score = score
                                        alpha = max(alpha, best_score)
                                        if alpha >= beta:
                                            prunned = True
                                            break
                                        best_action = ( "wall" , anchor, orientation)
                                
                        elif orientation == "v":
                            if 0 <= y-1 and y+1 < len(self.board):
                                if self.board[y][x] == 1 and self.board[y-1][x] == 1 and self.board[y+1][x] == 1:
                                    self.board[y][x] = 2
                                    self.board[y-1][x] = 2
                                    self.board[y+1][x] = 2
                                    route_pc = self.virtual_djikstra(self.current_player_position , target_value=4)
                                    if not route_pc:
                                        self.board[y][x] = 1
                                        self.board[y-1][x] = 1
                                        self.board[y+1][x] = 1
                                        continue
                                    self.pc_walls -= 1
                                    score = self.minimax(depth + 1, alpha, beta, turn="player" , original_way = original_way , original_number_of_pc_walls = original_number_of_pc_walls)

                                    self.board[y][x] = 1
                                    self.board[y-1][x] = 1
                                    self.board[y+1][x] = 1
                                    self.pc_walls += 1
                                    if score >= best_score:
                                        best_score = score
                                        alpha = max(alpha, best_score)
                                        if alpha >= beta:
                                            prunned = True
                                            break
                                        best_action = ( "wall" , anchor, orientation)
                        
        else:
            best_score = float('inf')
            player_moves = [["move"]]
            prunned = False
            if self.player_walls > 0:
                player_moves.extend([["wall" , "h"] , ["wall" , "v"]])
            for player_move in player_moves:
                if prunned:
                    break
                if player_move[0] == "move":
                    route_player = self.virtual_djikstra(self.current_player_position , target_value=4)
                    route = route_player if route_player else None
                    if route:
                        move = route[0] 
                        old_pos = self.current_player_position
                        self.board[old_pos[0]][old_pos[1]] = 0
                        self.board[move[0]][move[1]] = 6
                        self.current_player_position = move
                        score = self.minimax(depth + 1, alpha, beta, turn="PC" , original_way = original_way , original_number_of_pc_walls = original_number_of_pc_walls)
                        self.board[move[0]][move[1]] = 0
                        self.board[old_pos[0]][old_pos[1]] = 6
                        self.current_player_position = old_pos
                        if score < best_score:
                            best_score = score
                            beta = min(beta, best_score)
                            if alpha >= beta:
                                prunned = True
                                break

                elif player_move[0] == "wall":
                    orientation = player_move[1]
                    route_player = self.virtual_djikstra(self.current_position , target_value=3)
                    self.virtual_find_anchors(pc=False, player=True) 
                    for anchor in list(self.anchors):
                        y, x = anchor
                        
                        if orientation == "h":
                            if 0 <= x-1 and x+1 < len(self.board[0]):
                                if self.board[y][x] == 1 and self.board[y][x-1] == 1 and self.board[y][x+1] == 1:
                                    self.board[y][x] = 2
                                    self.board[y][x-1] = 2
                                    self.board[y][x+1] = 2
                                    route_player = self.virtual_djikstra(self.current_position , target_value=3)
                                    if not route_player:
                                        self.board[y][x] = 1
                                        self.board[y][x-1] = 1
                                        self.board[y][x+1] = 1
                                        continue
                                    self.player_walls -= 1
                                    score = self.minimax(depth + 1, alpha, beta, turn="PC" , original_way = original_way , original_number_of_pc_walls = original_number_of_pc_walls)

                                    self.board[y][x] = 1
                                    self.board[y][x-1] = 1
                                    self.board[y][x+1] = 1
                                    self.player_walls += 1
                                    if score <= best_score:
                                        best_score = score
                                        beta = min(beta, best_score)
                                        if alpha >= beta:
                                            prunned = True
                                            break
                                
                        elif orientation == "v":
                            if 0 <= y-1 and y+1 < len(self.board):
                                if self.board[y][x] == 1 and self.board[y-1][x] == 1 and self.board[y+1][x] == 1:
                                    self.board[y][x] = 2
                                    self.board[y-1][x] = 2
                                    self.board[y+1][x] = 2
                                    route_player = self.virtual_djikstra(self.current_position , target_value=3)
                                    if not route_player:
                                        self.board[y][x] = 1
                                        self.board[y-1][x] = 1
                                        self.board[y+1][x] = 1
                                        continue
                                    self.player_walls -= 1
                                    score = self.minimax(depth + 1, alpha, beta, turn="PC" , original_way = original_way , original_number_of_pc_walls = original_number_of_pc_walls)

                                    self.board[y][x] = 1
                                    self.board[y-1][x] = 1
                                    self.board[y+1][x] = 1
                                    self.player_walls += 1
                                    if score <= best_score:
                                        best_score = score
                                        beta = min(beta, best_score)
                                        if alpha >= beta:
                                            prunned = True
                                            break

    
        if depth == 0:           
            return best_action
        else:
            return best_score
    def make_move(self):
        print("PC is thinking...")
        best_action = self.minimax(depth=0, alpha=float('-inf'), beta=float('inf'), turn="PC" , original_way=None , original_number_of_pc_walls=self.pc_walls)
        if best_action and best_action[0] == "wall" and self.pc_walls <= 0:
            best_action = None
        if not best_action:
            print("No valid move found. Using virtual Dijkstra...")
            route_player = self.virtual_djikstra(self.current_position, target_value=3)
            if route_player and len(route_player) > 0:
                best_action = ("move", route_player[0])
        if best_action[0] == "move":
            move_position = best_action[1]
            self.board[self.current_position[0]][self.current_position[1]] = 0
            self.previous_positions.append(self.current_position)
            self.board[move_position[0]][move_position[1]] = 5
            self.current_position = move_position
            print(f"PC moved to {move_position}")
        elif best_action[0] == "wall":
            _ , anchor, orientation = best_action
            y, x = anchor
            if orientation == "h":
                self.board[y][x] = 2
                self.board[y][x-1] = 2
                self.board[y][x+1] = 2
                self.pc_walls -= 1
            elif orientation == "v":
                self.board[y][x] = 2
                self.board[y-1][x] = 2
                self.board[y+1][x] = 2
                self.pc_walls -= 1
            print(f"PC placed a {orientation} wall at {anchor}. Remaining walls: {self.pc_walls}")


# test the PC class
# board = Board()
# board_matrix = board.initialize_board()
# bot = PC(board = board_matrix , current_position = (15 , 8) , current_player_position = (1 , 8) , pc_walls = 10 , player_walls = 10)
# bot.make_move()

# =====================================================================
# 2. PYGAME and GUI Implementation , THIS PART WAS BUILT BY AI !!!
# =====================================================================

class QuoridorGUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Quoridor AI Engine")
        self.game_over = False
        

        self.SCREEN_WIDTH = 1240
        self.SCREEN_HEIGHT = 880
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()


        self.TILE_SIZE = 68       # 0 olan zemin karelerinin boyutu
        self.WALL_THICK = 16      # Duvar ve çapa kalınlığı
        self.GOAL_HEIGHT = 30     # 0. ve 16. hedef satırlarının yüksekliği
        self.OFFSET_X = 50
        self.OFFSET_Y = 50


        self.BG_COLOR = (24, 26, 32)
        self.BOARD_BG = (15, 16, 20)
        self.TILE_COLOR = (42, 46, 58)
        self.TILE_HOVER = (60, 66, 84)
        self.GROOVE_COLOR = (28, 30, 38)
        

        self.ANCHOR_COLOR = (48, 52, 65)
        self.ANCHOR_HOVER = (245, 158, 11)      # Turuncu vurgu
        self.ANCHOR_SELECTED = (239, 68, 68)   # Kırmızı seçim
        self.WALL_PLACED = (245, 158, 11)       # Yerleştirilmiş duvar

        self.GOAL_PC = (59, 130, 246, 120)     # Mavi
        self.GOAL_PLAYER = (16, 185, 129, 120) # Yeşil


        self.PLAYER_COLOR = (16, 185, 129)     # Zümrüt Yeşili (Player)
        self.PC_COLOR = (59, 130, 246)         # Safir Mavisi (PC)

        self.font_title = pygame.font.SysFont("Segoe UI, Arial", 26, bold=True)
        self.font_body = pygame.font.SysFont("Segoe UI, Arial", 18)
        self.font_small = pygame.font.SysFont("Segoe UI, Arial", 14)


        self.board_obj = Board()
        self.board = self.board_obj.initialize_board()
        self.bot = PC(
            board=self.board, 
            current_position=(15, 8), 
            current_player_position=(1, 8), 
            pc_walls=10, 
            player_walls=10
        )


        self.current_turn = "PLAYER"  # "PLAYER" veya "PC"
        self.mode = "MOVE"            # "MOVE" veya "WALL"
        self.selected_anchor = None   # (y, x)
        self.status_message = "Your turn. Press 'M' for Move, 'O' for Wall."

    def get_cell_rect(self, r, c):

        x = self.OFFSET_X
        for col_idx in range(c):
            if col_idx % 2 == 0:
                x += self.TILE_SIZE
            else:
                x += self.WALL_THICK

        # Y Hesabı
        y = self.OFFSET_Y
        for row_idx in range(r):
            if row_idx == 0 or row_idx == 16:
                y += self.GOAL_HEIGHT
            elif row_idx % 2 == 1:
                y += self.TILE_SIZE
            else:
                y += self.WALL_THICK


        w = self.TILE_SIZE if (c % 2 == 0) else self.WALL_THICK
        if r == 0 or r == 16:
            h = self.GOAL_HEIGHT
        else:
            h = self.TILE_SIZE if (r % 2 == 1) else self.WALL_THICK

        return pygame.Rect(x, y, w, h)

    def draw_board(self, mouse_pos):
        # Arka plan çerçevesi
        total_w = 9 * self.TILE_SIZE + 8 * self.WALL_THICK
        total_h = 2 * self.GOAL_HEIGHT + 8 * self.TILE_SIZE + 7 * self.WALL_THICK
        pygame.draw.rect(self.screen, self.BOARD_BG, (self.OFFSET_X - 10, self.OFFSET_Y - 10, total_w + 20, total_h + 20), border_radius=12)


        for r in range(17):
            for c in range(17):
                rect = self.get_cell_rect(r, c)
                val = self.board[r][c]


                if r % 2 == 1 and c % 2 == 0:
                    color = self.TILE_COLOR
                    if self.mode == "MOVE" and self.current_turn == "PLAYER":
                        if rect.collidepoint(mouse_pos):
                            color = self.TILE_HOVER
                    pygame.draw.rect(self.screen, color, rect, border_radius=6)


                elif r == 0 and c % 2 == 0:
                    pygame.draw.rect(self.screen, (30, 41, 59), rect, border_radius=4)
                elif r == 16 and c % 2 == 0:
                    pygame.draw.rect(self.screen, (20, 48, 40), rect, border_radius=4)


                elif r % 2 == 0 and c % 2 == 1 and 2 <= r <= 14:
                    color = self.ANCHOR_COLOR
                    if self.selected_anchor == (r, c):
                        color = self.ANCHOR_SELECTED
                    elif self.mode == "WALL" and rect.collidepoint(mouse_pos):
                        color = self.ANCHOR_HOVER
                    
                    if val == 2:
                        color = self.WALL_PLACED
                    pygame.draw.rect(self.screen, color, rect, border_radius=3)


                elif val == 1 or val == 2:
                    color = self.WALL_PLACED if val == 2 else self.GROOVE_COLOR
                    pygame.draw.rect(self.screen, color, rect, border_radius=2)


                if val == 6:  # Player
                    center = rect.center
                    pygame.draw.circle(self.screen, (10, 80, 50), center, self.TILE_SIZE // 2 - 6)
                    pygame.draw.circle(self.screen, self.PLAYER_COLOR, center, self.TILE_SIZE // 2 - 10)
                elif val == 5:  # PC
                    center = rect.center
                    pygame.draw.circle(self.screen, (20, 50, 100), center, self.TILE_SIZE // 2 - 6)
                    pygame.draw.circle(self.screen, self.PC_COLOR, center, self.TILE_SIZE // 2 - 10)

    def draw_hud(self):
        panel_x = 880
        panel_y = 50


        title = self.font_title.render("QUORIDOR ENGINE", True, (240, 240, 245))
        self.screen.blit(title, (panel_x, panel_y))


        turn_text = f"Turn: {'YOU (Player)' if self.current_turn == 'PLAYER' else 'PC (Thinking...)'}"
        turn_col = self.PLAYER_COLOR if self.current_turn == 'PLAYER' else self.PC_COLOR
        turn_surf = self.font_body.render(turn_text, True, turn_col)
        self.screen.blit(turn_surf, (panel_x, panel_y + 50))


        mode_box = pygame.Rect(panel_x, panel_y + 90, 310, 45)
        pygame.draw.rect(self.screen, (32, 35, 45), mode_box, border_radius=8)
        mode_label = f"CURRENT MODE:  {self.mode}"
        mode_col = (245, 158, 11) if self.mode == "WALL" else (16, 185, 129)
        self.screen.blit(self.font_body.render(mode_label, True, mode_col), (panel_x + 15, panel_y + 102))


        p_walls = self.font_body.render(f"Your Walls: {self.bot.player_walls} / 10", True, (220, 220, 230))
        pc_walls = self.font_body.render(f"PC Walls:   {self.bot.pc_walls} / 10", True, (220, 220, 230))
        self.screen.blit(p_walls, (panel_x, panel_y + 160))
        self.screen.blit(pc_walls, (panel_x, panel_y + 190))


        anchor_str = f"Selected Anchor: {self.selected_anchor if self.selected_anchor else 'None'}"
        self.screen.blit(self.font_body.render(anchor_str, True, (200, 200, 210)), (panel_x, panel_y + 240))
        if self.selected_anchor:
            hint = self.font_small.render("Press 'H' for Horizontal, 'V' for Vertical", True, (245, 158, 11))
            self.screen.blit(hint, (panel_x, panel_y + 270))


        status_box = pygame.Rect(panel_x, panel_y + 310, 310, 60)
        pygame.draw.rect(self.screen, (32, 35, 45), status_box, border_radius=8)
        status_surf = self.font_small.render(self.status_message, True, (180, 190, 205))
        self.screen.blit(status_surf, (panel_x + 10, panel_y + 330))


        guide_y = panel_y + 420
        self.screen.blit(self.font_title.render("CONTROLS", True, (160, 170, 185)), (panel_x, guide_y))
        
        controls = [
            ("M", "Move Mode (Click adjacent tile)"),
            ("O", "Obstacle Mode (Click anchor)"),
            ("H", "Place Horizontal Wall at Anchor"),
            ("V", "Place Vertical Wall at Anchor"),
            ("ESC", "Deselect Anchor")
        ]
        for idx, (k, desc) in enumerate(controls):
            txt = self.font_small.render(f"[{k}] - {desc}", True, (140, 150, 165))
            self.screen.blit(txt, (panel_x, guide_y + 40 + idx * 26))

    def handle_player_move(self, target_r, target_c):

        pr, pc = self.bot.current_player_position
        dr = target_r - pr
        dc = target_c - pc


        if (abs(dr) == 2 and dc == 0) or (abs(dc) == 2 and dr == 0):
            wall_r = pr + dr // 2
            wall_c = pc + dc // 2


            if self.board[wall_r][wall_c] == 2:
                self.status_message = "Blocked! A wall is in the way."
                return False


            self.board[pr][pc] = 0
            self.board[target_r][target_c] = 6
            self.bot.current_player_position = (target_r, target_c)
            self.status_message = f"Player moved to {(target_r, target_c)}"
            return True

        self.status_message = "Invalid move! Click an adjacent square."
        return False

    def handle_player_wall(self, orientation):

        if not self.selected_anchor:
            self.status_message = "Select an anchor square first!"
            return False
        if self.bot.player_walls <= 0:
            self.status_message = "No walls remaining! (Count: 0)"
            return False

        y, x = self.selected_anchor

        if orientation == "h":
            if 0 <= x - 1 and x + 1 < 17:
                # 1. Alan kontrolü: Seçilen yer boş mu?
                if not (self.board[y][x] == 1 and self.board[y][x - 1] == 1 and self.board[y][x + 1] == 1):
                    self.status_message = "Cannot place wall: Space is occupied!"
                    return False


                self.board[y][x] = 2
                self.board[y][x - 1] = 2
                self.board[y][x + 1] = 2


                route_player = self.bot.virtual_djikstra(self.bot.current_player_position, target_value=4)
                route_pc = self.bot.virtual_djikstra(self.bot.current_position, target_value=3)

                print(f"DEBUG: route_player len = {len(route_player)}, route_pc len = {len(route_pc)}")

                if not route_player or not route_pc:
                    # Yolu kapattığı için geri al
                    self.board[y][x] = 1
                    self.board[y][x - 1] = 1
                    self.board[y][x + 1] = 1
                    self.status_message = "Illegal wall! It blocks the path to the goal."
                    return False


                self.bot.player_walls -= 1
                self.selected_anchor = None
                self.status_message = f"Placed horizontal wall at {(y, x)}"
                return True

        elif orientation == "v":
            if 0 <= y - 1 and y + 1 < 17:
                if not (self.board[y][x] == 1 and self.board[y - 1][x] == 1 and self.board[y + 1][x] == 1):
                    self.status_message = "Cannot place wall: Space is occupied!"
                    return False

                self.board[y][x] = 2
                self.board[y - 1][x] = 2
                self.board[y + 1][x] = 2

                route_player = self.bot.virtual_djikstra(self.bot.current_player_position, target_value=4)
                route_pc = self.bot.virtual_djikstra(self.bot.current_position, target_value=3)

                print(f"DEBUG: route_player len = {len(route_player)}, route_pc len = {len(route_pc)}")

                if not route_player or not route_pc:
                    self.board[y][x] = 1
                    self.board[y - 1][x] = 1
                    self.board[y + 1][x] = 1
                    self.status_message = "Illegal wall! It blocks the path to the goal."
                    return False

                self.bot.player_walls -= 1
                self.selected_anchor = None
                self.status_message = f"Placed vertical wall at {(y, x)}"
                return True

        self.status_message = "Anchor already occupied or invalid!"
        return False
    def check_win(self):
        if self.bot.current_player_position[0] == 15:
            self.status_message = "🏆 YOU WIN! GAME OVER. 🏆"
            self.game_over = True
            self.current_turn = "NONE"
        elif self.bot.current_position[0] == 1:
            self.status_message = "💻 PC WINS! GAME OVER. 💻"
            self.game_over = True
            self.current_turn = "NONE"

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.mode = "MOVE"
                        self.status_message = "Mode: MOVE. Click adjacent tile."
                    elif event.key == pygame.K_o:
                        self.mode = "WALL"
                        self.status_message = "Mode: OBSTACLE. Click an anchor."
                    elif event.key == pygame.K_ESCAPE:
                        self.selected_anchor = None


                    elif self.mode == "WALL" and self.current_turn == "PLAYER":
                        if event.key == pygame.K_h:
                            if self.handle_player_wall("h"):
                                self.current_turn = "PC"
                        elif event.key == pygame.K_v:
                            if self.handle_player_wall("v"):
                                self.current_turn = "PC"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.current_turn == "PLAYER":
                        # Tıklanan hücreyi bul
                        for r in range(17):
                            for c in range(17):
                                rect = self.get_cell_rect(r, c)
                                if rect.collidepoint(mouse_pos):
                                    if self.mode == "MOVE" and r % 2 == 1 and c % 2 == 0:
                                        if self.handle_player_move(r, c):
                                            self.current_turn = "PC"
                                    elif self.mode == "WALL" and r % 2 == 0 and c % 2 == 1 and 2 <= r <= 14:
                                        self.selected_anchor = (r, c)
                                        self.status_message = f"Anchor {(r, c)} selected. Press H or V."


            self.screen.fill(self.BG_COLOR)
            self.draw_board(mouse_pos)
            self.draw_hud()
            pygame.display.flip()


            if self.current_turn == "PC":
                pygame.time.wait(300)  
                self.bot.make_move()
                self.current_turn = "PLAYER"
                self.status_message = "Your turn."
                self.check_win()  

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = QuoridorGUI()
    game.run()

                    





   





            
            
    
        



            








        





