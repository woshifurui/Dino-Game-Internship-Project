def get_team(score):
    if score >= 50:
        return "Alpha"
    else:
        return "Beta"

team_alpha = []
team_beta = []
for i in range (10):
    print(f"\n---Entering new info for player {i+1}---")
    name = input("Enter player name:")
    score = int(input("Enter player skill score:"))
    assign_team = get_team(score)
    if assign_team == "Alpha":
        team_alpha.append(name)
    else:
        team_beta.append(name)

print("\n" + "="*20 +" FINAL ROSTERS "+ "="*20)
print("Team alpha rosters:", team_alpha)
print("Team beta rosters:", team_beta)