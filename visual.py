import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import random
from datetime import datetime, timedelta


def load_initial_data():
    district_data = [
        {'lgd_code': 470, 'year': 1998, 'district': 'Bastar', 'area': 14970, 'parent_lgd': None},
        {'lgd_code': 472, 'year': 1998, 'district': 'Bilaspur', 'area': 8270, 'parent_lgd': None},
        {'lgd_code': 474, 'year': 1998, 'district': 'Durg', 'area': 8537, 'parent_lgd': None},
        {'lgd_code': 478, 'year': 1998, 'district': 'Raigarh', 'area': 7086, 'parent_lgd': None},
        {'lgd_code': 480, 'year': 1998, 'district': 'Raipur', 'area': 13083, 'parent_lgd': None},
        {'lgd_code': 481, 'year': 1998, 'district': 'Rajnandgaon', 'area': 8070, 'parent_lgd': None},
        {'lgd_code': 482, 'year': 1998, 'district': 'Surguja', 'area': 15731, 'parent_lgd': None},
        {'lgd_code': 473, 'year': 1998, 'district': 'Dantewada', 'area': 3410.50, 'parent_lgd': 470},
        {'lgd_code': 476, 'year': 1998, 'district': 'Kanker', 'area': 7161, 'parent_lgd': 470},
        {'lgd_code': 475, 'year': 1998, 'district': 'Janjgir-Champa', 'area': 4466.74, 'parent_lgd': 472},
        {'lgd_code': 477, 'year': 1998, 'district': 'Korba', 'area': 7145.44, 'parent_lgd': 472},
        {'lgd_code': 479, 'year': 1998, 'district': 'Jashpur', 'area': 5838, 'parent_lgd': 478},
        {'lgd_code': 471, 'year': 1998, 'district': 'Dhamtari', 'area': 4084, 'parent_lgd': 480},
        {'lgd_code': 469, 'year': 1998, 'district': 'Mahasamund', 'area': 4790, 'parent_lgd': 480},
        {'lgd_code': 468, 'year': 1998, 'district': 'Koriya', 'area': 5977, 'parent_lgd': 482},
        {'lgd_code': 467, 'year': 1998, 'district': 'Kabirdham', 'area': 4447.05, 'parent_lgd': 472},
        {'lgd_code': 601, 'year': 2007, 'district': 'Bijapur', 'area': 6562.48, 'parent_lgd': 473},
        {'lgd_code': 602, 'year': 2007, 'district': 'Narayanpur', 'area': 7010, 'parent_lgd': 470},
        {'lgd_code': 613, 'year': 2012, 'district': 'Balod', 'area': 3527, 'parent_lgd': 474},
        {'lgd_code': 614, 'year': 2012, 'district': 'Bemetara', 'area': 2854.81, 'parent_lgd': 474},
        {'lgd_code': 615, 'year': 2012, 'district': 'Baloda Bazar', 'area': 3733.87, 'parent_lgd': 480},
        {'lgd_code': 616, 'year': 2012, 'district': 'Gariaband', 'area': 5822.86, 'parent_lgd': 480},
        {'lgd_code': 617, 'year': 2012, 'district': 'Mungeli', 'area': 2750.36, 'parent_lgd': 472},
        {'lgd_code': 618, 'year': 2012, 'district': 'Kondagaon', 'area': 7769, 'parent_lgd': 470},
        {'lgd_code': 619, 'year': 2012, 'district': 'Sukma', 'area': 5636, 'parent_lgd': 473},
        {'lgd_code': 612, 'year': 2012, 'district': 'Balrampur-Ramanujganj', 'area': 6016, 'parent_lgd': 482},
        {'lgd_code': 620, 'year': 2012, 'district': 'Surajpur', 'area': 2786.76, 'parent_lgd': 482},
        {'lgd_code': 727, 'year': 2020, 'district': 'Gaurela-Pendra-Marwahi', 'area': 2307.39, 'parent_lgd': 472},
        {'lgd_code': 732, 'year': 2022, 'district': 'Khairagarh-Chhuikhadan-Gandai', 'area': 1553.84,
         'parent_lgd': 481},
        {'lgd_code': 731, 'year': 2022, 'district': 'Manendragarh-Chirmiri-Bharatpur', 'area': 4226, 'parent_lgd': 468},
        {'lgd_code': 730, 'year': 2022, 'district': 'Mohla-Manpur-Ambagarh Chowki', 'area': 2145.29, 'parent_lgd': 481},
        {'lgd_code': 734, 'year': 2022, 'district': 'Sakti', 'area': 1600, 'parent_lgd': 475},
        {'lgd_code': 733, 'year': 2022, 'district': 'Sarangarh-Bilaigarh', 'area': 1650, 'parent_lgd': [478, 615]},
    ]
    return pd.DataFrame(district_data)


def generate_time_series_data():
    df = load_initial_data()

    years = list(range(1998, 2026))

    time_series_data = []

    for year in years:
        existing_districts = df[df['year'] <= year].copy()

        for _, district in existing_districts.iterrows():
            base_area = district['area']

            years_since_creation = year - district['year']

            growth_factor = 1 + (np.sin(years_since_creation * 0.3) * 0.02)
            seasonal_factor = 1 + (np.sin((year - 1998) * 0.5) * 0.01)
            random_factor = 1 + (np.random.normal(0, 0.005))

            adjusted_area = base_area * growth_factor * seasonal_factor * random_factor

            time_series_data.append({
                'year': year,
                'district': district['district'],
                'lgd_code': district['lgd_code'],
                'area': adjusted_area,
                'base_area': base_area,
                'change_percent': ((adjusted_area - base_area) / base_area) * 100
            })

    return pd.DataFrame(time_series_data)


def create_animated_heatmap_plotly():
    df = generate_time_series_data()

    heatmap_data = df.pivot(index='district', columns='year', values='area')

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis',
        hovertemplate='District: %{y}<br>Year: %{x}<br>Area: %{z:.2f} km²<extra></extra>',
        colorbar=dict(title="Area (km²)")
    ))

    fig.update_layout(
        title="District Area Changes Over Time",
        xaxis_title="Year",
        yaxis_title="District",
        width=1200,
        height=800
    )

    return fig


def create_animated_change_heatmap():
    df = generate_time_series_data()

    change_data = df.pivot(index='district', columns='year', values='change_percent')

    fig = go.Figure()

    fig.add_trace(go.Heatmap(
        z=change_data.values,
        x=change_data.columns,
        y=change_data.index,
        colorscale='RdBu',
        zmid=0,
        hovertemplate='District: %{y}<br>Year: %{x}<br>Change: %{z:.2f}%<extra></extra>',
        colorbar=dict(title="Change from Base (%)")
    ))

    fig.update_layout(
        title="District Area Percentage Changes Over Time",
        xaxis_title="Year",
        yaxis_title="District",
        width=1200,
        height=800
    )

    return fig


def create_rolling_heatmap():
    df = generate_time_series_data()

    frames = []
    years = sorted(df['year'].unique())

    for i, current_year in enumerate(years):
        start_year = max(1998, current_year - 4)
        window_data = df[(df['year'] >= start_year) & (df['year'] <= current_year)]

        pivot_data = window_data.pivot(index='district', columns='year', values='area')

        pivot_data = pivot_data.fillna(0)

        frame = go.Frame(
            data=[go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='Viridis',
                hovertemplate='District: %{y}<br>Year: %{x}<br>Area: %{z:.2f} km²<extra></extra>',
                colorbar=dict(title="Area (km²)")
            )],
            name=str(current_year)
        )
        frames.append(frame)

    initial_data = df[df['year'] <= 2002]
    initial_pivot = initial_data.pivot(index='district', columns='year', values='area').fillna(0)

    fig = go.Figure(
        data=[go.Heatmap(
            z=initial_pivot.values,
            x=initial_pivot.columns,
            y=initial_pivot.index,
            colorscale='Viridis',
            hovertemplate='District: %{y}<br>Year: %{x}<br>Area: %{z:.2f} km²<extra></extra>',
            colorbar=dict(title="Area (km²)")
        )],
        frames=frames
    )

    fig.update_layout(
        title="Rolling 5-Year Window: District Area Changes",
        xaxis_title="Year",
        yaxis_title="District",
        width=1200,
        height=800,
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 800, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 300}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }],
        sliders=[{
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Year:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [
                {
                    "args": [[str(year)], {"frame": {"duration": 300, "redraw": True},
                                           "mode": "immediate", "transition": {"duration": 300}}],
                    "label": str(year),
                    "method": "animate"
                } for year in years
            ]
        }]
    )

    return fig


def create_matplotlib_animated_heatmap():
    df = generate_time_series_data()

    years = sorted(df['year'].unique())
    districts = sorted(df['district'].unique())

    fig, ax = plt.subplots(figsize=(15, 10))

    def animate(frame_num):
        ax.clear()

        current_year = years[frame_num]
        current_data = df[df['year'] <= current_year]

        pivot_data = current_data.pivot(index='district', columns='year', values='area')
        pivot_data = pivot_data.fillna(0)

        sns.heatmap(pivot_data,
                    annot=False,
                    cmap='viridis',
                    cbar_kws={'label': 'Area (km²)'},
                    ax=ax)

        ax.set_title(f'District Areas Over Time (Up to {current_year})', fontsize=16)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('District', fontsize=12)

        plt.xticks(rotation=45)
        plt.yticks(rotation=0)

        plt.tight_layout()

    anim = FuncAnimation(fig, animate, frames=len(years), interval=1000, repeat=True)

    anim.save('district_area_heatmap.gif', writer='pillow', fps=1)
    print("Animated heatmap saved as 'district_area_heatmap.gif'")

    return anim


def create_district_grid_heatmap():
    df = generate_time_series_data()

    formation_groups = df.groupby('district')['year'].min().reset_index()
    formation_groups.columns = ['district', 'formation_year']

    n_districts = len(formation_groups)
    grid_size = int(np.ceil(np.sqrt(n_districts)))

    positions = {}
    for i, district in enumerate(formation_groups['district']):
        row = i // grid_size
        col = i % grid_size
        positions[district] = (row, col)

    years = sorted(df['year'].unique())
    frames = []

    for year in years:
        grid_data = np.zeros((grid_size, grid_size))

        year_data = df[df['year'] == year]

        for _, row in year_data.iterrows():
            if row['district'] in positions:
                grid_row, grid_col = positions[row['district']]
                grid_data[grid_row, grid_col] = row['area']

        frames.append(grid_data)

    fig = go.Figure()

    plot_frames = []
    for i, grid_data in enumerate(frames):
        frame = go.Frame(
            data=[go.Heatmap(
                z=grid_data,
                colorscale='Viridis',
                hovertemplate='Row: %{y}<br>Col: %{x}<br>Area: %{z:.2f} km²<extra></extra>',
                colorbar=dict(title="Area (km²)")
            )],
            name=str(years[i])
        )
        plot_frames.append(frame)

    fig.frames = plot_frames

    fig.add_trace(go.Heatmap(
        z=frames[0],
        colorscale='Viridis',
        hovertemplate='Row: %{y}<br>Col: %{x}<br>Area: %{z:.2f} km²<extra></extra>',
        colorbar=dict(title="Area (km²)")
    ))

    fig.update_layout(
        title="District Grid Heatmap Animation",
        width=800,
        height=800,
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 1000, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 300}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate", "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }]
    )

    return fig


def main():
    print("Generating time series data...")

    np.random.seed(42)

    print("Creating static area heatmap...")
    fig1 = create_animated_heatmap_plotly()
    fig1.show()

    print("Creating percentage change heatmap...")
    fig2 = create_animated_change_heatmap()
    fig2.show()

    print("Creating rolling window heatmap...")
    fig3 = create_rolling_heatmap()
    fig3.show()

    print("Creating district grid heatmap...")
    fig4 = create_district_grid_heatmap()
    fig4.show()

    print("Creating matplotlib animated heatmap (saves as GIF)...")
    try:
        anim = create_matplotlib_animated_heatmap()
        print("GIF animation created successfully!")
    except Exception as e:
        print(f"Error creating GIF: {e}")
        print("Make sure you have matplotlib and pillow installed")

    df = generate_time_series_data()
    print(f"\nTime Series Statistics:")
    print(f"Years covered: {df['year'].min()} - {df['year'].max()}")
    print(f"Total districts: {df['district'].nunique()}")
    print(f"Total data points: {len(df)}")
    print(f"Average area change: {df['change_percent'].mean():.2f}%")
    print(f"Max area change: {df['change_percent'].max():.2f}%")
    print(f"Min area change: {df['change_percent'].min():.2f}%")

    return fig1, fig2, fig3, fig4


if __name__ == "__main__":
    fig1, fig2, fig3, fig4 = main()

    
    fig1.write_html("area_over_time.html")
    fig2.write_html("percentage_change.html")
    fig3.write_html("rolling_window.html")
    fig4.write_html("district_grid.html")
