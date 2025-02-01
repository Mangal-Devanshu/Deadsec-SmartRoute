#%% Part 1: High-Performance Clustering Engine
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from haversine import haversine
from datetime import datetime
import time

class ClusterOptimizer:
    def __init__(self, store_loc,
                 max_time_gap=25,      # User-tuned parameter
                 geo_eps=0.15,         # User-tuned parameter
                 min_samples=1,        # User-tuned parameter
                 max_cluster_size=5):  # User-tuned parameter
        self.store = store_loc
        self.max_time_gap = max_time_gap
        self.geo_eps = geo_eps
        self.min_samples = min_samples
        self.max_cluster_size = max_cluster_size
        self.cluster_stats = []

    def time_to_minutes(self, time_str):
        """Efficient time conversion without datetime overhead"""
        try:
            h, m = map(int, time_str.split('-')[0].strip().split(':'))
            return h * 60 + m
        except:
            return 0

    def process_shipments(self, shipments):
        """Main clustering pipeline with performance optimizations"""
        start_time = time.time()

        # Preprocess with vectorized operations
        shipments = shipments.copy()
        shipments['start_min'] = shipments['Delivery Timeslot'].apply(self.time_to_minutes)
        shipments.sort_values('start_min', inplace=True)

        # Time-based segmentation
        time_clusters = self._create_time_clusters(shipments)

        # Geo-clustering with density control
        final_clusters = self._cluster_geographically(time_clusters)

        # Post-process statistics
        self._calculate_final_stats(final_clusters)

        print(f"\nProcessing completed in {time.time()-start_time:.2f} seconds")
        return final_clusters

    def _create_time_clusters(self, shipments):
        """Create tight time windows with size constraints"""
        clusters = []
        current_cluster = []

        for _, row in shipments.iterrows():
            if not current_cluster:
                current_cluster.append(row)
                continue

            # Time difference check
            time_diff = row['start_min'] - current_cluster[-1]['start_min']
            size_ok = len(current_cluster) < self.max_cluster_size

            if time_diff <= self.max_time_gap and size_ok:
                current_cluster.append(row)
            else:
                clusters.append(pd.DataFrame(current_cluster))
                current_cluster = [row]

        if current_cluster:
            clusters.append(pd.DataFrame(current_cluster))

        return clusters

    def _cluster_geographically(self, time_clusters):
        """Density-based spatial clustering with size enforcement"""
        final_clusters = []

        for t_cluster in time_clusters:
            coords = t_cluster[['Latitude', 'Longitude']].values

            # DBSCAN with tuned parameters
            db = DBSCAN(eps=self.geo_eps/111,
                       min_samples=self.min_samples,
                       metric='haversine',
                       n_jobs=-1)
            labels = db.fit_predict(np.radians(coords))

            # Cluster splitting logic
            for label in set(labels):
                if label == -1: continue  # Ignore noise
                cluster_group = t_cluster[labels == label]

                # Split large clusters
                while len(cluster_group) > self.max_cluster_size:
                    final_clusters.append(cluster_group.iloc[:self.max_cluster_size].to_dict('records'))
                    cluster_group = cluster_group.iloc[self.max_cluster_size:]

                if not cluster_group.empty:
                    final_clusters.append(cluster_group.to_dict('records'))

        return final_clusters

    def _calculate_final_stats(self, clusters):
        """Compute and display terminal statistics"""
        sizes = [len(c) for c in clusters]
        radii = []
        store_distances = []
        time_windows = []

        for cluster in clusters:
            lats = [s['Latitude'] for s in cluster]
            lons = [s['Longitude'] for s in cluster]
            times = [s['start_min'] for s in cluster]

            # Cluster metrics
            centroid = (np.mean(lats), np.mean(lons))
            radii.append(max(haversine(centroid, (lat, lon)) for lat, lon in zip(lats, lons)))
            store_distances.append(max(haversine(self.store, (lat, lon)) for lat, lon in zip(lats, lons)))
            time_windows.append((min(times), max(times)))

        # Terminal output formatting
        print(f"\n{' CLUSTERING STATISTICS ':=^80}")
        print(f"{'Total Clusters:':<25}{len(clusters):>10}")
        print(f"{'Average Cluster Size:':<25}{np.mean(sizes):>10.1f}")
        print(f"{'Max Cluster Size:':<25}{max(sizes):>10}")
        print(f"{'Min Cluster Size:':<25}{min(sizes):>10}\n")

        print(f"{'Cluster Size Distribution':-^80}")
        size_counts = pd.Series(sizes).value_counts().sort_index()
        for size, count in size_counts.items():
            print(f"{size} shipments:{count:>10} clusters ({count/len(clusters):.1%})")

        print(f"\n{'Geographical Metrics':-^80}")
        print(f"{'Average Cluster Radius:':<25}{np.mean(radii):>10.2f} km")
        print(f"{'Max Distance from Store:':<25}{max(store_distances):>10.2f} km")

        print(f"\n{'Temporal Metrics':-^80}")
        avg_window = np.mean([end-start for start, end in time_windows])
        print(f"{'Average Time Window:':<25}{avg_window//60:02.0f}h{avg_window%60:02.0f}m")

#%% Batch Processing
if __name__ == "__main__":
    # Load data
    shipments = pd.read_excel('Data.xlsx', sheet_name='Shipments_Data')
    store_df = pd.read_excel('Data.xlsx', sheet_name='Store Location')
    store_loc = (store_df['Latitute'].iloc[0], store_df['Longitude'].iloc[0])

    # Initialize with user-tuned parameters
    optimizer = ClusterOptimizer(
        store_loc,
        max_time_gap=25,
        geo_eps=0.2,
        min_samples=1,
        max_cluster_size=4
    )

    # Process in chunks for large datasets
    chunk_size = 1240
    all_clusters = []

    for i in range(0, len(shipments), chunk_size):
        chunk = shipments.iloc[i:i+chunk_size]
        all_clusters.extend(optimizer.process_shipments(chunk))

    # Final statistics
    optimizer._calculate_final_stats(all_clusters)