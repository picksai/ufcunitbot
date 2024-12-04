from flask import Flask, render_template, request
import itertools

app = Flask(__name__)

class Fighter:
    def __init__(self, name, odds, condition="normal"):
        self.name = name
        self.odds = odds
        self.condition = condition

    def adjusted_odds(self):
        """ Adjust odds based on the fighter's condition """
        if self.condition == "mentally unprepared":
            return self.odds * 0.9  # Decrease odds if mentally unprepared
        return self.odds

class Bet:
    def __init__(self, fighters, stake):
        self.fighters = fighters
        self.stake = stake

    def calculate_payout(self):
        """ Calculate the payout for this bet (parlay) """
        odds = 1
        for fighter in self.fighters:
            odds *= fighter.adjusted_odds()
        return self.stake * odds

    def __repr__(self):
        return f"Parlay with {len(self.fighters)} fighters, Payout: ${self.calculate_payout()}"

def generate_parlays(fighters, stake):
    """ Generate all possible parlays (combinations) from a list of fighters """
    parlays = []
    # Generate parlays of different sizes (2-leg parlays, 3-leg parlays, etc.)
    for r in range(2, len(fighters) + 1):  # Start from 2 fighters up to all fighters
        combinations = itertools.combinations(fighters, r)
        for combo in combinations:
            bet = Bet(list(combo), stake)
            parlays.append(bet)
    return parlays

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        fighter_names = request.form.getlist('fighter_name')  # List of fighter names
        fighter_odds = request.form.getlist('fighter_odds')  # List of fighter odds
        fighter_conditions = request.form.getlist('fighter_condition')  # List of conditions
        stake = float(request.form.get('stake', 10))  # Default stake is 10 if not provided
        
        fighters = []
        
        for i in range(len(fighter_names)):
            odds = float(fighter_odds[i])  # Convert odds to float
            fighter = Fighter(fighter_names[i], odds, fighter_conditions[i])
            fighters.append(fighter)
        
        # Generate parlays based on selected fighters
        parlays = generate_parlays(fighters, stake)
        
        # Calculate payouts for each parlay
        payouts = [parlay.calculate_payout() for parlay in parlays]
        
        return render_template('index.html', parlays=parlays, payouts=payouts)
    
    return render_template('index.html', parlays=None, payouts=None)

if __name__ == '__main__':
    app.run(debug=True)
