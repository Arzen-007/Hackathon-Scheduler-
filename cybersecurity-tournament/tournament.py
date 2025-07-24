import tkinter as tk
from tkinter import ttk, messagebox, font
import random
from PIL import ImageTk, Image
import os

# ---------------------------- CONSTANTS ---------------------------- #
class ColorPalette:
    PRIMARY = "#1a1a2e"      # Dark navy blue
    SECONDARY = "#16213e"    # Slightly lighter navy
    ACCENT = "#0f3460"       # Dark blue accent
    HIGHLIGHT = "#e94560"    # Coral pink for highlights
    TEXT = "#f1f1f1"         # Off-white text
    SUCCESS = "#4CAF50"      # Green for success messages
    WARNING = "#FF9800"      # Orange for warnings
    ERROR = "#F44336"        # Red for errors

class Fonts:
    TITLE = ("SF Pro Display", 24, "bold")
    SUBTITLE = ("SF Pro Display", 18)
    BODY = ("SF Pro Text", 12)
    BUTTON = ("SF Pro Text", 12, "bold")
    CODE = ("Fira Code", 11)

# ---------------------------- DATA CLASSES ---------------------------- #
class Team:
    def __init__(self, name, members, rank):
        self.name = name
        self.members = members
        self.rank = rank

class Match:
    def __init__(self, team1, team2, round_name):
        self.team1 = team1
        self.team2 = team2
        self.round_name = round_name
        self.status = "Scheduled"
        self.winner = None

    def complete(self):
        self.status = "Completed"
        self.winner = random.choice([self.team1, self.team2])
        return self.winner

class Scheduler:
    def __init__(self):
        self.teams = []
        self.group_A = []
        self.group_B = []
        self.rounds = {
            "Round 1": [],
            "Quarter Final": [],
            "Semi Final": [],
            "Final": []
        }
        self.winner = None

    def load_teams(self, filename):
        self.teams = []
        with open(filename, 'r') as file:
            for line in file:
                name, members, rank = line.strip().split(";")
                team = Team(name, members.split(","), int(rank))
                self.teams.append(team)
        self.teams.sort(key=lambda t: t.rank)
        return True

    def divide_groups(self):
        self.group_A = self.teams[:8]
        self.group_B = self.teams[8:]
        return self.group_A, self.group_B

    def schedule_matches(self, teams, round_name):
        random.shuffle(teams)
        matches = []
        for i in range(0, len(teams), 2):
            match = Match(teams[i], teams[i+1], round_name)
            matches.append(match)
        self.rounds[round_name] = matches
        return matches

    def complete_round(self, round_name):
        winners = []
        for match in self.rounds[round_name]:
            winners.append(match.complete())
        
        if round_name == "Final":
            self.winner = winners[0]
        return winners

# ---------------------------- GUI CLASSES ---------------------------- #
class CustomButton(ttk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = ttk.Style()
        self.style.configure('CustomButton.TButton',
                            font=Fonts.BUTTON,
                            foreground=ColorPalette.TEXT,
                            background=ColorPalette.ACCENT,
                            bordercolor=ColorPalette.ACCENT,
                            focuscolor=self.style.configure('.')['background'],
                            padding=10,
                            relief="raised")
        self.configure(style='CustomButton.TButton')
        
class ModernTournamentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cybersecurity Hackathon Scheduler")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=ColorPalette.PRIMARY)
        
        # Configure styles
        self.configure_styles()
        
        # Initialize scheduler
        self.scheduler = Scheduler()
        self.current_view = None
        
        # Load custom fonts
        self.load_fonts()
        
        # Show loading screen first
        self.show_splash_screen()
        
    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Frame style
        self.style.configure('Custom.TFrame', background=ColorPalette.PRIMARY)
        
        # Label styles
        self.style.configure('Title.TLabel',
                            font=Fonts.TITLE,
                            foreground=ColorPalette.TEXT,
                            background=ColorPalette.PRIMARY)
                            
        self.style.configure('Subtitle.TLabel',
                            font=Fonts.SUBTITLE,
                            foreground=ColorPalette.HIGHLIGHT,
                            background=ColorPalette.PRIMARY)
                            
        # Entry style
        self.style.configure('Custom.TEntry',
                            font=Fonts.BODY,
                            foreground=ColorPalette.TEXT,
                            fieldbackground=ColorPalette.SECONDARY,
                            bordercolor=ColorPalette.ACCENT,
                            lightcolor=ColorPalette.ACCENT,
                            darkcolor=ColorPalette.ACCENT)
        
        # Treeview style
        self.style.configure('Custom.Treeview',
                            font=Fonts.BODY,
                            foreground=ColorPalette.TEXT,
                            background=ColorPalette.SECONDARY,
                            fieldbackground=ColorPalette.SECONDARY,
                            bordercolor=ColorPalette.ACCENT,
                            lightcolor=ColorPalette.ACCENT)
                            
        self.style.map('Custom.Treeview',
                      background=[('selected', ColorPalette.ACCENT)])
                      
        # Scrollbar style
        self.style.configure('Custom.Vertical.TScrollbar',
                            background=ColorPalette.ACCENT)
        
    def load_fonts(self):
        # Try to load custom fonts (would need to be installed on system)
        try:
            custom_font = font.Font(family="SF Pro Display", size=12)
        except:
            pass
        
    def clear_window(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = ttk.Frame(self.root, style='Custom.TFrame')
        self.current_view.pack(fill="both", expand=True)
        
    def show_splash_screen(self):
        self.clear_window()
        
        # Splash container
        splash_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        splash_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        ttk.Label(splash_frame, text="CYBERSECURITY\nHACKATHON SCHEDULER",
                 style='Title.TLabel', justify="center").pack(pady=20)
        
        # Subtitle
        ttk.Label(splash_frame, text="Advanced Tournament Management System",
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Load team button
        load_btn = CustomButton(splash_frame,
                               text="LOAD TEAMS",
                               command=self.show_load_window)
        load_btn.pack(pady=30, ipadx=20, ipady=10)
        
    def show_load_window(self):
        self.clear_window()
        
        # Header frame
        header_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Back button
        back_btn = CustomButton(header_frame,
                               text="← BACK",
                               command=self.show_splash_screen)
        back_btn.pack(side="left")
        
        # Title
        ttk.Label(header_frame, text="TEAM MANAGEMENT",
                 style='Title.TLabel').pack(side="left", padx=20)
                 
        # Main content
        content_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Left panel - team loading
        left_panel = ttk.Frame(content_frame, style='Custom.TFrame')
        left_panel.pack(side="left", fill="both", expand=True, padx=10)
        
        ttk.Label(left_panel, text="Load Team Data", style='Subtitle.TLabel').pack(pady=10)
        
        # Team info text
        info_text = tk.Text(left_panel,
                           font=Fonts.BODY,
                           bg=ColorPalette.SECONDARY,
                           fg=ColorPalette.TEXT,
                           height=10,
                           width=40,
                           padx=10,
                           pady=10,
                           wrap="word")
        info_text.pack(pady=10)
        info_text.insert("1.0", "Teams will be loaded from 'teams.txt' in the format:\n\n")
        info_text.insert("end", "Team Name;Member1,Member2;Rank\n")
        info_text.insert("end", "Example:\n")
        info_text.insert("end", "Team Alpha;Alice,Bob;1")
        info_text.config(state="disabled")
        
        # Load button
        load_btn = CustomButton(left_panel,
                              text="LOAD TEAMS",
                              command=self.load_teams)
        load_btn.pack(pady=20)
        
        # Right panel - visualization
        right_panel = ttk.Frame(content_frame, style='Custom.TFrame')
        right_panel.pack(side="right", fill="both", expand=True, padx=10)
        
        ttk.Label(right_panel, text="Team Visualization", style='Subtitle.TLabel').pack(pady=10)
        
        # Team treeview
        self.team_tree = ttk.Treeview(right_panel,
                                     style='Custom.Treeview',
                                     columns=("Rank", "Name", "Members"),
                                     show="headings")
        self.team_tree.heading("Rank", text="Rank")
        self.team_tree.heading("Name", text="Team Name")
        self.team_tree.heading("Members", text="Members")
        
        self.team_tree.column("Rank", width=50, anchor="center")
        self.team_tree.column("Name", width=150)
        self.team_tree.column("Members", width=200)
        
        scrollbar = ttk.Scrollbar(right_panel,
                                 orient="vertical",
                                 command=self.team_tree.yview,
                                 style='Custom.Vertical.TScrollbar')
        self.team_tree.configure(yscrollcommand=scrollbar.set)
        
        self.team_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Next button (disabled until teams are loaded)
        self.next_btn = CustomButton(content_frame,
                                    text="DIVIDE GROUPS →",
                                    state="disabled",
                                    command=self.show_groups_window)
        self.next_btn.pack(pady=20)
        
    def load_teams(self):
        try:
            success = self.scheduler.load_teams("teams.txt")
            if success:
                # Update treeview
                self.team_tree.delete(*self.team_tree.get_children())
                for team in self.scheduler.teams:
                    self.team_tree.insert("", "end", values=(
                        team.rank,
                        team.name,
                        ", ".join(team.members)
                    ))
                
                # Enable next button
                self.next_btn.config(state="normal")
                
                messagebox.showinfo("Success", "Teams loaded successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load teams:\n{str(e)}")
            return False
            
    def show_groups_window(self):
        self.clear_window()
        
        # Divide groups
        group_A, group_B = self.scheduler.divide_groups()
        
        # Header frame
        header_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Back button
        back_btn = CustomButton(header_frame,
                               text="← BACK",
                               command=self.show_load_window)
        back_btn.pack(side="left")
        
        # Title
        ttk.Label(header_frame, text="TEAM GROUPS",
                 style='Title.TLabel').pack(side="left", padx=20)
                 
        # Main content
        content_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Group A frame
        group_a_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        group_a_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        ttk.Label(group_a_frame, text="GROUP A (Top 8)", style='Subtitle.TLabel').pack(pady=10)
        
        group_a_tree = ttk.Treeview(group_a_frame,
                                   style='Custom.Treeview',
                                   columns=("Rank", "Name"),
                                   show="headings")
        group_a_tree.heading("Rank", text="Rank")
        group_a_tree.heading("Name", text="Team Name")
        
        for team in group_A:
            group_a_tree.insert("", "end", values=(team.rank, team.name))
            
        scroll_a = ttk.Scrollbar(group_a_frame,
                                orient="vertical",
                                command=group_a_tree.yview,
                                style='Custom.Vertical.TScrollbar')
        group_a_tree.configure(yscrollcommand=scroll_a.set)
        
        group_a_tree.pack(side="left", fill="both", expand=True)
        scroll_a.pack(side="right", fill="y")
        
        # Group B frame
        group_b_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        group_b_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        ttk.Label(group_b_frame, text="GROUP B (Bottom 8)", style='Subtitle.TLabel').pack(pady=10)
        
        group_b_tree = ttk.Treeview(group_b_frame,
                                   style='Custom.Treeview',
                                   columns=("Rank", "Name"),
                                   show="headings")
        group_b_tree.heading("Rank", text="Rank")
        group_b_tree.heading("Name", text="Team Name")
        
        for team in group_B:
            group_b_tree.insert("", "end", values=(team.rank, team.name))
            
        scroll_b = ttk.Scrollbar(group_b_frame,
                                orient="vertical",
                                command=group_b_tree.yview,
                                style='Custom.Vertical.TScrollbar')
        group_b_tree.configure(yscrollcommand=scroll_b.set)
        
        group_b_tree.pack(side="left", fill="both", expand=True)
        scroll_b.pack(side="right", fill="y")
        
        # Next button
        next_btn = CustomButton(content_frame,
                               text="START TOURNAMENT →",
                               command=self.show_round_window)
        next_btn.pack(pady=20, anchor="center")
        
    def show_round_window(self, round_name="Round 1"):
        self.clear_window()
        
        # Header frame
        header_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Back button
        back_btn = CustomButton(header_frame,
                               text="← BACK",
                               command=self.show_groups_window)
        back_btn.pack(side="left")
        
        # Title
        ttk.Label(header_frame, text=round_name.upper(),
                 style='Title.TLabel').pack(side="left", padx=20)
                 
        # Main content
        content_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Match frame
        match_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        match_frame.pack(fill="both", expand=True, pady=20)
        
        # Text widget for match display
        self.match_text = tk.Text(match_frame,
                                font=Fonts.CODE,
                                bg=ColorPalette.SECONDARY,
                                fg=ColorPalette.TEXT,
                                height=15,
                                width=80,
                                padx=15,
                                pady=15,
                                wrap="word")
        
        scrollbar = ttk.Scrollbar(match_frame,
                                 command=self.match_text.yview,
                                 style='Custom.Vertical.TScrollbar')
        self.match_text.configure(yscrollcommand=scrollbar.set)
        
        self.match_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Button frame
        btn_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        btn_frame.pack(fill="x", pady=20)
        
        # Schedule matches button
        schedule_btn = CustomButton(btn_frame,
                                   text=f"SCHEDULE {round_name} MATCHES",
                                   command=lambda: self.schedule_matches(round_name))
        schedule_btn.pack(side="left", padx=10)
        
        # Run matches button
        run_btn = CustomButton(btn_frame,
                              text=f"RUN {round_name}",
                              command=lambda: self.run_round(round_name))
        run_btn.pack(side="left", padx=10)
        
        # Next round button
        next_round = self.get_next_round(round_name)
        if next_round:
            self.next_round_btn = CustomButton(btn_frame,
                                             text=f"NEXT: {next_round} →",
                                             state="disabled",
                                             command=lambda: self.show_round_window(next_round))
            self.next_round_btn.pack(side="right", padx=10)
        else:
            self.show_winner_btn = CustomButton(btn_frame,
                                              text="SHOW WINNER",
                                              state="disabled",
                                              command=self.show_winner_window)
            self.show_winner_btn.pack(side="right", padx=10)
            
    def schedule_matches(self, round_name):
        if round_name == "Round 1":
            # Shuffle groups A and B
            group_A = self.scheduler.group_A.copy()
            group_B = self.scheduler.group_B.copy()
            random.shuffle(group_A)
            random.shuffle(group_B)
            
            # Create matchups (A1 vs B1, A2 vs B2, etc.)
            teams = []
            for a, b in zip(group_A, group_B):
                teams.extend([a, b])
        else:
            # Get winners from previous round
            prev_round = {
                "Quarter Final": "Round 1",
                "Semi Final": "Quarter Final",
                "Final": "Semi Final"
            }[round_name]
            teams = [match.winner for match in self.scheduler.rounds[prev_round]]
            
        # Schedule matches
        matches = self.scheduler.schedule_matches(teams, round_name)
        
        # Display matchups
        self.match_text.config(state="normal")
        self.match_text.delete(1.0, tk.END)
        self.match_text.insert(tk.END, f"--- {round_name} Matchups ---\n\n")
        
        for i, match in enumerate(matches, 1):
            self.match_text.insert(tk.END, f"Match {i}: {match.team1.name} vs {match.team2.name}\n")
        
        self.match_text.config(state="disabled")
        
    def run_round(self, round_name):
        winners = self.scheduler.complete_round(round_name)
        
        self.match_text.config(state="normal")
        self.match_text.delete(1.0, tk.END)
        self.match_text.insert(tk.END, f"--- {round_name} Results ---\n\n")
        
        for i, match in enumerate(self.scheduler.rounds[round_name], 1):
            self.match_text.insert(tk.END, 
                                 f"Match {i}: {match.team1.name} vs {match.team2.name}\n")
            self.match_text.insert(tk.END, 
                                 f"Winner: {match.winner.name}\n\n")
        
        self.match_text.config(state="disabled")
        
        # Enable next round button
        next_round = self.get_next_round(round_name)
        if next_round:
            self.next_round_btn.config(state="normal")
        else:
            self.show_winner_btn.config(state="normal")
            
    def get_next_round(self, current_round):
        rounds_order = ["Round 1", "Quarter Final", "Semi Final", "Final"]
        try:
            current_index = rounds_order.index(current_round)
            return rounds_order[current_index + 1] if current_index + 1 < len(rounds_order) else None
        except ValueError:
            return None
            
    def show_winner_window(self):
        self.clear_window()
        
        # Ensure final is complete
        if not self.scheduler.rounds["Final"]:
            self.scheduler.complete_round("Final")
            
        winner = self.scheduler.rounds["Final"][0].winner
        
        # Header frame
        header_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Back button
        back_btn = CustomButton(header_frame,
                               text="← BACK",
                               command=lambda: self.show_round_window("Final"))
        back_btn.pack(side="left")
        
        # Title
        ttk.Label(header_frame, text="TOURNAMENT WINNER",
                 style='Title.TLabel').pack(side="left", padx=20)
                 
        # Main content
        content_frame = ttk.Frame(self.current_view, style='Custom.TFrame')
        content_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Winner display
        winner_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        winner_frame.pack(expand=True, pady=50)
        
        ttk.Label(winner_frame,
                 text="🏆 CHAMPION 🏆",
                 style='Title.TLabel').pack(pady=20)
                 
        ttk.Label(winner_frame,
                 text=winner.name,
                 style='Subtitle.TLabel').pack(pady=20)
                 
        ttk.Label(winner_frame,
                 text=f"Team Members: {', '.join(winner.members)}",
                 style='Subtitle.TLabel').pack(pady=10)
                 
        # Tournament summary
        summary_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        summary_frame.pack(fill="x", pady=20)
        
        ttk.Label(summary_frame,
                 text="Tournament Summary",
                 style='Subtitle.TLabel').pack(pady=10)
                 
        summary_text = tk.Text(summary_frame,
                             font=Fonts.BODY,
                             bg=ColorPalette.SECONDARY,
                             fg=ColorPalette.TEXT,
                             height=10,
                             width=80,
                             padx=15,
                             pady=15,
                             wrap="word")
        summary_text.pack(fill="x")
        
        summary_text.insert(tk.END, "Match Results:\n\n")
        for round_name, matches in self.scheduler.rounds.items():
            summary_text.insert(tk.END, f"{round_name}:\n")
            for match in matches:
                summary_text.insert(tk.END, f"- {match.team1.name} vs {match.team2.name} → {match.winner.name}\n")
            summary_text.insert(tk.END, "\n")
        
        summary_text.config(state="disabled")
        
# ---------------------------- MAIN EXECUTION ---------------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        img = tk.Image("photo", file="tournament_icon.png")
        root.iconphoto(True, img)
    except:
        pass
        
    app = ModernTournamentGUI(root)
    root.mainloop()
