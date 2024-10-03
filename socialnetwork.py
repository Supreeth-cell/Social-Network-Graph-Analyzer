import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman
import pandas as pd
# edges = [
#     ("Alice", "Bob"),
#     ("Bob", "Catherine"),
#     ("Catherine", "Alice"),
#     ("Alice", "David"),
#     ("David", "Eve"),
#     ("Eve", "Frank"),
#     ("Frank", "Alice"),
#     ("Catherine", "David"),
#     ("David", "Frank")
# ]
# Load the data
file_path = "E:/Rushil/MINI proj/SNGA/dataset.xlsx"
excel_data = pd.ExcelFile(file_path)
df = pd.read_excel(file_path, sheet_name='Sheet1')
edges = list(df[['First', 'Second']].dropna().itertuples(index=False, name=None))

# Step 3: Graph Construction
# Create a graph from the edge list
G = nx.Graph()
G.add_edges_from(edges)

# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)

# Detect communities using the Girvan-Newman algorithm
communities = girvan_newman(G)
top_level_communities = next(communities)
community_list = [list(community) for community in top_level_communities]

# Print analysis results
print("Degree Centrality:", degree_centrality)
print("Betweenness Centrality:", betweenness_centrality)
print("Closeness Centrality:", closeness_centrality)
print("Eigenvector Centrality:", eigenvector_centrality)
print("Communities:", community_list)

# Position nodes using the spring layout
pos = nx.spring_layout(G)

# Create subplots
fig, axs = plt.subplots(3, 2, figsize=(15, 20))

def highlight_nodes_by_centrality(ax, G, pos, centrality, title):
    nodes = nx.draw_networkx_nodes(G, pos, node_size=2000, cmap=plt.cm.plasma, node_color=list(centrality.values()), nodelist=centrality.keys(), ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', ax=ax)
    ax.set_title(title)
    plt.colorbar(nodes, ax=ax)

# Default visualization
def draw_default_graph(ax, G, pos):
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=2000, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', ax=ax)
    ax.set_title("Default Visualization")

# Highlight degree centrality
highlight_nodes_by_centrality(axs[0, 0], G, pos, degree_centrality, "Degree Centrality")

# Highlight betweenness centrality
highlight_nodes_by_centrality(axs[0, 1], G, pos, betweenness_centrality, "Betweenness Centrality")

# Highlight closeness centrality
highlight_nodes_by_centrality(axs[1, 0], G, pos, closeness_centrality, "Closeness Centrality")

# Highlight eigenvector centrality
highlight_nodes_by_centrality(axs[1, 1], G, pos, eigenvector_centrality, "Eigenvector Centrality")

# Visualize communities
def visualize_communities(ax, G, pos, communities):
    colors = ['skyblue', 'lightgreen', 'salmon', 'lightyellow', 'lightpink']
    for i, community in enumerate(communities):
        nx.draw_networkx_nodes(G, pos, nodelist=community, node_color=colors[i % len(colors)], node_size=2000, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', ax=ax)
    ax.set_title("Communities")

visualize_communities(axs[2, 0], G, pos, community_list)

# Draw default graph
draw_default_graph(axs[2, 1], G, pos)

plt.tight_layout()
plt.show()
