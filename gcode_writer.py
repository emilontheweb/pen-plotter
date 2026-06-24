WORK_AREA_MM = 220
PEN_UP = 30
PEN_DOWN = 60
TRAVEL_FEED = 3000
DRAW_FEED = 1500

SERVO_DELAY = 300

def px_to_mm(x, y, scale):
    x_mm = x * scale
    y_mm = WORK_AREA_MM - (y * scale)
    return (x_mm, y_mm)

def pen_up():
    return [f"M280 P0 S{PEN_UP}", f"G4 P{SERVO_DELAY}"]
def pen_down():
    return [f"M280 P0 S{PEN_DOWN}", f"G4 P{SERVO_DELAY}"]

def draw_line(line, scale):
    (x0, y0), (x1, y1) = line
    start = px_to_mm(x0, y0, scale)
    end = px_to_mm(x1, y1, scale)
    
    cmds = []
    cmds += pen_up()
    cmds.append(f"G0 X{start[0]:.2f} Y{start[1]:.2f} F{TRAVEL_FEED}")
    cmds += pen_down()
    cmds.append(f"G1 X{end[0]:.2f} Y{end[1]:.2f} F{DRAW_FEED}")
    return cmds

def draw_layer(layer, scale):
    cmds = []
    cmds.append(f"; --- layer color {layer['color']} ---")
    for line in layer["lines"]:
        cmds += draw_line(line, scale)
    return cmds

def start_script():
    cmds = [
        "; === START ===",
        "G21", # units = mm
        "G90", # absolute positioning
        "M140 S0", # bed to 0°C (no heat)
        "G28", # home all axes
    ]
    cmds += pen_up()
    return cmds

def end_script():
    cmds = [
        "; === END ==="
    ] + pen_up()
    cmds.append("G0 X0 Y220")
    cmds.append("M84")
    return cmds

def write_gcode(layers, image_width, filename):
    scale = WORK_AREA_MM / image_width
    
    cmds = start_script()
    
    for i, layer in enumerate(layers):
        if i > 0:
            cmds.append("M0 Swap pen and resume")
        cmds += draw_layer(layer, scale)
        
    cmds += end_script()
    
    with open(filename, "w") as f:
        f.write("\n".join(cmds))