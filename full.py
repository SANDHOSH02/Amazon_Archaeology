import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
from shapely.geometry import Point
from pyproj import CRS

# Load rivers
rivers = gpd.read_file("HydroRIVERS_v10_sa_shp/HydroRIVERS_v10_sa.shp").to_crs(epsg=3857)

# Load country borders
world = gpd.read_file("natural_earth/ne_110m_admin_0_countries.shp")
south_america = world[world["CONTINENT"] == "South America"].to_crs(epsg=3857)

# Load Mound Villages with UTM coordinates (EPSG:32719 for UTM Zone 19S in Acre)
mound_df = pd.read_csv("Dataset/mound_villages_acre.csv")

# Rename UTM columns to x and y for clarity
mound_df = mound_df.rename(columns={"UTM X (Easting)": "x", "UTM Y (Northing)": "y"})

# Create GeoDataFrame in UTM CRS
mound_gdf = gpd.GeoDataFrame(
    mound_df,
    geometry=gpd.points_from_xy(mound_df["x"], mound_df["y"]),
    crs="EPSG:32719"  # UTM zone appropriate for Acre, Brazil
).to_crs(epsg=3857)  # Convert to Web Mercator

# Plotting
fig, ax = plt.subplots(figsize=(15, 12), facecolor="#f8f9fa")

# Rivers
rivers.plot(ax=ax, color='royalblue', linewidth=0.5, alpha=0.5, label="Rivers")

# Borders
south_america.boundary.plot(ax=ax, edgecolor='black', linewidth=1)

# Mound Villages
mound_gdf.plot(ax=ax, color='green', markersize=30, label='Mound Villages')

# Set bounds to region of interest
ax.set_xlim(rivers.total_bounds[0], rivers.total_bounds[2])
ax.set_ylim(rivers.total_bounds[1], rivers.total_bounds[3])

# Basemap
cx.add_basemap(ax, source=cx.providers.CartoDB.Positron, zoom=5)

# Decorations
ax.set_title("Mound Villages and River Network in the Amazon", fontsize=18, fontweight='bold')
ax.axis("off")
plt.legend(loc='lower left')
plt.tight_layout()
plt.show()
