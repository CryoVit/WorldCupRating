from trueskill import Rating, rate_1vs1, TrueSkill

env = TrueSkill(
    mu = 1500,
    sigma = 750,
    beta = 250,
    tau = 5,
    draw_probability = 1 / 6
)

g = (
    ("Qatar", "Ecuador", "Senegal", "Netherlands"),
    ("England", "Iran", "United States", "Wales"),
    ("Argentina", "Saudi Arabia", "Mexico", "Poland"),
    ("France", "Australia", "Denmark", "Tunisia"),
    ("Spain", "Costa Rica", "Germany", "Japan"),
    ("Belgium", "Canada", "Morocco", "Croatia"),
    ("Brazil", "Serbia", "Switzerland", "Cameroon"),
    ("Portugal", "Ghana", "Uruguay", "Korea Republic"),
 ) # groups

gn = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H') # group names

m = {
    # 1st Group Stage: 1-16
    ("Qatar", "Ecuador"): (0, 2),
    ("Senegal", "Netherlands"): (0, 2),
    ("England", "Iran"): (6, 2),
    ("United States", "Wales"): (1, 1), # 4
    ("Argentina", "Saudi Arabia"): (1, 2),
    ("Denmark", "Tunisia"): (0, 0),
    ("Mexico", "Poland"): (0, 0),
    ("France", "Australia"): (4, 1), # 8
    ("Morocco", "Croatia"): (0, 0),
    ("Germany", "Japan"): (1, 2),
    ("Spain", "Costa Rica"): (7, 0),
    ("Belgium", "Canada"): (1, 0), # 12
    ("Switzerland", "Cameroon"): (1, 0),
    ("Uruguay", "Korea Republic"): (0, 0),
    ("Portugal", "Ghana"): (3, 2),
    ("Brazil", "Serbia"): (2, 0), # 16
    # 2nd Group Stage: 17-32
    ("Wales", "Iran"): (0, 2),
    ("Qatar", "Senegal"): (1, 3),
    ("Netherlands", "Ecuador"): (1, 1),
    ("United States", "England"): (0, 0), # 20
    ("Tunisia", "Australia"): (0, 1),
    ("Poland", "Saudi Arabia"): (2, 0),
    ("France", "Denmark"): (2, 1),
    ("Argentina", "Mexico"): (2, 0), # 24
    ("Japan", "Costa Rica"): (0, 1),
    ("Belgium", "Morocco"): (0, 2),
    ("Croatia", "Canada"): (4, 1),
    ("Spain", "Germany"): (1, 1), # 28
    ("Cameroon", "Serbia"): (3, 3),
    ("Korea Republic", "Ghana"): (2, 3),
    ("Brazil", "Switzerland"): (1, 0),
    ("Portugal", "Uruguay"): (2, 0), # 32
    # 3rd Group Stage: 33-48
    ("Ecuador", "Senegal"): (1, 2),
    ("Netherlands", "Qatar"): (2, 0),
    ("Wales", "England"): (0, 3),
    ("Iran", "United States"): (0, 1), # 36
    ("Tunisia", "France"): (1, 0),
    ("Australia", "Denmark"): (1, 0),
    ("Poland", "Argentina"): (0, 2),
    ("Saudi Arabia", "Mexico"): (1, 2), # 40
    ("Croatia", "Belgium"): (0, 0),
    ("Canada", "Morocco"): (1, 2),
    ("Japan", "Spain"): (2, 1),
    ("Costa Rica", "Germany"): (2, 4), # 44
    ("Korea Republic", "Portugal"): (2, 1),
    ("Ghana", "Uruguay"): (0, 2),
    ("Cameroon", "Brazil"): (1, 0),
    ("Serbia", "Switzerland"): (0, 1), # 48
    # Round of 16: 49-56
    ("Netherlands", "United States"): (3, 1),
    ("Argentina", "Australia"): (2, 1), # 50
    ("France", "Poland"): (3, 1),
    ("England", "Senegal"): (3, 0), # 52
    ("Japan", "Croatia"): (1 + 1, 1 + 3),
    ("Brazil", "Korea Republic"): (4, 1), # 54
    ("Morocco", "Spain"): (0 + 3, 0 + 0),
    ("Portugal", "Switzerland"): (6, 1), # 56
    # Quarterfinals: 57-60
    ("Croatia", "Brazil"): (1 + 4, 1 + 2),
    ("Netherlands", "Argentina"): (2 + 3, 2 + 4), # 58
    ("Morocco", "Portugal"): (1, 0),
    ("England", "France"): (1, 2), # 60
    # Semifinals: 61-62
    ("Argentina", "Croatia"): (3, 0),
    ("France", "Morocco"): (2, 0), # 62
} # matches

c = {} # countries

r = {} # rating

gs = {} # group score

gd = {} # goal difference

a = set() # advance to next round

new_a = set()

lw = set() # last win or loss

rt = lambda x: x.mu - 2 * x.sigma

def get_match(mid, match, score):
    print(f"{mid:02d}: {match[0]} {score[0]}:{score[1]} {match[1]}")
    print(f"{rt(c[match[0]]):.0f} vs {rt(c[match[1]]):.0f}", end = '')
    if score[0] > score[1]:
        c[match[0]], c[match[1]] = rate_1vs1(c[match[0]], c[match[1]])
        gs[match[0]] += 3
        lw.add(match[0])
    elif score[0] == score[1]:
        c[match[0]], c[match[1]] = rate_1vs1(c[match[0]], c[match[1]], drawn=True)
        gs[match[0]] += 1
        gs[match[1]] += 1
    else:
        c[match[1]], c[match[0]] = rate_1vs1(c[match[1]], c[match[0]])
        gs[match[1]] += 3
        lw.add(match[1])
    gd[match[0]] += score[0] - score[1]
    gd[match[1]] += score[1] - score[0]
    print(f" -> {rt(c[match[0]]):.0f} vs {rt(c[match[1]]):.0f}")

def get_ranking(stage, sid):
    global a
    print()
    print(f"Ranking after {stage}:")
    
    if sid <= 2:
        for index, country in enumerate(sorted(c, key=lambda x: rt(c[x]), reverse=True)):
            if sid: # sid = 1, 2
                print(f"({r[country]:02d}->)", end = '')
            print(f"{index + 1:02d}. {country}: {c[country].mu:.0f} - {2 * c[country].sigma:.0f}")
            r[country] = index + 1
        print()
        print(f"Group Scoreboard after {stage}:")
        for index, group in enumerate(g):
            board = sorted([(country, gs[country], gd[country]) for country in group], key=lambda x: (x[1], x[2]), reverse=True)
            if sid == 2 and index == 7: # Korea Republic > Uruguay
                board[1], board[2] = board[2], board[1]
            print(f"Group {gn[index]}:")
            for rank, country in enumerate(board):
                if sid == 2:
                    if rank < 2:
                        a.add(country[0])
                        print("[+]", end = '\t')
                    else:
                        print("[-]", end = '\t')
                else:
                    print('', end = '\t')
                print(f"{country[0]} {country[1]}({country[2]:+d})")
        print()
        lw.clear()
    
    else:
        for index, country in enumerate(sorted(c, key=lambda x: rt(c[x]), reverse=True)):
            if country in a:
                if country in lw:
                    print("[+]", end = '\t')
                    new_a.add(country)
                else:
                    print("[-]", end = '\t')
                print(f"({r[country]:02d}->)", end = '')
                print(f"{index + 1:02d}. {country}: {c[country].mu:.0f} - {2 * c[country].sigma:.0f}")
            r[country] = index + 1
        print()
        a.clear()
        a = new_a
        lw.clear()
    
if __name__ == "__main__":
    env.make_as_global()
    for group in g:
        for country in group:
            c[country] = Rating()
            gs[country] = 0
            gd[country] = 0
    for index, (match, score) in enumerate(m.items()):
        get_match(index + 1, match, score)
        if index == 15:
            get_ranking("1st Group Stage", 0)
        if index == 31:
            get_ranking("2nd Group Stage", 1)
        if index == 47:
            get_ranking("3rd Group Stage", 2)
        if index == 55:
            get_ranking("Round of 16", 3)
        if index == 59:
            get_ranking("Quarterfinals", 4)
# print(a)