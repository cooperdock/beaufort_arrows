#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 13:02:32 2025

@author: scooperd
"""

import math
import os
import zipfile
from io import BytesIO
from xml.etree.ElementTree import Element, SubElement, tostring
import glob
import svgutils.transform
import svgutils.compose


# used this as model: https://commons.wikimedia.org/wiki/File:Symbols_of_wind_speed_-_wind_barbs_-_var1.svg
def create_svg_arrow(angle_deg: int, wind_speed: int) -> str:
    svg = Element('svg', {
        'xmlns': "http://www.w3.org/2000/svg",
        # 'width': "100",
        # 'height': "100",
        'viewBox': "0 0 100 100"
    })
    
    g = SubElement(svg, 'g', {
        'transform': f'rotate({angle_deg}, 50, 50)',
        'stroke': 'black',
        'stroke-width': '4',
        'fill': 'black',
        'stroke-linecap': 'round'
    })

    SubElement(g, 'line', {
        'x1': '50',
        'y1': '80',
        'x2': '50',
        'y2': '20'
    })

    SubElement(g, 'polygon', {
        'points': '45,20 55,20 50,10',
        'fill': 'black'
    })

    # Add wind barbs (1 barb per 10 knots)
    barb_spacing = 10
    num_barbs = wind_speed // 10
    if wind_speed % 10 >= 5:
        end_small = True
    else:
        end_small = False
        
    if wind_speed < 50:
        for i in range(num_barbs):
            # if end_small and i==num_barbs-1:
            #     barb_length = 5
            # else:
            #     barb_length = 10
            y = 90 - (i + 1) * barb_spacing
            SubElement(g, 'line', {
                'x1': '50',
                'y1': str(y),
                'x2': '65',
                'y2': str(y + 5)
            })
        if end_small:
            y = 90 - (num_barbs + 1) * barb_spacing
            SubElement(g, 'line', {
                'x1': '50',
                'y1': str(y),
                'x2': '58',
                'y2': str(y + 2.5)
                })
    elif wind_speed < 100:
        SubElement(g, 'polygon', {
            'points': '50,90 50,80 60,85',
            'fill': 'black'
        })
        num_barbs = num_barbs - 5
        for i in range(num_barbs):
            # if end_small and i==num_barbs-1:
            #     barb_length = 5
            # else:
            #     barb_length = 10
            y = 80 - (i + 1) * barb_spacing
            SubElement(g, 'line', {
                'x1': '50',
                'y1': str(y),
                'x2': '65',
                'y2': str(y + 5)
            })
        if end_small:
            y = 80 - (num_barbs + 1) * barb_spacing
            SubElement(g, 'line', {
                'x1': '50',
                'y1': str(y),
                'x2': '58',
                'y2': str(y + 2.5)
                })
    else:
        SubElement(g, 'polygon', {
            'points': '50,90 50,80 60,85',
            'fill': 'black'
        })
        SubElement(g, 'polygon', {
            'points': '50,75 50,65 60,70',
            'fill': 'black'
        })
        

    return tostring(svg, encoding='unicode')

# Beaufort scale approximation (mid-range wind speeds in knots)
beaufort_scale = {
    0: 0,
    1: 3,
    2: 7,
    3: 12,
    4: 18,
    5: 24,
    6: 31,
    7: 38,
    8: 46,
    9: 54,
    10: 63,
    11: 72,
    12: 82
}

values = list(range(0,105,5))

angles = list(range(0, 360, 15))

# Output directory
output_dir = "beaufort_arrows"
os.makedirs(output_dir, exist_ok=True)


    
# def rotate_svg(file, angle_deg):

#     # Load the SVG file
#     svg = svgutils.transform.fromfile(f)

#     # Create an SVG object from the loaded file
#     originalSVG = svgutils.compose.SVG(f)

#     # Rotate the SVG (e.g., 90 degrees)
#     originalSVG.rotate(angle_deg)

#     # Optionally, move the rotated SVG (adjust coordinates as needed)
#     # originalSVG.move(svg.height, 10) # Example: move based on original height

#     # Create a new Figure to contain the transformed SVG
#     # Ensure width and height are correctly set, especially after rotation
#     figure = svgutils.compose.Figure(float(svg.height), float(svg.width), originalSVG)

#     # Save the rotated SVG
#     figure.save(file.split(".")[0] + "_" + str(15) + "deg.svg")


# def rotate_svg(svg,angle_deg):
    
#     g = SubElement(svg, 'g', {
#         'transform': f'rotate({angle_deg}, 50, 50)',
#         'stroke': 'black',
#         'stroke-width': '4',
#         'fill': 'black',
#         'stroke-linecap': 'round'
#     })
    
#     filename = f'arrow_bft{bft}_{angle}deg.svg'
#     with open(os.path.join(output_dir, filename), 'w') as f:
#         f.write(svg)

# f='/Users/scooperd/Documents/From Woodwell Comp/Brown/beaufort_arrows/arrow_bft0_0deg.svg'

# directory = '/Users/scooperd/Documents/wind_icons/'

# files = glob.glob(directory+"*.svg",recursive=True)

angles = list(range(0, 360, 15))
# Generate SVGs
for angle in angles:
    #for bft, wind_speed in beaufort_scale.items():
    for val in values:
    # for file in files:
    #     rotate_svg(file,angle)
        svg = create_svg_arrow(angle, val)
        filename = f'arrow_bft{val}_{angle}deg.svg'
        with open(os.path.join(output_dir, filename), 'w') as f:
            f.write(svg)

# Zip all SVGs
zip_filename = "beaufort_barbed_arrows.zip"
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for filename in os.listdir(output_dir):
        zipf.write(os.path.join(output_dir, filename), filename)

print(f"✅ Done! Archive saved as: {zip_filename}")
