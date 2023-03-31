"""Analysis on Dutch airstrikes during Operation Inherent Resolve

Siem de Jong
"""

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from cartopy.mpl.geoaxes import GeoAxes

def read_data(file: str):
    """Read the data.

    Data is separated in a ; separated file.
    Decimal values are stored with commas.
    """
    data = pd.read_csv("(UNCLASS) 20230330 Database Nederlandse luchtaanvallen tijdens Operation Inherent Resolve.csv", delimiter=";", decimal=",")
    return data

def clean(data: pd.DataFrame) -> pd.DataFrame:
    """Clean the data."""
    data["Mission (UNCLASS)"] = data["Mission (UNCLASS)"].str.strip() # Because " CAS" should == "CAS"
    return data

def show_locations(data: pd.DataFrame) -> None:
    """Show the location distribution."""
    fig: Figure = plt.figure()
    ax: GeoAxes = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Bounding boxes: https://gist.github.com/graydon/11198540
    ax.set_extent((38.7923405291-1, 48.5679712258+1, 29.0990251735-1, 37.3852635768+1), crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    for label, grp in data.groupby("Mission (UNCLASS)"):
        lon = grp["Position LONG (UNCLASS)"].to_numpy()
        lat = grp["Position LAT (UNCLASS)"].to_numpy()
        ax.scatter(lon, lat, marker="o", s=11, alpha=0.7, transform=ccrs.Geodetic(), label=label)

    plt.title("Dutch airstrikes during Operation Inherent Resolve")
    plt.text(0.5, 0.25, "Iraq", fontsize=15, transform=ax.transAxes)
    plt.legend()
    plt.show()


def main(file) -> None:

    # Data is directly downloaded from
    # https://www.defensie.nl/downloads/applicaties/2023/03/30/database-nederlandse-luchtaanvallen-tijdens-operation-inherent-resolve
    data = read_data(file)
    
    cleaned_data = clean(data)

    show_locations(cleaned_data)


if __name__ == '__main__':
    file: str = "(UNCLASS) 20230330 Database Nederlandse luchtaanvallen tijdens Operation Inherent Resolve.csv"
    main(file)
