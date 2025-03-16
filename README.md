# Campsite Alert 

Welcome to Campsite Alert! This script monitors the availability of campsites at your favorite parks on [recreation.gov](https://recreation.gov/) and alerts you based on your specified criteria. 

## Features
- Supports multiple **parks** (`--park_ids`) and **campsites** (`--campsites`).
- Filters results based on **minimum consecutive days** (`--num_days`).
- Runs automatically on a schedule (`--cycle_time` and `--total_time`).
- Outputs data in **summary** or **table** format (`--output_format`).

---

## Using Campsite_Alert

### **Required Parameters**
- `--start_date` → Start date of your search (format: `YYYY-MM-DD`).
- `--end_date` → End date of your search (format: `YYYY-MM-DD`).
- `--park_ids` → One or more park IDs from recreation.gov.

### **Optional Parameters**
- `--campsites` → List of specific campsites to track.
- `--num_days` → Minimum consecutive days required for booking.
- `--cycle_time` → Time interval (in minutes) to refresh the search.
- `--total_time` → Total script runtime (in minutes).
- `--output_format` → Choose output format:  
  - `"summary"` → Compact text output.
  - `"table"` → Structured tabular format.
  - `"both"` (default) → Shows both summary and table.

---

## Example Usage

### **Find a campsite at a specific park**
This command searches for campsite availability at `park_id 232453` for **March 2025**, checking every **1 minute** for up to **60 minutes**.

```bash
python Campsite_Alert.py \
    --start_date 2025-03-01 \
    --end_date 2025-03-30 \
    --park_ids 232453 \
    --campsites 042 \
    --num_days 2 \
    --cycle_time 1 \
    --total_time 60 \
    --output_format both