import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

rivers = gpd.read_file("HydroRIVERS_v10_sa_shp/HydroRIVERS_v10_sa.shp")
rivers = rivers.to_crs(epsg=3857)

world = gpd.read_file("natural_earth//ne_110m_admin_0_countries.shp")
south_america = world[world['CONTINENT'] == 'South America'].to_crs(epsg=3857)

fig, ax = plt.subplots(figsize=(15, 12), facecolor="#f8f9fa")

rivers.plot(ax=ax, color='royalblue', linewidth=0.5, alpha=0.7, label="Rivers")
south_america.boundary.plot(ax=ax, edgecolor='black', linewidth=1, label="Country Borders")

ax.set_xlim(rivers.total_bounds[0], rivers.total_bounds[2])
ax.set_ylim(rivers.total_bounds[1], rivers.total_bounds[3])

cx.add_basemap(ax, source=cx.providers.CartoDB.Positron, zoom=5)

ax.set_title("South America River Network", fontsize=18, fontweight="bold", pad=15)
ax.set_facecolor("#eaeaea")
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
ax.axis("off")

plt.tight_layout()
plt.show()
