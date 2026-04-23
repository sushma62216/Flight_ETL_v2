import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def altitude_color(alt, alt_min, alt_max):
    """Map altitude to an RGBA color: green (low) -> red (high)."""
    alt_range = alt_max - alt_min if alt_max != alt_min else 1
    ratio = (alt - alt_min) / alt_range
    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    return [r, g, 80, 180]


def apply_filters(df, selected_countries, selected_sources):
    """Filter dataframe by selected countries and position sources."""
    return df[
        df["origin_country"].isin(selected_countries) &
        df["position_source"].isin(selected_sources)
    ]


class TestAltitudeColor:
    def test_low_altitude_is_green(self):
        color = altitude_color(0, 0, 1000)
        assert color[1] == 255  # green channel max
        assert color[0] == 0    # red channel min

    def test_high_altitude_is_red(self):
        color = altitude_color(1000, 0, 1000)
        assert color[0] == 255  # red channel max
        assert color[1] == 0    # green channel min

    def test_midpoint_is_mixed(self):
        color = altitude_color(500, 0, 1000)
        assert color[0] == 127
        assert color[1] == 127

    def test_equal_min_max_no_division_error(self):
        color = altitude_color(500, 500, 500)
        assert len(color) == 4

    def test_alpha_always_180(self):
        color = altitude_color(200, 0, 1000)
        assert color[3] == 180

    def test_blue_always_80(self):
        color = altitude_color(200, 0, 1000)
        assert color[2] == 80


class TestApplyFilters:
    def setup_method(self):
        self.df = pd.DataFrame({
            "origin_country": ["USA", "Germany", "France", "USA"],
            "position_source": ["ADS-B", "MLAT", "ADS-B", "FLARM"],
            "velocity": [200, 150, 180, 220],
        })

    def test_filter_by_country(self):
        result = apply_filters(self.df, ["USA"], ["ADS-B", "MLAT", "FLARM"])
        assert len(result) == 2
        assert all(result["origin_country"] == "USA")

    def test_filter_by_source(self):
        result = apply_filters(self.df, ["USA", "Germany", "France"], ["ADS-B"])
        assert len(result) == 2
        assert all(result["position_source"] == "ADS-B")

    def test_filter_by_both(self):
        result = apply_filters(self.df, ["USA"], ["ADS-B"])
        assert len(result) == 1

    def test_no_filters_returns_all(self):
        all_countries = self.df["origin_country"].unique().tolist()
        all_sources = self.df["position_source"].unique().tolist()
        result = apply_filters(self.df, all_countries, all_sources)
        assert len(result) == 4

    def test_empty_filter_returns_empty(self):
        result = apply_filters(self.df, [], [])
        assert len(result) == 0
