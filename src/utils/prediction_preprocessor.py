import pandas as pd
import numpy as np
import soccerdata as sd


class EPLMatchPredictorPreprocessor:

    def __init__(self, seasons, league="ENG-Premier League"):
        self.seasons = seasons
        self.league = league
        self.df = None

        self.input_features = [
            'home_shots_on_target_avg_last5',
            'away_shots_on_target_avg_last5',
            'home_shots_avg_last5',
            'away_shots_avg_last5',
            'home_team_goals_conceded_avg_last5',
            'away_team_goals_conceded_avg_last5',
            'home_goals_avg_last5',
            'away_goals_avg_last5',
            'home_points_last5_matches',
            'away_points_last5_matches',
            'points_diff_last5',
            'goal_diff_avg5',
            'shots_diff_avg5',
            'x_defense_diff',
            'home_advantage',
            'shots_on_target_diff_avg5'
        ]

    # -------------------------------
    # LOAD & PREPARE DATA
    # -------------------------------
    def load_data(self):
        dfs = []
        for season in self.seasons:
            mh = sd.MatchHistory(leagues=self.league, seasons=season)
            dfs.append(mh.read_games())

        df = pd.concat(dfs, ignore_index=True)

        df = df[[
            "date", "home_team", "away_team",
            "FTHG", "FTAG",
            "HS", "AS", "HST", "AST"
        ]].copy()

        df.rename(columns={
            "FTHG": "home_goals",
            "FTAG": "away_goals",
            "HS": "home_shots",
            "AS": "away_shots",
            "HST": "home_shots_on_target",
            "AST": "away_shots_on_target",
        }, inplace=True)

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        self.df = df

    # -------------------------------
    # LAST 5 MATCHES (HOME + AWAY)
    # -------------------------------
    def _get_last5_matches(self, team, before_date):
        df = self.df[
            ((self.df["home_team"] == team) | (self.df["away_team"] == team)) &
            (self.df["date"] < before_date)
        ].sort_values("date").tail(5)

        if len(df) < 5:
            raise ValueError(f"Not enough history for {team}")

        return df

    # -------------------------------
    # TEAM FORM (MEANS)
    # -------------------------------
    def _compute_team_form(self, matches, team):
        goals, shots, shots_ot, conceded = [], [], [], []

        for _, r in matches.iterrows():
            if r["home_team"] == team:
                goals.append(r["home_goals"])
                shots.append(r["home_shots"])
                shots_ot.append(r["home_shots_on_target"])
                conceded.append(r["away_goals"])
            else:
                goals.append(r["away_goals"])
                shots.append(r["away_shots"])
                shots_ot.append(r["away_shots_on_target"])
                conceded.append(r["home_goals"])

        return {
            "goals_avg": np.mean(goals),
            "shots_avg": np.mean(shots),
            "shots_ot_avg": np.mean(shots_ot),
            "conceded_avg": np.mean(conceded)
        }

    # -------------------------------
    # POINTS FROM LAST 5 MATCHES
    # -------------------------------
    def _compute_points_last5(self, matches, team):
        points = 0
        for _, r in matches.iterrows():
            if r["home_team"] == team:
                gf, ga = r["home_goals"], r["away_goals"]
            else:
                gf, ga = r["away_goals"], r["home_goals"]

            if gf > ga:
                points += 3
            elif gf == ga:
                points += 1

        return points

    # -------------------------------
    # BUILD ONE ROW FOR PREDICTION
    # -------------------------------
    def make_prediction_row(self, home_team, away_team, match_date):
        """
        Generate a single row of features for prediction.
        
        Args:
            home_team (str): Name of the home team
            away_team (str): Name of the away team
            match_date (str or datetime): Date of the match
            
        Returns:
            pd.DataFrame: Single row DataFrame with all required features
        """
        match_date = pd.to_datetime(match_date)

        home_last5 = self._get_last5_matches(home_team, match_date)
        away_last5 = self._get_last5_matches(away_team, match_date)

        home_form = self._compute_team_form(home_last5, home_team)
        away_form = self._compute_team_form(away_last5, away_team)

        home_points = self._compute_points_last5(home_last5, home_team)
        away_points = self._compute_points_last5(away_last5, away_team)

        row = {
            "home_shots_on_target_avg_last5": home_form["shots_ot_avg"],
            "away_shots_on_target_avg_last5": away_form["shots_ot_avg"],

            "home_shots_avg_last5": home_form["shots_avg"],
            "away_shots_avg_last5": away_form["shots_avg"],

            "home_team_goals_conceded_avg_last5": home_form["conceded_avg"],
            "away_team_goals_conceded_avg_last5": away_form["conceded_avg"],

            "home_goals_avg_last5": home_form["goals_avg"],
            "away_goals_avg_last5": away_form["goals_avg"],

            "home_points_last5_matches": home_points,
            "away_points_last5_matches": away_points,

            "points_diff_last5": home_points - away_points,
            "goal_diff_avg5": home_form["goals_avg"] - away_form["goals_avg"],
            "shots_diff_avg5": home_form["shots_avg"] - away_form["shots_avg"],
            "shots_on_target_diff_avg5": home_form["shots_ot_avg"] - away_form["shots_ot_avg"],
            "x_defense_diff": away_form["conceded_avg"] - home_form["conceded_avg"],

            "home_advantage": 1
        }

        return pd.DataFrame([row])[self.input_features]
