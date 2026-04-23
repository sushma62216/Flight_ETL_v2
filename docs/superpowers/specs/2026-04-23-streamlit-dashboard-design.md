# Streamlit Dashboard Enhancement — Design Spec

**Date:** 2026-04-23  
**Status:** Approved  

---

## Goal

Enhance the existing Streamlit flight dashboard to be visually striking and recruiter-appealing, using data already available in PostgreSQL. Changes are limited to `app.py` and `requirements.txt` — no pipeline changes.

---

## Layout

```
┌─ Sidebar ──────────────────────────────────┐
│  Filter by Origin Country (multiselect)    │
│  Filter by Position Source (multiselect)   │
│  Auto-refresh toggle + interval            │
└────────────────────────────────────────────┘

┌─ Main ─────────────────────────────────────┐
│  Title                                     │
│  [KPI] [KPI] [KPI] [KPI]  ← 4 columns     │
│  World Map (full width)                    │
│  [Bar: Top Countries] [Scatter: Alt/Speed] │
│  Data Table (filtered)                     │
└────────────────────────────────────────────┘
```

---

## Components

### KPI Row
Four `st.metric` cards in a 4-column row:
- Total Flights Tracked
- Average Speed (m/s)
- Average Geo Altitude (m)
- Countries Represented

### World Map
- `st.pydeck_chart` with `pydeck.Layer("ScatterplotLayer")`
- One dot per flight at `longitude` / `latitude`
- Dot color scales green (low altitude) → red (high altitude) based on `geo_altitude`
- Hover tooltip: flight number, origin country, speed, altitude
- Dark basemap: `mapbox://styles/mapbox/dark-v9`

### Bar Chart — Top 15 Origin Countries
- `st.bar_chart` of top 15 countries by flight count
- Replaces current full-list bar chart

### Scatter Plot — Velocity vs Geo Altitude
- X axis: `velocity`, Y axis: `geo_altitude`
- Colored by `position_source` (ADS-B, MLAT, ASTERIX, FLARM)
- Rendered with `st.scatter_chart`

### Sidebar Filters
- Multiselect: Origin Country
- Multiselect: Position Source
- All components (map, KPIs, charts, table) react to filters via a shared `filtered_df`

### Auto-Refresh
- Sidebar toggle: on/off
- When on: `time.sleep(60)` then `st.rerun()`
- Pulls fresh data from DB on each rerun

---

## Files Changed

| File | Change |
|---|---|
| `app.py` | Full UI rewrite — layout, map, KPIs, charts, filters, auto-refresh |
| `requirements.txt` | Add `pydeck` |

## Files Unchanged
`extract.py`, `transform.py`, `load.py`, `db_config.py`, `db_schema.py`, `retrieve_data.py`

---

## Data Flow

```
PostgreSQL → retrieve_data.load_data_from_db() → df
                                                   ↓
                                          sidebar filters applied
                                                   ↓
                                             filtered_df
                                            ↙    ↓    ↓    ↘
                                         KPIs  Map  Charts  Table
```
