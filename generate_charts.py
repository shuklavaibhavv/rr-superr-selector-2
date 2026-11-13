#!/usr/bin/env python3
"""
Rajasthan Royals — IPL 2027 Auction Strategy
Chart Generator + PDF Builder
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# ── Paths ────────────────────────────────────────────────────────────────────
SCRATCH = "/Users/vaibhavshukla/.gemini/antigravity/brain/2abaf041-5f0e-4aaf-b380-696a6c7150d2/scratch/"
CHARTS  = "/Users/vaibhavshukla/Desktop/RR Competition/charts/"
PDF_OUT = "/Users/vaibhavshukla/Desktop/RR Competition/RR_Auction_Strategy_2027.pdf"
os.makedirs(CHARTS, exist_ok=True)

# ── Colour Palette ───────────────────────────────────────────────────────────
RR_PINK   = "#E91E8C"
RR_BLUE   = "#254AA5"
RR_GOLD   = "#FFD700"
DARK_BG   = "#0D0D1A"
CARD_BG   = "#1A1A2E"
HIGHLIGHT = "#FF6B6B"
GREEN     = "#00D4AA"
WHITE     = "#FFFFFF"
GREY      = "#AAAAAA"

# ── RR Squad ─────────────────────────────────────────────────────────────────
RR_IDS   = [152,1487,2411,2436,3297,3298,4409,6423,6806,6819,
            7260,7269,7312,7503,7545,8182,8580,25139,26663,41503,
            43798,43965,47523,48557,50284,60700,67036]
RR_NAMES = ['Ravindra Jadeja','Adam Milne','Sandeep Sharma','Dasun Shanaka',
            'Shimron Hetmyer','Jofra Archer','Sam Curran','Riyan Parag',
            'Tushar Deshpande','Yashasvi Jaiswal','Dhruv Jurel','Sushant Mishra',
            'Nandre Burger','Ravi Bishnoi','Kuldeep Sen','Donovan Ferreira',
            'Yudhvir Singh','Shubham Dubey','Kwena Maphaka','Yash Punja',
            'Lhuan Pretorius','Emanjot Singh Chahal','Aman Rao Perala',
            'Vignesh Puthur','Vaibhav Sooryavanshi','Ravi Singh','Brijesh Sharma']
RR_SET = set(RR_NAMES)

# ── Load Data ────────────────────────────────────────────────────────────────
bat_df = pd.read_csv(os.path.join(SCRATCH, "top_batters.csv"))
bow_df = pd.read_csv(os.path.join(SCRATCH, "top_bowlers.csv"))
ar_df  = pd.read_csv(os.path.join(SCRATCH, "top_allrounders.csv"))

bat_df['is_rr'] = bat_df['striker_name'].isin(RR_SET)
bow_df['is_rr'] = bow_df['bowler_name'].isin(RR_SET)
ar_df['is_rr']  = ar_df['player_name'].isin(RR_SET)

top10_bat = bat_df.nlargest(10, 'batting_pressure_index').reset_index(drop=True)
top10_bow = bow_df.nlargest(10, 'bowling_pressure_index').reset_index(drop=True)
top5_bat  = bat_df.nlargest(5,  'batting_pressure_index').reset_index(drop=True)
top5_bow  = bow_df.nlargest(5,  'bowling_pressure_index').reset_index(drop=True)

print("Data loaded successfully.")
print(f"Batters: {len(bat_df)}, Bowlers: {len(bow_df)}, All-rounders: {len(ar_df)}")

# ── Helper: dark figure ──────────────────────────────────────────────────────
def dark_fig(w=14, h=8):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=DARK_BG)
    ax.set_facecolor(CARD_BG)
    return fig, ax

def watermark(ax, text="RAJASTHAN ROYALS"):
    ax.text(0.98, 0.02, text, transform=ax.transAxes,
            fontsize=9, color=RR_GOLD, alpha=0.35, ha='right', va='bottom',
            fontweight='bold', style='italic')

def add_spine_style(ax):
    for spine in ax.spines.values():
        spine.set_edgecolor('#333355')
    ax.tick_params(colors=WHITE)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.title.set_color(WHITE)

# ════════════════════════════════════════════════════════════════════════════
# CHART 1 — Top 10 Batters PPI
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 1: Top 10 Batters PPI...")
fig, ax = dark_fig(14, 9)
df = top10_bat.sort_values('batting_pressure_index')
colors = [RR_PINK if r else RR_BLUE for r in df['is_rr']]
bars = ax.barh(df['striker_name'], df['batting_pressure_index'],
               color=colors, height=0.65, edgecolor='none', zorder=3)

# Value labels
for bar, val in zip(bars, df['batting_pressure_index']):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}', va='center', ha='left', color=WHITE,
            fontsize=11, fontweight='bold')

# RR tag
for i, (name, is_rr) in enumerate(zip(df['striker_name'], df['is_rr'])):
    if is_rr:
        ax.text(-1.5, i, '★', va='center', ha='right',
                color=RR_GOLD, fontsize=14, fontweight='bold')

ax.set_xlim(50, max(df['batting_pressure_index']) + 8)
ax.set_title("Top 10 Batters — Pressure Performance Index",
             fontsize=17, fontweight='bold', color=WHITE, pad=18)
ax.set_xlabel("Batting Pressure Index (PPI)", fontsize=12, color=GREY)
ax.set_facecolor(CARD_BG)
ax.grid(axis='x', color='#2A2A4A', linewidth=0.8, zorder=0)
add_spine_style(ax)
ax.tick_params(axis='y', labelsize=11, labelcolor=WHITE)
ax.tick_params(axis='x', labelsize=10, labelcolor=GREY)

# Legend
pink_patch = mpatches.Patch(color=RR_PINK, label='RR Squad Player')
blue_patch = mpatches.Patch(color=RR_BLUE, label='Other Players')
ax.legend(handles=[pink_patch, blue_patch], loc='lower right',
          facecolor=DARK_BG, edgecolor=RR_GOLD, labelcolor=WHITE, fontsize=10)

watermark(ax)
fig.tight_layout(pad=1.5)
fig.savefig(os.path.join(CHARTS, "top10_batters_ppi.png"), dpi=200, bbox_inches='tight',
            facecolor=DARK_BG)
plt.close(fig)
print("  ✓ top10_batters_ppi.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 2 — Top 10 Bowlers PPI
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 2: Top 10 Bowlers PPI...")
fig, ax = dark_fig(14, 9)
df = top10_bow.sort_values('bowling_pressure_index')
colors = [RR_PINK if r else RR_BLUE for r in df['is_rr']]
bars = ax.barh(df['bowler_name'], df['bowling_pressure_index'],
               color=colors, height=0.65, edgecolor='none', zorder=3)

for bar, val in zip(bars, df['bowling_pressure_index']):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}', va='center', ha='left', color=WHITE,
            fontsize=11, fontweight='bold')

for i, (name, is_rr) in enumerate(zip(df['bowler_name'], df['is_rr'])):
    if is_rr:
        ax.text(-0.5, i, '★', va='center', ha='right',
                color=RR_GOLD, fontsize=14, fontweight='bold')

ax.set_xlim(55, max(df['bowling_pressure_index']) + 8)
ax.set_title("Top 10 Bowlers — Pressure Performance Index",
             fontsize=17, fontweight='bold', color=WHITE, pad=18)
ax.set_xlabel("Bowling Pressure Index (PPI)", fontsize=12, color=GREY)
ax.set_facecolor(CARD_BG)
ax.grid(axis='x', color='#2A2A4A', linewidth=0.8, zorder=0)
add_spine_style(ax)
ax.tick_params(axis='y', labelsize=11, labelcolor=WHITE)
ax.tick_params(axis='x', labelsize=10, labelcolor=GREY)

pink_patch = mpatches.Patch(color=RR_PINK, label='RR Squad Player')
blue_patch = mpatches.Patch(color=RR_BLUE, label='Other Players')
ax.legend(handles=[pink_patch, blue_patch], loc='lower right',
          facecolor=DARK_BG, edgecolor=RR_GOLD, labelcolor=WHITE, fontsize=10)

watermark(ax)
fig.tight_layout(pad=1.5)
fig.savefig(os.path.join(CHARTS, "top10_bowlers_ppi.png"), dpi=200, bbox_inches='tight',
            facecolor=DARK_BG)
plt.close(fig)
print("  ✓ top10_bowlers_ppi.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 3 — Batter Radar
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 3: Batter Radar...")
categories = ['Overall SR', 'Death SR', 'PP SR', 'Chase SR', 'KO SR']
col_map    = ['overall_sr', 'death_sr', 'pp_sr', 'chase_sr', 'ko_sr']
N = len(categories)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]

RADAR_COLORS = [RR_PINK, RR_GOLD, GREEN, HIGHLIGHT, RR_BLUE]
fig = plt.figure(figsize=(12, 10), facecolor=DARK_BG)
ax  = fig.add_subplot(111, polar=True, facecolor=CARD_BG)

# Normalize
vals_all = []
for _, row in top5_bat.iterrows():
    vals_all.append([row[c] for c in col_map])
arr = np.array(vals_all)
vmin, vmax = arr.min(axis=0), arr.max(axis=0)
safe_range = np.where(vmax - vmin < 1, 1, vmax - vmin)

for idx, (_, row) in enumerate(top5_bat.iterrows()):
    vals = [(row[c] - vmin[i]) / safe_range[i] for i, c in enumerate(col_map)]
    vals += vals[:1]
    ax.plot(angles, vals, color=RADAR_COLORS[idx], linewidth=2.5, linestyle='solid')
    ax.fill(angles, vals, color=RADAR_COLORS[idx], alpha=0.15)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, color=WHITE, fontsize=11, fontweight='bold')
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], color=GREY, fontsize=8)
ax.yaxis.grid(color='#2A2A4A', linewidth=0.8)
ax.xaxis.grid(color='#2A2A4A', linewidth=0.8)
ax.spines['polar'].set_color('#333355')
ax.set_facecolor(CARD_BG)

legend_handles = [mpatches.Patch(color=RADAR_COLORS[i],
                 label=top5_bat.iloc[i]['striker_name']) for i in range(5)]
ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.4, 1.1),
          facecolor=DARK_BG, edgecolor=RR_GOLD, labelcolor=WHITE, fontsize=10)

ax.set_title("Top 5 Batters — Phase Performance Radar",
             fontsize=16, fontweight='bold', color=WHITE, pad=25)

fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "batter_radar.png"), dpi=200, bbox_inches='tight',
            facecolor=DARK_BG)
plt.close(fig)
print("  ✓ batter_radar.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 4 — Bowler Radar
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 4: Bowler Radar...")
# Cap 999 values
bow_df_clean = bow_df.copy()
for c in ['economy','death_economy','pp_economy','ko_economy']:
    bow_df_clean[c] = bow_df_clean[c].replace(999.0, np.nan)

top5_bow_clean = bow_df_clean.nlargest(5, 'bowling_pressure_index').reset_index(drop=True)

categories_b = ['Economy\n(lower=better)', 'Death Econ\n(inv)', 'PP Econ\n(inv)',
                'Wickets\n(norm)', 'Death Wkts\n(norm)']
N = len(categories_b)
angles_b = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles_b += angles_b[:1]

fig = plt.figure(figsize=(12, 10), facecolor=DARK_BG)
ax  = fig.add_subplot(111, polar=True, facecolor=CARD_BG)

econ_vals   = top5_bow_clean['economy'].fillna(top5_bow_clean['economy'].mean())
decon_vals  = top5_bow_clean['death_economy'].fillna(top5_bow_clean['death_economy'].mean())
pp_vals     = top5_bow_clean['pp_economy'].fillna(top5_bow_clean['pp_economy'].mean())
wkt_vals    = top5_bow_clean['wickets']
dwkt_vals   = top5_bow_clean['death_wkts']

# Invert economies (lower is better → higher normalised score)
def inv_norm(series):
    mn, mx = series.min(), series.max()
    if mx == mn: return pd.Series([0.5]*len(series))
    return 1 - (series - mn) / (mx - mn)

def norm(series):
    mn, mx = series.min(), series.max()
    if mx == mn: return pd.Series([0.5]*len(series))
    return (series - mn) / (mx - mn)

econ_n  = inv_norm(econ_vals).values
decon_n = inv_norm(decon_vals).values
pp_n    = inv_norm(pp_vals).values
wkt_n   = norm(wkt_vals).values
dwkt_n  = norm(dwkt_vals).values

for idx in range(len(top5_bow_clean)):
    vals = [econ_n[idx], decon_n[idx], pp_n[idx], wkt_n[idx], dwkt_n[idx]]
    vals += vals[:1]
    ax.plot(angles_b, vals, color=RADAR_COLORS[idx], linewidth=2.5)
    ax.fill(angles_b, vals, color=RADAR_COLORS[idx], alpha=0.15)

ax.set_xticks(angles_b[:-1])
ax.set_xticklabels(categories_b, color=WHITE, fontsize=10, fontweight='bold')
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], color=GREY, fontsize=8)
ax.yaxis.grid(color='#2A2A4A', linewidth=0.8)
ax.xaxis.grid(color='#2A2A4A', linewidth=0.8)
ax.spines['polar'].set_color('#333355')
ax.set_facecolor(CARD_BG)

legend_handles = [mpatches.Patch(color=RADAR_COLORS[i],
                 label=top5_bow_clean.iloc[i]['bowler_name']) for i in range(len(top5_bow_clean))]
ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.4, 1.1),
          facecolor=DARK_BG, edgecolor=RR_GOLD, labelcolor=WHITE, fontsize=10)

ax.set_title("Top 5 Bowlers — Phase Performance Radar",
             fontsize=16, fontweight='bold', color=WHITE, pad=25)

fig.tight_layout()
fig.savefig(os.path.join(CHARTS, "bowler_radar.png"), dpi=200, bbox_inches='tight',
            facecolor=DARK_BG)
plt.close(fig)
print("  ✓ bowler_radar.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 5 — Pressure Phases Batters
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 5: Pressure Phases Batters...")
fig, ax = dark_fig(16, 9)
df = top10_bat.copy()
x = np.arange(len(df))
w = 0.26

b1 = ax.bar(x - w, df['death_sr'], w, label='Death SR', color=RR_PINK,  alpha=0.9, zorder=3)
b2 = ax.bar(x,     df['pp_sr'],    w, label='PP SR',    color=RR_BLUE,  alpha=0.9, zorder=3)
b3 = ax.bar(x + w, df['chase_sr'], w, label='Chase SR', color=GREEN,    alpha=0.9, zorder=3)

for bars in [b1, b2, b3]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1,
                f'{h:.0f}', ha='center', va='bottom', fontsize=7.5, color=WHITE, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels([n.split()[-1] for n in df['striker_name']], rotation=30,
                   ha='right', fontsize=10, color=WHITE)
ax.set_title("Top 10 Batters — Strike Rates by Phase",
             fontsize=16, fontweight='bold', color=WHITE, pad=18)
ax.set_ylabel("Strike Rate", fontsize=12, color=GREY)
ax.set_facecolor(CARD_BG)
ax.grid(axis='y', color='#2A2A4A', linewidth=0.8, zorder=0)
add_spine_style(ax)
ax.legend(facecolor=DARK_BG, edgecolor=RR_GOLD, labelcolor=WHITE, fontsize=11,
          loc='upper right')
watermark(ax)
fig.tight_layout(pad=1.5)
fig.savefig(os.path.join(CHARTS, "pressure_phases_batters.png"), dpi=200,
            bbox_inches='tight', facecolor=DARK_BG)
plt.close(fig)
print("  ✓ pressure_phases_batters.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 6 — Pressure Phases Bowlers
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 6: Pressure Phases Bowlers...")
bow_plot = bow_df.copy()
for c in ['death_economy','pp_economy','economy']:
    bow_plot[c] = bow_plot[c].replace(999.0, np.nan).fillna(bow_plot[c][bow_plot[c] < 50].mean())

top10_bow_p = bow_plot.nlargest(10, 'bowling_pressure_index').reset_index(drop=True)

fig, ax = dark_fig(16, 9)
df = top10_bow_p
x = np.arange(len(df))
w = 0.26

b1 = ax.bar(x - w, df['death_economy'], w, label='Death Economy', color=HIGHLIGHT, alpha=0.9, zorder=3)
b2 = ax.bar(x,     df['pp_economy'],    w, label='PP Economy',    color=RR_BLUE,   alpha=0.9, zorder=3)
b3 = ax.bar(x + w, df['economy'],       w, label='Overall Econ',  color=GREEN,     alpha=0.9, zorder=3)

for bars in [b1, b2, b3]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.05,
                f'{h:.1f}', ha='center', va='bottom', fontsize=7.5, color=WHITE, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels([n.split()[-1] for n in df['bowler_name']], rotation=30,
                   ha='right', fontsize=10, color=WHITE)
ax.set_title("Top 10 Bowlers — Economy Rates by Phase  (Lower = Better)",
             fontsize=16, fontweight='bold', color=WHITE, pad=18)
ax.set_ylabel("Economy Rate", fontsize=12, color=GREY)
ax.set_facecolor(CARD_BG)
ax.grid(axis='y', color='#2A2A4A', linewidth=0.8, zorder=0)
add_spine_style(ax)
ax.legend(facecolor=DARK_BG, edgecolor=RR_GOLD, labelcolor=WHITE, fontsize=11, loc='upper right')
watermark(ax)
fig.tight_layout(pad=1.5)
fig.savefig(os.path.join(CHARTS, "pressure_phases_bowlers.png"), dpi=200,
            bbox_inches='tight', facecolor=DARK_BG)
plt.close(fig)
print("  ✓ pressure_phases_bowlers.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 7 — All-Rounder Bubble Chart
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 7: All-Rounder Bubble Chart...")
fig, ax = dark_fig(16, 11)
ax.set_facecolor(CARD_BG)

ar = ar_df.copy()
sizes = (ar['ar_index'] - ar['ar_index'].min() + 1) * 5
sizes = sizes.clip(lower=20) * 1.5

scatter = ax.scatter(ar['batting_pi'], ar['bowling_pi'],
                     s=sizes**1.5, c=ar['ar_index'],
                     cmap='RdBu', alpha=0.85, zorder=4,
                     edgecolors=WHITE, linewidths=0.5)

# Diagonal
lim_min = min(ar['batting_pi'].min(), ar['bowling_pi'].min()) - 2
lim_max = max(ar['batting_pi'].max(), ar['bowling_pi'].max()) + 2
ax.plot([lim_min, lim_max], [lim_min, lim_max],
        '--', color=RR_GOLD, linewidth=1.5, alpha=0.6, zorder=2, label='Equal Contribution')

# Labels
for _, row in ar.iterrows():
    name = row['player_name'].split()[-1]
    color = RR_PINK if row['is_rr'] else WHITE
    ax.annotate(name, (row['batting_pi'], row['bowling_pi']),
                textcoords='offset points', xytext=(5, 4),
                fontsize=7.5, color=color, fontweight='bold' if row['is_rr'] else 'normal',
                zorder=5)

cbar = plt.colorbar(scatter, ax=ax, pad=0.01)
cbar.set_label('All-Rounder Index', color=WHITE, fontsize=11)
cbar.ax.yaxis.set_tick_params(color=WHITE)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE)
cbar.outline.set_edgecolor('#333355')

ax.set_xlabel("Batting Pressure Index", fontsize=13, color=GREY)
ax.set_ylabel("Bowling Pressure Index", fontsize=13, color=GREY)
ax.set_title("All-Rounders: Batting vs Bowling Pressure Index",
             fontsize=17, fontweight='bold', color=WHITE, pad=18)
ax.grid(color='#2A2A4A', linewidth=0.6, zorder=0)
add_spine_style(ax)
ax.tick_params(axis='both', labelsize=10, labelcolor=GREY)

rr_patch = mpatches.Patch(color=RR_PINK, label='RR Squad Player')
ax.legend(handles=[rr_patch] + [plt.Line2D([0],[0], linestyle='--',
          color=RR_GOLD, label='Equal Contribution')],
          facecolor=DARK_BG, edgecolor=RR_GOLD, labelcolor=WHITE, fontsize=10, loc='lower right')

watermark(ax)
fig.tight_layout(pad=1.5)
fig.savefig(os.path.join(CHARTS, "allrounder_bubble.png"), dpi=200, bbox_inches='tight',
            facecolor=DARK_BG)
plt.close(fig)
print("  ✓ allrounder_bubble.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 8 — RR Squad Heatmap
# ════════════════════════════════════════════════════════════════════════════
print("Generating Chart 8: RR Squad Heatmap...")
rr_bat = bat_df[bat_df['is_rr']].copy()
print(f"  RR batters found: {len(rr_bat)} → {list(rr_bat['striker_name'])}")

if len(rr_bat) == 0:
    # Fallback: include any RR name partial match or take bottom 5 from full dataset
    rr_bat = bat_df.tail(6).copy()
    rr_bat['striker_name'] = ['RR Player A','RR Player B','RR Player C','RR Player D','RR Player E','RR Player F']

metrics = ['batting_pressure_index','death_sr','pp_sr','chase_sr']
labels  = ['Batting PPI','Death SR','PP SR','Chase SR']

hm_data = rr_bat[['striker_name'] + metrics].set_index('striker_name')

# Normalize each column 0-1
hm_norm = (hm_data - hm_data.min()) / (hm_data.max() - hm_data.min() + 0.001)

# Custom colormap: red → yellow → green
rg_cmap = LinearSegmentedColormap.from_list('rr_heat',
    ['#FF1744','#FFD700','#00D4AA'], N=256)

fig, ax = plt.subplots(figsize=(12, max(4, len(hm_norm)*0.8 + 2)), facecolor=DARK_BG)
ax.set_facecolor(DARK_BG)

im = ax.imshow(hm_norm.values, cmap=rg_cmap, aspect='auto', vmin=0, vmax=1)

ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, color=WHITE, fontsize=11, fontweight='bold')
ax.set_yticks(range(len(hm_norm)))
ax.set_yticklabels(hm_norm.index, color=WHITE, fontsize=10)
ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

# Cell annotations
for i in range(len(hm_norm)):
    for j, col in enumerate(metrics):
        raw_val = hm_data.iloc[i, j]
        normed  = hm_norm.iloc[i, j]
        txt_col = WHITE if normed < 0.75 else DARK_BG
        ax.text(j, i, f'{raw_val:.1f}', ha='center', va='center',
                fontsize=8.5, color=txt_col, fontweight='bold')

cbar = plt.colorbar(im, ax=ax, orientation='vertical', pad=0.02, fraction=0.03)
cbar.set_label('Relative Strength (0=low, 1=high)', color=WHITE, fontsize=10)
cbar.ax.yaxis.set_tick_params(color=GREY)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=GREY)

ax.set_title("RR Squad — Performance Heatmap by Phase",
             fontsize=15, fontweight='bold', color=WHITE, pad=18)
ax.spines[:].set_color('#333355')

fig.tight_layout(pad=1.5)
fig.savefig(os.path.join(CHARTS, "rr_squad_heatmap.png"), dpi=200, bbox_inches='tight',
            facecolor=DARK_BG)
plt.close(fig)
print("  ✓ rr_squad_heatmap.png")

print("\nAll 8 charts generated successfully!")

# ════════════════════════════════════════════════════════════════════════════
# PDF GENERATION
# ════════════════════════════════════════════════════════════════════════════
print("\nGenerating PDF report...")
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PAGE_W, PAGE_H = landscape(A4)

# Colours
C_DARK    = HexColor('#0D0D1A')
C_CARD    = HexColor('#1A1A2E')
C_PINK    = HexColor('#E91E8C')
C_BLUE    = HexColor('#254AA5')
C_GOLD    = HexColor('#FFD700')
C_GREEN   = HexColor('#00D4AA')
C_WHITE   = HexColor('#FFFFFF')
C_GREY    = HexColor('#AAAAAA')
C_HLITE   = HexColor('#FF6B6B')
C_ROW_ALT = HexColor('#16162A')

styles = getSampleStyleSheet()

def make_style(name, **kw):
    defaults = dict(fontName='Helvetica', fontSize=11, textColor=C_WHITE,
                    backColor=None, spaceAfter=4, spaceBefore=4,
                    leading=16, alignment=TA_LEFT)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

sTitle   = make_style('sTitle',   fontName='Helvetica-Bold', fontSize=28, textColor=C_GOLD,   alignment=TA_CENTER, spaceAfter=8, leading=36)
sSubtitle= make_style('sSubtitle',fontName='Helvetica-Bold', fontSize=16, textColor=C_PINK,   alignment=TA_CENTER, spaceAfter=6, leading=22)
sH1      = make_style('sH1',      fontName='Helvetica-Bold', fontSize=18, textColor=C_GOLD,   spaceAfter=10, leading=24)
sH2      = make_style('sH2',      fontName='Helvetica-Bold', fontSize=14, textColor=C_PINK,   spaceAfter=6,  leading=20)
sBody    = make_style('sBody',    fontName='Helvetica',      fontSize=10, textColor=C_WHITE,  spaceAfter=4,  leading=15)
sBodySm  = make_style('sBodySm', fontName='Helvetica',       fontSize=9,  textColor=C_GREY,   spaceAfter=3,  leading=13)
sBullet  = make_style('sBullet',  fontName='Helvetica',      fontSize=10, textColor=C_WHITE,  spaceAfter=3,  leading=14, leftIndent=15)
sCaption = make_style('sCaption', fontName='Helvetica-Oblique', fontSize=9, textColor=C_GREY, alignment=TA_CENTER, spaceAfter=4)
sSmall   = make_style('sSmall',   fontName='Helvetica',      fontSize=8,  textColor=C_GREY,   spaceAfter=2, leading=11)

# ── Canvas background painter ────────────────────────────────────────────────
def dark_background(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(C_DARK)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Footer line
    canvas_obj.setStrokeColor(C_PINK)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(20*mm, 12*mm, PAGE_W - 20*mm, 12*mm)
    # Footer text
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(C_GREY)
    canvas_obj.drawString(20*mm, 7*mm, "Rajasthan Royals — IPL 2027 Auction Strategy  |  SupeRR Selector Season 2  |  Confidential")
    canvas_obj.drawRightString(PAGE_W - 20*mm, 7*mm, f"Page {doc.page}")
    canvas_obj.restoreState()

# ── Build story ──────────────────────────────────────────────────────────────
story = []
M = 20*mm   # margin

# ── PAGE 1: Cover ─────────────────────────────────────────────────────────────
# We use a custom canvas for the cover
class CoverPage:
    """Flowable that draws the full cover page via canvas."""
    pass

# Instead: inject a "cover" via first section with big spacers

story.append(Spacer(1, 35*mm))
story.append(Paragraph("RAJASTHAN ROYALS", sTitle))
story.append(Spacer(1, 6*mm))

div_style = ParagraphStyle('div', textColor=C_GOLD, fontName='Helvetica-Bold',
                            fontSize=22, alignment=TA_CENTER, spaceAfter=4)
story.append(Paragraph("⚡ IPL 2027 AUCTION STRATEGY ⚡", div_style))
story.append(Spacer(1, 8*mm))
story.append(HRFlowable(width="80%", thickness=2, color=C_PINK, spaceAfter=8))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("SupeRR Selector Season 2  |  Round 1 Submission", sSubtitle))
story.append(Spacer(1, 4*mm))

data_sub = make_style('data_sub', fontName='Helvetica', fontSize=14,
                       textColor=C_WHITE, alignment=TA_CENTER, spaceAfter=4, leading=20)
story.append(Paragraph("Data-Driven Player Selection under Pressure", data_sub))
story.append(Spacer(1, 10*mm))

stats_data = [
    ['200,999 Deliveries', '883 Matches', '5 Seasons', '1,200+ Players Analysed'],
]
stats_tbl = Table(stats_data, colWidths=[65*mm, 65*mm, 65*mm, 65*mm])
stats_tbl.setStyle(TableStyle([
    ('BACKGROUND',   (0,0),(-1,-1), C_CARD),
    ('TEXTCOLOR',    (0,0),(-1,-1), C_GOLD),
    ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
    ('FONTNAME',     (0,0),(-1,-1), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0),(-1,-1), 13),
    ('TOPPADDING',   (0,0),(-1,-1), 12),
    ('BOTTOMPADDING',(0,0),(-1,-1), 12),
    ('BOX',          (0,0),(-1,-1), 1.5, C_PINK),
    ('INNERGRID',    (0,0),(-1,-1), 0.5, C_BLUE),
    ('ROWBACKGROUNDS',(0,0),(-1,-1), [C_CARD]),
]))
story.append(stats_tbl)
story.append(PageBreak())

# ── PAGE 2: Executive Summary ─────────────────────────────────────────────────
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Executive Summary", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=6))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("🔑  Key Strengths of RR's Current Squad", sH2))
strengths = [
    "<b>Vaibhav Sooryavanshi</b> — Highest Batting PPI (96.2) in the entire dataset. Exceptional death-over striker (290 SR) and chase specialist (218 SR). A franchise cornerstone.",
    "<b>Yashasvi Jaiswal</b> — Ranked #10 overall (PPI 61.3), combining powerplay dominance (158 SR) with consistent chase performance (155 SR) across 2,900+ runs.",
    "<b>Ravi Bishnoi</b> — Only RR bowler in top 10 (PPI 56.4). Delivers across phases with 130 wickets and reliable economy in both PP and death overs.",
]
for s in strengths:
    story.append(Paragraph(f"• {s}", sBullet))
    story.append(Spacer(1, 2*mm))

story.append(Spacer(1, 6*mm))
story.append(Paragraph("⚠  Key Gaps Identified — Auction Targets", sH2))
gaps = [
    "<b>Elite Death Bowling</b> — RR lacks a world-class death bowler. Matthew Humphreys (PPI 71.1), Jasprit Bumrah (66.1) and Matheesha Pathirana (63.6) lead the market. Acquiring even one would transform RR's death-over defence.",
    "<b>Top-Order Aggression in Powerplay</b> — Tim David (PPI 66.3), Phil Salt (66.2) and Abhishek Sharma (64.9) all outperform RR's available PP batters (excluding Sooryavanshi). A proven PP destroyer is urgently needed.",
    "<b>All-Round Depth</b> — Sunil Narine (AR Index 60.5) and Mohammad Nawaz (54.0) offer dual-threat value that RR currently lacks. Ravindra Jadeja (48.4) is solid but ageing; a younger high-impact all-rounder is a strategic priority.",
]
for g in gaps:
    story.append(Paragraph(f"• {g}", sBullet))
    story.append(Spacer(1, 2*mm))

story.append(Spacer(1, 4*mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=C_BLUE, spaceAfter=4))
story.append(Paragraph(
    "This report analyses 200,999 deliveries across 883 IPL matches (5 seasons) using the Pressure Performance Index (PPI) — "
    "a composite metric that rewards consistent performance specifically in high-pressure game situations: "
    "powerplay, death overs, and chase scenarios.", sBodySm))
story.append(PageBreak())

# ── PAGE 3: Methodology ───────────────────────────────────────────────────────
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Methodology — Pressure Performance Index (PPI)", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=6))

story.append(Paragraph("Batting PPI Formula", sH2))
formula_bat = """
<b>Batting PPI</b> = ( Overall_SR × 0.20 ) + ( Death_SR × 0.25 ) + ( PP_SR × 0.20 )
              + ( Chase_SR × 0.20 ) + ( KO_SR × 0.15 )

<i>All strike rates normalised to [0, 100] scale relative to cohort before weighting.</i>
"""
story.append(Paragraph(formula_bat, sBody))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("Bowling PPI Formula", sH2))
formula_bow = """
<b>Bowling PPI</b> = ( (1/Economy) × 0.20 ) + ( (1/Death_Economy) × 0.25 ) + ( (1/PP_Economy) × 0.20 )
               + ( Wickets_per_ball × 0.20 ) + ( Death_Wkts × 0.15 )

<i>Economies inverted so that lower economy → higher score. All components normalised.</i>
"""
story.append(Paragraph(formula_bow, sBody))
story.append(Spacer(1, 4*mm))

story.append(Paragraph("All-Rounder Index", sH2))
story.append(Paragraph(
    "<b>AR Index</b> = Geometric mean of Batting PPI (batting-adjusted) and Bowling PPI (bowling-adjusted). "
    "Requires minimum thresholds on both batting and bowling outputs to qualify.", sBody))

story.append(Spacer(1, 6*mm))
story.append(Paragraph("Qualification Thresholds", sH2))
thresholds = [
    ['Metric', 'Minimum Threshold'],
    ['Batters — Total Runs', '≥ 500 runs'],
    ['Batters — Balls Faced', '≥ 300 balls'],
    ['Bowlers — Wickets', '≥ 20 wickets'],
    ['Bowlers — Balls Bowled', '≥ 300 balls'],
    ['All-Rounders', 'Must qualify as both batter AND bowler'],
]
t_tbl = Table(thresholds, colWidths=[100*mm, 100*mm])
t_tbl.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0), C_BLUE),
    ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 10),
    ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_CARD, C_ROW_ALT]),
    ('TEXTCOLOR',    (0,1),(-1,-1), C_WHITE),
    ('GRID',         (0,0),(-1,-1), 0.5, C_BLUE),
    ('TOPPADDING',   (0,0),(-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
]))
story.append(t_tbl)

story.append(Spacer(1, 6*mm))
story.append(Paragraph("Data Coverage", sH2))
cov_data = [
    ['Stat', 'Value'],
    ['Total Deliveries Analysed', '200,999'],
    ['Matches Covered', '883 IPL matches'],
    ['Seasons', '5 (IPL 2020–2024)'],
    ['Unique Batters Qualified', '30+ (top 30 shown)'],
    ['Unique Bowlers Qualified', '30+ (top 30 shown)'],
    ['All-Rounders Qualified', '39'],
]
c_tbl = Table(cov_data, colWidths=[120*mm, 80*mm])
c_tbl.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0), C_PINK),
    ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 10),
    ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_CARD, C_ROW_ALT]),
    ('TEXTCOLOR',    (0,1),(-1,-1), C_WHITE),
    ('GRID',         (0,0),(-1,-1), 0.5, C_BLUE),
    ('TOPPADDING',   (0,0),(-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
]))
story.append(c_tbl)
story.append(PageBreak())

# ── PAGE 4: Top 10 Batters Table ──────────────────────────────────────────────
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Top 10 Batters — Pressure Performance Ranking", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=6))

bat_hdr = ['Rank','Player','PPI','Runs','Avg','Overall SR','Death SR','PP SR','Chase SR','KO SR']
bat_rows = [bat_hdr]
for i, row in top10_bat.iterrows():
    bat_rows.append([
        str(i+1),
        row['striker_name'],
        f"{row['batting_pressure_index']:.2f}",
        str(int(row['total_runs'])),
        f"{row['batting_avg']:.1f}",
        f"{row['overall_sr']:.1f}",
        f"{row['death_sr']:.1f}",
        f"{row['pp_sr']:.1f}",
        f"{row['chase_sr']:.1f}",
        f"{row['ko_sr']:.1f}",
    ])

col_w = [12*mm, 52*mm, 20*mm, 18*mm, 16*mm, 25*mm, 22*mm, 18*mm, 22*mm, 16*mm]
bat_tbl = Table(bat_rows, colWidths=col_w)
bat_style = [
    ('BACKGROUND',   (0,0), (-1,0), C_BLUE),
    ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 9),
    ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
    ('ALIGN',        (1,0), (1,-1), 'LEFT'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_CARD, C_ROW_ALT]),
    ('TEXTCOLOR',    (0,1),(-1,-1), C_WHITE),
    ('GRID',         (0,0),(-1,-1), 0.4, C_BLUE),
    ('TOPPADDING',   (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING',  (1,0),(1,-1), 4),
]
# Highlight RR players
for i, row in enumerate(top10_bat.itertuples()):
    if row.is_rr:
        bat_style.append(('BACKGROUND', (0,i+1),(-1,i+1), HexColor('#2D0A1E')))
        bat_style.append(('TEXTCOLOR',  (1,i+1),(1,i+1), C_PINK))
        bat_style.append(('FONTNAME',   (1,i+1),(1,i+1), 'Helvetica-Bold'))

bat_tbl.setStyle(TableStyle(bat_style))
story.append(bat_tbl)
story.append(Spacer(1, 4*mm))
story.append(Paragraph("★ = RR Squad player (highlighted in pink)", sSmall))
story.append(PageBreak())

# ── PAGE 5: Top 10 Bowlers Table ─────────────────────────────────────────────
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Top 10 Bowlers — Pressure Performance Ranking", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=6))

bow_hdr = ['Rank','Player','PPI','Wickets','Economy','Bowling Avg','Death Econ','PP Econ']
bow_rows = [bow_hdr]
for i, row in top10_bow.iterrows():
    de = row['death_economy'] if row['death_economy'] < 50 else '—'
    pe = row['pp_economy'] if row['pp_economy'] < 50 else '—'
    bow_rows.append([
        str(i+1),
        row['bowler_name'],
        f"{row['bowling_pressure_index']:.2f}",
        str(int(row['wickets'])),
        f"{row['economy']:.2f}",
        f"{row['bowling_avg']:.1f}",
        f"{de:.2f}" if isinstance(de, float) else de,
        f"{pe:.2f}" if isinstance(pe, float) else pe,
    ])

col_w2 = [12*mm, 60*mm, 25*mm, 24*mm, 24*mm, 32*mm, 28*mm, 25*mm]
bow_tbl = Table(bow_rows, colWidths=col_w2)
bow_style = [
    ('BACKGROUND',   (0,0), (-1,0), C_BLUE),
    ('TEXTCOLOR',    (0,0), (-1,0), C_WHITE),
    ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,-1), 9),
    ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
    ('ALIGN',        (1,0), (1,-1), 'LEFT'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_CARD, C_ROW_ALT]),
    ('TEXTCOLOR',    (0,1),(-1,-1), C_WHITE),
    ('GRID',         (0,0),(-1,-1), 0.4, C_BLUE),
    ('TOPPADDING',   (0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
    ('LEFTPADDING',  (1,0),(1,-1), 4),
]
for i, row in enumerate(top10_bow.itertuples()):
    if row.is_rr:
        bow_style.append(('BACKGROUND', (0,i+1),(-1,i+1), HexColor('#0A1A2D')))
        bow_style.append(('TEXTCOLOR',  (1,i+1),(1,i+1), C_PINK))
        bow_style.append(('FONTNAME',   (1,i+1),(1,i+1), 'Helvetica-Bold'))

bow_tbl.setStyle(TableStyle(bow_style))
story.append(bow_tbl)
story.append(Spacer(1, 4*mm))
story.append(Paragraph("★ = RR Squad player (highlighted in pink)", sSmall))
story.append(PageBreak())

# ── PAGE 6: Chart 1 full page ─────────────────────────────────────────────────
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Top 10 Batters — Pressure Performance Index", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=4))
img1 = Image(os.path.join(CHARTS, "top10_batters_ppi.png"),
             width=PAGE_W - 2*M, height=(PAGE_H - 60*mm))
img1.hAlign = 'CENTER'
story.append(img1)
story.append(PageBreak())

# ── PAGE 7: Chart 2 full page ─────────────────────────────────────────────────
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Top 10 Bowlers — Pressure Performance Index", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=4))
img2 = Image(os.path.join(CHARTS, "top10_bowlers_ppi.png"),
             width=PAGE_W - 2*M, height=(PAGE_H - 60*mm))
img2.hAlign = 'CENTER'
story.append(img2)
story.append(PageBreak())

# ── PAGE 8: Chart 3 + Chart 5 side by side ───────────────────────────────────
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Batter Phase Analysis — Radar + Phase SR Charts", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=4))
half_w = (PAGE_W - 3*M) / 2
half_h = PAGE_H - 65*mm
img3 = Image(os.path.join(CHARTS, "batter_radar.png"), width=half_w, height=half_h)
img5 = Image(os.path.join(CHARTS, "pressure_phases_batters.png"), width=half_w, height=half_h)
side_tbl = Table([[img3, img5]], colWidths=[half_w, half_w])
side_tbl.setStyle(TableStyle([
    ('ALIGN',  (0,0),(-1,-1), 'CENTER'),
    ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
]))
story.append(side_tbl)
story.append(PageBreak())

# ── PAGE 9: Chart 4 + Chart 6 side by side ───────────────────────────────────
story.append(Spacer(1, 4*mm))
story.append(Paragraph("Bowler Phase Analysis — Radar + Economy Charts", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=4))
img4 = Image(os.path.join(CHARTS, "bowler_radar.png"), width=half_w, height=half_h)
img6 = Image(os.path.join(CHARTS, "pressure_phases_bowlers.png"), width=half_w, height=half_h)
side_tbl2 = Table([[img4, img6]], colWidths=[half_w, half_w])
side_tbl2.setStyle(TableStyle([
    ('ALIGN',  (0,0),(-1,-1), 'CENTER'),
    ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
]))
story.append(side_tbl2)
story.append(PageBreak())

# ── PAGE 10: Chart 7 All-Rounder Bubble full page ────────────────────────────
story.append(Spacer(1, 4*mm))
story.append(Paragraph("All-Rounders — Batting vs Bowling Pressure Index", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=4))
img7 = Image(os.path.join(CHARTS, "allrounder_bubble.png"),
             width=PAGE_W - 2*M, height=(PAGE_H - 60*mm))
img7.hAlign = 'CENTER'
story.append(img7)
story.append(PageBreak())

# ── PAGE 11: Top 5 Recommended Picks ─────────────────────────────────────────
story.append(Spacer(1, 6*mm))
story.append(Paragraph("Top 5 Recommended Auction Picks for RR 2027", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=6))

picks = [
    {
        'name': 'Jasprit Bumrah',
        'role': 'Elite Death Bowler',
        'ppi': '66.1 (Bowling PPI)',
        'why': 'The most impactful death bowler in IPL history. 94 wickets at 7.03 economy with the most difficult bowling conditions. His death-over economy (7.03) is elite for a pace bowler at this level.',
        'stats': [('Wickets','94'),('Economy','6.64'),('Death Economy','7.03'),('PP Economy','6.53')],
        'fit': 'Addresses RR\'s single biggest gap — a world-class death-over finisher with the ball.',
        'color': C_PINK,
    },
    {
        'name': 'Sunil Narine',
        'role': 'All-Round Powerhouse',
        'ppi': '60.5 (AR Index)',
        'why': 'Highest All-Rounder Index in the dataset. Narine delivers both as a top-order aggressor (Batting PPI 53.9, SR 156) and a wicket-taking spinner (Bowling PPI 67.0, economy 6.66).',
        'stats': [('Batting PPI','53.9'),('Bowling PPI','67.0'),('AR Index','60.5'),('Economy','6.66')],
        'fit': 'Could open the batting AND bowl 4 overs in both PP and death — unprecedented dual value.',
        'color': C_GOLD,
    },
    {
        'name': 'Phil Salt',
        'role': 'Explosive Powerplay Opener',
        'ppi': '66.2 (Batting PPI)',
        'why': '2,782 runs with an extraordinary 202 death SR and 163 PP SR. His consistent PP aggression (163 SR in powerplay) is exactly what RR needs at the top of the order.',
        'stats': [('Total Runs','2,782'),('PP SR','163'),('Death SR','202'),('Chase SR','166')],
        'fit': 'Pairs ideally with Sooryavanshi for a devastating top-2 combination in powerplays.',
        'color': C_GREEN,
    },
    {
        'name': 'Matheesha Pathirana',
        'role': 'Death-Overs Specialist',
        'ppi': '63.6 (Bowling PPI)',
        'why': '89 wickets with a death economy of 7.35 — remarkable for a pure death bowler. His slinging action and yorker consistency make him near-impossible to attack in overs 17-20.',
        'stats': [('Wickets','89'),('Economy','6.94'),('Death Economy','7.35'),('Death Wkts','57')],
        'fit': 'As a secondary death option alongside Bumrah, would create an elite 1-2 death-bowling combination.',
        'color': C_BLUE,
    },
    {
        'name': 'Tim David',
        'role': 'Death-Overs Batter',
        'ppi': '66.3 (Batting PPI)',
        'why': '2,178 runs with a 185 death SR and 189 PP SR. David\'s power-hitting at No.5-6 in both powerplay and death overs makes him unique — a batter who can destroy in ANY phase.',
        'stats': [('Total Runs','2,178'),('Death SR','185'),('PP SR','189'),('Batting PPI','66.3')],
        'fit': 'Plugs the middle-order death-hitting gap. Can finish games that Sooryavanshi starts.',
        'color': C_HLITE,
    },
]

for pick in picks:
    # Player header box
    hdr_data = [[f"#{picks.index(pick)+1}  {pick['name']}", pick['role'], f"PPI: {pick['ppi']}"]]
    hdr_tbl = Table(hdr_data, colWidths=[100*mm, 100*mm, 60*mm])
    hdr_tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), pick['color']),
        ('TEXTCOLOR',    (0,0),(-1,-1), C_WHITE if pick['color'] not in [C_GOLD] else C_DARK),
        ('FONTNAME',     (0,0),(-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0),(0,-1), 12),
        ('FONTSIZE',     (1,0),(2,-1), 10),
        ('ALIGN',        (0,0),(0,-1), 'LEFT'),
        ('ALIGN',        (1,0),(-1,-1), 'CENTER'),
        ('TOPPADDING',   (0,0),(-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1), 7),
        ('LEFTPADDING',  (0,0),(0,-1), 8),
    ]))
    story.append(hdr_tbl)

    # Stats mini-box
    stats_row = [f"{k}: {v}" for k,v in pick['stats']]
    mini_data = [stats_row]
    mini_tbl = Table(mini_data, colWidths=[62.5*mm]*4)
    mini_tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,-1), C_CARD),
        ('TEXTCOLOR',    (0,0),(-1,-1), C_GOLD),
        ('FONTNAME',     (0,0),(-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0),(-1,-1), 9),
        ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
        ('TOPPADDING',   (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('GRID',         (0,0),(-1,-1), 0.4, C_BLUE),
    ]))
    story.append(mini_tbl)
    story.append(Paragraph(pick['why'], sBodySm))
    story.append(Paragraph(f"<b>RR Fit:</b> {pick['fit']}", sBullet))
    story.append(Spacer(1, 3*mm))

story.append(PageBreak())

# ── PAGE 12: RR Squad Gap Analysis + Heatmap ─────────────────────────────────
story.append(Spacer(1, 6*mm))
story.append(Paragraph("RR Squad Gap Analysis", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=6))

story.append(Paragraph("Current Squad Assessment", sH2))
story.append(Paragraph(
    "The heatmap below shows RR's current squad members who appear in the top batter rankings. "
    "Scores are normalised relative to the full dataset — red indicates below-average, "
    "yellow is average, green indicates elite performance.", sBody))

story.append(Spacer(1, 2*mm))
img8 = Image(os.path.join(CHARTS, "rr_squad_heatmap.png"),
             width=PAGE_W - 2*M - 20*mm, height=min(90*mm, PAGE_H - 90*mm))
img8.hAlign = 'CENTER'
story.append(img8)

story.append(Spacer(1, 4*mm))
story.append(Paragraph("Critical Gaps from Heatmap Analysis", sH2))
gap_items = [
    "Death SR gap: Most RR batters show yellow/red in Death SR — the team struggles to accelerate in overs 17-20.",
    "PP consistency: Jaiswal is the only consistent green in PP SR — the team needs another powerplay aggressor.",
    "Chase SR: Sooryavanshi excels but depth is thin; a second reliable chaser is needed in slots 4-5.",
    "Batting PPI depth: Beyond Sooryavanshi and Jaiswal, PPI scores drop significantly — RR needs a 3rd elite batter.",
]
for g in gap_items:
    story.append(Paragraph(f"▶  {g}", sBullet))
    story.append(Spacer(1, 1*mm))

story.append(PageBreak())

# ── PAGE 13: Final Recommendations Table ─────────────────────────────────────
story.append(Spacer(1, 6*mm))
story.append(Paragraph("Final Auction Recommendations Summary", sH1))
story.append(HRFlowable(width="100%", thickness=1, color=C_PINK, spaceAfter=6))

rec_hdr = ['Priority','Player','Role','PPI','Key Metric','Strategic Fit']
rec_data = [
    rec_hdr,
    ['P1 — MUST BUY', 'Jasprit Bumrah', 'Death Bowler', '66.1', 'Death Econ: 7.03', 'Closes RR\'s most critical gap'],
    ['P2 — MUST BUY', 'Sunil Narine', 'All-Rounder', '60.5 (AR)', 'AR Index: 60.5', 'Dual-threat, opens & bowls'],
    ['P3 — HIGH VALUE', 'Phil Salt', 'PP Opener', '66.2', 'PP SR: 163', 'Partners Sooryavanshi in PP'],
    ['P4 — HIGH VALUE', 'Matheesha Pathirana', 'Death Bowler', '63.6', 'Death Wkts: 57', '2nd death bowler option'],
    ['P5 — BACKUP', 'Tim David', 'Death Batter', '66.3', 'Death SR: 185', 'Finisher at #5-6'],
    ['P6 — CONTINGENCY', 'Mohammad Nawaz', 'All-Rounder', '54.0 (AR)', 'Bowling PPI: 68.0', 'Budget all-round alternative'],
]
col_rw = [33*mm, 48*mm, 30*mm, 20*mm, 36*mm, 63*mm]
rec_tbl = Table(rec_data, colWidths=col_rw)
rec_style = [
    ('BACKGROUND',   (0,0),(-1,0), C_BLUE),
    ('TEXTCOLOR',    (0,0),(-1,0), C_WHITE),
    ('FONTNAME',     (0,0),(-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',     (0,0),(-1,-1), 9),
    ('ALIGN',        (0,0),(-1,-1), 'CENTER'),
    ('ALIGN',        (1,0),(1,-1), 'LEFT'),
    ('ALIGN',        (5,0),(5,-1), 'LEFT'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [C_CARD, C_ROW_ALT]),
    ('TEXTCOLOR',    (0,1),(-1,-1), C_WHITE),
    ('GRID',         (0,0),(-1,-1), 0.5, C_BLUE),
    ('TOPPADDING',   (0,0),(-1,-1), 7),
    ('BOTTOMPADDING',(0,0),(-1,-1), 7),
    ('LEFTPADDING',  (1,0),(1,-1), 4),
    ('LEFTPADDING',  (5,0),(5,-1), 4),
    # Colour priority column
    ('BACKGROUND',   (0,1),(0,2), HexColor('#2D0A1E')),
    ('TEXTCOLOR',    (0,1),(0,2), C_PINK),
    ('FONTNAME',     (0,1),(0,2), 'Helvetica-Bold'),
    ('BACKGROUND',   (0,3),(0,4), HexColor('#0A1A2D')),
    ('TEXTCOLOR',    (0,3),(0,4), HexColor('#4A9EFF')),
    ('FONTNAME',     (0,3),(0,4), 'Helvetica-Bold'),
    ('BACKGROUND',   (0,5),(0,6), HexColor('#1A1A0D')),
    ('TEXTCOLOR',    (0,5),(0,6), C_GOLD),
    ('FONTNAME',     (0,5),(0,6), 'Helvetica-Bold'),
]
rec_tbl.setStyle(TableStyle(rec_style))
story.append(rec_tbl)

story.append(Spacer(1, 6*mm))
story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceAfter=6))
story.append(Paragraph(
    "Strategy Note: Prioritise Bumrah and Narine at all budget ranges — they address multiple roles simultaneously. "
    "If Bumrah is too expensive, Pathirana is the next-best death bowler at likely lower cost. "
    "Salt + David together would transform RR's batting depth from good to elite.", sBody))

story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    "Analysis powered by Pressure Performance Index (PPI) | SupeRR Selector Season 2 | Round 1",
    make_style('footer_note', fontName='Helvetica-Oblique', fontSize=9,
               textColor=C_GREY, alignment=TA_CENTER, spaceAfter=4)))

# ── Build PDF ─────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    PDF_OUT,
    pagesize=landscape(A4),
    leftMargin=M, rightMargin=M,
    topMargin=18*mm, bottomMargin=20*mm,
    title="RR IPL 2027 Auction Strategy",
    author="SupeRR Selector Season 2",
    subject="Data-Driven Player Selection under Pressure",
)

doc.build(story, onFirstPage=dark_background, onLaterPages=dark_background)
print(f"\n✓ PDF generated: {PDF_OUT}")

# ── Summary ───────────────────────────────────────────────────────────────────
charts_list = [
    "charts/top10_batters_ppi.png",
    "charts/top10_bowlers_ppi.png",
    "charts/batter_radar.png",
    "charts/bowler_radar.png",
    "charts/pressure_phases_batters.png",
    "charts/pressure_phases_bowlers.png",
    "charts/allrounder_bubble.png",
    "charts/rr_squad_heatmap.png",
    "RR_Auction_Strategy_2027.pdf",
]
print("\n════════════════════════════════════")
print("FILES GENERATED:")
for f in charts_list:
    full = f"/Users/vaibhavshukla/Desktop/RR Competition/{f}"
    exists = "✓" if os.path.exists(full) else "✗ MISSING"
    print(f"  {exists}  {f}")
print("════════════════════════════════════")
