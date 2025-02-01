**SmartRoute Optimizer - Git Documentation**  
*Version 1.0 | Last Updated: [Date]*  

---

### **1. Repository Structure**
```
smartroute-optimizer/
├── data/
│   ├── SmartRoute Optimizer.xlsx     # Input data template
│   └── trip_details.xlsx            # Generated output
├── src/
│   ├── part1_clustering.py          # Cluster generation module
│   ├── part3_optimization.py        # Route planning module
│   └── helpers.py                   # Utility functions
├── outputs/
│   ├── optimized_routes.html         # Interactive map
│   └── clustering_stats.txt          # Cluster metrics
├── requirements.txt                  # Dependency list
└── README.md                         # This documentation
```

---

### **2. System Requirements**
#### Dependencies
```python
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
haversine==2.8.0
scipy==1.11.1
folium==0.14.0
openpyxl==3.1.2
```

#### Hardware Recommendations
- Minimum: 4GB RAM, Dual-core CPU  
- Recommended: 8GB RAM, Quad-core CPU (for 5,000+ shipments)

---

### **3. Installation**
```bash
# Clone repository
git clone https://github.com/yourusername/smartroute-optimizer.git
cd smartroute-optimizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Prepare data
mkdir -p data
# Place your Data.xlsx in data/ directory
```

---

### **4. Configuration Guide**
#### Part 1: Clustering Parameters (`part1_clustering.py`)
```python
class ClusterOptimizer:
    def __init__(self,
                 max_time_gap=25,     # Max minutes between shipments
                 geo_eps=0.15,        # 150m cluster radius
                 min_samples=1,       # Min shipments per cluster
                 max_cluster_size=5): # Match vehicle capacity
```

#### Part 3: Optimization Parameters (`part3_optimization.py`)
```python
class DualGreedyOptimizer:
    def __init__(self,
                 range_buffer_percent=15): # 15% safety margin
```

---

### **5. Execution Workflow**
#### Step 1: Cluster Generation
```bash
python src/part1_clustering.py
```
**Output**: 
- Temporal-spatial clusters
- Cluster statistics in console/outputs/

#### Step 2: Route Optimization
```bash
python src/part3_optimization.py
```
**Output**:
- `optimized_routes.html` (Interactive map)
- `trip_details.xlsx` (Trip sequences & metrics)
- Console optimization statistics

---

### **6. Technical Overview**
#### Part 1: Intelligent Clustering Engine
1. **Time-Based Segmentation**
   ```python
   def _create_time_clusters():
       # Groups shipments into 25-min windows
       while time_diff <= 25 and size < max_cluster_size:
           add_to_current_cluster()
   ```

2. **Geographic Density Clustering**
   ```python
   DBSCAN(eps=0.15/111, metric='haversine') 
   # Converts km to degrees (111km/degree)
   ```

3. **Size-Constrained Splitting**
   ```python
   while len(cluster) > max_size:
       split_into_valid_clusters()
   ```

#### Part 3: Dual-Greedy Optimization
1. **Phase 1 - Farthest-First Assignment**
   ```python
   for cluster in sorted_by_distance(reverse=True):
       if within_range(3W):
           assign_and_merge()
   ```

2. **Phase 2 - Nearest-Neighbor Fill**
   ```python
   while vehicles_available:
       find_nearest_valid()
       merge_if_valid()
   ```

3. **Phase 3 - 4W Batch Processing**
   ```python
   create_batches(max=25, time_window=4h)
   ```

---

### **7. Key Features**
#### Priority Vehicle Handling
```python
vehicle_priority = ['3W', '4W-EV', '4W']
remaining_vehicles = int(v_spec['Number'])
```

#### Time Window Management
```python
if (new_end - new_start) > 240:  # 4-hour max
    reject_merge()
```

#### Interactive Visualization
```python
folium.FeatureGroup(show=False)  # Initial layer state
folium.LayerControl().add_to(m)
```

---

### **8. Validation Metrics**
| Metric               | Formula                          | Target     |
|----------------------|----------------------------------|------------|
| Capacity Utilization | Actual/Max Capacity             | 50-100%    |
| Time Utilization     | Trip Time/Max Allowed Time      | ≤100%      |
| Distance Utilization | Route Distance/(2×Max Radius)   | ≤100%      |

---

### **9. Assumptions & Limitations**
#### Assumptions
1. Fixed travel time (5 mins/km)
2. 10 mins/shipment service time
3. MST distance approximation
4. Single-day deliveries

#### Limitations
1. No real-time traffic integration
2. Fixed priority vehicle order
3. 4-hour max trip window

---

### **10. Troubleshooting**
**Common Errors**:
```bash
# KeyError: 'Latitude'
⇒ Verify Excel column names match code expectations

# ZeroDivisionError in metrics
⇒ Check for empty clusters in input data

# MemoryError with large datasets
⇒ Reduce chunk_size in part1_clustering.py
```

---

### **11. License**
```text
MIT License
Copyright (c) 2024 [Your Name]
Permission is hereby granted... [Standard MIT text]
```

---

### **12. References**
1. Problem Statement: SmartRouteOptimizer.pdf
2. DBSCAN Clustering: scikit-learn Documentation
3. Haversine Formula: IEEE Floating-Point Standard
4. Folium Visualization: Python Spatial Visualization Guide

[End of Documentation]  

Let me know if you need any specific section expanded or additional implementation details!

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/51151485/c4d4fd69-ac6e-46ab-b409-5a2e51bcab76/SmartRouteOptimizer.pdf
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/51151485/852da726-d9e7-46b4-bd7b-e5488f1d6c97/part1.py
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/51151485/d598b9e6-f237-479d-a06b-d2de650c4bd3/paste-4.txt
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/51151485/3938d5b1-7b7f-4b9d-8b96-e72c0669873b/MINeD-2025-Submission-Guidelines.pdf

---
Answer from Perplexity: https://www.perplexity.ai/search/hey-i-have-created-solution-to-_TkhbGy6SQaNBCIgUtmOWA?utm_source=copy_output
