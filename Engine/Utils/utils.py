from typing import Tuple

def containsnum(string: str) -> bool:
    for i in range(10):
        if str(i) in string: return True

    return False

def ishex(string: str) -> bool:
    if "#" not in string: return False

    try:
        int(string.replace('#', ''), 16)
        return True
    except: return False

def hex_to_rgb(hex_string: str) -> Tuple[int, int, int]:
    if len(hex_string) < 7:
        for _ in range(7-len(hex_string)): hex_string += "0"

    return tuple(int(hex_string[i:i+2], 16) for i in range(1, 6, 2))

def convert_size_keywords(string: str) -> Tuple[float, str] | None:
    if string == "xx-small": return (0.5625, "rem")
    elif string == "x-small": return (0.625, "rem")
    elif string == "small": return (0.8125, "rem")
    elif string == "medium": return (1.0, "rem")
    elif string == "large": return (1.125, "rem")
    elif string == "x-large": return (1.5, "rem")
    elif string == "xx-large": return (2.0, "rem")
    else: return None

def find_nums_from_str(string_with_nums: str) -> Tuple[float, str] | None:
    for i in range(len(string_with_nums)):
        if string_with_nums[i].isalpha() or string_with_nums[i] == '%':
            if string_with_nums[:i] == '': return None

            try: return float(string_with_nums[:i]), string_with_nums[i:]
            except: return None

    return convert_size_keywords(string_with_nums)

def remove_units(num_str: str, tag_size: float, parent_size: float, view_width: float, view_height: float) -> float:
    if type(num_str) == int or type(num_str) == float: return num_str

    num_str = num_str.lower().split(' ')[0]

    split_num: Tuple[float, str] | None = find_nums_from_str(num_str)

    if split_num is None: 
        if type(tag_size) == str: return 16
        else: return tag_size
    
    value, unit = split_num
    
    if unit == "cm": return value * 37.8
    elif unit == "mm": return value * 3.78
    elif unit == "q": return value * 0.945
    elif unit == "in": return value * 96
    elif unit == "pc": return value * 16
    elif unit == "pt": return value * 1.333333
    elif unit == "px": return value

    # relative sizes
    elif unit == "em": return value * parent_size
    elif unit == "rem": return value * tag_size
    elif unit == "vw": return view_width / value
    elif unit == "vh": return view_height / value
    elif unit == "%":
        if type(tag_size) == str: return 16
        return tag_size * value / 100

    # Style not found    
    if type(tag_size) == str: return 16
    else: return tag_size