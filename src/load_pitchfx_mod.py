#----------------------------------------------
# load_pitchfx_mod.py
#    module to add pitch fx data to database
#----------------------------------------------
# things to do
#   DONE label whether regular season or playoff game
#   DONE fix the event id after pitching changes
#   DONE change score so that it does not change with pitching changes


#----------------------------------------------
# imports and aliases
#----------------------------------------------
import xml.etree.ElementTree as ET
import urllib
import re


#----------------------------------------------
# begin definitions
#----------------------------------------------
def pitchfx_init(hdb):
    """Initializes tables in PitchFX database

    Creates Sqlite3 tables. Tables include: player id data, pitchfx data, game
    id data, time id data

    Args:
        hdb: sqlite3 database handle

    Returns:
        Empty tables in the sqlite PitchFX database
    """
    # game id data from game.xml
    comm = "CREATE TABLE games (" \
        "game_id INTEGER, " \
        "game_type TEXT, " \
        "date INTEGER, " \
        "game_time INTEGER, " \
        "home_id INTEGER, " \
        "home_wins INTEGER, " \
        "home_losses INTEGER, " \
        "visit_id INTEGER, " \
        "visit_wins INTEGER, " \
        "visit_losses INTEGER, " \
        "stadium_id INTEGER, " \
        "umpire_home INTEGER," \
        "umpire_first INTEGER," \
        "umpire_second INTEGER," \
        "umpire_third INTEGER," \
        "UNIQUE(game_id)" \
        ")"
    hdb.execute(comm)

    # team id data from game.xml
    comm = "CREATE TABLE teams (" \
        "team_id INTEGER, " \
        "team_name TEXT, " \
        "team_abbr TEXT, " \
        "UNIQUE(team_id)" \
        ")"
    hdb.execute(comm)

    # stadium id data from game.xml
    comm = "CREATE TABLE stadiums (" \
        "stadium_id INTEGER, " \
        "stadium_name TEXT, " \
        "UNIQUE(stadium_id)" \
        ")"
    hdb.execute(comm)

    # player id from players.xml
    comm = "CREATE TABLE players (" \
        "player_id INTEGER, " \
        "player_first TEXT, " \
        "player_last TEXT, " \
        "position TEXT, " \
        "bats TEXT, " \
        "throws TEXT, " \
        "dob INTEGER, " \
        "UNIQUE(player_id, position)" \
        ")"
    hdb.execute(comm)

    # umpire id from players.xml
    comm = "CREATE TABLE umpires (" \
        "umpire_id INTEGER, " \
        "umpire_name TEXT," \
        "UNIQUE(umpire_id)" \
        ")"
    hdb.execute(comm)

    # events info from events directory
    comm = "CREATE TABLE events (" \
        "game_id INTEGER, " \
        "event_id INTEGER, " \
        "event_description TEXT, " \
        "inning INTEGER, " \
        "is_top_inning INTEGER, " \
        "pre_out INTEGER, " \
        "post_out INTEGER, " \
        "pitcher_id INTEGER, " \
        "batter_id INTEGER, " \
        "runner_id INTEGER, " \
        "run_start TEXT, " \
        "run_end TEXT, " \
        "home_score INTEGER, " \
        "away_score INTEGER, " \
        "UNIQUE(game_id, event_id, runner_id)" \
        ")"
    hdb.execute(comm)

    # pitchfx data from game info from inning directory
    comm = "CREATE TABLE pitchfx (" \
        "game_id INTEGER, " \
        "pitch_num INTEGER, " \
        "at_bat INTEGER, " \
        "time INTEGER, " \
        "prev_event INTEGER, " \
        "description TEXT, " \
        "outcome TEXT, " \
        "pre_balls INTEGER, " \
        "post_balls INTEGER, " \
        "pre_strike INTEGER, " \
        "post_strike INTEGER, " \
        "start_speed REAL, " \
        "end_speed REAL, " \
        "sz_top REAL, " \
        "sz_bot REAL, " \
        "pfx_x REAL, " \
        "pfx_z REAL, " \
        "px REAL, " \
        "pz REAL, " \
        "x REAL, " \
        "y REAL, " \
        "x0 REAL, " \
        "y0 REAL, " \
        "z0 REAL, " \
        "vx0 REAL, " \
        "vy0 REAL, " \
        "vz0 REAL, " \
        "ax REAL, " \
        "ay REAL, " \
        "az REAL, " \
        "break_y REAL, " \
        "break_angle REAL, " \
        "break_length REAL, " \
        "spin_dir REAL, " \
        "spin_rate REAL, " \
        "pitch_type TEXT, " \
        "UNIQUE(game_id, pitch_num)" \
        ")"
    hdb.execute(comm)


def pitchfx_add(db, hdb, date1, date2, prompt):
    """Add information to database

    Fill Sqlite3 databases with pitchfx data from http://gd2.mlb.com/.

    Args:
        db: sqlite database cursor
        hdb: sqlite3 database handle
        date1: starting date to fill database
        date2: ending date to fill database
        prompt: flag to determine whether to ask to continue adding data

    Returns:
        Filled tables of the database
    """
    # intial pitch data vector of nulls
    comm = "PRAGMA table_info(pitchfx)"
    hdb.execute(comm)
    npfx = len(hdb.fetchall())
    pfxinit = [None]*npfx

    # game types
    gtypes = ['R', 'F', 'D', 'L', 'W']

    # pitchfx variables: sqlite3 database indices
    pfxkeys = {
        'game_id': 0,
        'id': 1,
        'at_bat': 2,
        'time': 3,
        'prev_event': 4,
        'des': 5,
        'type': 6,
        'pre_balls': 7,
        'post_balls': 8,
        'pre_strikes': 9,
        'post_strikes': 10,
        'start_speed': 11,
        'end_speed': 12,
        'sz_top': 13,
        'sz_bot': 14,
        'pfx_x': 15,
        'pfx_z': 16,
        'px': 17,
        'pz': 18,
        'x': 19,
        'y': 20,
        'x0': 21,
        'y0': 22,
        'z0': 23,
        'vx0': 24,
        'vy0': 25,
        'vz0': 26,
        'ax': 27,
        'ay': 28,
        'az': 29,
        'break_y': 30,
        'break_angle': 31,
        'break_length': 32,
        'spin_dir': 33,
        'spin_rate': 34,
        'pitch_type': 35
        }

    # determine which dates already exist in the database
    query = "SELECT min(date) FROM games"                                       
    hdb.execute(query)                                                          
    dbmin = hdb.fetchone()[0]                                                   
    # empty database                                                            
    if dbmin == None:
        date_start = date1                                                      
        date_end = date2                                                        
    else:                                                                       
        query = "SELECT max(date) FROM games"                                   
        hdb.execute(query)
        dbmax = hdb.fetchone()[0]
        # date1 date2 dbmin dbmax                                               
        if date2 < dbmin:                                                       
            date_start = date1                                                  
            date_end = date2                                                    
        # dbmin dbmax date1 date2                                               
        elif date1 > dbmax:                                                     
            date_start = date1                                                  
            date_end = date2                                                    
        # date1 dbmin date2 dbmax                                               
        # date1 dbmin dbmax date2                                               
        elif date1 < dbmin:                                                     
            date_start = date1                                                  
            if date2 <= dbmax:                                                  
                date_end = dbmin                                                
            else:                                                               
                date_end = date2                                                
        # dbmin date1 dbmax date2                                               
        elif dbmin <= date1:                                                     
            if date2 >= dbmax:                                                   
                date_start = dbmax                                              
                date_end = date2                                                
            # dbmin date1 date2 dbmax                                           
            else:                                                               
                date_start = dbmin                                              
                date_end = dbmax   

    # loop through dates (as defined by the date_start and date_end values)
    sdate_start = str(date_start)
    sdate_end = str(date_end)
    years = [sdate_start[:4], sdate_end[:4]]
    months = [sdate_start[4:6], sdate_end[4:6]]
    month = int(months[0])
    days = [sdate_start[-2:], sdate_end[-2:]]
    day = int(days[0])

    # set up regular expression
    str_game = re.compile("""^.+href="(gid_\d+_\d+_\d+_.+)/".+$""")
    str_xml = re.compile("""^.+href="(.+\.xml)".+$""")

    # loop over years, months, days for games
    for year in range(int(years[0]), int(years[1])+1):
        while month < 13:
            while day < 32:
                # determine whether there are any files to look at on given day
                try:
                    url_root = "http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s" %(year, str(month).zfill(2), str(day).zfill(2))
                    output = urllib.urlopen(url_root)
                except:
                    day += 1
                    continue
                # create list of game ids on given day
                date = int(str(year).zfill(4)+str(month).zfill(2)+str(day).zfill(2))
                ggs = []
                for line in output:
                    find = str_game.search(line)
                    if find:
                        ggs.append(find.group(1))

                # read in game and team information from game url
                for gg in ggs:
                    url_game = url_root+"/%s" %(gg)
                    url = url_game+"/game.xml"
                    try:
                        output = urllib.urlopen(url).read()
                        log = ET.fromstring(output)
                    except:
                        continue
                    gdict = log.attrib
                    game_type = gdict['type']
                    # determine what sort of game it is
                    if game_type not in gtypes:
                        continue
                    try:
                        game_id = int(gdict['game_pk'])
                        #game_id_prev = game_id
                    except:
                        continue
                    #except:
                    #    game_id = game_id_prev+1
                    # check if game already exists in table
                    comm = "SELECT date FROM games WHERE game_id=%s" %(game_id)
                    hdb.execute(comm)
                    if hdb.fetchone() != None:
                        continue
                    print gg
                    temp_time = gdict['local_game_time']
                    gtime = int(temp_time[0:2]+temp_time[3:5])
                    for ginfo in log:
                        if ginfo.tag == 'team':
                            ggdict = ginfo.attrib
                            if ggdict["type"] == 'home':
                                hid = ggdict['id']
                                try:
                                    tname = ggdict['name_full']
                                except:
                                    tname = ggdict['name']
                                tid = int(hid)
                                tabbrv = ggdict['abbrev']
                                hw = int(ggdict['w'])
                                hl = int(ggdict['l'])
                            else:
                                vid = ggdict['id']
                                try:
                                    tname = ggdict['name_full']
                                except:
                                    tname = ggdict['name']
                                tid = int(vid)
                                tabbrv = ggdict['abbrev']
                                vw = int(ggdict['w'])
                                vl = int(ggdict['l'])
                            # fill in team table
                            info = (tid, tname, tabbrv)
                            insert = "INSERT OR IGNORE INTO teams VALUES " \
                                "(?, ?, ?)"
                            hdb.execute(insert, info)
                        # stadium information
                        elif ginfo.tag == 'stadium':
                            ggdict = ginfo.attrib
                            sid = int(ggdict['id'])
                            sname = ggdict['name']
                            # fill in stadium table
                            info = (sid, sname)
                            insert = "INSERT OR IGNORE INTO stadiums VALUES " \
                                "(?, ?)"
                            hdb.execute(insert, info)

                    # read in player info from players xml
                    url = url_game+'/players.xml'
                    output = urllib.urlopen(url).read()
                    log = ET.fromstring(output)
                    for dinfo in log:
                        for pinfo in dinfo:
                            if pinfo.tag == 'player':
                                try:
                                    pdict = pinfo.attrib
                                    player_id = pdict['id']                            
                                    first = pdict['first']                        
                                    last = pdict['last']                          
                                    pos = pdict['position']                                 
                                    bat = pdict['bats']                                
                                    throw = pdict['rl'] 
                                except:
                                    continue
                                try:
                                    info = (player_id, first, last, pos, bat, throw, -1)
                                    insert = "INSERT INTO players VALUES " \
                                        "(?, ?, ?, ?, ?, ?, ?)"
                                    hdb.execute(insert, info)
                                    dob_flag = 1
                                except:
                                    dob_flag = 0
                                # grab dob from individual player urls
                                if dob_flag == 1:
                                    url_player = url_game+'/batters/%s.xml' %(player_id)
                                    poutput = urllib.urlopen(url_player).read()
                                    plog = ET.fromstring(poutput)
                                    ppdict = plog.attrib
                                    pdob = ppdict['dob']
                                    yy = pdob[-4:]                                      
                                    mm = pdob[:2]                                       
                                    dd = pdob[3:5]                                      
                                    dob = int(yy+mm+dd)
                                    # update player table
                                    comm = "UPDATE players SET dob=%s " \
                                        "WHERE player_id=%s AND position='%s'" %(dob, player_id, pos)
                                    hdb.execute(comm)
                            elif pinfo.tag == 'umpire':
                                udict = pinfo.attrib
                                umpire_name = udict['name']
                                umpire_position = udict['position']
                                try:
                                    umpire_id = int(udict['id'])
                                    # fill in umpires table
                                    info = (umpire_id, umpire_name)
                                    insert = "INSERT OR IGNORE INTO umpires VALUES " \
                                        "(?, ?)"
                                    hdb.execute(insert, info)
                                except:
                                    umpire_id = -1
                                if umpire_position == 'home':
                                    u_home = umpire_id
                                elif umpire_position == 'first':
                                    u_first = umpire_id
                                elif umpire_position == 'second':
                                    u_second = umpire_id
                                elif umpire_position == 'third':
                                    u_third = umpire_id

                    # fill in game table if game does not already exist
                    info = (game_id, game_type, date, gtime, hid, hw, hl, vid, vw, vl, sid, u_home, u_first, u_second, u_third)
                    insert = "INSERT OR IGNORE INTO games VALUES " \
                        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    hdb.execute(insert, info)

                    # read in pitchfx and event tables
                    url = url_game+"/inning/inning_all.xml"
                    try:
                        output = urllib.urlopen(url).read()
                        log = ET.fromstring(output)
                    except:
                        continue
                    # intialize events and scores
                    event_id = -1
                    action_flag = 0
                    home_score = 0
                    away_score = 0
                    # loop over inning
                    for header in log:
                        iinfo = header.attrib
                        inning_num = iinfo['num']
                        for inning in header:
                            # new inning flag
                            inning_flag = 1
                            post_outs = 0
                            if inning.tag == 'top':
                                is_top = 1
                            else:
                                is_top = 0
                            # loop over events in an inning
                            for etype in inning:
                                # keep track of in-game player changes
                                if etype.tag == 'action':
                                    edict = etype.attrib
                                    action_description = edict['des']
                                    if 'Pinch-Hitter' in action_description:
                                        action_event = edict['event']
                                        action_flag = 1
                                    elif 'Change' in action_description:
                                        action_event = edict['event']
                                        action_flag = 1
                                elif etype.tag == 'atbat':
                                    pre_outs = post_outs
                                    # flag for events with multiple runners
                                    runner_flag = 1
                                    # reset count at beginning of at-bat
                                    pre_balls = 0
                                    post_balls = 0
                                    pre_strikes = 0
                                    post_stikes = 0
                                    edict = etype.attrib
                                    # to account for strikeouts
                                    max_strikes = int(edict['s'])
                                    ab = int(edict['num'])
                                    pitcher_id = int(edict['pitcher'])
                                    batter_id = int(edict['batter'])
                                    end_of_ab_outs = int(edict['o'])
                                    event_description_ab = edict['event']
                                    # if there is a previous action then write current ab info as event
                                    if action_flag == 1:
                                        event_id += 1
                                        info = (game_id, event_id, action_event, inning_num, is_top, pre_outs, post_outs, pitcher_id, batter_id, runner_id, base_start, base_end, home_score, away_score)
                                        insert = "INSERT OR IGNORE INTO events VALUES (" \
                                            "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                            "?, ?, ?, ?" \
                                            ")"
                                        hdb.execute(insert, info)
                                    if inning_flag == 1:
                                        event_id += 1
                                        info = (game_id, event_id, -1, inning_num, is_top, pre_outs, post_outs, pitcher_id, batter_id, -1, -1, -1, home_score, away_score)
                                        insert = "INSERT OR IGNORE INTO events VALUES (" \
                                             "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                             "?, ?, ?, ?" \
                                             ")"
                                        hdb.execute(insert, info)
                                    try:
                                        home_score = edict['home_team_runs']
                                        away_score = edict['away_team_runs']
                                    except:
                                        pass
                                    # reset inning and action flag
                                    action_flag = 0
                                    inning_flag = 0
                                    # read in pitches
                                    for event in etype:
                                        # registered pitch
                                        if event.tag == 'pitch':
                                            runner_flag = 1
                                            # initialize pitchfx list and read in basic info
                                            info = list(pfxinit)
                                            info[pfxkeys['game_id']] = game_id
                                            info[pfxkeys['at_bat']] = ab
                                            info[pfxkeys['prev_event']] = event_id
                                            idict = event.attrib
                                            try:
                                                time_stamp = int(idict['sv_id'][-6:])
                                                info[pfxkeys['time']] = time_stamp
                                            except:
                                                pass
                                            # only fill in pitchfx info that exist
                                            common = set(idict.keys()).intersection(pfxkeys)
                                            for pfxvars in common:
                                                info[pfxkeys[pfxvars]] = idict[pfxvars]
                                            # update balls and strikes information
                                            if idict['type'] == 'B':
                                                post_balls = min(pre_balls+1,4)
                                                post_strikes = pre_strikes
                                            elif idict['type'] == 'S':
                                                post_balls = pre_balls
                                                if idict['des'] == 'Foul':
                                                    post_strikes = min(pre_strikes+1,2)
                                                else:
                                                    post_strikes = min(pre_strikes+1,max_strikes)
                                            else:
                                                post_balls = pre_balls
                                                post_strikes = pre_strikes
                                            info[pfxkeys['pre_balls']] = pre_balls
                                            info[pfxkeys['post_balls']] = post_balls
                                            info[pfxkeys['pre_strikes']] = pre_strikes
                                            info[pfxkeys['post_strikes']] = post_strikes
                                            # fill in pitchfx table
                                            insert = "INSERT OR IGNORE INTO pitchfx VALUES (" \
                                                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                                "?, ?, ?, ?, ?, ?" \
                                                ")"
                                            hdb.execute(insert, info)
                                            # update balls and strikes again
                                            pre_balls = post_balls
                                            pre_strikes = post_strikes
                                        # update runner events
                                        elif event.tag == 'runner':
                                            if runner_flag == 1:
                                                event_id += 1
                                            rdict = event.attrib
                                            runner_id = rdict['id']
                                            event_description = rdict['event']
                                            base_start = rdict['start']
                                            if base_start == "":
                                                base_start = "H"
                                            base_end = rdict['end']
                                            if base_end == "":
                                                try:
                                                    if rdict['score'] == "T":
                                                        base_end = "H"
                                                except:
                                                    base_end = "0"
                                                    post_outs = pre_outs+1
                                            # fill in event table
                                            info = (game_id, event_id, event_description, inning_num, is_top, pre_outs, post_outs, pitcher_id, batter_id, runner_id, base_start, base_end, home_score, away_score)
                                            insert = "INSERT OR IGNORE INTO events VALUES (" \
                                                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                                "?, ?, ?, ?" \
                                                ")"
                                            hdb.execute(insert, info)
                                            # upcoming runner tags are not separate events
                                            runner_flag = 0
                                        # handle pitch-outs
                                        elif event.tag == 'po':
                                            runner_flag = 1
                                            event_id += 1
                                            rdict = event.attrib
                                            event_description = rdict['des']
                                            # fill in event table
                                            info = (game_id, event_id, event_description, inning_num, is_top, pre_outs, post_outs, pitcher_id, batter_id, runner_id, base_start, base_start, home_score, away_score)
                                            insert = "INSERT OR IGNORE INTO events VALUES (" \
                                                "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                                "?, ?, ? ,?" \
                                                ")"                             
                                            hdb.execute(insert, info)
                                    # add end of at-bat information only if an out
                                    if end_of_ab_outs > pre_outs:
                                        # if last entry in ab is not runner then there was nobody on base (new event)
                                        if event.tag != 'runner':
                                            event_id += 1
                                        # fill in event table
                                        info = (game_id, event_id, event_description_ab, inning_num, is_top, pre_outs, end_of_ab_outs, pitcher_id, batter_id, batter_id, 'H', '0', home_score, away_score)
                                        insert = "INSERT OR IGNORE INTO events VALUES (" \
                                            "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
                                            "?, ?, ? ,?" \
                                            ")"                             
                                        hdb.execute(insert, info)
                                        # update outs
                                        pre_outs = end_of_ab_outs
                                        post_outs = end_of_ab_outs
                                        # if last entry in ab is runner then there was someone on base (already registered as event)
                                        #if event.tag == 'runner':
                                        #    event_id += 1
                    ## temporary break from games
                    # commit game
                    db.commit()
                    #return
                # check whether to break out
                if date >= date_end:
                    return
                # update day
                day += 1
            # update day and month
            day = 1
            month += 1
        # reset month
        month = 1
