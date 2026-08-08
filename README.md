# IPL-Specific Resource Table for Target Resetting in T20 Cricket

An empirical and model-calibrated resource allocation framework designed for high-scoring limited-overs cricket formats. This repository contains the data processing pipelines, non-linear optimization routines, and generated 20x10 resource percentage lookup tables specifically calibrated on Indian Premier League (IPL) delivery datasets.

---

## 📌 Repository Structure

```text
DLS_2026/
├── charts/             # Generated visualization plots and curve fits
├── codes/              # Python scripts for data processing & model fitting
├── final_csv/          # Cleaned, processed IPL ball-by-ball outputs
├── ipl_csv2/           # Raw IPL delivery logs dataset
├── resource tables/    # Final calculated and calibrated IPL resource matrices
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

---

## ⚙️ Methodology

1. **Data Ingestion & Event Extraction (`ipl_csv2/` & `final_csv/`):**  
   Raw ball-by-ball IPL delivery logs are parsed into discrete match-state coordinates $(u, w)$, where $u \in [0.0, 20.0]$ represents remaining overs and $w \in [0, 9]$ represents lost wickets.

2. **Empirical Matrix Aggregation:**  
   Average remaining runs are computed for every valid $(u, w)$ state across historical IPL innings to build an initial raw resource grid.

3. **Non-Linear Parameter Calibration (`codes/`):**  
   To resolve data sparsity in rare match states (e.g., late overs with high wicket loss), we fit a non-linear exponential decay function $R(u, w) = Z_0(w) \cdot \left(1 - e^{-b(w) \cdot u}\right)$ using Levenberg-Marquardt least-squares optimization.

4. **Resource Matrix Normalization (`resource tables/`):**  
   Trajectories are normalized against the full-resource baseline ($20.0$ overs, $0$ wickets = $100\%$) to generate calibrated lookup tables tailored to IPL scoring dynamics.

---

## 🚀 How to Run

### 1. Prerequisites
Ensure Python 3.8+ is installed, then install dependencies:
pip install -r requirements.txt
### 2. Execute Pipeline
Run the calibration and table generation scripts inside the `codes/` directory:
cd codes
python exponential.py

Output charts and optimized resource CSVs will auto-populate in `charts/` and `resource tables/`.

---

## 📜 Citation & References

If you cite or adapt this model in your research, please use the following references:

* **Duckworth, F. C., & Lewis, A. J. (1998).** *A fair method of resetting targets in interrupted two-innings matches.* Journal of the Operational Research Society, 49(2), 116–127.
* **Stern, S. E. (2016).** *An overview of the Duckworth-Lewis-Stern method for target resetting in interrupted limited-overs cricket matches.* Journal of Sports Analytics, 2(1), 3–16.
* **Cricsheet (2026).** *Ball-by-ball IPL dataset logs.* Available at: https://cricsheet.org/

---

## 👥 Authors

* **Juyee Shirkhedkar** – *Independent Researcher* – [juyee1010@gmail.com](mailto:juyee1010@gmail.com)
* **Sandeep Shirkhedkar** – *Independent Researcher* – [shirkhedkar@yahoo.com](mailto:shirkhedkar@yahoo.com)