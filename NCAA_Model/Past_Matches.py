import pandas as pd
import sys

data = pd.read_csv("Big_Dance_CSV.csv")
teams = pd.read_csv("Teams.csv")
mop = pd.read_csv("MOP.csv")

d = {'this_team' : [], 'other_team' : [], 'won' : [], 'year' : [], 'score': [], 'region' : []}
d2 = {'year' : [], 'player' : [], 'school' : []}

for i in range(len(data.Year)):
    if data.Score1[i] > data.Score2[i]:
        d['this_team'].append(data.Team1[i])
        d['this_team'].append(data.Team2[i])
        
        d['other_team'].append(data.Team2[i])
        d['other_team'].append(data.Team1[i])
        
        d['won'].append('Win')
        d['won'].append('Lose')
        
        d['year'].append(data.Year[i])
        d['year'].append(data.Year[i])
        
        d['score'].append((data.Score1[i], data.Score2[i]))
        d['score'].append((data.Score2[i], data.Score1[i]))

        d['region'].append(data.RegionName[i])
        d['region'].append(data.RegionName[i])
    else:
        d['this_team'].append(data.Team2[i])
        d['this_team'].append(data.Team1[i])
        
        d['other_team'].append(data.Team1[i])
        d['other_team'].append(data.Team2[i])
        
        d['won'].append('Win')
        d['won'].append('Lose')
        
        d['year'].append(data.Year[i])
        d['year'].append(data.Year[i])
        
        d['score'].append((data.Score2[i], data.Score1[i]))
        d['score'].append((data.Score1[i], data.Score2[i]))

        d['region'].append(data.RegionName[i])
        d['region'].append(data.RegionName[i])

for i in range(len(mop.Year)):
    d2['year'].append(mop.Year[i])
    d2['player'].append(mop.Player[i])
    d2['school'].append(mop.School[i])
        
def all_matches():
    print("")
    for i in range(len(d['this_team'])):
        print("This Team:", d['this_team'][i], "| Other Team:", d['other_team'][i], "| Won/Lost: ", d['won'][i], "| Year:", d['year'][i])

def all_Teams():
    print("")
    for i in range(len(teams.TeamName)):
        print(teams.TeamName[i], "| First D1 Season:", teams.FirstD1Season[i], "| Last D1 Season:", teams.LastD1Season[i])

def Match_Up(team1, team2):
    print("")
    num_won = 0
    num_lost = 0
    years_won = []
    years_lost = []
    losing_score =[]
    winning_score =[]
    for i in range(len(d['this_team'])):
        if d['this_team'][i] == team1 and d['other_team'][i] == team2:
            if d['won'][i] == 'Win':
                num_won += 1
                years_won.append(d['year'][i])
                winning_score.append(d['score'][i])
            else:
                num_lost += 1
                years_lost.append(d['year'][i])
                losing_score.append(d['score'][i])
    if num_won != 0 or num_lost != 0:
        print("Since 1985", team1, "has won", num_won, "times, and lost", num_lost, "times against", team2, "in the NCAA Tournament")

        if len(years_won) > 0:
            print("")
            print("Years Won:")
            print(years_won, winning_score)
        if len(years_lost) > 0:
            print("")
            print("Years Lost:")
            print(years_lost, losing_score)
        
    else:
        print("Since 1985,", team1, "hasn't had a match-up against", team2, "in the NCAA Tournament (Check Spelling)")



def year_Champ(year):
    print("")
    for i in range(len(d['year'])):
        if year == 2018:
            print(year, "NCAA CHAMPION:", d['other_team'][-1])
            print("Played against:", d['this_team'][-1])
            print("Score:", d['score'][-2])
            break
        if d['year'][i] == (year + 1):
            print(year, "NCAA CHAMPION:", d['other_team'][i-1])
            print("Played against:", d['this_team'][i-1])
            print("Score:", d['score'][i-2])
            break

def history(team):
    champion = []
    final_loser = []
    final_four = []
    ff_winner = []
    print("")
    last = False
    found = False
    
    for i in range(len(d['this_team'])):
        if d['this_team'][i] == team and d['won'][i] == 'Win':
            found = True
            print("Year:", d['year'][i], "| Match against:", d['other_team'][i], "| Outcome: ", d['won'][i], "| Score:", d['score'][i])
            if d['region'][i] == 'Championship':
                champion.append(d['year'][i])
                final_loser.append(d['other_team'][i])
        if d['this_team'][i] == team and d['won'][i] == 'Lose':
            found = True
            print("Year:", d['year'][i], "| Match against:", d['other_team'][i], "| Outcome: ", d['won'][i], "| Score:", d['score'][i])
            if d['region'][i] == 'Final Four':
                final_four.append(d['year'][i])
                ff_winner.append(d['other_team'][i])
                
    if len(champion) > 0:
        print("")
        print("NCAA Champions in:")
        for i in range(len(champion)):
            print(champion[i], "against", final_loser[i])

    if len(final_four) > 0:
        print("")
        print("Went to Final Four in:")
        for i in range(len(final_four)):
            print(final_four[i], "losing to", ff_winner[i])
    
    if found == False:
        print(team, "has not played in the NCAA tournament since 1985")


def MOP(year):
    print("")
    for i in range(len(d2['year'])):
        if d2['year'][i] == year:
            print(d2['player'][i], "was the Most Outstanding Player in", d2['year'][i], "representing", d2['school'][i])

def helpmsg():
    print("")
    print("Options:")
    print(" --NOTE: Dataset only spans from 1985-2018")
    print(" --Type Winner Year to get Champion of the given year")
    print(" --Type MOP Year to get the Most Outstanding Player of the given year")
    print(" --Type All to get all NCAA Tournament match results")
    print(" --Type Teams to get all of the schools to have been in the NCAA Tournament")
    print(" --Type Team Name to get results of this team's past matches of NCAA Tournament")
    print(" --Type Team 1 Name Team 2 Name to get results of NCAA Tournament matches")
    print(" --NOTE: If Team Name is greater than 2 words, combine with ''")
    print(" --Type Exit to end program")
    print(" --Type help at any time to get options")

ext = False
helpmsg()
while(ext != True):
    print("")
    inpt = input("Enter: ")
    inpt = inpt.split(" ")
    i = 0
    inpt_list = []
    if inpt != ['']:
        while i < len(inpt):
            sub = inpt[i]
            if sub[0] == "'":   #Removing apostrophes for 2-Word Teams
                sub2 = inpt[i + 1]
                if sub2[-1] != "'": #Removing apostrophes for 3-Word Teams
                    strn = inpt[i] + " " + inpt[i+1] + " " + inpt[i+2]
                    length = len(strn) - 1
                    new_strn = strn[1:length]
                    inpt_list.append(new_strn)
                    i += 3
                else:
                    strn = inpt[i] + " " + inpt[i+1]
                    length = len(strn) - 1
                    new_strn = strn[1:length]
                    inpt_list.append(new_strn)
                    i += 2
            else:
                inpt_list.append(inpt[i])
                i += 1

    if len(inpt_list) == 1:
        if inpt_list[0] == 'help' or inpt_list[0] == 'Help':
            helpmsg()
        elif inpt_list[0] == 'all' or inpt_list[0] == 'All':
            all_matches()
        elif inpt_list[0] == 'teams' or inpt_list[0] == 'Teams':
            all_Teams()
        elif inpt_list[0] == 'exit' or inpt_list[0] == 'Exit':
            ext = True
        else:
            team = inpt_list[0]
            history(team)

    if len(inpt_list) == 2:
        if inpt_list[0] == 'Winner' or inpt_list[0] == "winner":
            yearC = inpt_list[1]
            yearI = int(yearC)
            if yearI > 2018 or yearI < 1985:
                print("Error: Given year is not within range")
            else:
                year_Champ(yearI)

        elif inpt_list[0] == "MOP" or inpt_list[0] == "mop":
            yearC = inpt_list[1]
            yearI = int(yearC)
            if yearI > 2018 or yearI < 1985:
                print("Error: Given year is not within range")
            else:
                MOP(yearI)
            
        else:
            team1 = inpt_list[0]
            team2 = inpt_list[1]
            Match_Up(team1, team2)

    if len(inpt_list) < 1 or len(inpt_list) > 2:
        print("Error: No teams given to compute past match-ups")
        print("")
        print("Must give proper inputs")

print("Done")
