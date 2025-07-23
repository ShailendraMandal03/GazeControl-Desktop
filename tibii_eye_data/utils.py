import matplotlib.pyplot as plt

def calculate_velocity(pos1, time1, pos2, time2):
    if pos1 is None or pos2 is None or time1 is None or time2 is None:
        return 0
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dt = time2 - time1
    if dt == 0:
        return 0
    return ((dx**2 + dy**2) ** 0.5) / dt

def plot_scanpath(gaze_log, fixations, saccades):
    plt.figure(figsize=(12, 8))

    x_vals = [x for _, x, _ in gaze_log]
    y_vals = [y for _, _, y in gaze_log]
    plt.plot(x_vals, y_vals, linestyle='--', color='gray', label='Raw Gaze Path', alpha=0.5)

    for i, (t, (x, y)) in enumerate(fixations):
        plt.scatter(x, y, c='red', s=60, label='Fixation' if i == 0 else "", zorder=3)

    for s in saccades:
        x_vals = [s['from'][0], s['to'][0]]
        y_vals = [s['from'][1], s['to'][1]]
        plt.arrow(x_vals[0], y_vals[0], x_vals[1] - x_vals[0], y_vals[1] - y_vals[0],
                  head_width=15, head_length=15,
                  length_includes_head=True,
                  color='blue', alpha=0.5,
                  zorder=2)

    plt.title("Scanpath: Fixations and Saccades")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
