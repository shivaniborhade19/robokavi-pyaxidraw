from pyaxidraw import axidraw


def plot_svg(final_path):
    try:
        print("🖨️ Plotting:", final_path)

        ad = axidraw.AxiDraw()
        ad.plot_setup(final_path)

        # AxiDraw speed/settings
        ad.options.pen_pos_down = 30
        ad.options.pen_pos_up = 70
        ad.options.speed_pendown = 25
        ad.options.speed_penup = 75
        ad.options.accel = 15
        ad.options.model = 2
        ad.options.units = 1
        ad.options.const_speed = False

        ad.plot_run()
        print("✅ Plotting complete.")
    except Exception as e:
        print("❌ Plotting failed:", str(e))
