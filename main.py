class Team:
    def __init__(self, name: str) -> None:
        self.name = name
        self.wins = 0
        self.losses = 0
        self.skipped = 0
        self.score_diff = 0

    def add_win(self, diff: int):
        self.wins += 1
        self.score_diff += diff

    def add_loss(self, diff: int):
        self.losses += 1
        self.score_diff -= diff

    def get_score(self) -> int:
        return self.wins + self.skipped - self.losses

    def get_diff(self) -> int:
        return self.score_diff

    def skip_round(self):
        self.skipped += 1

    def __str__(self):
        return self.name


class Match:
    def __init__(self, team1: Team, team2: Team) -> None:
        self.team1 = team1
        self.team2 = team2

    def includes_team(self, t: Team) -> bool:
        return t == self.team1 or t == self.team2

    def set_result(self, t1_score: int, t2_score: int):
        if t1_score > t2_score:
            self.team1.add_win(t1_score - t2_score)
            self.team2.add_loss(t1_score - t2_score)
        else:
            self.team1.add_loss(t2_score - t1_score)
            self.team2.add_win(t2_score - t1_score)

    def __str__(self):
        return f"{self.team1} VS {self.team2}"


class Round:
    def __init__(self) -> None:
        self.matches: list[Match] = []

    def add_match(self, t1: Team, t2: Team):
        self.matches.append(Match(t1, t2))

    def is_matched(self, t: Team) -> bool:
        return bool(list(filter(lambda match: match.includes_team(t), self.matches)))

    def are_matched(self, t1: Team, t2: Team):
        return bool(
            list(
                filter(
                    lambda match: match.includes_team(t1) and match.includes_team(t2),
                    self.matches,
                )
            )
        )

    def enter_results(self):
        for match in self.matches[1:]:
            print(f"{match.team1} - {match.team2}: ", end="")
            scores = list(map(int, input().split()))
            match.set_result(scores[0], scores[1])

    def __str__(self) -> str:
        return "\n".join(map(lambda match: str(match), self.matches))


class Game:
    def __init__(self) -> None:
        self.rounds: list[Round] = []

    def add_round(self, round: Round):
        self.rounds.append(round)

    def have_played(self, t1: Team, t2: Team):
        return bool(list(filter(lambda round: round.are_matched(t1, t2), self.rounds)))

    def __str__(self) -> str:
        return "\n".join(map(lambda round: str(round), self.rounds))


n_rounds = 4
n_teams = 13
teams = [
    Team("Ghostbusters"),
    Team("Dino"),
    Team("Tåg"),
    Team("Dunderhonung"),
    Team("Suntrip"),
    Team("MLRU"),
    Team("Guldgrävarna"),
    Team("Byggmyndigheten"),
    Team("Pineapple på pizza"),
    Team("DASS"),
    Team("D-tech-tiverna"),
    Team("Pepp"),
    Team("Stab"),
]
team_sitout = Team("-")


def write_results(filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        header = (
            "TEAM NAME".ljust(20)
            + " | "
            + "SCORE"
            + " | "
            + "DIFF"
            + " | "
            + "WINS"
            + " | "
            + "LOSSES"
            + "\n"
        )
        f.write(header)
        for team in teams:
            result = (
                team.name.ljust(20)
                + " | "
                + str(team.get_score()).ljust(len("SCORE"))
                + " | "
                + str(team.get_diff()).ljust(len("DIFF"))
                + " | "
                + str(team.wins).ljust(len("WINS"))
                + " | "
                + str(team.losses).ljust(len("LOSSES"))
                + "\n"
            )
            f.write(result)


game = Game()
for n in range(n_rounds):
    round = Round()

    # Worst team that has never skipped a round skips this round
    team_skipped = None
    for team in reversed(teams):
        if team.skipped == 0:
            round.add_match(team, team_sitout)
            team.skip_round()
            break

    for i, t1 in enumerate(teams):
        if round.is_matched(t1):
            continue

        for j in range(i + 1, len(teams)):
            t2 = teams[j]

            if not (round.is_matched(t2) or game.have_played(t1, t2)):
                round.add_match(t1, t2)
                break

        if not round.is_matched(t1):
            raise Exception("Well what do we do now???")

    # Print matchings
    print("=" * 20)
    print("ROUND", n + 1)
    print(round)

    # Enter results
    print("-" * 8, "ENTER SCORE", "-" * 8)
    round.enter_results()

    # Sort by score, then diff, then wins
    teams.sort(key=lambda team: team.wins, reverse=True)
    teams.sort(key=lambda team: team.get_diff(), reverse=True)
    teams.sort(key=lambda team: team.get_score(), reverse=True)

    # Write standings to file
    write_results(f"round{n+1}.txt")

    game.add_round(round)
