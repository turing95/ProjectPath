import time

import geopandas as gpd
import fiona
import matplotlib.pyplot as plt

import tilemapbase as tmp
from tilemapbase.mapping import points_from_frame
from tilemapbase.mapping import extent_from_frame

initated = False

def init():
    tmp.start_logging()

    tmp.init(create=True)
    t = tmp.tiles.build_OSM()
    initiated = True


def plot_path_to_png(timezone='2017-03-28 15:22:00.000000',
              shapefile='./shapefiles/speedy_Como_dataset.shp'):

    if not initated:
        init()

    print("Opening shapefile...")
    with fiona.open(shapefile) as np:
        meta = np.meta
        paths = []
        for feature in np:
            if feature['properties']['time_zone'] == timezone:
                paths.append(feature)
    print("Done.")

    tzgdf = gpd.GeoDataFrame.from_features(paths)

    extent = extent_from_frame(tzgdf)
    extent = extent.to_aspect(1.0)
    extent = extent.with_scaling(0.8)

    print("Plotting path...")

    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)


    plotter = tmp.Plotter(extent, t, width=600)
    points = points_from_frame(tzgdf)
    plotter.plot(ax, t)

    plt.plot(*points)


    ts = time.time()

    print("Done, saving image...")

    image_path='path' + str(ts).replace('.','') + '.png'
    plt.savefig(image_path, dpi=300)

    print("Done. Image saved as: " + image_path)

    return image_path
