from pyaxidraw import axidraw


ad = axidraw.AxiDraw()

# Ensure proper setup before applying options
# This connects to the AxiDraw and loads the SVG
ad.plot_setup("robo_kavi_box_with_footer_vectorized.svg", hold_output=True)

# --- AxiDraw General Settings ---
# These control the physical movement and pen lift.
# Your current values seem reasonable,
# but feel free to fine-tune based on your pen/paper.
ad.options.pen_pos_down = 30

ad.options.pen_pos_up = 70

ad.options.speed_pendown = 25   # Plotting speed (lower = slower, more precise)
ad.options.speed_penup = 75
# Pen-up travel speed (higher = faster movement when pen is up)
ad.options.accel = 15
# Acceleration setting
ad.options.model = 2
ad.options.units = 1
ad.options.const_speed = False   # Keep this False for typical plotting

# --- CRITICAL CHANGES FOR PREVENTING UNWANTED LINES ---
# These options tell pyaxidraw how to interpret and process the paths in th
# The goal is to ensure it treats distinct objects as separate and lifts the .

ad.options.mode = "plot"         # Ensure standard plotting mode is active.
ad.options.reordering = 0
ad.options.shuffling = 0

# --- Optional (but good practice) to ensure SVG dimensions are respected ---
ad.options.page_size = "custom"
ad.options.x_offset = 0.0        # No horizontal offset
ad.options.y_offset = 0.0        # No vertical offset
ad.options.rotate = 0.0          # No rotation of the entire plot

print("ℹ️ AxiDraw options set for clean plotting (no unwanted lines).")

# Run the plot operation
ad.plot_run()

print("✅ Plotting complete.")
