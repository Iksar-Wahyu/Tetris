import pygame
import sys
from game import TetrisGame  # Mengimpor logika utama game dari file eksternal
from colors import Colors  # Mengimpor kelas warna untuk digunakan di UI
from connect import Leaderboard  # Mengimpor koneksi leaderboard untuk database

# Inisialisasi koneksi leaderboard
leaderboard = Leaderboard(
    host="localhost",
    user="root",
    password="",
    database="tetris"   # Nama database yang digunakan
)

# Kelas dasar untuk UI Game (Contoh Inheritance)
class GameUI:
    def __init__(self):
        # Memulai encapsulation untuk atribut UI dasar
        self.screen = pygame.display.set_mode((500, 620))  # Ukuran layar
        pygame.display.set_caption("Python Tetris")  # Judul jendela
        self.clock = pygame.time.Clock()  # Mengatur kecepatan frame
        self.state = "MENU"  # Status awal UI
        self.fonts = {
            "title": pygame.font.Font(None, 50),
            "menu": pygame.font.Font(None, 40),
            "score": pygame.font.Font(None, 30),
        }
        self.fall_speed = 400  # Kecepatan jatuh awal dalam milidetik
        self.background_color = Colors.dark_blue  # Warna latar belakang default

    # Metode yang harus diimplementasikan oleh subclass (Contoh Polymorphism dimulai)
    def draw(self):
        raise NotImplementedError("Subclasses must implement this method")

    # Metode untuk menangani event, diimplementasikan di subclass (Polymorphism dimulai)
    def handle_event(self, event):
        raise NotImplementedError("Subclasses must implement this method")

# UI untuk game Tetris (Contoh Inheritance dimulai)
class TetrisUI(GameUI):
    def __init__(self):
        super().__init__()  # Memanggil constructor dari kelas dasar
        self.reset_game()  # Memulai ulang game saat UI diinisialisasi

    def reset_game(self):
        """Mengatur ulang game ke keadaan awal."""
        # Memulai encapsulation dengan membuat instance TetrisGame
        self.game = TetrisGame()  # Logika game dikapsulasi dalam TetrisGame
        self.player_name = ""  # Nama pemain kosong di awal
        self.input_active = True  # Status input aktif
        self.surfaces = {
            "score": self.fonts["title"].render("Score", True, Colors.white),
            "next": self.fonts["title"].render("Next", True, Colors.white),
            "game_over": self.fonts["title"].render("GAME OVER", True, Colors.red),
            "menu": self.fonts["title"].render("Python Tetris", True, Colors.white),
            "start": self.fonts["menu"].render("Press ENTER to Start", True, Colors.white),
            "quit": self.fonts["menu"].render("Press ESC to Quit", True, Colors.white),
        }

        self.update_fall_speed_and_color()  # Perbarui kecepatan jatuh dan warna latar
        pygame.time.set_timer(pygame.USEREVENT, self.fall_speed)  # Mengatur kecepatan jatuh awal

    def update_fall_speed_and_color(self):
        """Memperbarui kecepatan jatuh balok dan warna latar belakang berdasarkan skor."""
        # Encapsulation: logika penyesuaian berdasarkan skor dikapsulasi dalam metode ini
        if self.game.score >= 6000:
            self.fall_speed = 150
            self.background_color = Colors.red
        elif self.game.score >= 4000:
            self.fall_speed = 200
            self.background_color = Colors.green
        elif self.game.score >= 2000:
            self.fall_speed = 300
            self.background_color = Colors.light_blue
        else:
            self.fall_speed = 400
            self.background_color = Colors.dark_blue

        pygame.time.set_timer(pygame.USEREVENT, self.fall_speed)

    # Polymorphism: Mengimplementasikan metode `draw` dari kelas dasar
    def draw(self):
        self.screen.fill(self.background_color)  # Membersihkan layar dengan warna latar

        if self.state == "MENU":
            # Gambar elemen menu utama
            self.screen.blit(self.surfaces["menu"], self.surfaces["menu"].get_rect(center=(250, 200)))
            self.screen.blit(self.surfaces["start"], self.surfaces["start"].get_rect(center=(250, 300)))
            self.screen.blit(self.surfaces["quit"], self.surfaces["quit"].get_rect(center=(250, 350)))
        
        elif self.state == "GAME":
            # Gambar elemen UI saat permainan berlangsung
            score_value_surface = self.fonts["title"].render(str(self.game.score), True, Colors.white)
            self.screen.blit(self.surfaces["score"], (365, 20))
            self.screen.blit(self.surfaces["next"], (375, 180))
            pygame.draw.rect(self.screen, Colors.light_blue, pygame.Rect(320, 55, 170, 60), 0, 10)
            self.screen.blit(score_value_surface, score_value_surface.get_rect(center=(405, 85)))
            pygame.draw.rect(self.screen, Colors.light_blue, pygame.Rect(320, 215, 170, 180), 0, 10)
            self.game.draw(self.screen)  # Memanggil metode `draw` dari logika game
        
        elif self.state == "GAME_OVER":
            # Gambar elemen UI untuk layar game over
            self.screen.blit(self.surfaces["game_over"], self.surfaces["game_over"].get_rect(center=(250, 100)))
            final_score_surface = self.fonts["menu"].render(f"Your Score: {self.game.score}", True, Colors.white)
            self.screen.blit(final_score_surface, final_score_surface.get_rect(center=(250, 160)))

            input_surface = self.fonts["menu"].render(f"Name: {self.player_name}", True, Colors.white)
            pygame.draw.rect(self.screen, Colors.light_blue, pygame.Rect(120, 200, 260, 50), 0, 10)
            self.screen.blit(input_surface, input_surface.get_rect(center=(250, 225)))

            high_scores = leaderboard.get_top_scores(limit=10)  # Ambil skor tertinggi dari database
            y_offset = 280  # Posisi awal untuk menampilkan skor tinggi
            for rank, (player_name, score) in enumerate(high_scores, start=1):
                score_surface = self.fonts["score"].render(f"{rank}. {player_name} - {score}", True, Colors.white)
                self.screen.blit(score_surface, (150, y_offset))
                y_offset += 30

            if self.input_active:
                save_surface = self.fonts["menu"].render("Press ENTER to Save", True, Colors.white)
            else:
                save_surface = self.fonts["menu"].render("Press ESC to Restart", True, Colors.white)
            self.screen.blit(save_surface, save_surface.get_rect(center=(250, y_offset + 20)))
        
        pygame.display.update()

    # Polymorphism: Mengimplementasikan metode `handle_event` dari kelas dasar
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if self.state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = "GAME"  # Mulai permainan
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        elif self.state == "GAME":
            if self.game.game_over:
                self.state = "GAME_OVER"
                self.input_active = True  # Aktifkan input untuk nama
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.game.move_right()
                elif event.key == pygame.K_DOWN:
                    self.game.move_down()
                elif event.key == pygame.K_UP:
                    self.game.rotate()
                elif event.key == pygame.K_SPACE:
                    self.game.fall_down()
            elif event.type == pygame.USEREVENT:
                self.game.move_down()  # Gerakan balok otomatis
                self.update_fall_speed_and_color()  # Perbarui kecepatan dan warna

        elif self.state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.unicode.isalnum() and len(self.player_name) < 10:
                        self.player_name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_RETURN and self.player_name:
                        leaderboard.add_score(self.player_name, self.game.score)  # Simpan skor ke database
                        self.input_active = False  # Nonaktifkan input setelah menyimpan
                else:
                    if event.key == pygame.K_RETURN:  # Mulai ulang game
                        self.reset_game()
                        self.state = "GAME"
                    elif event.key == pygame.K_ESCAPE:  # Kembali ke menu
                        self.reset_game()
                        self.state = "MENU"

# Main loop
if __name__ == "__main__":
    pygame.init()
    tetris_ui = TetrisUI()
    while True:
        for event in pygame.event.get():
            tetris_ui.handle_event(event)
        tetris_ui.draw()
        tetris_ui.clock.tick(60)
