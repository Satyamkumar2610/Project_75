import networkx as nx
import plotly.graph_objects as go
import pandas as pd

try:
    import pydot
    PYDOT_AVAILABLE = True
except ImportError:
    PYDOT_AVAILABLE = False

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
        {'lgd_code': 732, 'year': 2022, 'district': 'Khairagarh-Chhuikhadan-Gandai', 'area': 1553.84, 'parent_lgd': 481},
        {'lgd_code': 731, 'year': 2022, 'district': 'Manendragarh-Chirmiri-Bharatpur', 'area': 4226, 'parent_lgd': 468},
        {'lgd_code': 730, 'year': 2022, 'district': 'Mohla-Manpur-Ambagarh Chowki', 'area': 2145.29, 'parent_lgd': 481},
        {'lgd_code': 734, 'year': 2022, 'district': 'Sakti', 'area': 1600, 'parent_lgd': 475},
        {'lgd_code': 733, 'year': 2022, 'district': 'Sarangarh-Bilaigarh', 'area': 1650, 'parent_lgd': [478, 615]},
    ]
    return pd.DataFrame(district_data)

def create_district_graph(df):
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
    G.graph['graph'] = {'rankdir': 'LR', 'splines': 'true', 'nodesep': '0.6'}
    try:
        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        except (ImportError, AttributeError):
            if PYDOT_AVAILABLE:
                pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
            else:
                raise ImportError
    except (ImportError, FileNotFoundError):
        print("Warning: Graphviz/pydot not found. Using spring layout.")
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
        node_text.append(f"<b>{node_info['district']} ({node_info['year']})</b><br>LGD Code: {node}<br>Area: {node_info['area']:,} sq km")
        node_size.append(max(8, node_info['area'] / 350))

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers', hoverinfo='text', text=node_text,
        marker=dict(
            showscale=True,
            colorscale='Viridis',
            reversescale=True,
            color=[G.nodes[node]['year'] for node in G.nodes()],
            size=node_size,
            colorbar=dict(thickness=15, title='Year of Formation', xanchor='left'),
            line_width=2
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(text='<b>Interactive Visualization of Chhattisgarh District Evolution (LGD Standardized)</b>', font=dict(size=18), x=0.5, xanchor='center'),
            showlegend=False, hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=60),
            annotations=[
                dict(text="Node size represents area. Color represents year of formation.", showarrow=False,
                     xref="paper", yref="paper", x=0.005, y=-0.002, xanchor='left', yanchor='bottom', font=dict(size=12, color='#666'))
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white', paper_bgcolor='white'
        )
    )
    fig.show()

def interactive_lineage_tracer(df, G):
    name_to_lgd = {row['district'].lower(): row['lgd_code'] for _, row in df.iterrows()}
    while True:
        print("\n" + "="*50)
        print("     District Lineage Tracer")
        print("="*50)
        print("\nAvailable districts:")
        districts = sorted([row['district'] for _, row in df.iterrows()])
        for i, district in enumerate(districts, 1):
            print(f"{i:2d}. {district}")
        print("\nEnter district name or number (or 'exit' to quit):")
        user_input = input("> ").strip()
        if user_input.lower() == 'exit':
            break
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(districts):
                district_name = districts[idx].lower()
            else:
                print(f"Error: Number must be between 1 and {len(districts)}")
                continue
        else:
            district_name = user_input.lower()
        if district_name not in name_to_lgd:
            print(f"Error: District '{user_input}' not found in the dataset.")
            continue
        lgd_code = name_to_lgd[district_name]
        node_info = G.nodes[lgd_code]
        print(f"\n{'='*60}")
        print(f"  LINEAGE FOR {node_info['district'].upper()} ({node_info['year']})")
        print(f"{'='*60}")
        print(f"LGD Code: {lgd_code}")
        print(f"Area: {node_info['area']:,} sq km")
        ancestors = list(nx.ancestors(G, lgd_code))
        if ancestors:
            print(f"\n🔼 ANCESTORS (Formed From):")
            for ancestor_lgd in sorted(ancestors, key=lambda x: G.nodes[x]['year']):
                ancestor_info = G.nodes[ancestor_lgd]
                print(f"   • {ancestor_info['district']} ({ancestor_info['year']}) - {ancestor_info['area']:,} sq km")
        else:
            print("\n🔼 ANCESTORS: This is an original district (no parents in this dataset).")
        descendants = list(nx.descendants(G, lgd_code))
        if descendants:
            print(f"\n🔽 DESCENDANTS (Contributed To):")
            for descendant_lgd in sorted(descendants, key=lambda x: G.nodes[x]['year']):
                descendant_info = G.nodes[descendant_lgd]
                print(f"   • {descendant_info['district']} ({descendant_info['year']}) - {descendant_info['area']:,} sq km")
        else:
            print("\n🔽 DESCENDANTS: This district has not been split further.")
        direct_parents = list(G.predecessors(lgd_code))
        direct_children = list(G.successors(lgd_code))
        if direct_parents:
            print(f"\n↗️  DIRECT PARENTS:")
            for parent_lgd in direct_parents:
                parent_info = G.nodes[parent_lgd]
                print(f"   • {parent_info['district']} ({parent_info['year']})")
        if direct_children:
            print(f"\n↘️  DIRECT CHILDREN:")
            for child_lgd in direct_children:
                child_info = G.nodes[child_lgd]
                print(f"   • {child_info['district']} ({child_info['year']})")
        print("="*60)

def show_statistics(df, G):
    print("\n" + "="*60)
    print("   📊 CHHATTISGARH DISTRICT STATISTICS")
    print("="*60)
    total_districts = len(df)
    original_districts = len(df[df['parent_lgd'].isna()])
    derived_districts = total_districts - original_districts
    print(f"Total Districts: {total_districts}")
    print(f"Original Districts (1998): {original_districts}")
    print(f"Derived Districts: {derived_districts}")
    total_area = df['area'].sum()
    avg_area = df['area'].mean()
    largest_district = df.loc[df['area'].idxmax()]
    smallest_district = df.loc[df['area'].idxmin()]
    print(f"\nArea Statistics:")
    print(f"Total Area: {total_area:,.2f} sq km")
    print(f"Average Area: {avg_area:,.2f} sq km")
    print(f"Largest District: {largest_district['district']} ({largest_district['area']:,} sq km)")
    print(f"Smallest District: {smallest_district['district']} ({smallest_district['area']:,} sq km)")
    years = df['year'].unique()
    print(f"\nFormation Years: {sorted(years)}")
    for year in sorted(years):
        count = len(df[df['year'] == year])
        districts_that_year = df[df['year'] == year]['district'].tolist()
        print(f"  {year}: {count} districts - {', '.join(districts_that_year)}")
    split_counts = {}
    for _, row in df.iterrows():
        if row['parent_lgd'] is not None:
            parents = row['parent_lgd']
            if not isinstance(parents, list):
                parents = [parents]
            for parent_lgd in parents:
                if parent_lgd not in split_counts:
                    split_counts[parent_lgd] = 0
                split_counts[parent_lgd] += 1
    if split_counts:
        print(f"\nMost Split Districts:")
        for lgd_code, count in sorted(split_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            district_name = df[df['lgd_code'] == lgd_code]['district'].iloc[0]
            print(f"  {district_name}: {count} child districts")
    print("="*60)

def main():
    district_df = load_and_prepare_data()
    district_graph = create_district_graph(district_df)
    while True:
        print("\n" + "="*55)
        print("   🏛️  CHHATTISGARH DISTRICT EVOLUTION EXPLORER")
        print("="*55)
        print("1. 📊 Show Full Interactive Visualization")
        print("2. 🔍 Trace Lineage of a Specific District")
        print("3. 📈 Show District Statistics")
        print("4. 🚪 Exit")
        print("="*55)
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            print("\n🎨 Generating visualization... Please check your browser or plot viewer.")
            visualize_graph(district_graph)
        elif choice == '2':
            interactive_lineage_tracer(district_df, district_graph)
        elif choice == '3':
            show_statistics(district_df, district_graph)
        elif choice == '4':
            print("\n👋 Thank you for using the Chhattisgarh District Evolution Explorer!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == '__main__':
    main()






