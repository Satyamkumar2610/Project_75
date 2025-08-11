
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_prepare_data():
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


def create_3d_network_visualization():
    df = load_and_prepare_data()

    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_node(row['lgd_code'], **row.to_dict())

    for _, row in df.iterrows():
        if row['parent_lgd'] is not None:
            parents = row['parent_lgd'] if isinstance(row['parent_lgd'], list) else [row['parent_lgd']]
            for parent in parents:
                G.add_edge(parent, row['lgd_code'])

    pos = nx.spring_layout(G, k=3, iterations=50, dim=3)

    x_nodes = [pos[node][0] for node in G.nodes()]
    y_nodes = [pos[node][1] for node in G.nodes()]
    z_nodes = [pos[node][2] for node in G.nodes()]

    x_edges, y_edges, z_edges = [], [], []
    for edge in G.edges():
        x_edges.extend([pos[edge[0]][0], pos[edge[1]][0], None])
        y_edges.extend([pos[edge[0]][1], pos[edge[1]][1], None])
        z_edges.extend([pos[edge[0]][2], pos[edge[1]][2], None])

    node_colors = []
    node_text = []
    for node in G.nodes():
        year = G.nodes[node]['year']
        district = G.nodes[node]['district']
        area = G.nodes[node]['area']

        if year == 1998:
            color = 'red'
        elif year == 2007:
            color = 'orange'
        elif year == 2012:
            color = 'blue'
        elif year == 2020:
            color = 'green'
        else:
            color = 'purple'

        node_colors.append(color)
        node_text.append(f"{district}<br>LGD: {node}<br>Year: {year}<br>Area: {area} km²")

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=x_edges, y=y_edges, z=z_edges,
        mode='lines',
        line=dict(color='gray', width=2),
        hoverinfo='none',
        showlegend=False
    ))

    fig.add_trace(go.Scatter3d(
        x=x_nodes, y=y_nodes, z=z_nodes,
        mode='markers+text',
        marker=dict(
            size=8,
            color=node_colors,
            line=dict(width=2, color='black')
        ),
        text=[G.nodes[node]['district'] for node in G.nodes()],
        textposition="middle center",
        hovertext=node_text,
        hoverinfo='text',
        showlegend=False
    ))

    fig.update_layout(
        title="3D Network of District Relationships",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=900,
        height=700
    )

    return fig


def create_timeline_visualization():
    df = load_and_prepare_data()

    year_counts = df['year'].value_counts().sort_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=year_counts.index,
        y=year_counts.values,
        text=year_counts.values,
        textposition='auto',
        marker_color=['red', 'orange', 'blue', 'green', 'purple']
    ))

    fig.update_layout(
        title="District Formation Timeline",
        xaxis_title="Year",
        yaxis_title="Number of Districts Created",
        width=800,
        height=500
    )

    return fig


def create_area_analysis():
    df = load_and_prepare_data()

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Area Distribution by Year', 'Top 10 Largest Districts',
                        'Area vs Year Scatter', 'District Area Histogram'),
        specs=[[{"type": "box"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "histogram"}]]
    )

    for year in df['year'].unique():
        year_data = df[df['year'] == year]
        fig.add_trace(
            go.Box(y=year_data['area'], name=str(year), showlegend=False),
            row=1, col=1
        )

    top_10 = df.nlargest(10, 'area')
    fig.add_trace(
        go.Bar(x=top_10['district'], y=top_10['area'], showlegend=False),
        row=1, col=2
    )

    colors = {'1998': 'red', '2007': 'orange', '2012': 'blue', '2020': 'green', '2022': 'purple'}
    for year in df['year'].unique():
        year_data = df[df['year'] == year]
        fig.add_trace(
            go.Scatter(x=year_data['year'], y=year_data['area'],
                       mode='markers', name=str(year),
                       marker=dict(color=colors[str(year)], size=8),
                       text=year_data['district'], showlegend=False),
            row=2, col=1
        )

    fig.add_trace(
        go.Histogram(x=df['area'], nbinsx=15, showlegend=False),
        row=2, col=2
    )

    fig.update_layout(height=800, title_text="District Area Analysis")
    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="District", row=1, col=2)
    fig.update_xaxes(title_text="Year", row=2, col=1)
    fig.update_xaxes(title_text="Area (km²)", row=2, col=2)
    fig.update_yaxes(title_text="Area (km²)", row=1, col=1)
    fig.update_yaxes(title_text="Area (km²)", row=1, col=2)
    fig.update_yaxes(title_text="Area (km²)", row=2, col=1)
    fig.update_yaxes(title_text="Count", row=2, col=2)

    return fig


def perform_clustering():
    df = load_and_prepare_data()

    features = df[['year', 'area']].copy()

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)

    df['cluster'] = clusters

    fig = px.scatter(df, x='year', y='area', color='cluster',
                     hover_data=['district', 'lgd_code'],
                     title="District Clustering (K-means)",
                     labels={'cluster': 'Cluster'})

    fig.update_layout(width=800, height=600)

    return fig, df


def main():
    print("Creating visualizations...")

    fig_3d = create_3d_network_visualization()
    fig_3d.show()

    fig_timeline = create_timeline_visualization()
    fig_timeline.show()

    fig_area = create_area_analysis()
    fig_area.show()

    fig_cluster, df_clustered = perform_clustering()
    fig_cluster.show()

    df = load_and_prepare_data()
    print(f"\nDataset Statistics:")
    print(f"Total districts: {len(df)}")
    print(f"Years covered: {df['year'].min()} - {df['year'].max()}")
    print(f"Total area: {df['area'].sum():.2f} km²")
    print(f"Average area: {df['area'].mean():.2f} km²")
    print(f"Largest district: {df.loc[df['area'].idxmax(), 'district']} ({df['area'].max():.2f} km²)")
    print(f"Smallest district: {df.loc[df['area'].idxmin(), 'district']} ({df['area'].min():.2f} km²)")

    print(f"\nDistricts by formation year:")
    for year in sorted(df['year'].unique()):
        count = len(df[df['year'] == year])
        print(f"{year}: {count} districts")


if __name__ == "__main__":
    main()
