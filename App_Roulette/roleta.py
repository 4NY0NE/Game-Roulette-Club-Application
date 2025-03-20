# ======================================================#
#         ___  _   _ __   __ _____  _   _  _____ 
#        /   || \ | |\ \ / /|  _  || \ | ||  ___|
#       / /| ||  \| | \ V / | | | ||  \| || |__
#      / /_| || . ` |  \ /  | | | || . ` ||  __|
#      \___  || |\  |  | |  \ \_/ /| |\  || |___
#          |_/\_| \_/  \_/   \___/ \_| \_/\____/
#     Follow me on github: https://github.com/4NY0NE                                    
# ======================================================#

import sys
import random
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QListWidget, QLineEdit, QInputDialog,
    QMessageBox, QColorDialog
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QTimer, QSettings

class RouletteWidget(QWidget):
    def __init__(self, category, games, user_text_color="green"):
        super().__init__()
        self.category = category
        self.games = games
        
        self.layout = QVBoxLayout()
        self.label = QLabel(f"Roleta {category}")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(f"color: {user_text_color};")
        self.layout.addWidget(self.label)
        
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.games)
        self.layout.addWidget(self.list_widget)
        
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Adicionar novo jogo")
        self.entry.returnPressed.connect(self.add_game)
        self.layout.addWidget(self.entry)
        
        self.add_button = QPushButton("Adicionar Jogo")
        self.add_button.clicked.connect(self.add_game)
        self.layout.addWidget(self.add_button)
        
        self.remove_button = QPushButton("Remover Selecionado")
        self.remove_button.clicked.connect(self.remove_game)
        self.layout.addWidget(self.remove_button)
        
        self.spin_button = QPushButton("Girar Roleta")
        self.spin_button.clicked.connect(self.spin_roulette)
        self.layout.addWidget(self.spin_button)
        
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet(f"color: {user_text_color};")
        self.layout.addWidget(self.result_label)
        
        self.setLayout(self.layout)
    
    def updateUserTextColor(self, color):
        """Atualiza a cor dos textos (título e resultado)."""
        self.label.setStyleSheet(f"color: {color};")
        self.result_label.setStyleSheet(f"color: {color};")
    
    def add_game(self):
        new_game = self.entry.text().strip()
        if new_game:
            self.list_widget.addItem(new_game)
            self.entry.clear()
    
    def remove_game(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            self.list_widget.takeItem(self.list_widget.row(selected_item))
    
    def spin_roulette(self):
        if self.list_widget.count() == 0:
            QMessageBox.warning(self, "Aviso", "Nenhum jogo na lista!")
            return
        
        self.spin_list = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        self.current_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_spin)
        self.timer.start(100)
        self.spin_duration = 20

    def animate_spin(self):
        if self.spin_duration > 0:
            self.result_label.setText(f"Sorteando: {self.spin_list[self.current_index]}")
            self.current_index = (self.current_index + 1) % len(self.spin_list)
            self.spin_duration -= 1
        else:
            self.timer.stop()
            chosen_game = random.choice(self.spin_list)
            self.result_label.setText(f"{chosen_game}")

class ClubTab(QWidget):
    def __init__(self, user_text_color="green"):
        super().__init__()
        self.user_text_color = user_text_color
        self.layout = QVBoxLayout()
        self.label = QLabel("Clube dos Jogos")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(f"color: {self.user_text_color};")
        self.layout.addWidget(self.label)

        self.players_list = QListWidget()
        self.layout.addWidget(self.players_list)

        add_player_layout = QHBoxLayout()
        self.player_entry = QLineEdit()
        self.player_entry.setPlaceholderText("Adicionar novo jogador")
        self.player_entry.returnPressed.connect(self.add_player)
        add_player_layout.addWidget(self.player_entry)
        self.add_player_button = QPushButton("Adicionar Jogador")
        self.add_player_button.clicked.connect(self.add_player)
        add_player_layout.addWidget(self.add_player_button)
        self.layout.addLayout(add_player_layout)

        self.remove_player_button = QPushButton("Remover Jogador Selecionado")
        self.remove_player_button.clicked.connect(self.remove_player)
        self.layout.addWidget(self.remove_player_button)

        self.sort_button = QPushButton("Sortear Clube")
        self.sort_button.clicked.connect(self.sort_club)
        self.layout.addWidget(self.sort_button)

        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet(f"color: {self.user_text_color};")
        self.layout.addWidget(self.result_label)
        
        self.setLayout(self.layout)
        self.is_club_tab = True

        self.club_sort_callback = None

    def updateUserTextColor(self, color):
        self.user_text_color = color
        self.label.setStyleSheet(f"color: {color};")
        self.result_label.setStyleSheet(f"color: {color};")
    
    def add_player(self):
        name = self.player_entry.text().strip()
        if name:
            self.players_list.addItem(name)
            self.player_entry.clear()
    
    def remove_player(self):
        selected_item = self.players_list.currentItem()
        if selected_item:
            self.players_list.takeItem(self.players_list.row(selected_item))
    
    def sort_club(self):
        if self.club_sort_callback and callable(self.club_sort_callback):
            self.club_sort_callback()
        else:
            QMessageBox.information(self, "Clube dos Jogos", "Função de sorteio não configurada.")
    
    def get_players(self):
        return [self.players_list.item(i).text() for i in range(self.players_list.count())]
    
    def set_result(self, text):
        self.result_label.setText(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roleta de Jogos")
        self.setGeometry(100, 100, 600, 600)
        self.setWindowIcon(QIcon("app_icon.ico"))
        
        self.settings = QSettings("MyCompany", "RoletaDeJogos")
        
        self.user_color = self.settings.value("user_color", "#2c7")
        self.user_text_color = self.settings.value("user_text_color", "green")
        
        self.update_global_styles()
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.update_tab_style()
        
        self.club_tab = ClubTab(user_text_color=self.user_text_color)
        self.club_tab.club_sort_callback = self.perform_club_sort
        self.tabs.addTab(self.club_tab, "Clube dos Jogos")
        
        if self.settings.contains("roletas"):
            roletas_json = self.settings.value("roletas")
            try:
                roletas_data = json.loads(roletas_json)
            except Exception:
                roletas_data = None
            if roletas_data and isinstance(roletas_data, list) and len(roletas_data) > 0:
                for roleta in roletas_data:
                    self.add_tab(roleta["category"], roleta["games"])
            else:
                self.load_default_roletas()
        else:
            self.load_default_roletas()
        
        self.top_buttons_container = QWidget()
        top_layout = QHBoxLayout(self.top_buttons_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        self.new_tab_button = QPushButton("Adicionar Nova Roleta")
        self.new_tab_button.clicked.connect(self.add_new_tab)
        top_layout.addWidget(self.new_tab_button)
        
        self.delete_tab_button = QPushButton("Excluir Roleta")
        self.delete_tab_button.clicked.connect(self.delete_current_tab)
        top_layout.addWidget(self.delete_tab_button)
        
        self.rename_tab_button = QPushButton("Renomear Roleta")
        self.rename_tab_button.clicked.connect(self.rename_current_tab)
        top_layout.addWidget(self.rename_tab_button)
        
        self.user_color_button = QPushButton("Mudar Cor do Usuário")
        self.user_color_button.clicked.connect(self.change_user_color)
        top_layout.addWidget(self.user_color_button)
        
        self.text_color_button = QPushButton("Mudar Cor dos Textos")
        self.text_color_button.clicked.connect(self.change_text_color)
        top_layout.addWidget(self.text_color_button)
        
        self.tabs.setCornerWidget(self.top_buttons_container, Qt.Corner.TopRightCorner)
        
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
    
    def load_default_roletas(self):
        """Carrega as roletas padrão (15 categorias com 20 jogos cada)."""
        self.game_categories = {
            "RPG": ["Skyrim", "The Witcher 3", "Final Fantasy VII", "Dark Souls", "Dragon Age", "Cyberpunk 2077", "Persona 5", "Divinity: Original Sin 2", "Elden Ring", "Bloodborne", "Baldur's Gate 3", "Octopath Traveler", "Diablo IV", "Kingdom Hearts", "Mass Effect 2", "Nier Automata", "Planescape Torment", "Starfield", "Tales of Arise", "Chrono Trigger"],
            "Ação": ["DOOM", "God of War", "Devil May Cry 5", "Horizon Zero Dawn", "Sekiro", "Hades", "Ghost of Tsushima", "Control", "Dead Cells", "Bayonetta", "Resident Evil 4", "Nioh", "Metal Gear Rising", "Returnal", "The Last of Us", "Uncharted", "Bloodborne", "Cuphead", "Hollow Knight", "Shadow of Mordor"],
            "Estratégia": ["Age of Empires IV", "Total War: Warhammer 3", "Civilization VI", "StarCraft II", "XCOM 2", "Crusader Kings III", "Anno 1800", "Company of Heroes 3", "Warcraft III", "Europa Universalis IV", "Frostpunk", "Hearts of Iron IV", "Tropico 6", "Cities: Skylines", "RimWorld", "Factorio", "Surviving Mars", "The Settlers", "Rise of Nations", "Command & Conquer"],
            "Terror": ["Resident Evil Village", "Silent Hill 2", "Outlast", "Amnesia: The Dark Descent", "Dead Space", "The Evil Within", "Alien: Isolation", "Layers of Fear", "Phasmophobia", "Fatal Frame", "Dying Light", "SOMA", "Observer", "Until Dawn", "Darkwood", "Slender: The Arrival", "Little Nightmares", "F.E.A.R.", "Tormented Souls", "Ghostwire: Tokyo"],
            "Esporte": ["FIFA 23", "NBA 2K23", "Madden NFL 23", "MLB The Show 23", "PES 2021", "Rocket League", "Tony Hawk's Pro Skater", "SSX", "F1 2021", "WWE 2K22", "NHL 22", "NBA Live 19", "FIFA Street", "Virtua Tennis 4", "Pro Evolution Soccer", "Madden NFL 22", "Rugby 20", "F1 2020", "Grid Legends", "Madden NFL 24"],
            "Simulação": ["The Sims 4", "Cities: Skylines", "Microsoft Flight Simulator", "Euro Truck Simulator 2", "Farming Simulator 22", "Planet Coaster", "Kerbal Space Program", "Train Simulator", "House Flipper", "SimCity", "RollerCoaster Tycoon", "Prison Architect", "Job Simulator", "Stardew Valley", "Animal Crossing", "Transport Fever 2", "Farming Simulator 19", "Surgeon Simulator", "Space Engineers", "PC Building Simulator"],
            "Corrida": ["Forza Horizon 5", "Need for Speed Heat", "Gran Turismo 7", "Project CARS 3", "F1 2021", "DiRT Rally 2.0", "Assetto Corsa", "Burnout Paradise", "MotoGP 21", "Grid Legends", "WRC 10", "Crash Team Racing Nitro-Fueled", "Sonic & All-Stars Racing Transformed", "Ridge Racer", "F1 2020", "Test Drive Unlimited", "Mario Kart 8", "Forza Motorsport 7", "Need for Speed Payback", "The Crew 2"],
            "Aventura": ["The Legend of Zelda: Breath of the Wild", "Uncharted 4", "Tomb Raider", "Assassin's Creed Odyssey", "Red Dead Redemption 2", "Shadow of the Colossus", "Journey", "God of War", "Horizon Zero Dawn", "Far Cry 5", "The Last Guardian", "Bioshock Infinite", "Control", "Batman: Arkham City", "Prince of Persia", "Metal Gear Solid", "Infamous", "Watch Dogs", "Just Cause 3", "Mad Max"],
            "Plataforma": ["Super Mario Odyssey", "Celeste", "Ori and the Blind Forest", "Rayman Legends", "Hollow Knight", "Shovel Knight", "Limbo", "Inside", "Donkey Kong Country", "Mega Man 11", "Sonic Mania", "Little Nightmares", "Cuphead", "Trine 4", "Super Meat Boy", "Braid", "Fez", "Spelunky", "Yoshi's Crafted World", "A Hat in Time"],
            "Puzzle": ["Portal 2", "The Witness", "Tetris Effect", "Baba Is You", "Limbo", "Monument Valley", "Inside", "Fez", "The Talos Principle", "Human Resource Machine", "Q.U.B.E.", "Antichamber", "Puyo Puyo Tetris", "Lemmings", "Professor Layton", "Candy Crush Saga", "Bejeweled", "Unravel", "World of Goo", "Myst"],
            "MMO": ["World of Warcraft", "Final Fantasy XIV", "Elder Scrolls Online", "Guild Wars 2", "Black Desert Online", "Runescape", "Star Wars: The Old Republic", "Blade & Soul", "TERA", "ArcheAge", "EverQuest II", "MapleStory", "RIFT", "DC Universe Online", "Lineage II", "Albion Online", "Skyforge", "Aion", "Warhammer Online", "Entropia Universe"],
            "Indie": ["Undertale", "Hades", "Celeste", "Stardew Valley", "Hollow Knight", "Limbo", "Cuphead", "Hotline Miami", "Shovel Knight", "Fez", "Braid", "Inside", "Super Meat Boy", "Oxenfree", "Papers, Please", "Hyper Light Drifter", "Journey", "Spelunky", "Terraria", "Don't Starve"],
            "Arcade": ["Pac-Man", "Space Invaders", "Donkey Kong", "Asteroids", "Galaga", "Frogger", "Centipede", "Defender", "Q*bert", "Tempest", "Missile Command", "Dig Dug", "BurgerTime", "Joust", "Pengo", "Xevious", "Ms. Pac-Man", "Rally-X", "Pole Position", "Qix"],
            "Fighting": ["Street Fighter V", "Tekken 7", "Mortal Kombat 11", "Super Smash Bros. Ultimate", "Soul Calibur VI", "Injustice 2", "Guilty Gear Strive", "BlazBlue", "Dragon Ball FighterZ", "King of Fighters XIV", "Virtua Fighter 5", "Dead or Alive 6", "Samurai Shodown", "Skullgirls", "Power Rangers: Battle for the Grid", "Fatal Fury", "Killer Instinct", "Under Night In-Birth", "Melty Blood", "Bushido Blade"],
            "Sandbox": ["Minecraft", "Terraria", "Garry's Mod", "Roblox", "The Sims", "Don't Starve", "Starbound", "No Man's Sky", "Rust", "ARK: Survival Evolved", "Subnautica", "Factorio", "Space Engineers", "7 Days to Die", "Eco", "RimWorld", "Fortnite Creative", "Creativerse", "Empyrion", "Blockland"]
        }
        categories = list(self.game_categories.items())
        random.shuffle(categories)
        for category, games in categories:
            self.add_tab(category, games)
    
    def update_global_styles(self):
        global_style = f"""
            QMainWindow {{ 
                background-color: #1a1a1a; 
            }}
            QPushButton {{
                background-color: #444;
                color: #ccc;
                padding: 10px;
                border: 1px solid #222;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {self.user_color};
                color: white;
            }}
        """
        self.setStyleSheet(global_style)
    
    def update_tab_style(self):
        tab_style = f"""
            QTabBar::tab {{
                background-color: #444;
                color: #ccc;
                padding: 10px;
                border: 1px solid #222;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }}
            QTabBar::tab:selected {{
                background-color: {self.user_color};
                color: #ccc;
                font-weight: bold;
            }}
            QTabBar::tab:hover {{
                background-color: {self.user_color};
            }}
        """
        self.tabs.setStyleSheet(tab_style)
    
    def change_user_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.user_color = color.name()
            self.settings.setValue("user_color", self.user_color)
            self.update_global_styles()
            self.update_tab_style()
    
    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.user_text_color = color.name()
            self.settings.setValue("user_text_color", self.user_text_color)
            for i in range(self.tabs.count()):
                widget = self.tabs.widget(i)
                if hasattr(widget, "updateUserTextColor"):
                    widget.updateUserTextColor(self.user_text_color)
    
    def add_tab(self, category, games):
        new_tab = RouletteWidget(category, games, user_text_color=self.user_text_color)
        self.tabs.addTab(new_tab, category)
   
    def add_new_tab(self):
        category, ok = QInputDialog.getText(self, "Nova Roleta", "Digite o nome da nova roleta:")
        if ok and category:
            self.add_tab(category, [])
   
    def delete_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index == 0:
            QMessageBox.information(self, "Ação inválida", "A aba Clube dos Jogos não pode ser excluída!")
            return
        reply = QMessageBox.question(
            self, "Excluir Roleta", "Tem certeza que deseja excluir esta roleta?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.tabs.removeTab(current_index)
    
    def rename_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index == 0:
            QMessageBox.information(self, "Ação inválida", "A aba Clube dos Jogos não pode ser renomeada!")
            return
        widget = self.tabs.widget(current_index)
        if not hasattr(widget, "category"):
            return
        new_name, ok = QInputDialog.getText(
            self, "Renomear Roleta", "Digite o novo nome para a roleta:",
            text=widget.category
        )
        if ok and new_name:
            widget.category = new_name
            widget.label.setText(f"Roleta {new_name}")
            self.tabs.setTabText(current_index, new_name)
    
    def perform_club_sort(self):
        """Realiza o sorteio animado do clube:
           - Obtém os jogadores da aba do clube.
           - Seleciona aleatoriamente uma roleta dentre as demais.
           - Verifica se há jogos suficientes para que cada jogador receba um jogo distinto.
           - Para cada jogador, anima a rotação e, após alguns instantes, fixa o jogo sorteado.
           - Os jogos sorteados não se repetem.
        """
        players = self.club_tab.get_players()
        if not players:
            QMessageBox.warning(self, "Clube dos Jogos", "Nenhum jogador informado!")
            return
        roleta_widgets = []
        for i in range(1, self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, "category"):
                roleta_widgets.append(widget)
        if not roleta_widgets:
            QMessageBox.warning(self, "Clube dos Jogos", "Nenhuma roleta disponível!")
            return
        chosen_widget = random.choice(roleta_widgets)
        chosen_category = chosen_widget.category
        games = [chosen_widget.list_widget.item(j).text() for j in range(chosen_widget.list_widget.count())]
        if len(games) < len(players):
            QMessageBox.warning(self, "Clube dos Jogos", f"A roleta {chosen_category} não possui jogos suficientes para atribuir sem repetições!")
            return
        
        self.club_players = players
        self.club_results = []  
        self.club_games = games[:]  
        self.club_chosen_category = chosen_category
        self.current_player_index = 0
        
        initial_lines = [f"{p}: " for p in players]
        self.club_tab.set_result(f"Categoria sorteada: {chosen_category}\n" + "\n".join(initial_lines))
        
        self.animate_player_spin()
    
    def animate_player_spin(self):
        if self.current_player_index >= len(self.club_players):
            return
        self.animation_counter = 0
        self.animation_timer = QTimer()
        self.animation_timer.setInterval(100)
        self.animation_timer.timeout.connect(self.update_current_player_animation)
        self.animation_timer.start()
    
    def update_current_player_animation(self):
        self.animation_counter += 1
        candidate = random.choice(self.club_games)
        lines = []
        for i, player in enumerate(self.club_players):
            if i < self.current_player_index:
                lines.append(f"{player}: {self.club_results[i]}")
            elif i == self.current_player_index:
                lines.append(f"{player}: {candidate}")
            else:
                lines.append(f"{player}: ")
        display_text = f"Categoria sorteada: {self.club_chosen_category}\n" + "\n".join(lines)
        self.club_tab.set_result(display_text)
        
        if self.animation_counter >= 10:  
            self.animation_timer.stop()
            final_game = random.choice(self.club_games)
            self.club_results.append(final_game)
            self.club_games.remove(final_game)
            self.current_player_index += 1
            lines = []
            for i, player in enumerate(self.club_players):
                if i < self.current_player_index:
                    lines.append(f"{player}: {self.club_results[i]}")
                else:
                    lines.append(f"{player}: ")
            display_text = f"Categoria sorteada: {self.club_chosen_category}\n" + "\n".join(lines)
            self.club_tab.set_result(display_text)
            QTimer.singleShot(500, self.animate_player_spin)
    
    def save_roletas(self):
        """Percorre as roletas (abas com atributo 'category') e salva o estado no QSettings."""
        roletas = []
        for i in range(1, self.tabs.count()):
            widget = self.tabs.widget(i)
            if hasattr(widget, "category"):
                games = [widget.list_widget.item(j).text() for j in range(widget.list_widget.count())]
                roletas.append({"category": widget.category, "games": games})
        roletas_json = json.dumps(roletas)
        self.settings.setValue("roletas", roletas_json)
    
    def closeEvent(self, event):
        """Salva o estado das roletas e a geometria da janela ao fechar."""
        self.save_roletas()
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
