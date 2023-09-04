import pcbnew
import os
import re

X_OFFSET = 0
Y_OFFSET = 40
X_KEY_CENTER_OFFSET = -0.5625
Y_KEY_CENTER_OFFSET = -4.7750
KEY_MM = 19.05
LEFT_PAD = 2
RIGHT_PAD = 2
BOTTOM_PAD = 2
CORNER_RADIUS = 3

layout = [
    ['RotaryEncoder_Switch', 'SW_`', 'SW_1', 'SW_2', 'SW_3', 'SW_4', 'SW_5', 'SW_6', 'SW_7', 'SW_8', 'SW_9', 'SW_0', 'SW_-', 'SW_+', 'SW_back'],
    ['SW_esc', 'SW_tab', 'SW_q', 'SW_w', 'SW_e', 'SW_r', 'SW_t', 'SW_y', 'SW_u', 'SW_i', 'SW_o', 'SW_p', 'SW_[', 'SW_]', 'SW_\\'],
    ['SW_del', 'SW_caps', 'SW_a', 'SW_s', 'SW_d', 'SW_f', 'SW_g', 'SW_h', 'SW_j', 'SW_k', 'SW_l', 'SW_;', 'SW_\'', 'SW_enter'],
    ['SW_ins', 'SW_shift', 'SW_z', 'SW_x', 'SW_c', 'SW_v', 'SW_b', 'SW_n', 'SW_m', 'SW_,', 'SW_.', 'SW_/', 'SW_r_shift'],
    ['SW_fn1', 'SW_ctrl', 'SW_super', 'SW_alt', 'SW_space', 'SW_fn2', 'SW_left', 'SW_down', 'SW_up', 'SW_right'],
]

layout_flatten = sum(layout, [])
switch_names = set(layout_flatten)
assert len(switch_names) == len(layout_flatten), (len(switch_names), len(layout_flatten))

special_sizes = {
    'SW_back': 2.0,
    'SW_tab': 1.5,
    'SW_\\': 1.5,
    'SW_caps': 1.75,
    'SW_enter': 2.25,
    'SW_shift': 2.25,
    'SW_r_shift': 2.75,
    'SW_ctrl': 1.25,
    'SW_super': 1.25,
    'SW_alt': 1.25,
    'SW_space': 6.25,
}

stablizers = {
    'SW_back': 'Stabilizer_Cherry_MX_2.00u',
    'SW_enter': 'Stabilizer_Cherry_MX_2.00u',
    'SW_shift': 'Stabilizer_Cherry_MX_2.00u',
    'SW_r_shift': 'Stabilizer_Cherry_MX_2.00u',
    'SW_space': 'Stabilizer_Cherry_MX_6.25u',
}

STABLIZER_LIB_PATH = 'footprints/com_github_perigoso_keyswitch-kicad-library/Mounting_Keyboard_Stabilizer.pretty'

pcb = pcbnew.GetBoard()

name_to_footprint = dict()
reference_to_footprint = dict()
for f in pcb.Footprints():
    show_text = f.Value().GetShownText()
    name_to_footprint[show_text] = f
    reference_to_footprint[f.GetReference()] = f

y = KEY_MM / 2 + Y_OFFSET
name_to_xy = dict()

# Place the switches

for row in layout:
    x = LEFT_PAD + X_OFFSET
    previous_width = 0
    for key in row:
        f = name_to_footprint[key]
        width = special_sizes.get(key, 1.0) * KEY_MM
        x += (previous_width + width) / 2
        f.Flip(f.GetPosition(), True)
        f.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x + X_KEY_CENTER_OFFSET, y + Y_KEY_CENTER_OFFSET)))
        name_to_xy[key] = (x, y)
        previous_width = width
        if key in stablizers:
            stab_name = stablizers[key]
            stab_f = pcbnew.FootprintLoad(os.path.join(os.getenv('KICAD7_3RD_PARTY'), STABLIZER_LIB_PATH),
                                          stab_name)
            stab_f.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x, y)))
            stab_f.Reference().SetVisible(False)
            pcb.Add(stab_f)
    y += KEY_MM

rotary_encoder = name_to_footprint['RotaryEncoder_Switch']
rotary_encoder.Flip(rotary_encoder.GetPosition(), True)
x = name_to_xy['SW_esc'][0] - 7.48
y = name_to_xy['SW_back'][1] - 2.48
rotary_encoder.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x, y)))
name_to_xy['RotaryEncoder_Switch'] = (x, y)

# Place Pi Zero

rpi = name_to_footprint['Pi_Zero']
rpi.Rotate(rpi.GetPosition(), pcbnew.EDA_ANGLE(270, pcbnew.DEGREES_T))
y = name_to_xy['SW_back'][1] - 6 - KEY_MM / 2
x = name_to_xy['SW_right'][0] - 33 + KEY_MM / 2
rpi.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x, y)))
name_to_xy['Pi_Zero'] = (x, y)

# Place Pico

pico = name_to_footprint['Pico']
pico.Rotate(pico.GetPosition(), pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
y = name_to_xy['Pi_Zero'][1] - 8
x = X_OFFSET + 26  # Length of pico is 52. Height is 22.
pico.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x, y)))
name_to_xy['Pico'] = (x, y)

# Place the screen

x, y = name_to_xy['Pico']
screen = name_to_footprint['JMD0.96C']
screen.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x + 42, y - 3)))

# Place the diodes

# Diode length 9.720 mm and width 2.5 mm. Location is at center

all_diodes = []
for ref in reference_to_footprint.keys():
    match = re.findall('D([0-9]+)', ref)
    if match:
        all_diodes.append((ref, int(match[0])))

all_diodes.sort(key=lambda x: x[1])

assert len(all_diodes) == 84
all_diode_rows = []
for _ in range(6):
    all_diode_rows.append([])

for ref, idx in all_diodes:
    all_diode_rows[(idx - 1) // 14].append(reference_to_footprint[ref])


horizontal_gap = 1
vertical_gap = 1
pico_x, pico_y = name_to_xy['Pico']
start_x, start_y = pico_x + 55 + 9.72 - 1.05, pico_y - 15

for i, row in enumerate(all_diode_rows):
    for j, diode in enumerate(row):
        x = start_x + j * (9.72 + horizontal_gap)
        y = start_y + i * (2.5 + horizontal_gap)
        diode.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(x, y)))
        name_to_xy[diode.Value()] = (x, y)

# Add edge cut border lines

switch_width = name_to_xy['SW_right'][0] + KEY_MM / 2
switch_bottom = name_to_xy['SW_space'][1] + KEY_MM / 2

left_x = X_OFFSET
right_x = switch_width + RIGHT_PAD
top_y = name_to_xy['Pi_Zero'][1] - 27
bottom_y = switch_bottom + BOTTOM_PAD

left = pcbnew.PCB_SHAPE()
left.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x, top_y + CORNER_RADIUS)))
left.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x, bottom_y - CORNER_RADIUS)))
left.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(left)

right = pcbnew.PCB_SHAPE()
right.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x, top_y + CORNER_RADIUS)))
right.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x, bottom_y - CORNER_RADIUS)))
right.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(right)

top = pcbnew.PCB_SHAPE()
top.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x + CORNER_RADIUS, top_y)))
top.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x - CORNER_RADIUS, top_y)))
top.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(top)

bottom = pcbnew.PCB_SHAPE()
bottom.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x + CORNER_RADIUS, bottom_y)))
bottom.SetEnd(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x - CORNER_RADIUS, bottom_y)))
bottom.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(bottom)

# Add corner arcs

top_left = pcbnew.PCB_SHAPE()
top_left.SetShape(pcbnew.SHAPE_T_ARC)
top_left.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x, top_y + CORNER_RADIUS)))
top_left.SetCenter(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x + CORNER_RADIUS, top_y + CORNER_RADIUS)))
top_left.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
top_left.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(top_left)

top_right = pcbnew.PCB_SHAPE()
top_right.SetShape(pcbnew.SHAPE_T_ARC)
top_right.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x - CORNER_RADIUS, top_y)))
top_right.SetCenter(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x - CORNER_RADIUS, top_y + CORNER_RADIUS)))
top_right.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
top_right.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(top_right)

bottom_right = pcbnew.PCB_SHAPE()
bottom_right.SetShape(pcbnew.SHAPE_T_ARC)
bottom_right.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x, bottom_y - CORNER_RADIUS)))
bottom_right.SetCenter(pcbnew.VECTOR2I(pcbnew.wxPointMM(right_x - CORNER_RADIUS, bottom_y - CORNER_RADIUS)))
bottom_right.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
bottom_right.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(bottom_right)

bottom_left = pcbnew.PCB_SHAPE()
bottom_left.SetShape(pcbnew.SHAPE_T_ARC)
bottom_left.SetStart(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x + CORNER_RADIUS, bottom_y)))
bottom_left.SetCenter(pcbnew.VECTOR2I(pcbnew.wxPointMM(left_x + CORNER_RADIUS, bottom_y - CORNER_RADIUS)))
bottom_left.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
bottom_left.SetLayer(pcb.GetLayerID('Edge.Cuts'))
pcb.Drawings().append(bottom_left)

# Place the connectors

space_x = name_to_xy['SW_space'][0]

extra_key = name_to_footprint['Extra_Keys']
extra_key.Flip(extra_key.GetPosition(), True)
extra_key.Rotate(extra_key.GetPosition(), pcbnew.EDA_ANGLE(270, pcbnew.DEGREES_T))
extra_key.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(space_x + (20 + KEY_MM) + 5.08, bottom_y - 10.09)))

joystick = name_to_footprint['JoyStick_Or_I2C1']
joystick.Flip(joystick.GetPosition(), True)
joystick.Rotate(joystick.GetPosition(), pcbnew.EDA_ANGLE(270, pcbnew.DEGREES_T))
joystick.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(space_x - (20 + KEY_MM) + 5.08, bottom_y - 10.09)))

# Add mounting holes
MOUNTING_HOLE_PATH = os.path.join(os.getenv('KICAD7_FOOTPRINT_DIR'), 'MountingHole.pretty')
space_y = name_to_xy['SW_space'][1]

centers = [(space_x - 9 - KEY_MM, space_y - 4), (space_x + 9 + KEY_MM, space_y - 4)]

for center in centers:
    hole = pcbnew.FootprintLoad(MOUNTING_HOLE_PATH, 'MountingHole_3.2mm_M3')
    hole.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPointMM(*center)))
    hole.Reference().SetVisible(False)
    pcb.Add(hole)

pcbnew.Refresh()