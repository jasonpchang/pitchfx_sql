# imports
import pandas as pd
import sqlite3

class Player():
    """Player class for extracting information from pitchfx database"""
    def __init__(self, name):
        """Initialize player object
        
        Inputs:
            name: name of player in "first last" format
        """
        # parse name
        self.first, self.last = name.split(" ")
        
    def pitch_games(self, database):
        """Grab all games from database player pitched in
        
        Inputs:
            database: sqlite object of database to read from
        
        Outpus:
            games: pandas dataframe containing games player played in
        """
        # grab all games
        query = """SELECT DISTINCT games.*
                FROM games
                JOIN events ON (games.game_id=events.game_id)
                WHERE events.pitcher_id=(SELECT player_id
                FROM players
                WHERE players.player_first='%s'
                    AND players.player_last='%s')
                ORDER BY games.game_id""" %(self.first, self.last)
        self.player_pgames = pd.read_sql_query(query, database)
        
        # clean up
        return self.player_pgames

    def pitches(self, database, **params):
        """Grab all pitches from database thrown by player
        
        Inputs:
            database: sqlite object of database to read from
            clean [False]: remove Nans, pitch-outs, intentional balls
        
        Outputs:
            pitches: pandas dataframe containing pitchfx data
        """
        # grab all pitches
        query = """SELECT DISTINCT pitchfx.* 
                FROM pitchfx
                JOIN events ON (pitchfx.game_id=events.game_id
                    AND pitchfx.cur_event=events.event_id)
                WHERE events.pitcher_id=(SELECT player_id
                FROM players
                WHERE players.player_first='%s'
                    AND players.player_last='%s')
                ORDER BY game_id, pitch_num""" %(self.first, self.last)
        self.player_pfx = pd.read_sql_query(query, database)
        
        # clean or not
        if params:
            if "clean" in params:
                if bool(params["clean"]):
                    self.player_pfx = self.player_pfx.dropna(axis=0, how="any")
                    self.player_pfx = self.player_pfx[self.player_pfx.pitch_type!="IN"]
                    self.player_pfx = self.player_pfx[self.player_pfx.pitch_type!="PO"]
        
        # clean up
        return self.player_pfx
    
    def pitch_events(self, database):
        """Grab events where player is the pitcher
        
        Inputs:
            database: sqlite object of database to read from
            
        Output:
            events: events where player is the pitcher
        """
        # grab all events
        query = """SELECT DISTINCT * 
                FROM events
                WHERE pitcher_id=(SELECT player_id
                FROM players
                WHERE players.player_first='Barry'
                    AND players.player_last='Zito')
                ORDER BY game_id, event_id"""
        self.player_pevents = pd.read_sql_query(query, database)
        
        # clean up
        return self.player_pevents