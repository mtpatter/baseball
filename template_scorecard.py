#!/usr/bin/env python

"""Make a blank scorecard printable for specified game.
"""

import argparse
from collections import namedtuple

from pytz import timezone
from baseball.fetch_game import get_game_from_url

FakePlateAppearance = namedtuple(
    'FakePlateAppearance',
    'scorecard_summary batter plate_appearance_description'
)

EASTERN_TIMEZONE_STR = 'America/New_York'
DEFAULT_LOGO = 'baseball-fairy-161.png'
LOGO_DICT = {
    'LAA': 'team_logos/angels.gif',
    'CAL': 'team_logos/angels.gif',
    'HOU': 'team_logos/astros.gif',
    'OAK': 'team_logos/athletics.gif',
    'TOR': 'team_logos/blue-jays.gif',
    'ATL': 'team_logos/braves.gif',
    'MIL': 'team_logos/brewers.gif',
    'ML4': 'team_logos/brewers.gif',
    'STL': 'team_logos/cardinals.gif',
    'CHC': 'team_logos/cubs.gif',
    'ARI': 'team_logos/diamondbacks.gif',
    'LAD': 'team_logos/dodgers.gif',
    'SF': 'team_logos/giants.gif',
    'CLE': 'team_logos/indians.gif',
    'NAS': 'team_logos/nl.svg',
    'AAS': 'team_logos/al.svg',
    'SEA': 'team_logos/mariners.gif',
    'MIA': 'team_logos/marlins.gif',
    'FLO': 'team_logos/florida.svg',
    'NYM': 'team_logos/mets.gif',
    'WSH': 'team_logos/nationals.gif',
    'BAL': 'team_logos/orioles.gif',
    'SD': 'team_logos/padres.gif',
    'PHI': 'team_logos/phillies.gif',
    'PIT': 'team_logos/pirates.gif',
    'TEX': 'team_logos/rangers.gif',
    'TB': 'team_logos/rays.gif',
    'CIN': 'team_logos/reds.gif',
    'BOS': 'team_logos/red-sox.gif',
    'COL': 'team_logos/rockies.gif',
    'KC': 'team_logos/royals.gif',
    'DET': 'team_logos/tigers.gif',
    'MIN': 'team_logos/twins.gif',
    'MON': 'team_logos/expos.svg',
    'CWS': 'team_logos/white-sox.gif',
    'CHW': 'team_logos/white-sox.gif',
    'NYY': 'team_logos/yankees.gif'
}


HEIGHT = 4913
WIDTH = 3192

EXTRA_COLUMNS = 4
NUM_MINIMUM_INNINGS = 10
LEN_BATTING_LIST = 10

BOX_WIDTH = 266
BOX_HEIGHT = 200

AUTOMATIC_BALL_COORDINATE = (300, 300)

PITCHER_LARGE_FONT_SIZE = 30
PITCHER_MED_FONT_SIZE = 26
PITCHER_SMALL_FONT_SIZE = 22
PITCHER_STATS_LARGE_FONT_SIZE = 25
PITCHER_STATS_MED_FONT_SIZE = 23
PITCHER_STATS_SMALL_FONT_SIZE = 20
PITCHER_BOX_SCORE_LARGE_Y = 90
PITCHER_BOX_SCORE_MED_Y = 85
PITCHER_BOX_SCORE_SMALL_Y = 78
PITCHER_BOX_SCORE_X_INCREMENT = 70
PITCHER_BOX_SCORE_LARGE_Y_INCREMENT = 40
PITCHER_BOX_SCORE_MED_Y_INCREMENT = 34
PITCHER_BOX_SCORE_SMALL_Y_INCREMENT = 26
PITCHER_BOX_STATS_LARGE_Y_OFFSET = 73
PITCHER_BOX_STATS_MED_Y_OFFSET = 70
PITCHER_BOX_STATS_SMALL_Y_OFFSET = 67
SMALL_CHUNK_SIZE = 5
LARGE_CHUNK_SIZE = 5
BASE_SVG_FONT_SMALL = 11
BASE_SVG_FONT_BIG = 22

BATTER_FONT_SIZE_BIG = 38
BATTER_FONT_SIZE_MED_PLUS = 34  # 18
BATTER_FONT_SIZE_MED = 30  # 15
BATTER_FONT_SIZE_SMALL = 25  # 10

BATTER_SPACE_BIG = 48
BATTER_SPACE_MED_PLUS = 42
BATTER_SPACE_MED = 32
BATTER_SPACE_SMALL = 25
BATTER_STATS_OFFSET_BIG = 15
BATTER_STATS_OFFSET_MED_PLUS = 13
BATTER_STATS_OFFSET_MED = 10
BATTER_STATS_OFFSET_SMALL = 6
BATTER_STATS_SPACES_BIG = 4
BATTER_STATS_SPACES_MED_PLUS = 5
BATTER_STATS_SPACES_MED = 6
BATTER_STATS_SPACES_SMALL = 10
BATTER_INITIAL_Y_POS = 45
BIG_TITLE_SIZE = 75
SMALL_TITLE_SIZE = 65
SUMMARY_SIZE_LARGE = 43
SUMMARY_SIZE_SMALL = 30
RED_COLOR = '#e63946'  # '#c10000' # strikes
BLUE_COLOR = '#4361ee'  # 'blue'  # hits
DARK_GREEN_COLOR = 'darkgreen'  # '#006400' '#0a9396' # runs
BLACK_COLOR = 'darkgrey'  # '#c1dbb3' '#70e000' '#76c893' # balls and other
HALF_SCALE_HEADER = '<g transform="scale(0.5)">'
HALF_SCALE_FOOTER = '</g>'
SVG_FOOTER = '</svg>'

PITCH_TYPE_DESCRIPTION = {'Ball': 'B',
                          'Ball In Dirt': 'D',
                          'Called Strike': 'C',
                          'Automatic Strike': 'C',
                          'Swinging Strike': 'S',
                          'Strike': 'S',
                          'Unknown Strike': 'S',
                          'Swinging Pitchout': 'S',
                          'Foul': 'F',
                          'Foul Tip': 'T',
                          'Pitchout': 'P',
                          'Foul Pitchout': 'P',
                          'Balk': 'N',
                          'Hit By Pitch': 'H',
                          'Automatic Ball': 'I',
                          'Intent Ball': 'I',
                          'Foul Bunt': 'L',
                          'Missed Bunt': 'M',
                          'In play, run(s)': 'X',
                          'In play, runs(s)': 'X',
                          'In play, out(s)': 'X',
                          'In play, no out': 'X'}

BIG_SVG_HEADER = (
    '<?xml version="1.0" standalone="no"?>'

    '<svg height="2356" viewBox="0 0 {width} {height}" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'

    # Importing Google fonts
    '<defs> '
    '<style type="text/css"> @import url(\'https://fonts.googleapis.com/css2?family=Bebas+Neue\&amp;display=swap\');</style> '
    '<style type="text/css"> @import url(\'https://fonts.googleapis.com/css2?family=Roboto:wght@700\&amp;display=swap\');</style> '
    '<style type="text/css"> @import url(\'https://fonts.googleapis.com/css2?family=Staatliches\&amp;display=swap\');</style> '
    '<style type="text/css"> @import url(\'https://fonts.googleapis.com/css2?family=Jockey+One\&amp;display=swap\');</style> '
    '<style type="text/css"> @import url(\'https://fonts.googleapis.com/css2?family=Oswald\&amp;display=swap\');</style> '

    '</defs>'

    #'<rect x="0" y="0" width="{width}" height="4513" fill="#AAAAAA"/> '
    '<rect x="0" y="0" width="{width}" height="4913" fill="#AAAAAA"/> ' # extra batter
    '<rect x="0" y="0" width="532" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="250" y="75" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="60">Batter</text>'

    #'<rect x="0" y="2256" width="532" height="100" fill="white" '
    '<rect x="0" y="2456" width="532" height="100" fill="white" ' # extra batter
    'stroke="black" stroke-width="1"/>'
    '<text x="250" y="2526" font-family="Bebas Neue" text-anchor="middle" ' # was 2326
    'font-size="60">Batter</text>'

    '<rect x="0" y="2100" width="532" height="100" fill="white" ' # extra batter
    'stroke="black" stroke-width="1"/>'
    '<text x="250" y="2160" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="40">Inning Stats</text>'

    #'<rect x="0" y="4156" width="532" height="100" fill="white" '
    '<rect x="0" y="4556" width="532" height="100" fill="white" ' # extra batter
    'stroke="black" stroke-width="1"/>'
    '<text x="250" y="4616" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="40">Inning Stats</text>'

    '<line x1="0" y1="2456" x2="{width}" y2="2456" stroke="black" '
    'stroke-width="1"/>'  # line
)

PITCHER_STATS_HEADER = (
    '<svg x="{x_box}" y="{y_box}" width="1596" height="256" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="1596" height="256" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="150" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">PITCHER</text>'

    '<text x="545" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">IP</text>'
    '<text x="609" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">WLS</text>'
    '<text x="682" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">BF</text>'
    '<text x="745" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">H</text>'
    '<text x="815" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">R</text>'
    '<text x="885" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">ER</text>'
    '<text x="955" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">SO</text>'
    '<text x="1025" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">BB</text>'
    '<text x="1097" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">IBB</text>'
    '<text x="1167" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">HBP</text>'
    '<text x="1237" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">BLK</text>'
    '<text x="1305" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">WP</text>'
    '<text x="1375" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">HR</text>'
    '<text x="1450" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">S</text>'
    '<text x="1520" y="35" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="20">P</text>'
    #'<text x="1398" y="35" font-family="Bebas Neue" text-anchor="middle" '
    #'font-size="20">ERA</text>'
    #'<text x="1475" y="35" font-family="Bebas Neue" text-anchor="middle" '
    #'font-size="20">WHIP</text>'
)

PITCHER_STATS_LINE_TEMPLATE = (
    '<a target="_parent" xlink:href="http://mlb.com/player/{pitcher_id}">'

    '<text x="10" y="{name_y_pos}" font-family="Roboto" font-size="{size_1}" '
    'text-anchor="start" fill="blue">{pitcher}</text></a>'
    '<text x="350" y="{name_y_pos}" font-family="Roboto" font-size="{size_2}" '
    'text-anchor="start">{stats}</text>'
    '<text x="520" y="{name_y_pos}" font-family="Roboto" font-size="{size_2}" '
    'text-anchor="end">{appears}</text>'
    '<b>page-break-after : always</b> '

)

INNING_STATS_BOX = (
    '<svg x="{box_x}" y="{box_y}" width="1596" height="256" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="256" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="20" y="30" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="22">{stats_str_1}</text>'
    '<text x="90" y="30" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="22">{stats_str_2}</text>'
    '<text x="160" y="30" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="22">{stats_str_3}</text>'
    '<text x="20" y="80" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="22">{stats_str_4}</text>'
    '<text x="90" y="80" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="22">{stats_str_5}</text>'
    '<text x="160" y="80" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="22">{stats_str_6}</text>'
    '</svg>'
)

PROOF_BOX = (
    '<svg x="{box_x}" y="{box_y}" width="1596" height="256" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="256" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="20" y="30" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="24">{stats_str_1}</text>'
    '<text x="20" y="80" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="24">{stats_str_2}</text>'
    '<text x="20" y="130" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="24">{stats_str_3}</text>'
    '<text x="20" y="180" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="24">{stats_str_4}</text>'

    '<line x1="0" y1="200" x2="266" y2="200" stroke="black" stroke-width="1" fill="transparent"/>'

    '<text x="20" y="230" font-family="Roboto" '
    'text-anchor="start" '
    'font-size="24">{stats_str_5}</text>'
    '</svg>'
)

TOTAL_BOX_SCORE_STATS_BOX = (
    '<svg x="{box_x}" y="{box_y}" width="266" height="400" '
    'version="1.1" xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="400" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="50" y="100" font-family="Bebas Neue" text-anchor="start" '
    'font-size="100" font-weight="bold">R</text>'
    '<text x="50" y="225" font-family="Bebas Neue" text-anchor="start" '
    'font-size="100" font-weight="bold">H</text>'
    '<text x="50" y="350" font-family="Bebas Neue" text-anchor="start" '
    'font-size="100" font-weight="bold">E</text>'
    '</svg>'
)

BIG_SVG_COLUMN = (
    '<rect x="{x_pos}" y="0" width="266" height="100" fill="white" '
    'stroke="black" '
    'stroke-width="1"/>'
    '<text x="{text_x_pos}" y="70" font-family="Bebas Neue" '
    'text-anchor="middle" '
    'font-size="60">{inning_num}</text>'


    '<rect x="{x_pos}" y="2456" width="266" height="100" '  # + 200
    'fill="white" '
    'stroke="black" '
    'stroke-width="1"/>'

    '<text x="{text_x_pos}" y="2526" font-family="Bebas Neue" '  # + 200
    'text-anchor="middle" '
    'font-size="60">{inning_num}</text>'

    '<line x1="0" y1="2456" x2="{width}" y2="2456" '
    'stroke="black" stroke-width="1"/>'
)

BIG_SVG_TITLE = (
    '<svg width="266" height="1300" x="{x_pos}" y="{y_pos}" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="1300" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<rect x="0" y="0" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="133" y="67" font-family="Bebas Neue" text-anchor="middle" '
    'font-size="50">{inning_half}</text>'
    '<text x="80" y="700" transform="rotate(-90,80,700)" '
    'fill="black" font-size="{title_size}" font-family="Bebas Neue" text-anchor="middle" '
    '>{game_str}</text>'
    '<text x="145" y="700" transform="rotate(-90,145,700)" '
    'fill="black" font-size="45" font-family="Bebas Neue" text-anchor="middle" '
    '>{location}</text>'
    '<text x="200" y="700" transform="rotate(-90,200,700)" '
    'fill="black" font-size="30" font-family="Bebas Neue" text-anchor="middle" '
    '>{datetime}</text>'
    '<text x="235" y="700" transform="rotate(-90,235,700)" '
    'fill="black" font-size="30" font-family="Bebas Neue" text-anchor="middle" '
    '>{detail_str}</text>'
    '</svg>'
)

BOX_SCORE_COLUMN_HEADER = (
    '<rect x="{x_pos}" y="0" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="{text_x_pos}" y="60" font-family="Roboto" '
    'text-anchor="start" font-size="24">'
    'AB'
    '&#160;R'
    '&#160;H'
    '&#160;RBI'
    '&#160;BB'
    '&#160;SO'
    '&#160;LOB'
    '</text>'
    '<rect x="{x_pos}" y="2456" width="266" height="100" fill="white" '
    'stroke="black" stroke-width="1"/>'
    '<text x="{text_x_pos}" y="2516" font-family="Roboto" text-anchor="start" '
    'font-size="24">'
    'AB'
    '&#160;R'
    '&#160;H'
    '&#160;RBI'
    '&#160;BB'
    '&#160;SO'
    '&#160;LOB'
    '</text>'
)

BATTER_SVG_HEADER = (
    '<svg x="{x_pos}" y="{y_pos}" width="532" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="532" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
)

BATTER_SVG_HEADER_SUMMARY = (
    '<svg x="{x_pos}" y="{y_pos}" width="532" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="532" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'

)

BATTER_NAME_TEMPLATE = (
    '<a target="_parent" xlink:href="http://mlb.com/player/{batter_id}">'
    '<text x="10" y="{name_y_pos}" font-family="Roboto" '
    'font-size="{batter_font_size}" '
    'text-anchor="start" fill="blue">{batter}</text></a>'
    '<text x="520" y="{name_y_pos}" font-family="Roboto" '
    'font-size="{stats_font_size}" '
    'text-anchor="end">{appears}</text>'
)

HOME_LOGO = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
    '<image xlink:href="{logo}" x="50" y="0" height="200" '
    'width="163" />'
    '</svg>'
)

AWAY_LOGO = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
    '<image xlink:href="{logo}" x="50" y="0" height="200" '
    'width="163" />'
    '</svg>'
)

BOX_SCORE_LINE_TEMPLATE = (
    '<text x="13" y="{name_y_pos}" font-family="Roboto" '
    'font-size="{batter_font_size}" text-anchor="start">{box_score_line}</text>'
)


SVG_HEADER = (
    '<svg x="{x_pos}" y="{y_pos}" width="266" height="200" version="1.1" '
    'xmlns="http://www.w3.org/2000/svg" '
    'xmlns:xlink="http://www.w3.org/1999/xlink">'
    '<rect x="0" y="0" width="266" height="200" stroke="black" fill="white" '
    'stroke-width="1"/>'
    # Remove line splitting box
    # '<line x1="67" y1="0" x2="67" y2="266" stroke="black" fill="transparent"/>'
    '<!-- Diamond -->'
    '<path d="M71 101 A 45 45, 0, 0, 1, 261 101 L 166 196 Z" stroke="black" '
    'stroke-dasharray="5,5" fill="transparent"/>'
    '<path d="M112 142 L 166 89 L 220 142" stroke="black" stroke-dasharray="5,5" fill="transparent"/>'

    # Balls and strikes
    # '<circle cx="20" cy="17" '
    # 'r="15" stroke="lightgrey" stroke-width="2" fill="white"/>'
    # '<circle cx="20" cy="52" '
    # 'r="15" stroke="lightgrey" stroke-width="2" fill="white"/>'
    # #'<circle cx="20" cy="85" '
    # #'r="15" stroke="lightgrey" stroke-width="2" fill="white"/>'
    # '<circle cx="55" cy="17" '
    # 'r="15" stroke="lightgrey" stroke-width="2" fill="white"/>'
    # '<circle cx="55" cy="52" '
    # 'r="15" stroke="lightgrey" stroke-width="2" fill="white"/>'
    # '<circle cx="90" cy="17" '
    # 'r="15" stroke="lightgrey" stroke-width="2" fill="white"/>'

    '<rect x="2" y="2" width="30" height="30" stroke="lightgrey" fill="white" '
    'stroke-width="1"/>'
    '<rect x="32" y="2" width="30" height="30" stroke="lightgrey" fill="white" '
    'stroke-width="1"/>'
    '<rect x="62" y="2" width="30" height="30" stroke="lightgrey" fill="transparent" '
    'stroke-width="1"/>'
    '<rect x="2" y="32" width="30" height="30" stroke="lightgrey" fill="white" '
    'stroke-width="1"/>'
    '<rect x="32" y="32" width="30" height="30" stroke="lightgrey" fill="white" '
    'stroke-width="1"/>'

    # outs
    '<circle cx="245" cy="19" '
    'r="18" stroke="darkgrey" stroke-width="2" stroke-dasharray="5,5" fill="white"/>'

)

BIG_RECTANGLE = ('<path d="M0 {y_pos} L {width} {y_pos} '
                 'L {width} {y_pos_2} L 0 {y_pos_2}" '
                 'stroke="black" stroke-width="4" fill="none"/>')


SVG_SUMMARY_TEMPLATE = (
    '<text x="260" y="192" font-family="Bebas Neue" font-size="34" '
    'text-anchor="end">{summary}'
    '<title id="title">{title}</title>'
    '</text>'
)


def get_game_width():
    inning_length = NUM_MINIMUM_INNINGS
    game_width = BOX_WIDTH * (inning_length + EXTRA_COLUMNS)

    return game_width


def get_big_svg_header():
    inning_length = NUM_MINIMUM_INNINGS
    game_width = get_game_width()

    big_svg_str = BIG_SVG_HEADER.format(width=game_width, height=HEIGHT)

    for inning_num in range(1, inning_length + 1):
        x_pos = (inning_num + 1) * BOX_WIDTH
        text_x_pos = x_pos + (BOX_WIDTH // 2)
        big_svg_str += BIG_SVG_COLUMN.format(inning_num=inning_num,
                                             x_pos=x_pos,
                                             text_x_pos=text_x_pos,
                                             width=game_width)

    box_score_header_x_pos = (inning_length + 2) * BOX_WIDTH
    box_score_header_text_x_pos = box_score_header_x_pos + 13

    big_svg_str += BOX_SCORE_COLUMN_HEADER.format(
        x_pos=box_score_header_x_pos,
        text_x_pos=box_score_header_text_x_pos,
    )

    return big_svg_str


def get_player_last_name(player_obj):
    return player_obj.last_name


def get_inning_half_stats_tuple_list(game):
    inning_half_stats_tuple_list = []
    for inning_index, inning in enumerate(game.inning_list):
        inning_half_stats_tuple_list.extend(
            [(inning_index + 1, 'top', inning.top_half_inning_stats),
             (inning_index + 1, 'bottom', inning.bottom_half_inning_stats)]
        )

    return inning_half_stats_tuple_list


def get_batter_spacing_values(batter_list):
    if len(batter_list) <= 4:
        batter_font_size = BATTER_FONT_SIZE_BIG
        batter_space_increment = BATTER_SPACE_BIG
        stats_y_offset = BATTER_STATS_OFFSET_BIG
        box_score_line_template = (
            ('&#160;' * (BATTER_STATS_SPACES_BIG // 2)) + '%s' +
            ('&#160;' * BATTER_STATS_SPACES_BIG + '%s') * 6
        )
    elif len(batter_list) > 4 and len(batter_list) < 8:
        batter_font_size = BATTER_FONT_SIZE_MED
        batter_space_increment = BATTER_SPACE_MED
        stats_y_offset = BATTER_STATS_OFFSET_MED
        box_score_line_template = (
            ('&#160;' * (BATTER_STATS_SPACES_MED // 2)) + '%s' +
            ('&#160;' * BATTER_STATS_SPACES_MED + '%s') * 6
        )
    else:
        batter_font_size = BATTER_FONT_SIZE_SMALL
        batter_space_increment = BATTER_SPACE_SMALL
        stats_y_offset = BATTER_STATS_OFFSET_SMALL
        box_score_line_template = (
            ('&#160;' * (BATTER_STATS_SPACES_SMALL // 2)) + '%s' +
            ('&#160;' * BATTER_STATS_SPACES_SMALL + '%s') * 6
        )

    for batter in batter_list:
        if (len(str(batter.player_obj)) > 18 and
                batter_font_size == BATTER_FONT_SIZE_BIG):
            batter_font_size = BATTER_FONT_SIZE_MED_PLUS
            batter_space_increment = BATTER_SPACE_MED_PLUS
            stats_y_offset = BATTER_STATS_OFFSET_MED_PLUS
            box_score_line_template = (
                ('&#160;' * (BATTER_STATS_SPACES_MED_PLUS // 2)) + '%s' +
                ('&#160;' * BATTER_STATS_SPACES_MED_PLUS + '%s') * 6
            )

    return (batter_font_size,
            batter_space_increment,
            stats_y_offset,
            box_score_line_template)


def get_team_batter_box_score_list(game, team, box_score_dict, offset):
    box_score_svg = ''
    box_score_x_offset = BOX_WIDTH * (NUM_MINIMUM_INNINGS + 2)

    for batter_list in team.batting_order_list_list:
        box_score_svg += BATTER_SVG_HEADER_SUMMARY.format(
            x_pos=box_score_x_offset,
            y_pos=offset + (BOX_HEIGHT // 2)
        )

        batter_font_size, batter_space_increment, _, box_score_line_template = (
            get_batter_spacing_values(batter_list)
        )

        batter_y_pos = BATTER_INITIAL_Y_POS
        last_batter = None
        for batter_appearance in batter_list:

            box_score_svg += BOX_SCORE_LINE_TEMPLATE.format(
                name_y_pos=batter_y_pos,
                box_score_line='',
                batter_font_size=batter_font_size
            )

            batter_y_pos += batter_space_increment
            last_batter = batter_appearance.player_obj

        box_score_svg += SVG_FOOTER
        offset += BOX_HEIGHT

    # Extra batters
    for b in range(LEN_BATTING_LIST - 9):
        box_score_svg += BATTER_SVG_HEADER_SUMMARY.format(
            x_pos=box_score_x_offset,
            y_pos=offset + (BOX_HEIGHT // 2)
        )
        box_score_svg += BOX_SCORE_LINE_TEMPLATE.format(
            name_y_pos=batter_y_pos,
            box_score_line='',
            batter_font_size=batter_font_size
        )

        batter_y_pos += batter_space_increment

        b += 1
        box_score_svg += SVG_FOOTER
        offset += BOX_HEIGHT

    return box_score_svg


def get_team_batter_list(team, offset):
    batter_svg = ''
    for batter_list in team.batting_order_list_list:
        batter_svg += BATTER_SVG_HEADER.format(
            x_pos=0,
            y_pos=offset + (BOX_HEIGHT // 2)
        )

        batter_font_size, batter_space_increment, stats_y_offset, _ = (
            get_batter_spacing_values(batter_list)
        )

        batter_y_pos = BATTER_INITIAL_Y_POS
        last_batter = None
        for batter_appearance in batter_list:
            if last_batter == batter_appearance.player_obj:
                batter_str = ''
                stats_str = ''
            else:
                batter_str = '{}'.format(batter_appearance.player_obj)
                if batter_appearance.player_obj.bat_side:
                    batter_str += ' - {}'.format(
                        batter_appearance.player_obj.bat_side
                    )

                if (batter_appearance.player_obj.obp and
                        batter_appearance.player_obj.slg):
                    stats_str = 'OBP: {:.3f}, SLG: {:.3f}'.format(
                        batter_appearance.player_obj.obp,
                        batter_appearance.player_obj.slg
                    )
                else:
                    stats_str = ''

            # FIXME  doesn't work
            appears_str = '{: <3s} / {: >3s}'.format(str(batter_appearance.start_inning_num),
                                                     str(batter_appearance.position))

            batter_svg += BATTER_NAME_TEMPLATE.format(
                batter_id=batter_appearance.player_obj.mlb_id,
                name_y_pos=batter_y_pos,
                stats_y_pos=batter_y_pos + stats_y_offset,
                stats=stats_str,
                appears=appears_str,
                batter=batter_str,
                batter_font_size=batter_font_size,
                stats_font_size=batter_font_size - 5
            )

            batter_y_pos += batter_space_increment
            last_batter = batter_appearance.player_obj

        batter_svg += SVG_FOOTER
        offset += BOX_HEIGHT

    for b in range(LEN_BATTING_LIST-9):
        # Extra batters

        batter_svg += BATTER_SVG_HEADER.format(
            x_pos=0,
            y_pos=offset + (BOX_HEIGHT // 2)
        )

        batter_y_pos = BATTER_INITIAL_Y_POS
        last_batter = None

        batter_svg += BATTER_NAME_TEMPLATE.format(
           batter_id='',
           name_y_pos='',
           stats_y_pos='',
           stats='',
           appears='',
           batter='',
           batter_font_size='',
           stats_font_size=''
        )

        batter_y_pos += batter_space_increment

        batter_svg += SVG_FOOTER
        offset += BOX_HEIGHT
        b += 1

    return batter_svg


def get_batter_list_and_stats(game):
    both_teams_batters_svg = ''

    tuple_list = [
        (game.away_team, game.away_batter_box_score_dict, 0),
        (game.home_team, game.home_batter_box_score_dict, HEIGHT // 2)
    ]

    for team, box_score_dict, offset in tuple_list:
        both_teams_batters_svg += '{}{}'.format(
            get_team_batter_list(team, offset),
            get_team_batter_box_score_list(game, team, box_score_dict, offset)
        )

    return both_teams_batters_svg


def get_team_stats_box(box_x, box_y):
    box_1_x = box_x
    stats_box_1_svg = PROOF_BOX.format(
        box_x=box_1_x,
        box_y=box_y,
        stats_str_1='Runs',
        stats_str_2='LOB',
        stats_str_3='PO',
        stats_str_4='',
        stats_str_5='TOTAL'
    )

    box_2_x = box_x + BOX_WIDTH
    stats_box_2_svg = PROOF_BOX.format(
        box_x=box_2_x,
        box_y=box_y,
        stats_str_1='AB',
        stats_str_2='BB',
        stats_str_3='SAC',
        stats_str_4='HBP/Int',
        stats_str_5='TOTAL'
    )

    both_stats_boxes_svg = stats_box_1_svg + stats_box_2_svg

    return both_stats_boxes_svg


def get_inning_stats_box(box_x, box_y):
    stats_box_svg = (
        INNING_STATS_BOX.format(
            box_x=box_x,
            box_y=box_y,
            stats_str_1='R:',
            stats_str_2='H:',
            stats_str_3='LOB:',
            stats_str_4='K:',
            stats_str_5='BB:',
            stats_str_6='E:'
        )
    )

    return stats_box_svg


def get_this_pa_num(player_appearance, appearance_list):
    this_pa_num = None
    if appearance_list:
        for pa_index, plate_app in enumerate(appearance_list):
            if plate_app.batter == player_appearance.player_obj:
                this_pa_num = pa_index + 1

    return this_pa_num


def get_pitcher_box_score_lines(pitcher_app_list, chunk_size, box_score_dict):
    pitcher_rows_svg = ''
    row_increment = 0

    if chunk_size == SMALL_CHUNK_SIZE:
        initial_y = PITCHER_BOX_SCORE_LARGE_Y
        text_size_1 = PITCHER_LARGE_FONT_SIZE
        text_size_2 = PITCHER_STATS_LARGE_FONT_SIZE
        stats_offset = PITCHER_BOX_STATS_LARGE_Y_OFFSET
        defined_text_increment = PITCHER_BOX_SCORE_LARGE_Y_INCREMENT
    elif chunk_size == LARGE_CHUNK_SIZE:
        initial_y = PITCHER_BOX_SCORE_SMALL_Y
        text_size_1 = PITCHER_SMALL_FONT_SIZE
        text_size_2 = PITCHER_STATS_SMALL_FONT_SIZE
        stats_offset = PITCHER_BOX_STATS_SMALL_Y_OFFSET
        defined_text_increment = PITCHER_BOX_SCORE_SMALL_Y_INCREMENT

    for pitcher_app in pitcher_app_list:
        if (len(str(pitcher_app.player_obj)) > 18 and
                chunk_size == SMALL_CHUNK_SIZE):
            initial_y = PITCHER_BOX_SCORE_MED_Y
            text_size_1 = PITCHER_MED_FONT_SIZE
            text_size_2 = PITCHER_STATS_MED_FONT_SIZE
            stats_offset = PITCHER_BOX_STATS_MED_Y_OFFSET
            defined_text_increment = PITCHER_BOX_SCORE_MED_Y_INCREMENT

    for pitcher_app in pitcher_app_list:
        initial_y = PITCHER_BOX_SCORE_SMALL_Y
        initial_era_stat_str = 'ERA: ' + str(pitcher_app.player_obj.era)
        appears_str = 'IN: {:2s}'.format(str(pitcher_app.start_inning_num))

        pitcher_str = '{}'.format(pitcher_app.player_obj)
        if pitcher_app.player_obj.pitch_hand:
            pitcher_str += ', {}'.format(pitcher_app.player_obj.pitch_hand)

        pitcher_rows_svg += PITCHER_STATS_LINE_TEMPLATE.format(
            pitcher_id=pitcher_app.player_obj.mlb_id,
            name_y_pos=initial_y + row_increment,
            stats_y_pos=stats_offset + row_increment,
            pitcher=pitcher_str,
            stats=initial_era_stat_str,
            appears=appears_str,
            size_1=text_size_1,
            size_2=text_size_2
        )

        row_increment += defined_text_increment

    return pitcher_rows_svg


def chunks(this_list, num_elements):
    for i in range(0, len(this_list), num_elements):
        yield this_list[i:i + num_elements]


def create_pitcher_stats_svg(chunk_tuple_list, chunk_size, box_score_dict):
    pitcher_stats_svg = ''
    for location, pitcher_chunk in chunk_tuple_list:
        x_box, y_box = location
        pitcher_stats_svg += PITCHER_STATS_HEADER.format(x_box=x_box,
                                                         y_box=y_box+(BOX_HEIGHT*(LEN_BATTING_LIST-9)))

        pitcher_stats_svg += '{}{}'.format(
            get_pitcher_box_score_lines(pitcher_chunk,
                                        chunk_size,
                                        box_score_dict),
            SVG_FOOTER
        )

    return pitcher_stats_svg


def add_team_pitcher_box_score(team, box_score_dict, offset):
    pitcher_app_list = team.pitcher_list
    if len(pitcher_app_list) <= 10:
        chunk_size = SMALL_CHUNK_SIZE
    else:
        chunk_size = LARGE_CHUNK_SIZE

    pitcher_chunk_list = list(chunks(pitcher_app_list, chunk_size))
    location_tuple_list = [
        (0, BOX_HEIGHT * 10 + offset),
        (WIDTH // 2, BOX_HEIGHT * 10 + offset)
    ]

    chunk_tuple_list = []
    for location_index, location_tuple in enumerate(location_tuple_list):
        if location_index < len(pitcher_chunk_list):
            pitcher_chunk = pitcher_chunk_list[location_index]
        else:
            pitcher_chunk = []

        chunk_tuple_list.append((location_tuple, pitcher_chunk))

    pitcher_stats_svg = create_pitcher_stats_svg(chunk_tuple_list,
                                                 chunk_size,
                                                 box_score_dict)

    return pitcher_stats_svg


def add_all_pitcher_box_scores(game):
    all_pitcher_box_svg = ''

    tuple_list = [
        (game.home_team,
         game.home_pitcher_box_score_dict,
         0),
        (game.away_team,
         game.away_pitcher_box_score_dict,
         HEIGHT // 2)
    ]

    for this_tuple in tuple_list:
        team, box_score_dict, offset = this_tuple
        all_pitcher_box_svg += add_team_pitcher_box_score(team,
                                                          box_score_dict,
                                                          offset)

    return all_pitcher_box_svg


def get_team_stats_svg():
    team_stats_svg = ''
    game_width = get_game_width()
    tuple_list = [
        (
            game_width - (BOX_WIDTH * 2),
            (BOX_HEIGHT * LEN_BATTING_LIST +
             BOX_HEIGHT),
        ), (
            game_width - (BOX_WIDTH * 2),
            (HEIGHT // 2 +
             BOX_HEIGHT * LEN_BATTING_LIST +
             BOX_HEIGHT),
        )
    ]

    for box_x, box_y in tuple_list:
        team_stats_svg += get_team_stats_box(box_x, box_y)

    return team_stats_svg


def get_box_score_totals():
    box_score_totals_svg = ''
    game_width = get_game_width()

    tuple_list = [
        (
            game_width - BOX_WIDTH,
            6 * BOX_HEIGHT + BOX_HEIGHT // 2
        ),
        (
            game_width - BOX_WIDTH,
            (6 * BOX_HEIGHT + BOX_HEIGHT // 2 +
             HEIGHT // 2)
        )
    ]

    for x_pos, y_pos in tuple_list:
        box_score_totals_svg += TOTAL_BOX_SCORE_STATS_BOX.format(
            box_x=x_pos,
            box_y=y_pos
        )

    return box_score_totals_svg


def assemble_stats_svg():
    stats_svg = ''
    for n in range(2, NUM_MINIMUM_INNINGS+EXTRA_COLUMNS):
        box_x = n * BOX_WIDTH

        box_y = (HEIGHT // 2 +
                 BOX_HEIGHT * LEN_BATTING_LIST +
                 BOX_HEIGHT // 2)

        if n <= NUM_MINIMUM_INNINGS + 1:
            stats_svg += get_inning_stats_box(box_x, box_y)
        else:
            stats_svg += (INNING_STATS_BOX.format(
                box_x=box_x,
                box_y=box_y,
                stats_str_1='',
                stats_str_2='',
                stats_str_3='',
                stats_str_4='',
                stats_str_5='',
                stats_str_6=''
            ))

        box_y = (BOX_HEIGHT * LEN_BATTING_LIST +
                 BOX_HEIGHT // 2)

        if n <= NUM_MINIMUM_INNINGS + 1:
            stats_svg += get_inning_stats_box(box_x, box_y)
        else:
            stats_svg += (INNING_STATS_BOX.format(
                box_x=box_x,
                box_y=box_y,
                stats_str_1='',
                stats_str_2='',
                stats_str_3='',
                stats_str_4='',
                stats_str_5='',
                stats_str_6='')
            )

    return stats_svg


def get_logo(game):
    signature_svg = ''
    game_width = get_game_width()

    signature_svg = ''
    x_pos = game_width - BOX_WIDTH
    y_pos = 8 * BOX_HEIGHT + BOX_HEIGHT // 2
    away_logo_str = LOGO_DICT.get(game.away_team.abbreviation, DEFAULT_LOGO)
    signature_svg += AWAY_LOGO.format(x_pos=x_pos,
                                      y_pos=y_pos,
                                      logo=away_logo_str)

    x_pos = game_width - BOX_WIDTH
    y_pos = 8 * BOX_HEIGHT + BOX_HEIGHT // 2 + HEIGHT // 2
    home_logo_str = LOGO_DICT.get(game.home_team.abbreviation, DEFAULT_LOGO)
    signature_svg += HOME_LOGO.format(x_pos=x_pos,
                                      y_pos=y_pos,
                                      logo=home_logo_str)

    return signature_svg


def write_individual_pa_svg(this_x_pos, this_y_pos):
    this_svg = '{}{}'.format(
        SVG_HEADER.format(x_pos=this_x_pos, y_pos=this_y_pos),
        SVG_FOOTER
    )

    return this_svg


def assemble_box_content_dict():
    content_list_svg = ''
    top_pa_index = 0
    bottom_pa_index = 0
    for inning_num in range(2, NUM_MINIMUM_INNINGS+2):
        for b in range(1, LEN_BATTING_LIST+1):
            top_offset = top_pa_index % LEN_BATTING_LIST
            bottom_offset = bottom_pa_index % LEN_BATTING_LIST
            this_x_pos = inning_num * BOX_WIDTH

            if inning_num > 9:
                bottom_offset = (bottom_pa_index - 1) % LEN_BATTING_LIST

            this_y_pos = (HEIGHT // 2 +
                          bottom_offset * BOX_HEIGHT +
                          BOX_HEIGHT // 2)
            content_list_svg += write_individual_pa_svg(
                                            this_x_pos,
                                            this_y_pos)
            if inning_num > 9:
                top_offset = (top_pa_index - 1) % LEN_BATTING_LIST

            this_y_pos = (top_offset * BOX_HEIGHT +
                          BOX_HEIGHT // 2)

            content_list_svg += write_individual_pa_svg(
                                            this_x_pos,
                                            this_y_pos)
            bottom_pa_index += 1
            top_pa_index += 1

    return content_list_svg


def get_game_title_str(game):
    game_teams_str = '{} @ {}'.format(game.away_team.name,
                                      game.home_team.name)

    return game_teams_str


def assemble_game_title_svg(game):
    game_title_svg = ''
    game_str = '{} @ {}'.format(game.away_team.name, game.home_team.name)
    this_start_datetime = (game.start_datetime if game.start_datetime
                           else game.expected_start_datetime)

    if this_start_datetime:
        this_start_datetime = this_start_datetime.astimezone(
            timezone(game.timezone_str)
        )

        est_time = this_start_datetime.astimezone(
            timezone(EASTERN_TIMEZONE_STR)
        )

        if ((est_time.hour == 23 and est_time.minute == 33) or
                (est_time.hour == 0 and est_time.minute == 0)):
            game_datetime = '{}'.format(
                this_start_datetime.strftime('%a %b %d %Y')
            )
        elif game.start_datetime and game.end_datetime:
            start_str = game.start_datetime.astimezone(
                timezone(game.timezone_str)
            ).strftime('%a %b %d %Y, %-I:%M %p')

            end_str = game.end_datetime.astimezone(
                timezone(game.timezone_str)
            ).strftime(' - %-I:%M %p %Z')

            game_datetime = '{}{}'.format(start_str, end_str)
        else:
            game_datetime = game.expected_start_datetime.astimezone(
                timezone(game.timezone_str)
            ).strftime('%a %b %d %Y, %-I:%M %p %Z')

        if game.is_doubleheader:
            game_datetime += ', Game {}'.format(game.game_date_str[-1])

        if game.is_suspended:
            game_datetime += ', Suspended'
        elif game.is_postponed:
            game_datetime += ', Postponed'

    else:
        game_datetime = ''

    game_width = get_game_width()
    location_str = game.location.replace('&', '&amp;')
    detail_str = ''
    if game.attendance:
        detail_str += 'Att. {:,}'.format(int(game.attendance))

    if game.weather:
        if detail_str != '':
            detail_str += ' - '

        detail_str += game.weather

    if game.temp:
        if detail_str != '':
            detail_str += ' - '

        detail_str += '{} F'.format(int(game.temp))

    tuple_list = [('TOP', 0), ('BOTTOM', HEIGHT // 2)]
    for inning_half_str, y_pos in tuple_list:
        title_size = BIG_TITLE_SIZE if len(game_str) < 42 else SMALL_TITLE_SIZE
        game_title_svg += BIG_SVG_TITLE.format(
            x_pos=game_width - BOX_WIDTH,
            y_pos=y_pos,
            inning_half=inning_half_str,
            game_str=game_str,
            location=location_str,
            datetime=game_datetime,
            detail_str=detail_str,
            title_size=title_size
        )

    return game_title_svg


def get_big_rectangles():
    game_width = get_game_width()

    big_rectangles_svg = '{}{}'.format(
        BIG_RECTANGLE.format(y_pos=0, y_pos_2=HEIGHT // 2, width=game_width),
        BIG_RECTANGLE.format(y_pos=HEIGHT // 2, y_pos_2=HEIGHT, width=game_width)
    )

    return big_rectangles_svg


def get_game_svg_str(game):
    big_svg_text = '{}{}{}{}{}{}{}{}{}{}{}'.format(
        get_big_svg_header(),  # header of BATTER 1-10
        get_batter_list_and_stats(game),  # left batter list and right stats
        assemble_stats_svg(),  # inning stats
        assemble_box_content_dict(),  # the boxes!!!!
        get_team_stats_svg(),  # bottom right box
        add_all_pitcher_box_scores(game),   # bottom pitcher box list
        assemble_game_title_svg(game),  # side team name / info
        get_logo(game),  # team logo
        get_box_score_totals(),  # final stats
        get_big_rectangles(),  # large outer box
        SVG_FOOTER
    )

    return big_svg_text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('date', type=str,
                        help='Format: YYYY-MM-DD')
    parser.add_argument('away_team', type=str,
                        help='Three letters, e.g., "CHC" for Chicago Cubs')
    parser.add_argument('home_team', type=str,
                        help='Three letters, e.g., "CHC" for Chicago Cubs')
    parser.add_argument('--game', type=int, default=1, required=False,
                        help='1 or 2 for a double header')
    args = parser.parse_args()

    game_id, game = get_game_from_url(args.date, args.away_team, args.home_team, args.game)

    with open(game_id + '.svg', 'w') as fh:
        fh.write(get_game_svg_str(game))


if __name__ == "__main__":
    main()
