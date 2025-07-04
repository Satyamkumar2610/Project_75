[6:05 pm, 30/6/2025] Satyam: import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import pydot  # Required for graphviz_layout
from typing import Dict, List, Any, Optional

# --- Configuration for Visualization ---
VIS_CONFIG = {
    'graph_layout': {'rankdir': 'LR', 'splines': 'true', 'nodesep': '0.6'},
    'edge_line': {'width': 0.7, 'color': '#888'},
    'node_marker': {
        'showscale': True,
        'colorscale': 'Viridis',
        'reversescale': True,
        'size_divisor': 350,  # Adjust to scale node sizes
        'min_size': 8,
        'line_width': 2
    },
    'figure_layout': {
        'title_text': '<br><b>Interactive Visualization of Chhattisgarh District Evolution (LGD Standardized)</b>',
        'title_font_size': 18,
        'showlegend': Fa…
[6:06 pm, 30/6/2025] Satyam: import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import pydot  # pydot is now explicitly imported to check for its existence.
def load_and_prepare_data():
    """
    Loads the district data, including LGD codes for standardization.
    The LGD code is the official, unique identifier for each district.
    """
    district_data = [
        # Data enriched with Local Government Directory (LGD) codes for standardization
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
def create_district_graph(df):
    """Creates a directed graph from the district DataFrame using LGD codes as node IDs."""
    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_node(row['lgd_code'], year=row['year'], district=row['district'], area=row['area'])
    for _, row in df.iterrows():
        if row['parent_lgd'] is not None:
            parents = row['parent_lgd']
            if not isinstance(parents, list):
                parents = [parents]
            for parent_lgd in parents:
                G.add_edge(int(parent_lgd), row['lgd_code'])
    return G
def visualize_graph(G):
    """Generates and displays an interactive Plotly visualization of the graph."""
    # --- THIS IS THE CORRECTED SECTION ---
    # Set Graphviz attributes directly on the graph object for the layout engine.
    # This is the modern way to pass layout options, replacing the old 'args' parameter.
    G.graph['graph'] = {'rankdir': 'LR', 'splines': 'true', 'nodesep': '0.6'}
    try:
        # The 'args' parameter is removed from this call.
        pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
    except (ImportError, FileNotFoundError):
        print("Warning: Graphviz/pydot not found. Falling back to a standard layout.")
        print(
            "For a hierarchical view, please install them (e.g., 'pip install pydot' and install Graphviz separately).")
        pos = nx.spring_layout(G, iterations=50)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.7, color='#888'), hoverinfo='none', mode='lines')
    node_x, node_y, node_text, node_size = [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_info = G.nodes[node]
        node_text.append(f"<b>{node_info['district']} ({node_info['year']})</b><br>"
                         f"LGD Code: {node}<br>"
                         f"Area: {node_info['area']:,} sq km")
        node_size.append(max(8, node_info['area'] / 350))
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers', hoverinfo='text', text=node_text,
        marker=dict(
            showscale=True, colorscale='Viridis', reversescale=True, color=[], size=node_size,
            colorbar=dict(thickness=15, title='Year of Formation', xanchor='left', titleside='right'),
            line_width=2
        )
    )
    node_trace.marker.color = [G.nodes[node]['year'] for node in G.nodes()]
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br><b>Interactive Visualization of Chhattisgarh District Evolution (LGD Standardized)</b>',
                        titlefont_size=18, showlegend=False, hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()
def interactive_lineage_tracer(df, G):
    """Provides a command-line interface to trace district lineage interactively."""
    name_to_lgd = {row['district'].lower(): row['lgd_code'] for _, row in df.iterrows()}
    while True:
        print("\n--- District Lineage Tracer ---")
        district_name = input("Enter the name of the district to trace (or 'exit' to quit): ").strip().lower()
        if district_name == 'exit':
            break
        if district_name not in name_to_lgd:
            print(f"Error: District '{district_name.capitalize()}' not found in the dataset.")
            continue
        lgd_code = name_to_lgd[district_name]
        node_info = G.nodes[lgd_code]
        print(f"\n--- Lineage for {node_info['district']} ({node_info['year']}) ---")
        ancestors = list(nx.ancestors(G, lgd_code))
        if ancestors:
            print(f"\n[▲] ANCESTORS (Formed From):")
            for ancestor_lgd in sorted(ancestors, key=lambda x: G.nodes[x]['year']):
                ancestor_info = G.nodes[ancestor_lgd]
                print(f"  - {ancestor_info['district']} ({ancestor_info['year']})")
        else:
            print("\n[▲] ANCESTORS: This is an original district (no parents in this dataset).")
        descendants = list(nx.descendants(G, lgd_code))
        if descendants:
            print(f"\n[▼] DESCENDANTS (Contributed To):")
            for descendant_lgd in sorted(descendants, key=lambda x: G.nodes[x]['year']):
                descendant_info = G.nodes[descendant_lgd]
                print(f"  - {descendant_info['district']} ({descendant_info['year']})")
        else:
            print("\n[▼] DESCENDANTS: This district has not been split further.")
        print("-" * 35)
if _name_ == '_main_':
    district_df = load_and_prepare_data()
    district_graph = create_district_graph(district_df)
    while True:
        print("\n=============================================")
        print("  Chhattisgarh District Evolution Explorer")
        print("=============================================")
        print("1. Show Full Interactive Visualization")
        print("2. Trace Lineage of a Specific District")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        if choice == '1':
            print("Generating visualization... Please check your browser or plot viewer.")
            visualize_graph(district_graph)
        elif choice == '2':
            interactive_lineage_tracer(district_df, district_graph)
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
