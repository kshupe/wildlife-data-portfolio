# Wildlife Data Science & Conservation Intelligence
> **A framework for wildlife movement ecology and conservation intelligence: Transforming raw telemetry into spatial insights to support ecosystem management, biodiversity monitoring, and human-wildlife coexistence.**

## Thesis
This repository serves as a framework for the digital defense of ecosystems. The goal is to bridge the gap between **raw sensor data** (GPS, satellite, acoustic) and **operational field action**. 

Rather than focusing on a single species, this portfolio develops methodologies to solve the core challenges in modern conservation: 
1. **Biological Stress Identification** (How environmental factors change behavior).
2. **Conflict Mitigation** (Predicting when and where wildlife meets human infrastructure).
3. **Resource Optimization** (Helping managers prioritize efforts through data).

---

## Active Analysis

### High-Frequency Movement Analysis: Kruger Megafauna
* **The Challenge:** Decoding "behavioral states" from GPS telemetry to identify fine-scale movement patterns and environmental drivers.
* **The Solution:** Using trajectory analysis to distinguish between foraging, resting, and rapid movement toward resources.
* **Analysis Link:** [View Movement Case Study](./boundarybreach_krugerelephants.ipynb)

---

## Tech Stack
* **Analysis:** Python (GeoPandas, Ecoscope, MovingPandas, Shapely)
* **Visualization:** Lonboard, Folium
* **Data Engineering:** Automated cleaning pipelines, Coordinate Reference System (CRS) standardization

---

## Data Ethics & Security
Conservation data is highly sensitive. This repository adheres to the following principles:
* **No Raw Data Storage:** All datasets are ignored via `.gitignore` to prevent the exposure of sensitive species locations.
* **Security-First Workflow:** Demonstrated experience in managing data that requires restricted access (e.g., CITES-listed species).
* **Open Source:** All code is licensed under **Apache 2.0**, encouraging global collaboration.

---

## Impact Goals
The ultimate objective of this work is to provide tools that:
* **Decrease Response Time:** Moving from historical analysis to "Live" situational awareness.
* **Optimize Resources:** Using heatmaps and density models to deploy ranger patrols effectively.
* **Support Policy:** Providing evidence-based spatial data for land-use planning and corridor protection.

---

*This is a living portfolio; new case studies and spatial analyses are added as they are developed.*

---

© 2026 | Wildlife Data Portfolio
