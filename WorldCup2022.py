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
    ("United States", "Wales"): (1, 1),
    ("Argentina", "Saudi Arabia"): (1, 2),
    ("Denmark", "Tunisia"): (0, 0),
    ("Mexico", "Poland"): (0, 0),
    ("France", "Australia"): (4, 1),
    ("Morocco", "Croatia"): (0, 0),
    ("Germany", "Japan"): (1, 2),
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

def get_ranking(stage):
    print()
    print(f"Ranking after {stage}:")
    for index, country in enumerate(sorted(c, key=lambda x: c[x].mu, reverse=True)):
        print(f"{index + 1:02d}. {country}: {c[country].mu:.0f} ± {c[country].sigma:.0f}")
    print()
    
for index, (match, score) in enumerate(m.items()):
    get_match(index + 1, match, score)

get_ranking("1st Group Stage")