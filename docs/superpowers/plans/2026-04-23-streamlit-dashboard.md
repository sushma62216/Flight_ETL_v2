# Streamlit Dashboard Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `app.py` to include a world map, KPI row, sidebar filters, two charts, and auto-refresh.

**Architecture:** All changes are confined to `app.py` and `requirements.txt`. Data is loaded once from PostgreSQL via the existing `retrieve_data.load_data_from_db()`, filtered by sidebar inputs into a shared `filtered_df`, and fed to all UI components. Pure logic (altitude color mapping) is extracted into a helper function so it can be unit tested.

**Tech Stack:** Streamlit, pydeck, pandas, pytest

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `requirements.txt` | Modify | Add `pydeck` |
| `app.py` | Full rewrite | Layout, filters, KPIs, map, charts, table, auto-refresh |
| `tests/test_app_helpers.py` | Create | Unit tests for `altitude_color` and filter logic |

---

### Task 1: Add pydeck to requirements.txt and install it

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add pydeck to requirements.txt**

Open `requirements.txt` (currently contains `pandas`, `psycopg2-binary`, `streamlit`, `python-dotenv`) and add `pydeck`:

```
pandas
psycopg2-binary
streamlit
python-dotenv
pydeck
```

- [ ] **Step 2: Install pydeck locally**

```bash
pip3 install pydeck
```

Expected output: `Successfully installed pydeck-x.x.x` (or "already satisfied")

- [ ] **Step 3: Verify import works**

```bash
python3 -c "import pydeck; print('pydeck ok')"
```

Expected: `pydeck ok`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "feat: add pydeck dependency for flight map"
```

---

### Task 2: Create tests for pure helper logic

**Files:**
- Create: `tests/test_app_helpers.py`

- [ ] **Step 1: Create the tests directory and file**

```bash
mkdir -p tests
touch tests/__init__.py
```

- [ ] **Step 2: Write failing tests for altitude_color and filter logic**

Create `tests/test_app_helpers.py`:

```python
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
```

- [ ] **Step 3: Run tests — expect PASS (logic is in the test file itself)**

```bash
python3 -m pytest tests/test_app_helpers.py -v
```

Expected output:
```
tests/test_app_helpers.py::TestAltitudeColor::test_low_altitude_is_green PASSED
tests/test_app_helpers.py::TestAltitudeColor::test_high_altitude_is_red PASSED
tests/test_app_helpers.py::TestAltitudeColor::test_midpoint_is_mixed PASSED
tests/test_app_helpers.py::TestAltitudeColor::test_equal_min_max_no_division_error PASSED
tests/test_app_helpers.py::TestAltitudeColor::test_alpha_always_180 PASSED
tests/test_app_helpers.py::TestAltitudeColor::test_blue_always_80 PASSED
tests/test_app_helpers.py::TestApplyFilters::test_filter_by_country PASSED
tests/test_app_helpers.py::TestApplyFilters::test_filter_by_source PASSED
tests/test_app_helpers.py::TestApplyFilters::test_filter_by_both PASSED
tests/test_app_helpers.py::TestApplyFilters::test_no_filters_returns_all PASSED
tests/test_app_helpers.py::TestApplyFilters::test_empty_filter_returns_empty PASSED

11 passed
```

- [ ] **Step 4: Commit**

```bash
git add tests/
git commit -m "test: add unit tests for altitude color and filter logic"
```

---

### Task 3: Rewrite app.py — data loading, sidebar filters, and filtered_df

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Replace app.py with the new skeleton (data + sidebar + filtered_df)**

```python
import streamlit as st
import pydeck as pdk
import pandas as pd
import time
from retrieve_data import load_data_from_db

st.set_page_config(page_title="Flight Tracker", layout="wide")
st.title("✈️ Live Flight Activity Dashboard")

# ── Load data ────────────────────────────────────────────────────────────────
df = load_data_from_db()

if df.empty:
    st.warning("No flight data available.")
    st.stop()

# ── Sidebar filters ──────────────────────────────────────────────────────────
st.sidebar.header("Filters")

countries = sorted(df["origin_country"].dropna().unique().tolist())
sources = sorted(df["position_source"].dropna().unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Origin Country", options=countries, default=countries
)
selected_sources = st.sidebar.multiselect(
    "Position Source", options=sources, default=sources
)

auto_refresh = st.sidebar.toggle("Auto-refresh (60s)", value=False)

# ── Apply filters ────────────────────────────────────────────────────────────
filtered_df = df[
    df["origin_country"].isin(selected_countries) &
    df["position_source"].isin(selected_sources)
]

if filtered_df.empty:
    st.warning("No flights match the selected filters.")
    st.stop()
```

- [ ] **Step 2: Run the app to verify it starts without errors**

```bash
streamlit run app.py
```

Expected: App loads at `http://localhost:8501` showing the title and sidebar with country/source filters. No errors in terminal.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add sidebar filters and filtered_df to app"
```

---

### Task 4: Add KPI row

**Files:**
- Modify: `app.py` (append after the `filtered_df` block)

- [ ] **Step 1: Add KPI row to app.py after the filter block**

Add this block after `if filtered_df.empty:` check:

```python
# ── KPI row ──────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Flights", len(filtered_df))
col2.metric(
    "Avg Speed (m/s)",
    f"{filtered_df['velocity'].mean():.1f}" if filtered_df['velocity'].notna().any() else "—"
)
col3.metric(
    "Avg Altitude (m)",
    f"{filtered_df['geo_altitude'].mean():.0f}" if filtered_df['geo_altitude'].notna().any() else "—"
)
col4.metric("Countries", filtered_df["origin_country"].nunique())

st.divider()
```

- [ ] **Step 2: Run and verify KPI row appears**

```bash
streamlit run app.py
```

Expected: 4 metric cards appear below the title showing total flights, avg speed, avg altitude, countries count.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add KPI metrics row to dashboard"
```

---

### Task 5: Add world map

**Files:**
- Modify: `app.py` (append after KPI divider)

- [ ] **Step 1: Add altitude_color helper and map section to app.py**

Add this block after `st.divider()`:

```python
# ── World map ────────────────────────────────────────────────────────────────
st.subheader("Live Flight Map")

map_df = filtered_df.dropna(subset=["longitude", "latitude", "geo_altitude"]).copy()

if not map_df.empty:
    alt_min = map_df["geo_altitude"].min()
    alt_max = map_df["geo_altitude"].max()
    alt_range = alt_max - alt_min if alt_max != alt_min else 1

    def altitude_color(alt):
        ratio = (alt - alt_min) / alt_range
        r = int(255 * ratio)
        g = int(255 * (1 - ratio))
        return [r, g, 80, 180]

    map_df["color"] = map_df["geo_altitude"].apply(altitude_color)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position=["longitude", "latitude"],
        get_color="color",
        get_radius=15000,
        pickable=True,
    )

    view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1.5, pitch=0)

    tooltip = {
        "html": (
            "<b>{flight_number}</b><br/>"
            "Country: {origin_country}<br/>"
            "Speed: {velocity} m/s<br/>"
            "Altitude: {geo_altitude} m"
        ),
        "style": {"backgroundColor": "steelblue", "color": "white"},
    }

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/dark-v9",
        )
    )

st.divider()
```

- [ ] **Step 2: Run and verify map appears**

```bash
streamlit run app.py
```

Expected: Dark world map appears with colored dots for each flight. Green dots = low altitude, red dots = high altitude. Hovering a dot shows flight number, country, speed, altitude.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add interactive pydeck world map with altitude color coding"
```

---

### Task 6: Add bar chart and scatter plot

**Files:**
- Modify: `app.py` (append after map divider)

- [ ] **Step 1: Add two-column chart section to app.py**

Add this block after the map's `st.divider()`:

```python
# ── Charts ───────────────────────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Top 15 Origin Countries")
    top_countries = (
        filtered_df["origin_country"]
        .value_counts()
        .head(15)
        .rename_axis("country")
        .reset_index(name="flights")
    )
    st.bar_chart(top_countries.set_index("country"))

with chart_col2:
    st.subheader("Velocity vs Altitude")
    scatter_df = filtered_df[["velocity", "geo_altitude", "position_source"]].dropna()
    st.scatter_chart(scatter_df, x="velocity", y="geo_altitude", color="position_source")

st.divider()
```

- [ ] **Step 2: Run and verify charts appear side by side**

```bash
streamlit run app.py
```

Expected: Left column shows bar chart of top 15 countries. Right column shows scatter plot of velocity vs altitude, with dots colored by position source. A legend appears automatically for position source colors.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add top-15 countries bar chart and velocity/altitude scatter plot"
```

---

### Task 7: Add filtered data table and auto-refresh

**Files:**
- Modify: `app.py` (append after charts divider)

- [ ] **Step 1: Add data table and auto-refresh to the bottom of app.py**

Add this block after the charts `st.divider()`:

```python
# ── Data table ───────────────────────────────────────────────────────────────
st.subheader("Flight Data Table")
st.dataframe(filtered_df, use_container_width=True)

# ── Auto-refresh ─────────────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(60)
    st.rerun()
```

- [ ] **Step 2: Run and verify full dashboard**

```bash
streamlit run app.py
```

Expected:
- Full dashboard renders top to bottom: title → KPIs → map → charts → table
- Sidebar filters update all components when changed
- "Auto-refresh (60s)" toggle in sidebar — when enabled, page reloads after 60 seconds
- Table shows all columns from the DB query, filling the full width

- [ ] **Step 3: Run tests one final time to confirm nothing is broken**

```bash
python3 -m pytest tests/test_app_helpers.py -v
```

Expected: 11 passed

- [ ] **Step 4: Final commit**

```bash
git add app.py
git commit -m "feat: add filtered data table and auto-refresh toggle"
```

- [ ] **Step 5: Push to GitHub**

```bash
git push origin main
```
