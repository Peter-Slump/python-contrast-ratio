#!/usr/bin/env python
import re

def get_hex_code(color):
    result = re.match(r'^#?([a-f0-9]{3,3}|[a-f0-9]{6,6})$', color)
    
    if result is None:
        raise Exception('Could not extract color')
        
    result = list(result.group(1))

    if len(result) == 6:
        result = [result[i] + result[i+1] for i in range(0, len(result), 2)]
    else:
        result = [result[i] + result[i] for i in range(0, len(result))]
        
    return [int(hex_code, 16) for hex_code in result]
    
def calculate_luminace(color_code):
    index = float(color_code) / 255 

    if index < 0.03928:
        return index / 12.92
    else:
        return ( ( index + 0.055 ) / 1.055 ) ** 2.4
    
def calculate_relative_luminance(rgb):
    return 0.2126 * calculate_luminace(rgb[0]) + 0.7152 * calculate_luminace(rgb[1]) + 0.0722 * calculate_luminace(rgb[2]) 


if __name__ == '__main__':
    import sys

    color_one = get_hex_code(sys.argv[1])
    color_two = get_hex_code(sys.argv[2])

    light = color_one if sum(color_one) > sum(color_two) else color_two
    dark = color_one if sum(color_one) < sum(color_two) else color_two

    contrast_ratio = ( calculate_relative_luminance(light) + 0.05 ) / ( calculate_relative_luminance(dark) + 0.05 )

    if contrast_ratio < 3:
        usable_for = "incidental usage or logotypes."
    elif contrast_ratio >= 3 and contrast_ratio < 4.5:
        usable_for = "minimum contrast large text."
    elif contrast_ratio >= 4.5 and contrast_ratio < 7:
        usable_for = "minimum contrast or enhanced contrast large text."
    elif contrast_ratio >= 7:
        usable_for = "enhanced contrast."

    print """
    Contrast ratio calculator
    
    Usable for the W3C Web Content Accessibility Guidelines (WCAG) 2.0

    http://www.w3.org/TR/2008/REC-WCAG20-20081211/

    1.4.3 Contrast (Minimum): 4.5:1 (Large text: 3:1)
    1.4.6 Contrast (Enhanced): 7:1 (Large text: 4.5:1)

    Calculated contrast:
    
    {:.01F}:1 Usable for {}
    """.format(contrast_ratio, usable_for)
