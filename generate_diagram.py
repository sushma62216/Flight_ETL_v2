import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#0f1117')

# ── helpers ──────────────────────────────────────────────────────────────────

def box(ax, x, y, w, h, label, sublabel=None,
        facecolor='#1e2130', edgecolor='#4a90d9', radius=0.3, fontsize=11):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle=f"round,pad=0.05,rounding_size={radius}",
                          linewidth=2, edgecolor=edgecolor, facecolor=facecolor,
                          zorder=3)
    ax.add_patch(rect)
    cy = y + h / 2 + (0.15 if sublabel else 0)
    ax.text(x + w / 2, cy, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color='white', zorder=4)
    if sublabel:
        ax.text(x + w / 2, y + h / 2 - 0.25, sublabel, ha='center', va='center',
                fontsize=8.5, color='#aab0c6', zorder=4)

def arrow(ax, x1, y1, x2, y2, label=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#4a90d9',
                                lw=2.0, connectionstyle='arc3,rad=0.0'),
                zorder=2)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.08, my, label, fontsize=8, color='#7a8099', zorder=5)

def section_bg(ax, x, y, w, h, color, label):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.1,rounding_size=0.4",
                          linewidth=1.2, edgecolor=color,
                          facecolor=color + '22', zorder=1, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x + 0.18, y + h - 0.28, label, fontsize=8.5, color=color,
            fontweight='bold', zorder=2)

# ── section backgrounds ───────────────────────────────────────────────────────

section_bg(ax, 0.3, 6.8, 2.6, 2.5, '#f5a623', 'DATA SOURCE')
section_bg(ax, 3.3, 6.0, 9.4, 3.3, '#7ed321', 'AIRFLOW DAG  (daily schedule)')
section_bg(ax, 3.3, 2.2, 5.6, 3.2, '#9b59b6', 'POSTGRESQL DATABASE')
section_bg(ax, 9.4, 2.2, 3.3, 3.2, '#2980b9', 'DASHBOARD')

# ── nodes ────────────────────────────────────────────────────────────────────

# OpenSky API
box(ax, 0.5, 7.2, 2.2, 1.6, 'OpenSky', 'Network API',
    facecolor='#2a1f0a', edgecolor='#f5a623')

# Airflow tasks
box(ax, 3.5, 7.0, 2.4, 1.4, 'extract.py', 'Fetch live states',
    facecolor='#0d1f0d', edgecolor='#7ed321')
box(ax, 6.3, 7.0, 2.4, 1.4, 'transform.py', 'Clean & reshape',
    facecolor='#0d1f0d', edgecolor='#7ed321')
box(ax, 9.1, 7.0, 2.4, 1.4, 'load.py', 'Write to DB',
    facecolor='#0d1f0d', edgecolor='#7ed321')

# DB tables
box(ax, 3.5, 2.8, 2.2, 1.0, 'aircraft',
    facecolor='#1a0d2e', edgecolor='#9b59b6', fontsize=10)
box(ax, 5.9, 2.8, 2.0, 1.0, 'flight_status',
    facecolor='#1a0d2e', edgecolor='#9b59b6', fontsize=10)
box(ax, 8.1, 2.8, 2.2, 1.0, 'flight_position',
    facecolor='#1a0d2e', edgecolor='#9b59b6', fontsize=9.5)

# retrieve_data
box(ax, 9.6, 5.0, 2.8, 1.0, 'retrieve_data.py', 'JOIN query',
    facecolor='#0a1a2e', edgecolor='#2980b9', fontsize=10)

# Streamlit
box(ax, 9.6, 2.8, 2.8, 1.2, 'app.py', 'Streamlit Dashboard',
    facecolor='#0a1a2e', edgecolor='#2980b9', fontsize=10)

# db_config / db_schema
box(ax, 3.5, 4.5, 2.0, 0.8, 'db_config.py',
    facecolor='#111827', edgecolor='#4a5568', fontsize=9)
box(ax, 5.7, 4.5, 2.2, 0.8, 'db_schema.py',
    facecolor='#111827', edgecolor='#4a5568', fontsize=9)

# Docker
box(ax, 0.5, 1.0, 3.5, 1.0, 'Docker / docker-compose',
    facecolor='#091e2e', edgecolor='#0db7ed', fontsize=10)

# ── arrows ───────────────────────────────────────────────────────────────────

# API → extract
arrow(ax, 2.7, 8.0, 3.5, 7.7, 'HTTP GET')

# extract → transform (XCom)
arrow(ax, 5.9, 7.7, 6.3, 7.7, 'XCom')

# transform → load (XCom)
arrow(ax, 8.7, 7.7, 9.1, 7.7, 'XCom')

# load → aircraft
arrow(ax, 10.3, 7.0, 4.6, 3.8)

# load → flight_status
arrow(ax, 10.3, 7.0, 6.9, 3.8)

# load → flight_position
arrow(ax, 11.3, 7.0, 9.2, 3.8)

# db_config → load
ax.annotate('', xy=(9.1, 7.5), xytext=(5.5, 5.3),
            arrowprops=dict(arrowstyle='->', color='#4a5568', lw=1.4,
                            connectionstyle='arc3,rad=-0.3'), zorder=2)

# db_schema → load
ax.annotate('', xy=(9.2, 7.2), xytext=(6.8, 5.3),
            arrowprops=dict(arrowstyle='->', color='#4a5568', lw=1.4,
                            connectionstyle='arc3,rad=-0.2'), zorder=2)

# DB tables → retrieve_data
arrow(ax, 8.5, 3.3, 9.6, 5.3)

# retrieve_data → streamlit
arrow(ax, 11.0, 5.0, 11.0, 4.0, 'DataFrame')

# ── XCom label ───────────────────────────────────────────────────────────────
ax.text(7.0, 8.6, 'Airflow XCom passes data between tasks',
        ha='center', fontsize=8, color='#7a8099', style='italic')

# ── title ────────────────────────────────────────────────────────────────────
ax.text(8.0, 9.6, 'Flight ETL Pipeline — Architecture',
        ha='center', va='center', fontsize=16, fontweight='bold',
        color='white')

plt.tight_layout()
plt.savefig('architecture.png', dpi=150, bbox_inches='tight',
            facecolor=fig.get_facecolor())
print("Saved architecture.png")
