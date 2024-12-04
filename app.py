from flask import Flask, render_template, request
app = Flask(__name__)

class Fighter:
    def __init__(self, name, odds, condition="normal"):
        self.name = name
        self.odds = odds
        self.condition = condition  # "normal", "mentally unprepared", "injured", etc.

    def update_condition(self, new_condition):
        self.condition = new_condition

    def adjusted_odds(self):
        """ Adjust odds based on condition. """
        if self.condition == "mentally unprepared":
            return self.odds * 0.9  # Decrease odds if the fighter is mentally unprepared
        return self.odds

class Bet:
    def __init__(self, fighters, stake, type_of_bet="parlay"):
        self.fighters = fighters
        self.stake = stake
        self.type_of_bet = type_of_bet

    def calculate_payout(self):
        odds = 1
        for fighter in self.fighters:
            odds *= fighter.adjusted_odds()
        return self.stake * odds

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Getting the user inputs for fighters and conditions
        fighter_names = request.form.getlist('fighter_name')  # List of fighter names
        conditions = request.form.getlist('condition')  # List of conditions
        stake = float(request.form.get('stake', 10))  # Default stake is 10 if not provided
        
        fighters = []
        
        for i in range(len(fighter_names)):
            # Here we just assume odds, you can modify this to get live data
            odds = 1.5  # Placeholder odds for simplicity
            fighter = Fighter(fighter_names[i], odds, conditions[i])
            fighters.append(fighter)
        
        bet = Bet(fighters, stake)  # Create a bet with the selected fighters
        payout = bet.calculate_payout()
        
        return render_template('index.html', payout=payout)
    
    return render_template('index.html', payout=None)

if __name__ == '__main__':
    app.run(debug=True)
