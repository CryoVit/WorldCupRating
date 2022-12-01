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
} # matches

c = {} # countries

r = {} # rating

gs = {} # group score

gd = {} # goal difference

a = set() # advance to next round

def get_match(mid, match, score):
    print(f"{mid:02d}: {match[0]} {score[0]}:{score[1]} {match[1]}")
    print(f"{c[match[0]].mu:.0f} vs {c[match[1]].mu:.0f}", end = '')
    if score[0] > score[1]:
        c[match[0]], c[match[1]] = rate_1vs1(c[match[0]], c[match[1]])
        gs[match[0]] += 3
    elif score[0] == score[1]:
        c[match[0]], c[match[1]] = rate_1vs1(c[match[0]], c[match[1]], drawn=True)
        gs[match[0]] += 1
        gs[match[1]] += 1
    else:
        c[match[1]], c[match[0]] = rate_1vs1(c[match[1]], c[match[0]])
        gs[match[1]] += 3
    gd[match[0]] += score[0] - score[1]
    gd[match[1]] += score[1] - score[0]
    print(f" -> {c[match[0]].mu:.0f} vs {c[match[1]].mu:.0f}")

def get_ranking(stage, sid):
    print()
    print(f"Ranking after {stage}:")
    for index, country in enumerate(sorted(c, key=lambda x: c[x].mu, reverse=True)):
        if sid:
            print(f"({r[country]:02d}->)", end = '')
        print(f"{index + 1:02d}. {country}: {c[country].mu:.0f}")
        r[country] = index + 1
    print()
    if sid <= 2:
        print(f"Group Scoreboard after {stage}:")
        for index, group in enumerate(g):
            board = sorted([(country, gs[country], gd[country]) for country in group], key=lambda x: (x[1], x[2]), reverse=True)
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

    get_ranking("3rd Group Stage", 2)