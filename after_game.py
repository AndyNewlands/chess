def calculateNewElo(result, userRating, botRating):
    if result == 'User wins':
        if botRating > userRating:
            userRating = userRating + 50
        elif userRating > botRating:
            userRating = userRating + 10
        else:
            userRating = userRating + 25

    elif result == "Computer wins":
        if botRating > userRating:
            userRating = userRating - 10
        elif userRating > botRating:
            userRating = userRating - 50
        else:
            userRating = userRating - 25

    else:
        if botRating > userRating:
            userRating = userRating + 10
        elif userRating > botRating:
            userRating = userRating - 10
        else:
            pass

    userRating = isEloValid(userRating)
    return userRating

def isEloValid(rating):
    if rating > 3000:
        rating = 3000
    elif rating <= 0:
        rating = 0
    else:
        pass
    return rating

def calculateWinPercentage(result, current_games, current_won):
    initial_w_percent = (current_won / current_games) * 100
    initial_w_percent = round(initial_w_percent, 1)
    if result == "User wins":
        current_games = current_games + 1
        current_won = current_won + 1
        new_w_percent = (current_won / current_games) * 100
        new_w_percent = round(new_w_percent, 1)
        if new_w_percent > 100:
            print("Invalid percentage")
        elif new_w_percent == initial_w_percent:
            print("Win percentage has remained the same")
        else:
            print("Win percentage has increased from", initial_w_percent, "% to", new_w_percent, "%")
        initial_w_percent = new_w_percent
    else:
        current_games = current_games + 1
        new_w_percent = (current_won / current_games) * 100
        new_w_percent = round(new_w_percent, 1)
        if new_w_percent > 100:
            print("Invalid percentage")
        elif new_w_percent == initial_w_percent:
            print("Win percentage has remained the same")
        else:
            print("Win percentage has decreased from", initial_w_percent, "% to", new_w_percent, "%")
        initial_w_percent = new_w_percent

def calculateLosePercentage(result, current_games, current_lost):
    initial_l_percent = (current_lost / current_games) * 100
    initial_l_percent = round(initial_l_percent, 1)
    if result == "Computer wins":
        current_games = current_games + 1
        current_lost = current_lost + 1
        new_l_percent = (current_lost / current_games) * 100
        new_l_percent = round(new_l_percent, 1)
        if new_l_percent > 100:
            print("Invalid percentage")
        elif new_l_percent == initial_l_percent:
            print("Lose percentage has remained the same")
        else:
            print("Lose percentage has increased from", initial_l_percent, "% to", new_l_percent, "%")
        initial_l_percent = new_l_percent
    else:
        current_games = current_games + 1
        new_l_percent = (current_lost / current_games) * 100
        new_l_percent = round(new_l_percent, 1)
        if new_l_percent > 100:
            print("Invalid percentage")
        elif new_l_percent == initial_l_percent:
            print("Lose percentage has remained the same")
        else:
            print("Lose percentage has decreased from", initial_l_percent, "% to", new_l_percent, "%")
        initial_l_percent = new_l_percent

def calculateDrawPercentage(result, current_games, current_lost, current_won):
    current_drawn = current_games - (current_lost + current_won)
    initial_d_percent = (current_drawn / current_games) * 100
    initial_d_percent = round(initial_d_percent, 1)
    if result == "Stalemate":
        current_games = current_games + 1
        current_drawn = current_drawn + 1
        new_d_percent = (current_drawn / current_games) * 100
        new_d_percent = round(new_d_percent, 1)
        if new_d_percent > 100:
            print("Invalid percentage")
        elif new_d_percent == initial_d_percent:
            print("Draw percentage has remained the same")
        else:
            print("Draw percentage has increased from", initial_d_percent, "% to", new_d_percent, "%")
        initial_d_percent = new_d_percent
    else:
        current_games = current_games + 1
        new_d_percent = (current_drawn / current_games) * 100
        new_d_percent = round(new_d_percent, 1)
        if new_d_percent > 100:
            print("Invalid percentage")
        elif new_d_percent == initial_d_percent:
            print("Draw percentage has remained the same")
        else:
            print("Draw percentage has decreased from", initial_d_percent, "% to", new_d_percent, "%")
        initial_d_percent = new_d_percent


#user_score = int(input("User Elo rating: "))
#bot_score = int(input("Bot Elo rating: "))
outcome = input("Result: ")
#print(calculateNewElo(outcome, user_score, bot_score))

gamesPlayed = int(input("Games Played (before match): "))
gamesWon = int(input("Games Won (before match): "))
gamesLost = int(input("Games Lost (before match): "))

valid = True
while valid == True:
    if gamesWon < 0 or gamesPlayed < 0:
        print("Invalid inputs")
        gamesPlayed = int(input("Games Played (before match): "))
        gamesWon = int(input("Games Lost (before match): "))
    else:
        valid = False

    games_not_drawn = gamesWon + gamesLost
    if games_not_drawn > gamesPlayed:
        print("Invalid inputs")
        outcome = input("Result: ")
        gamesPlayed = int(input("Games Played (before match): "))
        gamesWon = int(input("Games Won (before match): "))
        gamesLost = int(input("Games Lost (before match): "))
    else:
        valid = False

#calculateWinPercentage(outcome, gamesPlayed, gamesWon)
#calculateLosePercentage(outcome, gamesPlayed, gamesLost)
calculateDrawPercentage(outcome, gamesPlayed, gamesLost, gamesWon)
