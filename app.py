from flask import Flask, render_template, request
from itertools import combinations

app = Flask(__name__)

def generate_parlays(fighters, odds):
    """
    Generate all possible parlay combinations.
    
    :param fighters: List of fighter names
    :param odds: List of corresponding fighter odds
    :return: List of parlay combinations with payouts
    """
    parlays = []
    payouts = []
    
    # Combine fighters and odds into a dictionary
    picks = dict(zip(fighters, odds))
    
    # Generate 2-fighter parlays
    for r in range(2, min(len(fighters) + 1, 4)):  # Limit to 3-fighter parlays max
        for combo in combinations(fighters, r):
            parlay_odds = 1
            parlay_fighters = []
            
            for fighter in combo:
                fighter_index = fighters.index(fighter)
                parlay_odds *= odds[fighter_index]
                parlay_fighters.append(f"{fighter} ({odds[fighter_index]})")
            
            parlays.append(' + '.join(parlay_fighters))
            payouts.append(round(parlay_odds, 2))
    
    return parlays, payouts

@app.route('/', methods=['GET', 'POST'])
def index():
    parlays = None
    payouts = None
    
    if request.method == 'POST':
        # Parse input
        fighter_names = [name.strip() for name in request.form['fighter_name'].split(',')]
        fighter_odds = [float(odd.strip()) for odd in request.form['fighter_odds'].split(',')]
        
        # Optional: handle conditions (not used in this version)
        # conditions = request.form['fighter_condition'].split(',') if request.form['fighter_condition'] else []
        
        stake = float(request.form['stake'])
        
        # Generate parlays
        parlays, payouts = generate_parlays(fighter_names, fighter_odds)
        
        # Calculate actual payouts based on stake
        payouts = [round(stake * payout, 2) for payout in payouts]
    
    return render_template('index.html', parlays=parlays, payouts=payouts)

if __name__ == '__main__':
    app.run(debug=True)
