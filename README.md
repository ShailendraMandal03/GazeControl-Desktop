# GazeControl-Desktop
This project uses **Tobii Eye Tracker 5** along with **Tobii Ghost** (for green bubble overlay visualization) to detect and interact with desktop elements using eye gaze. The system tracks eye movements, identifies fixations and saccades, and triggers clicks (single/double) based on gaze hold. A green circle (from Tobii Ghost) is used as the visual indicator of the user's gaze point.

 ## 📌 Features

- Tracks real-time gaze using a green bubble overlay.
- Clicks on desktop icons or items by holding gaze.
- Double-click support to open files/folders.
- Detects fixations and saccades.
- Visualizes gaze path (scanpath) with matplotlib.
- Non-intrusive – clicks without moving mouse cursor.

________________________________________
## 🔧 Hardware and Software Requirements
### 💠 Hardware

- **Tobii Eye Tracker 5**
- A monitor with Tobii Eye Tracker 5 attached and calibrated.
- Windows PC with admin rights.

### 📍 Software

- **Tobii Ghost** (for visualizing gaze as a green bubble)
  - Install from: [https://gaming.tobii.com/software/ghost/](https://gaming.tobii.com/software/ghost/)
  - Use for visual overlay — enables detection through computer vision.

---

## 🐍 Python Environment Setup

### 🧰 Required Python Packages

Make sure you have Python 3.8+ installed. Then install the following dependencies:

```bash
pip install pyautogui keyboard opencv-python numpy pywinauto matplotlib
```

### ⚠️ Additional Notes:

- **Tkinter** may be preinstalled with Python, or can be installed via system package manager if needed.
- **Admin permissions** might be required for `pywinauto.mouse` to work properly.

---

## 📂 Folder Structure

```bash
🔹 gaze_click_tracker.py       # Main script
🔹 README.md                   # This file
🔹 logs/                       # (Optional) Save gaze logs here
🔹 requirements.txt            # (Optional) List of dependencies
```

---

## ▶️ Running the Program

### 🪟 Before You Start

1. Connect and calibrate **Tobii Eye Tracker 5** using **Tobii Experience**.
2. Launch **Tobii Ghost**:
   - Enable the **green bubble** overlay (usually a green circle showing gaze).
   - Ensure it is visible on your screen.

### 🏋️ Start the Script

Run the main script from terminal or your IDE:

```bash
python gaze_click_tracker.py
```

### 🎯 Interacting with the System

- **Hold gaze** on a desktop icon or item:
  - **≥ 0.5 seconds** = Single click.
  - **≥ 0.6 seconds** on desktop = Double click (e.g., open folder).
- **Fixation** is detected when gaze stays within a 25-pixel radius.
- **Saccade** is detected when gaze speed exceeds 1300 px/sec.
- **Exit** by pressing the `q` key.

---
## 📊 Output & Visualization

At the end of a session:
- Gaze data is stored in a list (`gaze_log`) and printed.
- Fixation and saccade details are tracked with time and position.
- You can optionally enable `plot_scanpath(...)` to visualize gaze behavior:

```python
# Uncomment in finally block
plot_scanpath(gaze_log, fixations, saccades)
```
This will plot:
- Gaze path (dotted line)
- Fixation points (red dots)
- Saccades (blue arrows)

---
## 🔍 Key Parameters and Thresholds

| Parameter                    | Description                         | Value                                |
| ---------------------------- | ----------------------------------- | ------------------------------------ |
| `GAZE_HOLD_TIME`             | Time to trigger single click        | 0.5 sec                              |
| `DOUBLE_CLICK_HOLD_TIME`     | Time to trigger double click        | 0.6 sec                              |
| `SACCADE_VELOCITY_THRESHOLD` | Minimum speed to qualify as saccade | 1300 px/sec                          |
| `GAZE_HOLD_RADIUS`           | Pixel radius for fixation           | 25 px                                |
| `CLICK_COOLDOWN`             | Time before next click allowed      | 3 sec                                |
| `HSV_LOWER/UPPER`            | HSV range for green detection       | `[55, 180, 180]` to `[70, 255, 255]` |

---
## 🧐 How It Works (Behind the Scenes)
1. **Tobii Ghost** overlays a green bubble indicating gaze position.
2. The Python script captures screen frames using `pyautogui.screenshot()`.
3. Applies HSV masking to detect the green circle.
4. Calculates:
   - Gaze position in screen coordinates.
   - Speed between gaze points to detect saccades.
   - If gaze is held still long enough — triggers click events.
5. Logs all gaze activity, fixations, and saccades.

---
## ✅ Tips for Best Accuracy

- Calibrate Tobii Eye Tracker using official **Tobii Experience** app.
- Use a **non-glossy monitor** to reduce reflection noise.
- Sit at a consistent distance and posture from the screen.
- Use under **consistent lighting conditions**.

---
## 🧪 Future Ideas

- Save gaze logs to CSV/JSON for post-analysis.
- Integrate with actual Tobii SDK for more precise data (if available).
- Real-time content-aware click targeting.
- Extend to web-based interaction or app controls.

---
## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---
## 🧛‍♂️ Author
Made with ❤️ by **[Shailendra Mandal]** — B.Tech Student.

