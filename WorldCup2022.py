from trueskill import Rating, rate_1vs1, TrueSkill
# from random import random
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
    "Qatar": Rating(),
    "Ecuador": Rating(),
    "Senegal": Rating(),
    "Netherlands": Rating(),
    # Group B
    "England": Rating(),
    "Iran": Rating(),
    "United States": Rating(),
    "Wales": Rating(),
    # Group C
    "Argentina": Rating(),
    "Saudi Arabia": Rating(),
    "Mexico": Rating(),
    "Poland": Rating(),
    # Group D
    "France": Rating(),
    "Australia": Rating(),
    "Denmark": Rating(),
    "Tunisia": Rating(),
    # Group E
    "Spain": Rating(),
    "Costa Rica": Rating(),
    "Germany": Rating(),
    "Japan": Rating(),
    # Group F
    "Belgium": Rating(),
    "Canada": Rating(),
    "Morocco": Rating(),
    "Croatia": Rating(),
    # Group G
    "Brazil": Rating(),
    "Serbia": Rating(),
    "Switzerland": Rating(),
    "Cameroon": Rating(),
    # Group H
    "Portugal": Rating(),
    "Ghana": Rating(),
    "Uruguay": Rating(),
    "Korea Republic": Rating(),
}
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

r = {}

def get_ranking(stage, cached = True):
    print()
    print(f"Ranking after {stage}:")
    for index, country in enumerate(sorted(c, key=lambda x: c[x].mu, reverse=True)):
        if cached:
            print(f"({r[country]:02d} ->)", end = '')
        print(f"{index + 1:02d}. {country}: {c[country].mu:.0f} ± {c[country].sigma:.0f}")
        r[country] = index + 1
    print()
    
for index, (match, score) in enumerate(m.items()):
    get_match(index + 1, match, score)
    if index == 15:
        get_ranking("1st Group Stage", cached = False)
    if index == 31:
        get_ranking("2nd Group Stage")