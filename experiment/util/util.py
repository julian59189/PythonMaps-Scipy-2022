import matplotlib as matplotlib
import matplotlib.cm as cm

def color_map_color(value, cmap_name='RdYlGn', vmin=0, vmax=1):
    # norm = plt.Normalize(vmin, vmax)
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cmap = cm.get_cmap(cmap_name)  # PiYG
    cmap = cmap.reversed()
    rgb = cmap(norm(abs(value)))[:3]  # will return rgba, we take only first 3 so we get rgb
    color = matplotlib.colors.rgb2hex(rgb)
    return color

def int_to_color(value, maxval, default_col='gray'):
    try:
        return color_map_color(float(value), vmin=0, vmax=maxval)
    except (TypeError, ValueError):
        return default_col