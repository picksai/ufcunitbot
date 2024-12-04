from flask import Flask, render_template, request

app = Flask(__name__)

# Define the Fighter class to store fighter name, odds, and condition
class Fighter:
    def __init__(self, name, odds, condition="normal"):
        self.name = name
        self.odds = odds
        self.condition = condition

    def __repr__(self):
        return f"{self.name} ({self.odds}) - {self.condition}"

# Function to generate parlays based on the selected fighters
def generate_parlays(fighters, stake):
    parlays = []
    for i in range(len(fighters)):
        # For simplicity, create 2-leg parlays for each fighter with the others
        for j in range(i + 1, len(fighters)):
            parlay_fighters = [fighters[i], fighters[j]]
            parlays.append(Parlay(parlay_fighters, stake))
    return parlays

# Parlay class to calculate the payout for a parlay
class Parlay:
    def __init__(self, fighters, stake):
        self.fighters = fighters
        self.stake = stake

    def calculate_payout(self):
        total_odds = 1
        for fighter in self.fighters:
            total_odds *= fighter.odds  # Multiply the odds of each fighter in the parlay
        return round(self.stake * total_odds, 2)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        fighter_names = request.form.getlist('fighter_name')  # List of fighter names
        fighter_odds = request.form.getlist('fighter_odds')  # List of fighter odds
        fighter_conditions = request.form.getlist('fighter_condition')  # List of conditions (optional)
        stake = float(request.form.get('stake', 10))  # Default stake is 10 if not provided
        
        fighters = []
        
        # Create Fighter objects for each fighter name
        for i in range(len(fighter_names)):
            odds = float(fighter_odds[i])  # Convert odds to float
            # If no condition provided, default it to "normal"
            condition = fighter_conditions[i] if i < len(fighter_conditions) else "normal"
            fighter = Fighter(fighter_names[i], odds, condition)
            fighters.append(fighter)
        
        # Generate parlays based on selected fighters
        parlays = generate_parlays(fighters, stake)
        
        # Calculate payouts for each parlay
        payouts = [parlay.calculate_payout() for parlay in parlays]
        
        return render_template('index.html', parlays=parlays, payouts=payouts)
    
    return render_template('index.html', parlays=None, payouts=None)

if __name__ == '__main__':
    app.run(debug=True)
