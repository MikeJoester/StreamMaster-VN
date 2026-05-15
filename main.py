import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys


def resource_path(relative_path):

    try:

        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


CHARACTERS = [
    "A.K.I", "Akuma", "Alex", "Blanka", "C. Viper", "Cammy", "Chun-Li", "Dee Jay",
    "Dhalsim", "Dictator", "E.Honda", "Ed", "Elena", "Guile", "Jamie", "JP", "Juri",
    "Ken", "Kimberly", "Lily", "Luke", "Mai", "Manon", "Marisa", "Rashid", "Ryu",
    "Sagat", "Terry", "Zangief"
]

DEFAULT_DATA = {
    "event": {
        "name": "CBT 2025",
        "best_of": "Grand Finals Reset"
    },
    "scoreboard": {
        "p1": {"name": "Player 1", "team": "Team A", "score": 0, "country": "US"},
        "p2": {"name": "Player 2", "team": "Team B", "score": 0, "country": "JP"}
    },
    "vs": {
        "p1": {"name": "Player 1", "character": "Ryu"},
        "p2": {"name": "Player 2", "character": "Ken"}
    },
    "winner": {
        "winner": "Player 1",
        "character": "Ryu",
        "team": "Team A",
        "country": "US"
    },
    "bracket": {
        "players": [
            {"name": "Player 1", "team": "Team A", "country": "US", "character": "Ryu"},
            {"name": "Player 2", "team": "Team B", "country": "JP", "character": "Ken"},
            {"name": "Player 3", "team": "Team C", "country": "BR", "character": "Chun-Li"},
            {"name": "Player 4", "team": "Team D", "country": "FR", "character": "Cammy"},
            {"name": "Player 5", "team": "Team E", "country": "CA", "character": "Guile"},
            {"name": "Player 6", "team": "Team F", "country": "DE", "character": "Zangief"},
            {"name": "Player 7", "team": "Team G", "country": "UK", "character": "Juri"},
            {"name": "Player 8", "team": "Team H", "country": "KR", "character": "Luke"}
        ],
        "matches": {
            "winners": {
                "WSF1": {
                    "participants": [
                        {"type": "player", "index": 0},
                        {"type": "player", "index": 1}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                },
                "WSF2": {
                    "participants": [
                        {"type": "player", "index": 2},
                        {"type": "player", "index": 3}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                },
                "WF": {
                    "participants": [
                        {"type": "match", "matchId": "WSF1", "outcome": "winner"},
                        {"type": "match", "matchId": "WSF2", "outcome": "winner"}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                }
            },
            "losers": {
                "LQF1": {
                    "participants": [
                        {"type": "player", "index": 4},
                        {"type": "player", "index": 5}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                },
                "LQF2": {
                    "participants": [
                        {"type": "player", "index": 6},
                        {"type": "player", "index": 7}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                },
                "LSF1": {
                    "participants": [
                        {"type": "match", "matchId": "WSF1", "outcome": "loser"},
                        {"type": "match", "matchId": "LQF1", "outcome": "winner"}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                },
                "LSF2": {
                    "participants": [
                        {"type": "match", "matchId": "WSF2", "outcome": "loser"},
                        {"type": "match", "matchId": "LQF2", "outcome": "winner"}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                },
                "LF": {
                    "participants": [
                        {"type": "match", "matchId": "LSF1", "outcome": "winner"},
                        {"type": "match", "matchId": "LSF2", "outcome": "winner"}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                },
                "LL": {
                    "participants": [
                        {"type": "match", "matchId": "LF", "outcome": "winner"},
                        {"type": "match", "matchId": "WF", "outcome": "loser"}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                }
            },
            "grandFinal": {
                "GF": {
                    "participants": [
                        {"type": "match", "matchId": "WF", "outcome": "winner"},
                        {"type": "match", "matchId": "LL", "outcome": "winner"}
                    ],
                    "score1": 0, "score2": 0, "winner": None,
                    "resetMatch": None
                }
            }
        }
    },
    "results": {
        "players": []
    }
}

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def resolve_participant(participant, bracket_data):
    if not participant:
        return None
    if participant["type"] == "player":
        idx = participant["index"]
        if 0 <= idx < len(bracket_data["players"]):
            return bracket_data["players"][idx]
        return None
    elif participant["type"] == "match":
        match_id = participant["matchId"]
        outcome = participant["outcome"]
        if match_id in bracket_data["matches"]["winners"]:
            match = bracket_data["matches"]["winners"][match_id]
        elif match_id in bracket_data["matches"]["losers"]:
            match = bracket_data["matches"]["losers"][match_id]
        elif match_id == "GF":
            match = bracket_data["matches"]["grandFinal"]["GF"]
        else:
            return None
        if not match or match["winner"] is None:
            return None
        winner_side = match["winner"]
        if outcome == "winner":
            side = winner_side
        else:
            side = 2 if winner_side == 1 else 1
        sub_participant = match["participants"][side - 1]
        return resolve_participant(sub_participant, bracket_data)
    return None

def compute_placements(bracket_data):
    def get_player_from_match(match, side):
        if not match or match["winner"] is None:
            return None
        part = match["participants"][side - 1]
        return resolve_participant(part, bracket_data)

    gf = bracket_data["matches"]["grandFinal"]["GF"]
    reset = gf.get("resetMatch")

    if reset and reset["winner"] is not None:
        champ_side = reset["winner"]
        champ = get_player_from_match(reset, champ_side)
        runner_up_side = 2 if champ_side == 1 else 1
        runner_up = get_player_from_match(reset, runner_up_side)
    else:
        if gf["winner"] is None:
            champ = runner_up = None
        else:
            champ_side = gf["winner"]
            champ = get_player_from_match(gf, champ_side)
            runner_up_side = 2 if champ_side == 1 else 1
            runner_up = get_player_from_match(gf, runner_up_side)

    ll_match = bracket_data["matches"]["losers"]["LL"]
    if ll_match and ll_match["winner"] is not None:
        loser_side = 2 if ll_match["winner"] == 1 else 1
        third = get_player_from_match(ll_match, loser_side)
    else:
        third = None

    lf_match = bracket_data["matches"]["losers"]["LF"]
    if lf_match and lf_match["winner"] is not None:
        loser_side = 2 if lf_match["winner"] == 1 else 1
        fourth = get_player_from_match(lf_match, loser_side)
    else:
        fourth = None

    fifth_players = []
    for match_id in ["LSF1", "LSF2"]:
        m = bracket_data["matches"]["losers"][match_id]
        if m and m["winner"] is not None:
            loser_side = 2 if m["winner"] == 1 else 1
            p = get_player_from_match(m, loser_side)
            if p:
                fifth_players.append(p)
    seventh_players = []
    for match_id in ["LQF1", "LQF2"]:
        m = bracket_data["matches"]["losers"][match_id]
        if m and m["winner"] is not None:
            loser_side = 2 if m["winner"] == 1 else 1
            p = get_player_from_match(m, loser_side)
            if p:
                seventh_players.append(p)

    while len(fifth_players) < 2:
        fifth_players.append(None)
    while len(seventh_players) < 2:
        seventh_players.append(None)

    placements = [champ, runner_up, third, fourth] + fifth_players + seventh_players
    placeholder = {"name": "TBD", "team": "", "country": "", "character": "Ryu"}
    return [p if p is not None else placeholder for p in placements]


class StreamMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StreamMaster")
        self.root.geometry("500x385")

        try:
            icon_path = resource_path('icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass  

        self.data = load_data()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_scoreboard = ttk.Frame(self.notebook)
        self.tab_vs = ttk.Frame(self.notebook)
        self.tab_winner = ttk.Frame(self.notebook)
        self.tab_bracket = ttk.Frame(self.notebook)
        self.tab_bracket_control = ttk.Frame(self.notebook)
        self.tab_results = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_scoreboard, text="Scoreboard")
        self.notebook.add(self.tab_vs, text="Player vs Player")
        self.notebook.add(self.tab_winner, text="Winner Screen")
        self.notebook.add(self.tab_bracket, text="Top 8 Bracket")
        self.notebook.add(self.tab_bracket_control, text="Bracket Control")
        self.notebook.add(self.tab_results, text="Top 8 Results")

        self.build_scoreboard_tab()
        self.build_vs_tab()
        self.build_winner_tab()
        self.build_bracket_tab()
        self.build_bracket_control_tab()
        self.build_results_tab()


    def make_scrollable_tab(self, parent):
        outer = ttk.Frame(parent)
        outer.pack(fill="both", expand=True)

        btn = ttk.Button(outer, text="Save All Changes", command=self.save_all)
        btn.pack(pady=5, padx=5, anchor='center')

        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        def _on_mousewheel_linux(event):
            canvas.yview_scroll(int(-1*event.num), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", _on_mousewheel_linux)
        canvas.bind("<Button-5>", _on_mousewheel_linux)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def get_participant_name(self, participant, bracket_data):
        if not participant:
            return "TBD"
        if participant["type"] == "player":
            idx = participant["index"]
            if 0 <= idx < len(bracket_data["players"]):
                return bracket_data["players"][idx]["name"]
            return "TBD"
        elif participant["type"] == "match":
            player = resolve_participant(participant, bracket_data)
            if player:
                return player["name"]
            return "TBD"
        return "TBD"

    def build_scoreboard_tab(self):
        content = self.make_scrollable_tab(self.tab_scoreboard)
        row = 0
        ttk.Label(content, text="Event Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_event_name = ttk.Entry(content, width=30)
        self.entry_event_name.insert(0, self.data["event"]["name"])
        self.entry_event_name.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ttk.Label(content, text="Best of / First of:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_best_of = ttk.Entry(content, width=30)
        self.entry_best_of.insert(0, self.data["event"]["best_of"])
        self.entry_best_of.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        # Player 1
        ttk.Label(content, text="Player 1 Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p1_name = ttk.Entry(content, width=30)
        self.entry_p1_name.insert(0, self.data["scoreboard"]["p1"]["name"])
        self.entry_p1_name.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ttk.Label(content, text="Player 1 Team:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p1_team = ttk.Entry(content, width=30)
        self.entry_p1_team.insert(0, self.data["scoreboard"]["p1"]["team"])
        self.entry_p1_team.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ttk.Label(content, text="Player 1 Score:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p1_score = ttk.Spinbox(content, from_=0, to=100, width=28)
        self.entry_p1_score.insert(0, self.data["scoreboard"]["p1"]["score"])
        self.entry_p1_score.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ttk.Label(content, text="Player 1 Country (abbr):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p1_country = ttk.Entry(content, width=30)
        self.entry_p1_country.insert(0, self.data["scoreboard"]["p1"]["country"])
        self.entry_p1_country.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        # Player 2
        ttk.Label(content, text="Player 2 Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p2_name = ttk.Entry(content, width=30)
        self.entry_p2_name.insert(0, self.data["scoreboard"]["p2"]["name"])
        self.entry_p2_name.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ttk.Label(content, text="Player 2 Team:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p2_team = ttk.Entry(content, width=30)
        self.entry_p2_team.insert(0, self.data["scoreboard"]["p2"]["team"])
        self.entry_p2_team.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ttk.Label(content, text="Player 2 Score:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p2_score = ttk.Spinbox(content, from_=0, to=100, width=28)
        self.entry_p2_score.insert(0, self.data["scoreboard"]["p2"]["score"])
        self.entry_p2_score.grid(row=row, column=1, sticky="w", padx=5)
        row += 1

        ttk.Label(content, text="Player 2 Country (abbr):").grid(row=row, column=0, sticky="w", padx=5, pady=2)
        self.entry_p2_country = ttk.Entry(content, width=30)
        self.entry_p2_country.insert(0, self.data["scoreboard"]["p2"]["country"])
        self.entry_p2_country.grid(row=row, column=1, sticky="w", padx=5)

    def build_vs_tab(self):
        content = self.make_scrollable_tab(self.tab_vs)
        ttk.Label(content, text="Player 1 Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_vs_p1_name = ttk.Entry(content, width=30)
        self.entry_vs_p1_name.insert(0, self.data["vs"]["p1"]["name"])
        self.entry_vs_p1_name.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(content, text="Player 1 Character:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combo_vs_p1_char = ttk.Combobox(content, values=CHARACTERS, width=27)
        self.combo_vs_p1_char.set(self.data["vs"]["p1"]["character"])
        self.combo_vs_p1_char.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(content, text="Player 2 Name:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_vs_p2_name = ttk.Entry(content, width=30)
        self.entry_vs_p2_name.insert(0, self.data["vs"]["p2"]["name"])
        self.entry_vs_p2_name.grid(row=2, column=1, sticky="w", padx=5)

        ttk.Label(content, text="Player 2 Character:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_vs_p2_char = ttk.Combobox(content, values=CHARACTERS, width=27)
        self.combo_vs_p2_char.set(self.data["vs"]["p2"]["character"])
        self.combo_vs_p2_char.grid(row=3, column=1, sticky="w", padx=5)

    def build_winner_tab(self):
        content = self.make_scrollable_tab(self.tab_winner)
        ttk.Label(content, text="Winner Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_winner_name = ttk.Entry(content, width=30)
        self.entry_winner_name.insert(0, self.data["winner"]["winner"])
        self.entry_winner_name.grid(row=0, column=1, sticky="w", padx=5)

        ttk.Label(content, text="Winner Team:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_winner_team = ttk.Entry(content, width=30)
        self.entry_winner_team.insert(0, self.data["winner"]["team"])
        self.entry_winner_team.grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(content, text="Winner Country (abbr):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_winner_country = ttk.Entry(content, width=30)
        self.entry_winner_country.insert(0, self.data["winner"]["country"])
        self.entry_winner_country.grid(row=2, column=1, sticky="w", padx=5)

        ttk.Label(content, text="Winner Character:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_winner_char = ttk.Combobox(content, values=CHARACTERS, width=27)
        self.combo_winner_char.set(self.data["winner"]["character"])
        self.combo_winner_char.grid(row=3, column=1, sticky="w", padx=5)

    def build_bracket_tab(self):
        content = self.make_scrollable_tab(self.tab_bracket)
        self.bracket_player_entries = []
        for i in range(8):
            row = i * 4
            ttk.Label(content, text=f"Player {i+1} Name:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
            name_entry = ttk.Entry(content, width=30)
            name_entry.insert(0, self.data["bracket"]["players"][i]["name"])
            name_entry.grid(row=row, column=1, sticky="w", padx=5)

            ttk.Label(content, text=f"Team:").grid(row=row+1, column=0, sticky="w", padx=5, pady=2)
            team_entry = ttk.Entry(content, width=30)
            team_entry.insert(0, self.data["bracket"]["players"][i]["team"])
            team_entry.grid(row=row+1, column=1, sticky="w", padx=5)

            ttk.Label(content, text=f"Country (abbr):").grid(row=row+2, column=0, sticky="w", padx=5, pady=2)
            country_entry = ttk.Entry(content, width=30)
            country_entry.insert(0, self.data["bracket"]["players"][i]["country"])
            country_entry.grid(row=row+2, column=1, sticky="w", padx=5)

            ttk.Label(content, text=f"Character:").grid(row=row+3, column=0, sticky="w", padx=5, pady=2)
            char_combo = ttk.Combobox(content, values=CHARACTERS, width=27)
            char_combo.set(self.data["bracket"]["players"][i]["character"])
            char_combo.grid(row=row+3, column=1, sticky="w", padx=5)

            self.bracket_player_entries.append((name_entry, team_entry, country_entry, char_combo))

    def build_bracket_control_tab(self):
        content = self.make_scrollable_tab(self.tab_bracket_control)

        self.reset_enabled = tk.BooleanVar()
        reset_match = self.data["bracket"]["matches"]["grandFinal"]["GF"].get("resetMatch")
        self.reset_enabled.set(reset_match is not None)
        toggle_frame = ttk.Frame(content)
        toggle_frame.pack(fill="x", pady=5)
        ttk.Checkbutton(toggle_frame, text="Enable Grand Final Reset", variable=self.reset_enabled,
                        command=self.toggle_reset).pack(anchor='w', padx=5)

        self.reset_frame = ttk.Frame(content)
        self.reset_frame.pack(fill="x", pady=2)
        self.reset_entry_vars = None

        self.match_entries = {}
        self.build_static_match_entries(content)
        self.toggle_reset()

    def build_static_match_entries(self, parent):
        all_matches = {}
        all_matches.update({f"Winners_{k}": v for k, v in self.data["bracket"]["matches"]["winners"].items()})
        all_matches.update({f"Losers_{k}": v for k, v in self.data["bracket"]["matches"]["losers"].items()})
        all_matches["GrandFinal_GF"] = self.data["bracket"]["matches"]["grandFinal"]["GF"]

        label_map = {
            "Winners_WSF1": "Winners_WSF1",
            "Winners_WSF2": "Winners_WSF2",
            "Winners_WF": "Winners_WF",
            "Losers_LQF1": "Losers_L1",
            "Losers_LQF2": "Losers_L2",
            "Losers_LSF1": "Losers_LQF1",
            "Losers_LSF2": "Losers_LQF2",
            "Losers_LF": "Losers_LSF",
            "Losers_LL": "Losers_LF",
            "GrandFinal_GF": "GrandFinal_GF"
        }

        for match_key, match_data in all_matches.items():
            participants = match_data.get("participants", [])
            p1_name = self.get_participant_name(participants[0] if len(participants) > 0 else None, self.data["bracket"])
            p2_name = self.get_participant_name(participants[1] if len(participants) > 1 else None, self.data["bracket"])
            display_name = label_map.get(match_key, match_key)

            match_frame = ttk.Frame(parent)
            match_frame.pack(fill="x", pady=2)

            lbl = ttk.Label(match_frame, text=f"{display_name}:", width=12, anchor='e')
            lbl.pack(side="left", padx=2)

            lbl_p1 = ttk.Label(match_frame, text=p1_name, width=15, anchor='w')
            lbl_p1.pack(side="left", padx=2)

            score1_var = tk.StringVar(value=str(match_data.get("score1", 0)))
            entry1 = ttk.Spinbox(match_frame, textvariable=score1_var, width=5, from_=0, to=100)
            entry1.pack(side="left", padx=2)

            sep = ttk.Label(match_frame, text="-")
            sep.pack(side="left", padx=2)

            lbl_p2 = ttk.Label(match_frame, text=p2_name, width=15, anchor='w')
            lbl_p2.pack(side="left", padx=2)

            score2_var = tk.StringVar(value=str(match_data.get("score2", 0)))
            entry2 = ttk.Spinbox(match_frame, textvariable=score2_var, width=5, from_=0, to=100)
            entry2.pack(side="left", padx=2)

            self.match_entries[match_key] = (score1_var, score2_var)

    def toggle_reset(self):
        for widget in self.reset_frame.winfo_children():
            widget.destroy()
        self.reset_entry_vars = None

        if self.reset_enabled.get():
            reset_data = self.data["bracket"]["matches"]["grandFinal"]["GF"].get("resetMatch")
            if not reset_data:
                reset_data = {
                    "participants": [
                        {"type": "match", "matchId": "WF", "outcome": "winner"},
                        {"type": "match", "matchId": "LL", "outcome": "winner"}
                    ],
                    "score1": 0, "score2": 0, "winner": None
                }
                self.data["bracket"]["matches"]["grandFinal"]["GF"]["resetMatch"] = reset_data

            participants = reset_data.get("participants", [])
            p1_name = self.get_participant_name(participants[0] if len(participants) > 0 else None, self.data["bracket"])
            p2_name = self.get_participant_name(participants[1] if len(participants) > 1 else None, self.data["bracket"])

            match_frame = ttk.Frame(self.reset_frame)
            match_frame.pack(fill="x", pady=2)

            lbl = ttk.Label(match_frame, text="GrandFinal_Reset:", width=12, anchor='e')
            lbl.pack(side="left", padx=2)

            lbl_p1 = ttk.Label(match_frame, text=p1_name, width=15, anchor='w')
            lbl_p1.pack(side="left", padx=2)

            score1_var = tk.StringVar(value=str(reset_data.get("score1", 0)))
            entry1 = ttk.Spinbox(match_frame, textvariable=score1_var, width=5, from_=0, to=100)
            entry1.pack(side="left", padx=2)

            sep = ttk.Label(match_frame, text="-")
            sep.pack(side="left", padx=2)

            lbl_p2 = ttk.Label(match_frame, text=p2_name, width=15, anchor='w')
            lbl_p2.pack(side="left", padx=2)

            score2_var = tk.StringVar(value=str(reset_data.get("score2", 0)))
            entry2 = ttk.Spinbox(match_frame, textvariable=score2_var, width=5, from_=0, to=100)
            entry2.pack(side="left", padx=2)

            self.reset_entry_vars = (score1_var, score2_var)
            self.match_entries["GrandFinal_Reset"] = self.reset_entry_vars
        else:
            self.data["bracket"]["matches"]["grandFinal"]["GF"]["resetMatch"] = None
            if "GrandFinal_Reset" in self.match_entries:
                del self.match_entries["GrandFinal_Reset"]

    def build_results_tab(self):
        content = self.make_scrollable_tab(self.tab_results)
        ttk.Label(content, text="Results are automatically taken from the bracket order.\n"
                                "After finishing the tournament, click 'Save' to update the results display."
                                ).grid(row=0, column=0, columnspan=2, pady=10)

    def refresh_bracket_control_tab(self):
        for widget in self.tab_bracket_control.winfo_children():
            widget.destroy()

        self.match_entries = {}
        self.build_bracket_control_tab() 

    def save_all(self):
        self.data["event"]["name"] = self.entry_event_name.get()
        self.data["event"]["best_of"] = self.entry_best_of.get()
        self.data["scoreboard"]["p1"]["name"] = self.entry_p1_name.get()
        self.data["scoreboard"]["p1"]["team"] = self.entry_p1_team.get()
        self.data["scoreboard"]["p1"]["score"] = int(self.entry_p1_score.get() or 0)
        self.data["scoreboard"]["p1"]["country"] = self.entry_p1_country.get()
        self.data["scoreboard"]["p2"]["name"] = self.entry_p2_name.get()
        self.data["scoreboard"]["p2"]["team"] = self.entry_p2_team.get()
        self.data["scoreboard"]["p2"]["score"] = int(self.entry_p2_score.get() or 0)
        self.data["scoreboard"]["p2"]["country"] = self.entry_p2_country.get()

        self.data["vs"]["p1"]["name"] = self.entry_vs_p1_name.get()
        self.data["vs"]["p1"]["character"] = self.combo_vs_p1_char.get()
        self.data["vs"]["p2"]["name"] = self.entry_vs_p2_name.get()
        self.data["vs"]["p2"]["character"] = self.combo_vs_p2_char.get()

        self.data["winner"]["winner"] = self.entry_winner_name.get()
        self.data["winner"]["team"] = self.entry_winner_team.get()
        self.data["winner"]["country"] = self.entry_winner_country.get()
        self.data["winner"]["character"] = self.combo_winner_char.get()

        for i, (name_entry, team_entry, country_entry, char_combo) in enumerate(self.bracket_player_entries):
            self.data["bracket"]["players"][i]["name"] = name_entry.get()
            self.data["bracket"]["players"][i]["team"] = team_entry.get()
            self.data["bracket"]["players"][i]["country"] = country_entry.get()
            self.data["bracket"]["players"][i]["character"] = char_combo.get()

        for match_key, (score1_var, score2_var) in self.match_entries.items():
            try:
                score1 = int(score1_var.get() or 0)
                score2 = int(score2_var.get() or 0)
            except ValueError:
                score1 = 0
                score2 = 0
            winner = None
            if score1 > score2:
                winner = 1
            elif score2 > score1:
                winner = 2

            if match_key.startswith("Winners_"):
                match_id = match_key[8:]
                match_data = self.data["bracket"]["matches"]["winners"].get(match_id)
            elif match_key.startswith("Losers_"):
                match_id = match_key[7:]
                match_data = self.data["bracket"]["matches"]["losers"].get(match_id)
            elif match_key == "GrandFinal_GF":
                match_data = self.data["bracket"]["matches"]["grandFinal"]["GF"]
            elif match_key == "GrandFinal_Reset":
                match_data = self.data["bracket"]["matches"]["grandFinal"]["GF"].get("resetMatch")
                if match_data is None:
                    match_data = {
                        "participants": [
                            {"type": "match", "matchId": "WF", "outcome": "winner"},
                            {"type": "match", "matchId": "LL", "outcome": "winner"}
                        ],
                        "score1": 0, "score2": 0, "winner": None
                    }
                    self.data["bracket"]["matches"]["grandFinal"]["GF"]["resetMatch"] = match_data
            else:
                continue

            if match_data is not None:
                match_data["score1"] = score1
                match_data["score2"] = score2
                match_data["winner"] = winner

        placements = compute_placements(self.data["bracket"])
        self.data["results"]["players"] = placements

        self.refresh_bracket_control_tab()

        save_data(self.data)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = StreamMasterApp(root)
        root.mainloop()
    except Exception as e:
        import traceback
        with open("error_log.txt", "w") as f:
            traceback.print_exc(file=f)