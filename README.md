# Wildlife Movement Ecology

*A portfolio of reproducible analyses exploring animal movement, space use, and landscape ecology using GPS telemetry and geospatial data.*

---

## Overview

This repository documents my work developing quantitative workflows for wildlife movement ecology using Python, R, and modern geospatial analysis tools.

The primary goal of this repository is to build reproducible methods for transforming raw GPS telemetry into ecological insights that can support wildlife research, conservation, and ecosystem management.

Rather than focusing on a single species or project, this repository serves as a growing collection of analytical workflows that can be applied across movement ecology studies.

Current areas of focus include:

- GPS telemetry processing
- Movement metric calculation
- Home range estimation
- Spatial visualization
- Geospatial data analysis
- Reproducible ecological workflows

Future work will integrate movement data with environmental variables such as vegetation productivity, habitat structure, hydrology, and landscape heterogeneity to investigate the ecological drivers of animal movement and ecosystem processes.

---

# Current Projects

## Kruger National Park Elephant Movement Analysis

**Objective**

Develop a reproducible workflow for exploring elephant GPS telemetry and quantifying movement patterns and space use.

### Current Analyses

- GPS data cleaning and preprocessing
- Coordinate Reference System (CRS) standardization
- Trajectory generation
- Step length calculation
- Speed calculation
- Turning angle calculation
- Interactive movement mapping
- Individual movement summaries
- Exploratory visualization of movement metrics

### In Progress

- Individual elephant movement profiles
- Home range estimation (MCP and KDE)
- Seasonal movement comparisons
- Spatial overlap among individuals

### Planned Analyses

- Environmental covariate integration
- Vegetation productivity (NDVI)
- Distance-to-water analyses
- Habitat selection
- Landscape connectivity
- Ecosystem engineering applications

---

# Repository Structure

```
Wildlife-Movement-Ecology/

│
├── data/
│   └── (excluded from GitHub)
│
├── notebooks/
│
├── src/
│   ├── data_cleaning.py
│   ├── movement_metrics.py
│   ├── mapping.py
│   ├── home_ranges.py
│   └── visualization.py
│
├── figures/
│
├── reports/
│
└── README.md
```

---

# Tools & Libraries

### Programming

- Python
- R

### Geospatial Analysis

- GeoPandas
- Shapely
- MovingPandas
- pyproj

### Movement Ecology

- Ecoscope
- MovingPandas

### Data Analysis

- pandas
- NumPy

### Visualization

- Matplotlib
- Plotly
- Folium
- Lonboard

---

# Reproducibility

This repository emphasizes reproducible scientific workflows.

Analyses are designed to progress through a consistent pipeline:

```
Raw GPS telemetry
        ↓
Data cleaning
        ↓
Trajectory generation
        ↓
Movement metrics
        ↓
Exploratory visualization
        ↓
Home range estimation
        ↓
Ecological interpretation
```

---

# Data Management

Wildlife telemetry data often contain sensitive location information.

To protect species and comply with data-sharing agreements:

- Raw telemetry datasets are not stored in this repository.
- Large datasets are excluded using `.gitignore`.
- Only reproducible analysis code, documentation, and derived figures are included.

---

# Repository Goals

This portfolio is intended to demonstrate skills in:

- Wildlife movement ecology
- Spatial data science
- Geospatial programming
- Reproducible ecological research
- Conservation analytics

As additional projects are completed, this repository will expand to include analyses across multiple species and ecosystems.

---

# About

I am an ecologist and science educator developing quantitative skills in wildlife movement ecology, landscape ecology, and conservation data science.

My long-term research interests include:

- Animal movement ecology
- Ecosystem engineering
- Spatial ecology
- Human–wildlife coexistence
- Conservation technology

This repository documents that learning process while building reproducible analytical tools for wildlife research.

© 2026 | Wildlife Data Portfolio
