#This program will perform pca with two principal components
# Component 1 might capture overall scoring ability (PPG, FG%, 3P%).
# Component 2 might capture playmaking ability (APG, assist-to-turnover ratio).
# Then Cluster it and apply K-Means which will divide players into 4 Clusters
# Scorers: High PPG, average playmaking, low defense.
# Defensive Specialists: High SPG, BPG, low scoring.
# All-Around Players: Balanced PPG, APG, RPG, etc.
# Playmakers: High APG, lower scoring but excellent at creating opportunities.

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

data = pd.read_csv("All_Players_season_2024-25_Stats.csv")

data_filtered = data[data['GP'] >= 30]

features = ['PTS', 'AST', 'REB', 'STL', 'BLK']

x = data[features]

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)

kmeans = KMeans(n_clusters=4)
data['Cluster'] = kmeans.fit_predict(x_pca)


def plot_clusters_with_labels(x_pca, clusters, player_names):
    plt.figure(figsize=(100, 12))

    # Plot players as scatter points with clusters colored
    plt.scatter(x_pca[:, 0], x_pca[:, 1], c=clusters, cmap='viridis', marker='o')

    # Label each player with their name and cluster number
    for i in range(len(x_pca)):
        plt.text(x_pca[i, 0], x_pca[i, 1], f"{player_names[i]}: Cluster {clusters[i]}", fontsize=8)

    plt.title('PCA Clustering of NBA Players')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')

    # Adding a color bar to indicate cluster labels
    plt.colorbar(label='Cluster')

    plt.show()



plot_clusters_with_labels(x_pca, data['Cluster'], data['PLAYER_NAME'].tolist())