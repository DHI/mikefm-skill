from datetime import datetime, timedelta
import numpy as np
import os
import pytest
from fmskill.data import DHIAltimetryRepository
from fmskill.data.altimetry import AltimetryData

try:
    import geopandas as gpd
except ImportError:
    pytest.skip("geopandas not available", allow_module_level=True)


def requires_DHI_ALTIMETRY_API_KEY():
    api_key = os.environ.get("DHI_ALTIMETRY_API_KEY")
    reason = "Environment variable DHI_ALTIMETRY_API_KEY not present"
    return pytest.mark.skipif(api_key is None, reason=reason)


@pytest.fixture
def repo():
    api_key = os.environ["DHI_ALTIMETRY_API_KEY"]
    return DHIAltimetryRepository(api_key=api_key)


@requires_DHI_ALTIMETRY_API_KEY()
def test_get_satellites(repo):
    sats = repo.satellites
    assert "3a" in sats


@requires_DHI_ALTIMETRY_API_KEY()
def test_get_daily_count(repo):
    area = "lon=10.9&lat=55.9&radius=10.0"
    df = repo.get_daily_count(area, start_time="2021")
    assert df.loc["2021-1-4"].values == 4


@requires_DHI_ALTIMETRY_API_KEY()
def test_parse_satellites(repo):
    sats = repo.parse_satellites("3b")
    assert sats[0] == "3b"


@requires_DHI_ALTIMETRY_API_KEY()
def test_time_of_newest_data(repo):
    latest = repo.time_of_newest_data()
    day_before_yesterday = datetime.now() - timedelta(days=2)
    assert latest > day_before_yesterday


@requires_DHI_ALTIMETRY_API_KEY()
def test_plot_observation_stats(repo):
    repo.plot_observation_stats()
    assert True


@requires_DHI_ALTIMETRY_API_KEY()
def test_get_spatial_coverage(repo):
    gdf = repo.get_spatial_coverage(
        area="lon=10.9&lat=55.9&radius=40", start_time="2021-1-1", end_time="2021-1-5"
    )
    assert gdf[["count"]].loc[0].values[0] == 8
    # assert isinstance(gdf, gpd.GeoDataFrame)
    gdf.plot("count")
    assert True


@requires_DHI_ALTIMETRY_API_KEY()
def test_get_altimetry_data(repo):
    ad = repo.get_altimetry_data(
        area="lon=10.9&lat=55.9&radius=50", start_time="1985", end_time="1985-5-1"
    )
    assert isinstance(ad, AltimetryData)
    assert ad.df.index.is_unique
    row = ad.df.iloc[0]
    assert row.lon == 10.795129
    assert np.isnan(row.water_level)
    assert row.wind_speed == 2.2