# ============================================================
# SALES PERFORMANCE DASHBOARD - PYTHON EDA
# Project by: Ayushmaan Pandey | BCA, CSJMU
# Dataset: 1000 orders | Year: 2023
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

# ── Load Data ────────────────────────────────────────────────
df = pd.read_csv('sales_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
print(f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}\n")

# ── KPI Summary ──────────────────────────────────────────────
print("=" * 50)
print("         BUSINESS KPI SUMMARY")
print("=" * 50)
print(f"  Total Orders     : {len(df):,}")
print(f"  Total Revenue    : ₹{df['Revenue'].sum():,.0f}")
print(f"  Total Profit     : ₹{df['Profit'].sum():,.0f}")
print(f"  Avg Profit Margin: {df['Profit_Margin_Pct'].mean():.2f}%")
print(f"  Total Units Sold : {df['Quantity'].sum():,}")
print(f"  Unique Products  : {df['Product'].nunique()}")
print(f"  Regions          : {', '.join(df['Region'].unique())}")
print("=" * 50)

# ── Month order ──────────────────────────────────────────────
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']

# ── Plot Setup ───────────────────────────────────────────────
fig = plt.figure(figsize=(20, 24))
fig.patch.set_facecolor('#0D1117')
colors = {'blue':'#2196F3','green':'#4CAF50','orange':'#FF9800',
          'red':'#F44336','purple':'#9C27B0','teal':'#00BCD4',
          'yellow':'#FFC107','pink':'#E91E63'}
text_color = '#E0E0E0'
grid_color = '#2D2D2D'
card_color = '#161B22'

def style_ax(ax, title):
    ax.set_facecolor(card_color)
    ax.tick_params(colors=text_color, labelsize=9)
    ax.set_title(title, color=text_color, fontsize=12, fontweight='bold', pad=12)
    ax.grid(axis='y', color=grid_color, linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(grid_color)

fig.suptitle('SALES PERFORMANCE DASHBOARD 2023\nAyushmaan Pandey | Data Analyst Project',
             color='white', fontsize=18, fontweight='bold', y=0.98)

# ── KPI Cards ────────────────────────────────────────────────
kpis = [
    ('Total Revenue', f"₹{df['Revenue'].sum()/1e7:.2f} Cr", colors['blue']),
    ('Total Profit',  f"₹{df['Profit'].sum()/1e7:.2f} Cr",  colors['green']),
    ('Avg Margin',    f"{df['Profit_Margin_Pct'].mean():.1f}%", colors['orange']),
    ('Total Orders',  f"{len(df):,}",                         colors['purple']),
]
for i, (label, value, color) in enumerate(kpis):
    ax = fig.add_axes([0.05 + i*0.235, 0.91, 0.21, 0.055])
    ax.set_facecolor(card_color)
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.axis('off')
    ax.add_patch(plt.Rectangle((0,0),1,1, color=card_color, zorder=0))
    ax.add_patch(plt.Rectangle((0,0),0.04,1, color=color, zorder=1))
    ax.text(0.1, 0.62, label, color=text_color, fontsize=9, transform=ax.transAxes)
    ax.text(0.1, 0.18, value, color=color, fontsize=16, fontweight='bold', transform=ax.transAxes)

# ── 1. Monthly Revenue Trend ─────────────────────────────────
ax1 = fig.add_subplot(4, 2, 1)
monthly = df.groupby('Month')['Revenue'].sum().reindex(month_order).dropna()
ax1.plot(range(len(monthly)), monthly.values/1e6, color=colors['blue'],
         linewidth=2.5, marker='o', markersize=5)
ax1.fill_between(range(len(monthly)), monthly.values/1e6, alpha=0.15, color=colors['blue'])
ax1.set_xticks(range(len(monthly)))
ax1.set_xticklabels([m[:3] for m in monthly.index], color=text_color)
ax1.set_ylabel('Revenue (₹ Millions)', color=text_color, fontsize=9)
style_ax(ax1, '📈 Monthly Revenue Trend')

# ── 2. Region Revenue ────────────────────────────────────────
ax2 = fig.add_subplot(4, 2, 2)
region_rev = df.groupby('Region')['Revenue'].sum().sort_values(ascending=True)
bars = ax2.barh(region_rev.index, region_rev.values/1e6,
                color=[colors['blue'],colors['teal'],colors['purple'],colors['orange']])
for bar, val in zip(bars, region_rev.values):
    ax2.text(bar.get_width()+0.1, bar.get_y()+bar.get_height()/2,
             f'₹{val/1e6:.1f}M', va='center', color=text_color, fontsize=9)
ax2.set_xlabel('Revenue (₹ Millions)', color=text_color, fontsize=9)
style_ax(ax2, '🗺️ Revenue by Region')

# ── 3. Category Performance ──────────────────────────────────
ax3 = fig.add_subplot(4, 2, 3)
cat_data = df.groupby('Category')[['Revenue','Profit']].sum().sort_values('Revenue', ascending=False)
x = np.arange(len(cat_data))
w = 0.35
ax3.bar(x-w/2, cat_data['Revenue']/1e6, w, label='Revenue', color=colors['blue'], alpha=0.85)
ax3.bar(x+w/2, cat_data['Profit']/1e6, w, label='Profit', color=colors['green'], alpha=0.85)
ax3.set_xticks(x)
ax3.set_xticklabels([c[:8] for c in cat_data.index], color=text_color, fontsize=8)
ax3.set_ylabel('₹ Millions', color=text_color, fontsize=9)
ax3.legend(facecolor=card_color, labelcolor=text_color, fontsize=8)
style_ax(ax3, '📦 Category Revenue vs Profit')

# ── 4. Top 5 Products ────────────────────────────────────────
ax4 = fig.add_subplot(4, 2, 4)
top5 = df.groupby('Product')['Revenue'].sum().nlargest(5).sort_values()
bar_colors = [colors['purple'],colors['teal'],colors['orange'],colors['blue'],colors['green']]
bars = ax4.barh(top5.index, top5.values/1e6, color=bar_colors)
for bar, val in zip(bars, top5.values):
    ax4.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
             f'₹{val/1e6:.1f}M', va='center', color=text_color, fontsize=9)
ax4.set_xlabel('Revenue (₹ Millions)', color=text_color, fontsize=9)
style_ax(ax4, '🏆 Top 5 Products by Revenue')

# ── 5. Quarterly Comparison ──────────────────────────────────
ax5 = fig.add_subplot(4, 2, 5)
qtr = df.groupby('Quarter')[['Revenue','Profit']].sum()
x = np.arange(len(qtr))
ax5.bar(x-0.2, qtr['Revenue']/1e6, 0.35, color=colors['blue'], label='Revenue', alpha=0.85)
ax5.bar(x+0.2, qtr['Profit']/1e6, 0.35, color=colors['green'], label='Profit', alpha=0.85)
ax5.set_xticks(x)
ax5.set_xticklabels(qtr.index, color=text_color)
ax5.set_ylabel('₹ Millions', color=text_color, fontsize=9)
ax5.legend(facecolor=card_color, labelcolor=text_color, fontsize=8)
style_ax(ax5, '📅 Quarterly Performance')

# ── 6. Salesperson Leaderboard ───────────────────────────────
ax6 = fig.add_subplot(4, 2, 6)
sp = df.groupby('Salesperson')['Revenue'].sum().sort_values(ascending=True)
bar_cols = [colors['green'] if v == sp.max() else colors['blue'] for v in sp.values]
bars = ax6.barh(sp.index, sp.values/1e6, color=bar_cols)
for bar, val in zip(bars, sp.values):
    ax6.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
             f'₹{val/1e6:.1f}M', va='center', color=text_color, fontsize=8)
ax6.set_xlabel('Revenue (₹ Millions)', color=text_color, fontsize=9)
style_ax(ax6, '👤 Salesperson Leaderboard')

# ── 7. Discount Impact ───────────────────────────────────────
ax7 = fig.add_subplot(4, 2, 7)
disc = df.groupby('Discount_Pct')['Profit_Margin_Pct'].mean()
ax7.bar(disc.index.astype(str), disc.values, color=colors['orange'], alpha=0.85, width=0.5)
ax7.set_xlabel('Discount %', color=text_color, fontsize=9)
ax7.set_ylabel('Avg Profit Margin %', color=text_color, fontsize=9)
for i, (d, v) in enumerate(zip(disc.index, disc.values)):
    ax7.text(i, v+0.3, f'{v:.1f}%', ha='center', color=text_color, fontsize=9)
style_ax(ax7, '💸 Discount vs Profit Margin Impact')

# ── 8. Category Profit Margin ────────────────────────────────
ax8 = fig.add_subplot(4, 2, 8)
cat_margin = df.groupby('Category')['Profit_Margin_Pct'].mean().sort_values(ascending=False)
bar_cols2 = [colors['green'] if v >= cat_margin.mean() else colors['red'] for v in cat_margin.values]
bars = ax8.bar(cat_margin.index, cat_margin.values, color=bar_cols2, alpha=0.85)
ax8.axhline(cat_margin.mean(), color=colors['yellow'], linewidth=1.5, linestyle='--', label=f'Avg: {cat_margin.mean():.1f}%')
ax8.set_xticklabels([c[:8] for c in cat_margin.index], color=text_color, fontsize=8)
ax8.set_ylabel('Avg Profit Margin %', color=text_color, fontsize=9)
ax8.legend(facecolor=card_color, labelcolor=text_color, fontsize=8)
for bar, val in zip(bars, cat_margin.values):
    ax8.text(bar.get_x()+bar.get_width()/2, val+0.2, f'{val:.1f}%',
             ha='center', color=text_color, fontsize=8)
style_ax(ax8, '📊 Profit Margin by Category')

plt.tight_layout(rect=[0, 0, 1, 0.90])
plt.savefig('/home/claude/sales_project/Sales_Dashboard_Ayushmaan_Pandey.png',
            dpi=150, bbox_inches='tight', facecolor='#0D1117')
plt.close()
print("\n✅ Dashboard image saved!")

# ── Key Insights ─────────────────────────────────────────────
print("\n" + "="*50)
print("        KEY BUSINESS INSIGHTS")
print("="*50)
top_region = df.groupby('Region')['Revenue'].sum().idxmax()
top_cat = df.groupby('Category')['Revenue'].sum().idxmax()
top_sp = df.groupby('Salesperson')['Revenue'].sum().idxmax()
top_prod = df.groupby('Product')['Revenue'].sum().idxmax()
low_margin = df[df['Profit_Margin_Pct'] < 25]
print(f"  1. Top Region     : {top_region}")
print(f"  2. Top Category   : {top_cat}")
print(f"  3. Top Salesperson: {top_sp}")
print(f"  4. Top Product    : {top_prod}")
print(f"  5. Low Margin Orders (<25%): {len(low_margin)} orders = ₹{low_margin['Revenue'].sum():,.0f} revenue at risk")
print(f"  6. Best Quarter   : {df.groupby('Quarter')['Revenue'].sum().idxmax()}")
print(f"  7. High discount (20%) reduces margin by ~{df[df['Discount_Pct']==0]['Profit_Margin_Pct'].mean() - df[df['Discount_Pct']==20]['Profit_Margin_Pct'].mean():.1f}% vs no discount")
print("="*50)
