from trueskill import Rating, rate_1vs1, TrueSkill

env = TrueSkill(
    mu = 1500,
    sigma = 750,
    beta = 250,
    tau = 5,
    draw_probability = 1 / 6
)

g = (
    ("Uruguay", "Russia", "Saudi Arabia", "Egypt"),
    ("Spain", "Portugal", "Morocco", "Iran"),
    ("France", "Denmark", "Peru", "Australia"),
    ("Croatia", "Argentina", "Nigeria", "Iceland"),
    ("Brazil", "Switzerland", "Serbia", "Costa Rica"),
    ("Sweden", "Mexico", "South Korea", "Germany"),
    ("Belgium", "England", "Tunisia", "Panama"),
    ("Colombia", "Japan", "Senegal", "Poland")
) # groups

gn = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H') # group names

m = {
    # 1st Group Stage
    ("Russia", "Saudi Arabia"): (5, 0),
    ("Egypt", "Uruguay"): (0, 1),
    ("Morocco", "Iran"): (0, 1),
    ("Portugal", "Spain"): (3, 3),
    ("France", "Australia"): (2, 1),
    ("Peru", "Denmark"): (0, 1),
    ("Argentina", "Iceland"): (1, 1),
    ("Croatia", "Nigeria"): (2, 0),
    ("Costa Rica", "Serbia"): (0, 1),
    ("Brazil", "Switzerland"): (1, 1),
    ("Germany", "Mexico"): (0, 1),
    ("Sweden", "South Korea"): (1, 0),
    ("Belgium", "Panama"): (3, 0),
    ("Tunisia", "England"): (1, 2),
    ("Colombia", "Japan"): (1, 2),
    ("Poland", "Senegal"): (1, 2),
    # 2nd Group Stage
    ("Russia", "Egypt"): (3, 1),
    ("Uruguay", "Saudi Arabia"): (1, 0),
    ("Portugal", "Morocco"): (1, 0),
    ("Iran", "Spain"): (0, 1),
    ("Denmark", "Australia"): (1, 1),
    ("France", "Peru"): (1, 0),
    ("Argentina", "Croatia"): (0, 3),
    ("Nigeria", "Iceland"): (2, 0),
    ("Brazil", "Costa Rica"): (2, 0),
    ("Serbia", "Switzerland"): (1, 2),
    ("South Korea", "Mexico"): (1, 2),
    ("Germany", "Sweden"): (2, 1),
    ("Belgium", "Tunisia"): (5, 2),
    ("England", "Panama"): (6, 1),
    ("Japan", "Senegal"): (2, 2),
    ("Poland", "Colombia"): (0, 3),
    # 3rd Group Stage
    ("Uruguay", "Russia"): (3, 0),
    ("Saudi Arabia", "Egypt"): (2, 1),
    ("Iran", "Portugal"): (1, 1),
    ("Spain", "Morocco"): (2, 2),
    ("Denmark", "France"): (0, 0),
    ("Australia", "Peru"): (0, 2),
    ("Nigeria", "Argentina"): (1, 2),
    ("Iceland", "Croatia"): (1, 2),
    ("Serbia", "Brazil"): (0, 2),
    ("Switzerland", "Costa Rica"): (2, 2),
    ("South Korea", "Germany"): (2, 0),
    ("Mexico", "Sweden"): (0, 3),
    ("England", "Belgium"): (0, 1),
    ("Panama", "Tunisia"): (1, 2),
    ("Japan", "Poland"): (0, 1),
    ("Senegal", "Colombia"): (0, 1),
    # Round of 16
    ("France", "Argentina"): (4, 3),
    ("Uruguay", "Portugal"): (2, 1),
    ("Spain", "Russia"): (4, 5),
    ("Croatia", "Denmark"): (4, 3),
    ("Brazil", "Mexico"): (2, 0),
    ("Belgium", "Japan"): (3, 2),
    ("Sweden", "Switzerland"): (1, 0),
    ("Colombia", "England"): (4, 5),
    # Quarter Finals
    ("Uruguay", "France"): (0, 2),
    ("Brazil", "Belgium"): (1, 2),
    ("Sweden", "England"): (0, 2),
    ("Russia", "Croatia"): (5, 6),
    # Semi Finals
    ("France", "Belgium"): (1, 0),
    ("Croatia", "England"): (2, 1),
    # Final
    ("Belgium", "England"): (2, 0),
    ("France", "Croatia"): (4, 2)
}

f = {
    "France": 1,
    "Croatia": 2,
    "Belgium": 3,
    "England": 4,
    "Uruguay": 5,
    "Brazil": 6,
    "Sweden": 7,
    "Russia": 8,
    "Colombia": 9,
    "Spain": 10,
    "Denmark": 11,
    "Mexico": 12,
    "Portugal": 13,
    "Switzerland": 14,
    "Japan": 15,
    "Argentina": 16,
    "Senegal": 17,
    "Iran": 18,
    "South Korea": 19,
    "Peru": 20,
    "Nigeria": 21,
    "Serbia": 22,
    "Germany": 22,
    "Tunisia": 24,
    "Poland": 25,
    "Saudi Arabia": 26,
    "Morocco": 27,
    "Australia": 28,
    "Iceland": 28,
    "Costa Rica": 28,
    "Egypt": 31,
    "Panama": 31
} # final ranking

c = {} # countries

r = {} # rating

gs = {} # group score

gd = {} # goal difference

a = set() # advance to next round

lim = (32, 32, 32, 16, 8, 4, 4)

rt = lambda x: x.mu - 2 * x.sigma

def get_match(mid, match, score):
    print(f"{mid:02d}: {match[0]} {score[0]}:{score[1]} {match[1]}")
    print(f"{rt(c[match[0]]):.0f} vs {rt(c[match[1]]):.0f}", end = '')
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
    print(f" -> {rt(c[match[0]]):.0f} vs {rt(c[match[1]]):.0f}")

def get_ranking(stage, sid):
    print()
    print(f"Ranking after {stage}:")
    for index, country in enumerate(sorted(c, key=lambda x: rt(c[x]), reverse=True)):
        if f[country] > lim[sid]:
            continue
        if sid:
            print(f"({r[country]:02d}->)", end = '')
        print(f"{index + 1:02d}. {country}: {c[country].mu:.0f} - {2 * c[country].sigma:.0f}")
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
        if index == 47:
            get_ranking("3rd Group Stage", 2)
        if index == 55:
            get_ranking("Round of 16", 3)
        if index == 59:
            get_ranking("Quarter Finals", 4)
        if index == 61:
            get_ranking("Semi Finals", 5)
        if index == 63:
            get_ranking("Final", 6)