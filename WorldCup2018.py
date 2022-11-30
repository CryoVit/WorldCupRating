from trueskill import Rating, rate_1vs1, TrueSkill
env = TrueSkill(
    mu = 1500,
    sigma = 750,
    beta = 250,
    tau = 5,
    draw_probability = 1 / 6
)
env.make_as_global()
c = {
    # Group A
    "Uruguay": Rating(),
    "Russia": Rating(),
    "Saudi Arabia": Rating(),
    "Egypt": Rating(),
    # Group B
    "Spain": Rating(),
    "Portugal": Rating(),
    "Morocco": Rating(),
    "Iran": Rating(),
    # Group C
    "France": Rating(),
    "Denmark": Rating(),
    "Peru": Rating(),
    "Australia": Rating(),
    # Group D
    "Croatia": Rating(),
    "Argentina": Rating(),
    "Nigeria": Rating(),
    "Iceland": Rating(),
    # Group E
    "Brazil": Rating(),
    "Switzerland": Rating(),
    "Serbia": Rating(),
    "Costa Rica": Rating(),
    # Group F
    "Sweden": Rating(),
    "Mexico": Rating(),
    "South Korea": Rating(),
    "Germany": Rating(),
    # Group G
    "Belgium": Rating(),
    "England": Rating(),
    "Tunisia": Rating(),
    "Panama": Rating(),
    # Group H
    "Colombia": Rating(),
    "Japan": Rating(),
    "Senegal": Rating(),
    "Poland": Rating()
}
m = {
    # match 1-48
    ("Russia", "Saudi Arabia"): (5, 0),
    ("Egypt", "Uruguay"): (0, 1),
    ("Russia", "Egypt"): (3, 1),
    ("Uruguay", "Saudi Arabia"): (1, 0),
    ("Uruguay", "Russia"): (3, 0),
    ("Saudi Arabia", "Egypt"): (2, 1),
    
    ("Morocco", "Iran"): (0, 1),
    ("Portugal", "Spain"): (3, 3),
    ("Portugal", "Morocco"): (1, 0),
    ("Iran", "Spain"): (0, 1),
    ("Iran", "Portugal"): (1, 1),
    ("Spain", "Morocco"): (2, 2),
    
    ("France", "Australia"): (2, 1),
    ("Peru", "Denmark"): (0, 1),
    ("Denmark", "Australia"): (1, 1),
    ("France", "Peru"): (1, 0),
    ("Denmark", "France"): (0, 0),
    ("Australia", "Peru"): (0, 2),
    
    ("Argentina", "Iceland"): (1, 1),
    ("Croatia", "Nigeria"): (2, 0),
    ("Argentina", "Croatia"): (0, 3),
    ("Nigeria", "Iceland"): (2, 0),
    ("Nigeria", "Argentina"): (1, 2),
    ("Iceland", "Croatia"): (1, 2),
    
    ("Costa Rica", "Serbia"): (0, 1),
    ("Brazil", "Switzerland"): (1, 1),
    ("Brazil", "Costa Rica"): (2, 0),
    ("Serbia", "Switzerland"): (1, 2),
    ("Serbia", "Brazil"): (0, 2),
    ("Switzerland", "Costa Rica"): (2, 2),
    
    ("Germany", "Mexico"): (0, 1),
    ("Sweden", "South Korea"): (1, 0),
    ("South Korea", "Mexico"): (1, 2),
    ("Germany", "Sweden"): (2, 1),
    ("South Korea", "Germany"): (2, 0),
    ("Mexico", "Sweden"): (0, 3),
    
    ("Belgium", "Panama"): (3, 0),
    ("Tunisia", "England"): (1, 2),
    ("Belgium", "Tunisia"): (5, 2),
    ("England", "Panama"): (6, 1),
    ("England", "Belgium"): (0, 1),
    ("Panama", "Tunisia"): (1, 2),
    
    ("Colombia", "Japan"): (1, 2),
    ("Poland", "Senegal"): (1, 2),
    ("Japan", "Senegal"): (2, 2),
    ("Poland", "Colombia"): (0, 3),
    ("Japan", "Poland"): (0, 1),
    ("Senegal", "Colombia"): (0, 1),
    # match 49-56
    ("France", "Argentina"): (4, 3),
    ("Uruguay", "Portugal"): (2, 1),
    ("Spain", "Russia"): (4, 5),
    ("Croatia", "Denmark"): (4, 3),
    ("Brazil", "Mexico"): (2, 0),
    ("Belgium", "Japan"): (3, 2),
    ("Sweden", "Switzerland"): (1, 0),
    ("Colombia", "England"): (4, 5),
    # match 57-60
    ("Uruguay", "France"): (0, 2),
    ("Brazil", "Belgium"): (1, 2),
    ("Sweden", "England"): (0, 2),
    ("Russia", "Croatia"): (5, 6),
    # match 61-62
    ("France", "Belgium"): (1, 0),
    ("Croatia", "England"): (2, 1),
    # match 63-64
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
}

def get_match(match_id, match, score):
    print(f"{match_id:02d}: {match[0]} {score[0]}:{score[1]} {match[1]}")
    print(f"{c[match[0]].mu:.0f} vs {c[match[1]].mu:.0f}", end = '')
    if score[0] > score[1]:
        c[match[0]], c[match[1]] = rate_1vs1(c[match[0]], c[match[1]])
    elif score[0] == score[1]:
        c[match[0]], c[match[1]] = rate_1vs1(c[match[0]], c[match[1]], drawn=True)
    else:
        c[match[1]], c[match[0]] = rate_1vs1(c[match[1]], c[match[0]])
    print(f" -> {c[match[0]].mu:.0f} vs {c[match[1]].mu:.0f}")

def get_ranking(stage, advance):
    print()
    print(f"Ranking after {stage}:")
    for index, country in enumerate(sorted(c, key=lambda x: c[x].mu, reverse=True)):
        if f[country] <= advance:
            print(f"{index + 1:02d}. {country} (F{f[country]:02d}): {c[country].mu:.0f} ± {c[country].sigma:.0f}")
    print()

# Group stage
mid = 0
for i in range(3):
    for index, (match, score) in enumerate(m.items()):
        if index >= 48:
            break
        if index % 6 == 2 * i or index % 6 == 2 * i + 1:
            mid += 1
            get_match(mid, match, score)
    get_ranking(f"{i+1}rd group stage", 32)

for index, (match, score) in enumerate(m.items()):
    if index < 48:
        continue
    mid += 1
    get_match(mid, match, score)
    if index == 55:
        get_ranking("Round of 16", 16)
    if index == 59:
        get_ranking("Quarter-finals", 8)
    if index == 63:
        get_ranking("Semi- and Finals", 4)