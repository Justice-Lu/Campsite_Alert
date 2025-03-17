### Campsite Alert

Welcome to Campsite Alert! This script helps you track campsite availability on [recreation.gov](https://recreation.gov/) and alerts you when your desired campsites become available.

---

### Installation Guide

Follow these steps to install and run Campsite Alert:

#### 1️⃣ Clone the Repository
If you don’t have Git installed, [download it here](https://git-scm.com/downloads) and install it first.

Then, open a terminal (Command Prompt, PowerShell, or Terminal on Mac/Linux) and run:
```bash
git clone https://github.com/yourusername/Campsite_Alert.git
cd Campsite_Alert
```

#### 2️⃣ Create a Virtual Environment (Recommended)
It’s best to run the script in a virtual environment to avoid dependency issues.

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies
Run the following command to install required Python packages:
```bash
pip install -r requirements.txt
```

If you don’t have `pip` installed, follow [this guide](https://pip.pypa.io/en/stable/installation/).

---

### Using Campsite Alert

The script requires the following parameters:
- `--start_date` (YYYY-MM-DD)
- `--end_date` (YYYY-MM-DD)
- `--park_id` (Numeric ID from recreation.gov)
- `--num_days` (Number of consecutive days needed)
- `--cycle_time` (Minutes between each check, default: 1)
- `--total_time` (Total minutes the script will run, default: 1)
- `--format` (Choose between `summary` or `table` output)

#### Example Command
This example searches for available campsites at park `232453` between `2025-06-01` and `2025-06-30` for a `3-day` stay, refreshing every `2 minutes` for a total of `10 minutes`:
```bash
python Campsite_Alert.py \
    --start_date 2025-06-01 \
    --end_date 2025-06-30 \
    --park_id 232453 \
    --num_days 3 \
    --cycle_time 2 \
    --total_time 10 \
    --format table
```

#### Example Output (Table Format)
```
🏞️  233235 : REVERSED CREEK CAMPGROUND
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┓
┃ Date Range                        ┃ 015   ┃ 016   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━╋━━━━━━━┫
┃ 2025-06-01 --> 2025-06-04         ┃ A     ┃ A     ┃
┃ 2025-06-02 --> 2025-06-05         ┃ A     ┃ A     ┃
┃ 2025-06-03 --> 2025-06-06         ┃ A     ┃ A     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━┻━━━━━━━┛
```

#### Example Output (Summary Format)
```
🗓️  On 2025-06-01 --> 2025-06-04: 2 out of 2 campsites are available.
🗓️  On 2025-06-02 --> 2025-06-05: 2 out of 2 campsites are available.
🗓️  On 2025-06-03 --> 2025-06-06: 2 out of 2 campsites are available.
```

---

### Find Campsites at Multiple Parks
You can track multiple parks at once by providing multiple `park_id` values:
```bash
python Campsite_Alert.py \
    --start_date 2025-06-01 \
    --end_date 2025-06-30 \
    --park_id 233235 232269 \
    --num_days 3 \
    --cycle_time 2 \
    --total_time 10 \
    --format table
```

---

### Finding Park and Campsite IDs
#### `--park_id`
To find the park ID, visit [recreation.gov](https://recreation.gov/) and navigate to the campground page.
For example, the URL:
```
https://www.recreation.gov/camping/campgrounds/232447
```
The park ID is **232447** (the number at the end of the URL).

#### `--campsite`
The campsite ID is the designated **Site** number shown in the availability chart on recreation.gov.

---

### Stopping the Script
To manually stop the script, press `CTRL + C` in the terminal.

---

### Notes
- If a park ID returns a `403` error, it may not be publicly available for querying.
- This script **does not** book campsites, it only alerts you of availability.
- The script runs until `total_time` expires or you manually stop it.

---

Happy camping! 🏕️

