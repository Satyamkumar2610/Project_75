import warnings
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
from typing import Tuple

GRAPHVIZ_LAYOUT_CONFIG = {
    'rankdir': 'LR',
    'splines': 'true',
    'nodesep': '1.0',
    'ranksep': '1.2'
}

def load_district_data() -> pd.DataFrame:
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
        {'lgd_code': 467, 'year': 1998, 'district': 'Kabirdham', 'area': 4447.05, 'parent_lgd': [481, 472]},
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

def create_district_graphs(df: pd.DataFrame) -> Tuple[nx.DiGraph, nx.DiGraph]:
    df_dict = df.set_index('lgd_code').to_dict('index')
    G_data = nx.DiGraph()
    G_visual = nx.DiGraph()

    for lgd_code, data in df_dict.items():
        G_visual.add_node(lgd_code, **data)
        G_data.add_node(lgd_code, **data)
        if data['parent_lgd'] is not None:
            parents = data['parent_lgd'] if isinstance(data['parent_lgd'], list) else [data['parent_lgd']]
            for p_code in parents:
                G_data.add_edge(int(p_code), lgd_code)

    for lgd_code, data in df_dict.items():
        if data['parent_lgd'] is not None:
            parents = data['parent_lgd'] if isinstance(data['parent_lgd'], list) else [data['parent_lgd']]

            if len(parents) > 1:
                junction_id = f"junction_{lgd_code}"
                G_visual.add_node(junction_id, year=data['year'], is_junction=True)
                for p_code in parents:
                    G_visual.add_edge(int(p_code), junction_id)
                G_visual.add_edge(junction_id, lgd_code)
            else:
                G_visual.add_edge(int(parents[0]), lgd_code)

    parents_with_children = defaultdict(lambda: defaultdict(list))
    for child_code, data in df_dict.items():
        if data['parent_lgd'] is not None:
            parents = data['parent_lgd'] if isinstance(data['parent_lgd'], list) else [data['parent_lgd']]
            for p_code in parents:
                parents_with_children[p_code][data['year']].append(child_code)

    for p_code, splits_by_year in parents_with_children.items():
        last_timeline_node = p_code
        for year in sorted(splits_by_year.keys()):
            source_node = p_code
            remnant_id = f"remnant_{p_code}_{year}"
            G_visual.add_node(remnant_id, year=year, district=df_dict[p_code]['district'], is_remnant=True)
            G_visual.add_edge(last_timeline_node, remnant_id)
            last_timeline_node = remnant_id

    return G_data, G_visual

def visualize_graph(G: nx.DiGraph) -> None:
    G.graph['graph'] = GRAPHVIZ_LAYOUT_CONFIG

    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    except (ImportError, FileNotFoundError):
        warnings.warn("pygraphviz not found. Using a less structured spring layout.")
        pos = nx.spring_layout(G, iterations=50, k=0.5)

    edge_trace = go.Scatter(
        x=[x for edge in G.edges() for x in (pos[edge[0]][0], pos[edge[1]][0], None)],
        y=[y for edge in G.edges() for y in (pos[edge[0]][1], pos[edge[1]][1], None)],
        line=dict(width=0.7, color='#777'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y, node_text, node_size, node_color, node_border_color = [], [], [], [], [], []
    for node, data in G.nodes(data=True):
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(data.get('year', 1998))

        if data.get('is_junction', False):
            node_text.append("")
            node_size.append(0)
            node_border_color.append('rgba(0,0,0,0)')
        elif data.get('is_remnant', False):
            node_text.append(f"<b>{data.get('district', '')} (Post-{data.get('year', '')})</b><br>Continuation")
            node_size.append(15)
            node_border_color.append('lightgrey')
        else:
            lgd_code_str = f"LGD: {data.get('lgd_code', 'N/A')}"
            area_val = data.get('area', 0)
            area_str = f"Area: {area_val:,.0f} sq km" if area_val > 0 else "Area: N/A"
            node_text.append(
                f"<b>{data.get('district', 'Unknown')} ({data.get('year', '')})</b><br>{lgd_code_str}<br>{area_str}")
            node_size.append(max(12, area_val / 350))
            node_border_color.append('black')

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers', hoverinfo='text', text=node_text,
        marker=dict(
            showscale=True, colorscale='Viridis', reversescale=True, color=node_color,
            size=node_size,
            colorbar=dict(thickness=15, title='Year of Formation'),
            line=dict(width=2.5, color=node_border_color)
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(text='<b>Evolution of Districts in Chhattisgarh (1998-2022)</b>', font_size=20, x=0.5),
            showlegend=False, hovermode='closest', plot_bgcolor='white',
            margin=dict(b=20, l=5, r=5, t=50),
            annotations=[dict(
                text="Node size corresponds to area. Color indicates formation year. Grey borders show a district's continuation after a split.",
                showarrow=False, xref="paper", yref="paper", x=0.5, y=-0.02
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
    )
    fig.show()

def trace_district_lineage(df: pd.DataFrame, G: nx.DiGraph) -> None:
    name_to_lgd = {row['district'].lower(): row['lgd_code'] for _, row in df.iterrows()}
    districts = sorted(df['district'].unique())

    while True:
        print("\n" + "=" * 50 + "\n     District Lineage Tracer\n" + "=" * 50)
        for i, district in enumerate(districts, 1):
            print(f"{i:2d}. {district}")
        print("\nEnter district name or number (or 'exit' to quit):")

        user_input = input("> ").strip()
        if user_input.lower() == 'exit':
            break

        try:
            district_name = ""
            if user_input.isdigit() and 0 < int(user_input) <= len(districts):
                district_name = districts[int(user_input) - 1].lower()
            elif user_input.lower() in name_to_lgd:
                district_name = user_input.lower()
            else:
                print("Error: Input not found. Please enter a valid name or number.")
                continue

            lgd_code = name_to_lgd[district_name]
            node_info = G.nodes[lgd_code]

            print(f"\n{'=' * 60}\n  Lineage for {node_info['district'].upper()} ({node_info['year']})\n{'=' * 60}")
            print(f"LGD Code: {lgd_code} | Area at Formation: {node_info['area']:,} sq km")

            direct_parents = list(G.predecessors(lgd_code))
            if direct_parents:
                print("\nDirect Parent(s):")
                for p_lgd in direct_parents:
                    print(f"   • {G.nodes[p_lgd]['district']} ({G.nodes[p_lgd]['year']})")
            else:
                print("\nDirect Parent(s): None (Original District)")

            descendants = list(nx.descendants(G, lgd_code))
            if descendants:
                print("\nDescendants (Districts Formed From This One):")
                for d_lgd in sorted(descendants, key=lambda x: G.nodes[x]['year']):
                    print(f"   • {G.nodes[d_lgd]['district']} ({G.nodes[d_lgd]['year']})")

            print("=" * 60)
        except (ValueError, KeyError) as e:
            print(f"An unexpected error occurred: {e}")

def show_statistics(df: pd.DataFrame, G: nx.DiGraph) -> None:
    print("\n" + "=" * 60 + "\n   Overall District Statistics\n" + "=" * 60)

    total_districts = len(df)
    original_districts = len(df[df['parent_lgd'].isna()])

    print(f"Total Districts Recorded: {total_districts}")
    print(f"Original Districts (pre-2000): {original_districts}")
    print(f"New Districts Created Since 1998: {total_districts - original_districts}")

    current_districts_area = sum(data['area'] for node, data in G.nodes(data=True) if not G.out_degree(node))
    print(f"\nCombined Area of Current Districts: {current_districts_area:,.2f} sq km")

    largest = df.loc[df['area'].idxmax()]
    smallest = df.loc[df['area'].idxmin()]
    print(f"Largest District (at formation): {largest['district']} ({largest['area']:,} sq km)")
    print(f"Smallest District (at formation): {smallest['district']} ({smallest['area']:,} sq km)")

    print("\nDistrict Formations by Year:")
    for year, count in df['year'].value_counts().sort_index().items():
        print(f"  {year}: {count} new district(s)")

    print("\nMost Prolific Parent Districts:")
    split_counts = {node: G.out_degree(node) for node in G.nodes() if G.out_degree(node) > 0}
    sorted_splits = sorted(split_counts.items(), key=lambda item: item[1], reverse=True)
    for lgd_code, count in sorted_splits[:5]:
        print(f"  {G.nodes[lgd_code]['district']}: {count} child district(s)")

    print("=" * 60)

def main() -> None:
    district_df = load_district_data()
    data_graph, visual_graph = create_district_graphs(district_df)

    while True:
        print("\n" + "=" * 55 + "\n   Chhattisgarh District Evolution Explorer\n" + "=" * 55)
        print("1. Show Full Interactive Visualization")
        print("2. Trace Lineage of a Specific District")
        print("3. Show Overall Statistics")
        print("4. Exit")
        print("=" * 55)
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            print("\nGenerating visualization...")
            visualize_graph(visual_graph)
        elif choice == '2':
            trace_district_lineage(district_df, data_graph)
        elif choice == '3':
            show_statistics(district_df, data_graph)
        elif choice == '4':
            print("\nExiting program.")
            break
        else:
            print("Error: Invalid choice. Please enter a number from 1 to 4.")


if __name__ == '__main__':
    main()