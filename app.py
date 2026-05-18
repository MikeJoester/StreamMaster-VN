from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

CHARACTERS = [
    "Alisa", "Anna", "Armor King", "Asuka", "Azucena", "Bryan", "Claudio", "Clive",
    "Devil Jin", "Dragunov", "Eddy", "Fahkumram", "Feng", "Heihachi", "Hwoarang",
    "Jack-8", "Jin", "Jun", "Kazuya", "King", "Kuma", "Lars", "Law", "Lee", "Leo",
    "Leroy", "Lidia", "Lili", "Miary Zo", "Nina", "Panda", "Paul", "Raven", "Reina",
    "Shaheen", "Steve", "Victor", "Xiaoyu", "Yoshimitsu", "Zafina"
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

@app.route('/')
def index():
    return render_template('index.html', characters=CHARACTERS)

@app.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard/scoreboard.html')

@app.route('/vs')
def vs():
    return render_template('vs/vs.html')

@app.route('/winner')
def winner():
    return render_template('winner/winner.html')

@app.route('/bracket')
def bracket():
    return render_template('bracket/bracket.html')

@app.route('/results')
def results():
    return render_template('results/results.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

@app.route('/api/data', methods=['POST'])
def update_data():
    new_data = request.json
    
    # Compute placements if bracket data is updated
    if "bracket" in new_data:
        placements = compute_placements(new_data["bracket"])
        new_data["results"]["players"] = placements
        
    save_data(new_data)
    return jsonify({"status": "success"})

# Serve data.json at the root
@app.route('/data.json')
def serve_data():
    return send_from_directory('.', 'data.json')

# Serve assets (images, characters, fonts) from the root or subfolders
@app.route('/<path:filename>')
def serve_static(filename):
    # Try serving from root first (for images/, characters/, etc.)
    if os.path.exists(os.path.join('.', filename)):
        return send_from_directory('.', filename)
    # If not found, it might be in templates/ (though routes above handle most)
    if os.path.exists(os.path.join('templates', filename)):
        return send_from_directory('templates', filename)
    return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
