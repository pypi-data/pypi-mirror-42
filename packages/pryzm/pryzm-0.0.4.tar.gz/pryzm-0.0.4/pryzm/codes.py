cap27 = '\033[27m'
text_attributes = {
    'at_off':       0,
    'at_bold':      1,
    'at_dim':       2,
    'at_italic':    3,
    'at_under':     4,
    'at_blink':     5,
    'at_reverse':   6,
    'at_hide':      8,

    'fg_black':     30,
    'fg_red':       31,
    'fg_green':     32,
    'fg_yellow':    33,
    'fg_blue':      34,
    'fg_magenta':   35,
    'fg_cyan':      36,
    'fg_white':     37,

    'bg_black':     40,
    'bg_red':       41,
    'bg_green':     42,
    'bg_yellow':    43,
    'bg_blue':      44,
    'bg_magenta':   45,
    'bg_cyan':      46,
    'bg_white':     47,
}

clear = {
    'clear_screen': '2J',
    'clear_screen_to_end': '0J',
    'clear_screen_to_start': '1J',
    'clear_line': '2K',
    'clear_line_to_end': '0K',
    'clear_line_to_start': '1K',
    }

cursor = {
    'move_up': 'A',
    'move_down': 'B',
    'move_right': 'C',
    'move_left': 'D',
    'move_next_line': 'E',
    'move_prev_line': 'F',
    'move_column': 'G'
    }

