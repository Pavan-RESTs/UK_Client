import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib import font_manager as fm
import matplotlib.patches as patches
import random
import matplotlib as mpl
import os


def giveFig(
    wedge1,
    dfobj,
    fileName,
    whitey=False,
    label12=False,
    lw=1,
    dpi1=300,
    l=7.2,
    b=7.2,
    colors=[],
    format="png",
    center_color="white",
):
    if whitey == False:
        lw = 0

    # Check if font files exist, use default fonts if not
    tamil_font_path = r"fonts\Tamil_Font.TTF"
    english_font_path = r"fonts\English_Font.ttf"

    try:
        if os.path.exists(tamil_font_path):
            tamil_prop = fm.FontProperties(fname=tamil_font_path)
        else:
            tamil_prop = fm.FontProperties()  # Use default font
    except:
        tamil_prop = fm.FontProperties()

    try:
        if os.path.exists(english_font_path):
            english_prop = fm.FontProperties(fname=english_font_path)
        else:
            english_prop = fm.FontProperties()  # Use default font
    except:
        english_prop = fm.FontProperties()

    english_prop.set_size(7.7)
    tamil_prop.set_size(8.5)

    df = dfobj.copy()  # Work with a copy to avoid modifying original

    categories = df.columns

    column_colors = (
        colors if colors else ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#ff99cc"]
    )
    outer_data = []
    outer_labels = []
    colors_list = []
    column_counts = []
    flagi = []
    counter = 0

    dfFor = dfobj.copy()
    mapping = {column: dfFor[column].count() for column in dfFor.columns}

    for i, category in enumerate(categories):
        category_values = df[category].dropna().unique()
        leng1 = len(category_values)
        unique_colors = dict(
            zip(
                category_values,
                [column_colors[i % len(column_colors)]] * len(category_values),
            )
        )

        for value in category_values:
            count = len(df[df[category] == value])

            label = str(value)
            color = unique_colors[value]
            threshold = 31
            if counter == 0:
                counter = 1
            else:
                counter = 0
            if len(label) > threshold:
                # Split long labels but keep single data point
                words = label.split()
                first_line = ""
                second_line = ""
                for word in words:
                    if len(first_line) + len(word) + 1 <= threshold:
                        first_line += word + " "
                    else:
                        second_line += word + " "
                outer_data.append(count)  # Single data point
                flagi.append(counter)
                first_line = first_line.rstrip()
                second_line = second_line.rstrip()

                # Combine lines for single label
                combined_label = first_line
                if second_line:
                    combined_label += "\n" + second_line

                outer_labels.append(combined_label)
                colors_list.append(color)
            else:
                label = label.rstrip()
                flagi.append(counter)
                outer_data.append(count)
                outer_labels.append(label)
                colors_list.append(color)
        column_counts.append(leng1)

    # Calculate positions for category annotations (middle of each group)
    pseudo_ind = []
    ing = 0
    for i in column_counts:
        pseudo_ind.append(ing + (i // 2))  # Middle position of each column group
        ing += i

    fig, ax = plt.subplots(figsize=(l, b), dpi=dpi1)

    size = 0.33
    wedgeprops_outer = dict(width=1.0, edgecolor="black")

    newl = []
    for i, element in enumerate(outer_labels):
        length = len(outer_labels)
        n = length // 4
        start = n + 1
        end = length - n - 1
        if start <= i <= end:
            newl.append([element, "left"])
        else:
            newl.append([element, "right"])

    for i in range(0, len(flagi) - 1):
        if flagi[i] == flagi[i + 1] and newl[i][1] == newl[i + 1][1] == "right":
            outer_labels[i], outer_labels[i + 1] = outer_labels[i + 1], outer_labels[i]

    def is_tamil(text):
        tamil_unicode_range = range(0x0B80, 0x0BFF)
        return any(ord(char) in tamil_unicode_range for char in text)

    # Create a copy of outer_labels for autopct_format to consume
    labels_for_autopct = outer_labels.copy()

    def autopct_format(pct):
        nonlocal labels_for_autopct  # Use nonlocal to access the copy
        if not labels_for_autopct:  # Safety check
            return ""

        threshold = 31
        label = labels_for_autopct.pop(0)
        pos = ""
        for i, ele in enumerate(newl):
            if ele[0] == label:
                pos = ele[1]
                break

        if pos == "right":
            if is_tamil(label):
                if len(label) > threshold:
                    label = "  " + label
                    words = label.split()
                    first_line = ""
                    second_line = ""
                    for word in words:
                        if len(first_line) + len(word) + 1 <= threshold:
                            first_line += word + " "
                        else:
                            second_line += word + " "
                    first_line = first_line.rstrip()
                    second_line = second_line.rstrip()
                    spaces_to_add_first = threshold - len(first_line)
                    spaces_to_add_second = threshold - len(second_line)
                    return f"{' ' * spaces_to_add_first*2}{'       '}{first_line}\n{' ' * spaces_to_add_second*2}{'           '}{second_line}{''}"
                spaces = threshold - len(label) - 3
                return f" {' ' * spaces*2}{''}{label}"
            else:
                threshold = 31
                if len(label) > threshold:
                    label = "  " + label
                    words = label.split()
                    first_line = ""
                    second_line = ""
                    for word in words:
                        if len(first_line) + len(word) + 1 <= threshold:
                            first_line += word + " "
                        else:
                            second_line += word + " "
                    first_line = first_line.rstrip()
                    second_line = second_line.rstrip()
                    spaces_to_add_first = threshold - len(first_line)
                    spaces_to_add_second = threshold - len(second_line)
                    return f"{' ' * spaces_to_add_first}{first_line}\n{' ' * spaces_to_add_second}{second_line}{''}"
                spaces = threshold - len(label)
                return f" {' ' * spaces}{label}"

        else:
            if is_tamil(label):
                if len(label) > threshold:
                    label = "  " + label
                    words = label.split()
                    first_line = ""
                    second_line = ""
                    for word in words:
                        if len(first_line) + len(word) + 1 <= threshold:
                            first_line += word + " "
                        else:
                            second_line += word + " "
                    first_line = first_line.rstrip()
                    second_line = second_line.rstrip()
                    spaces_to_add_first = threshold - len(first_line)
                    spaces_to_add_second = threshold - len(second_line)
                    return f"{first_line}{' ' * spaces_to_add_first}\n{second_line}{' ' * spaces_to_add_second }"
                spaces = threshold - len(label)
                return f"{label}{' ' * spaces }"
            else:
                threshold = 31
                if len(label) > threshold:
                    label = "  " + label
                    words = label.split()
                    first_line = ""
                    second_line = ""
                    for word in words:
                        if len(first_line) + len(word) + 1 <= threshold:
                            first_line += word + " "
                        else:
                            second_line += word + " "
                    first_line = first_line.rstrip()
                    second_line = second_line.rstrip()
                    spaces_to_add_first = threshold - len(first_line)
                    spaces_to_add_second = threshold - len(second_line)
                    return f"{first_line}{' ' * spaces_to_add_first}\n{second_line}{' ' * spaces_to_add_second }"
                spaces = threshold - len(label)
                return f"{label}{' ' * spaces }"

        return label

    # Apply whitey color override if requested
    final_colors = colors_list.copy()
    if whitey:
        final_colors = ["white"] * len(colors_list)

    outer_wedges, outer_texts, outer_autotexts = ax.pie(
        outer_data,
        labels=None,
        startangle=-0,
        colors=final_colors,
        autopct=autopct_format,
        textprops={"fontproperties": english_prop},  # Default font property
        wedgeprops=wedgeprops_outer if wedge1 else {},
    )

    pie_colors = column_colors

    fileName = str(fileName)  # Ensure fileName is a string
    plt.text(
        0,
        0,
        fileName,
        fontsize=12,
        color="black",
        ha="center",
        va="center",
        fontproperties=english_prop,
    )

    # Fixed angle calculation
    if len(outer_data) > 0:
        angles = np.linspace(0, 2 * np.pi, len(outer_data), endpoint=False).tolist()
        angles1 = []
        leng = len(outer_data)

        jump = 360.0 / len(outer_data)
        add = 179.95 * np.power(leng, -1.01)

        for i in np.arange(0.0, 360.0, jump):
            if 90 < i < 271:
                angles1.append(i + 180 + add)
            else:
                angles1.append(i + add)

        # Set rotation and font properties for text
        for index, auto_text in enumerate(outer_autotexts):
            if index < len(angles1):
                auto_text.set_rotation(angles1[index])
                if is_tamil(auto_text.get_text()):
                    auto_text.set_fontproperties(tamil_prop)
                else:
                    auto_text.set_fontproperties(english_prop)

    num_columns = len(df.columns)
    categories = list(categories)

    def pad_categories(categories):
        if not categories:  # Handle empty categories
            return categories

        max_len = max(len(category) for category in categories)
        padded_categories = []
        for category in categories:
            cur_len = len(category)
            total_padding = max_len - cur_len
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            padded_category = " " * left_padding + category + " " * right_padding
            padded_categories.append(padded_category)
        return padded_categories

    categories = pad_categories(categories=categories)

    try:
        if os.path.exists(english_font_path):
            english_prop2 = fm.FontProperties(fname=english_font_path, size=9)
        else:
            english_prop2 = fm.FontProperties(size=9)
    except:
        english_prop2 = fm.FontProperties(size=9)

    zind = 0
    for i, p in enumerate(outer_wedges):
        if i in pseudo_ind and zind < len(categories):
            bbox_props = dict(
                boxstyle="square,pad=1.8",
                fc="white" if whitey else pie_colors[zind % len(pie_colors)],
                ec="black" if whitey else pie_colors[zind % len(pie_colors)],
                lw=lw,
            )
            kw = dict(
                arrowprops=dict(
                    arrowstyle="<-",
                    color="black" if whitey else pie_colors[zind % len(pie_colors)],
                ),
                bbox=bbox_props,
                zorder=0,
                va="center",
            )
            ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(
                categories[zind],
                xy=(x, y),
                xytext=(1.35 * np.sign(x), 1.4 * y),
                horizontalalignment=horizontalalignment,
                **kw,
                fontproperties=(
                    tamil_prop if is_tamil(categories[zind]) else english_prop
                ),
            )
            zind += 1

    plt.axis("equal")

    # Draw radial lines between sections
    circle_radius = 0.25
    if len(column_counts) > 0 and len(outer_data) > 0:
        cumulative_counts = np.cumsum(column_counts)
        angles = np.linspace(0, 2 * np.pi, len(outer_data), endpoint=False)

        # Draw radial lines between column groups
        for i, count in enumerate(cumulative_counts[:-1]):
            if count < len(angles):
                angle = angles[count]  # Use angle directly, not degrees conversion
                x_inner = circle_radius * np.cos(angle)
                y_inner = circle_radius * np.sin(angle)
                x_outer = np.cos(angle)
                y_outer = np.sin(angle)
                ax.plot(
                    [x_outer, x_inner], [y_outer, y_inner], color="black", linewidth=lw
                )

        # Draw final radial line
        last_column_count = cumulative_counts[-1]
        if last_column_count < len(angles):
            angle = angles[last_column_count]
            x_inner = circle_radius * np.cos(angle)
            y_inner = circle_radius * np.sin(angle)
            x_outer = np.cos(angle)
            y_outer = np.sin(angle)
            ax.plot([x_outer, x_inner], [y_outer, y_inner], color="black", linewidth=lw)

    # Add center circle
    circle = patches.Circle(
        (0, 0),
        radius=circle_radius,
        edgecolor="black" if whitey else "white",
        facecolor=center_color,
        linewidth=lw,
    )
    ax.add_artist(circle)

    # Add outer circle
    circle_radius1 = 1
    circle1 = patches.Circle(
        (0, 0),
        radius=circle_radius1,
        edgecolor="black" if whitey else "white",
        facecolor="none",
        linewidth=lw,
    )
    ax.add_artist(circle1)

    # Create output directory if it doesn't exist
    output_dir = "./static/results/"
    os.makedirs(output_dir, exist_ok=True)

    plt.savefig(
        f"{output_dir}plot.{format}",
        dpi=dpi1,
        bbox_inches="tight",
        transparent=True,
    )

    return fig, ax  # Return the figure and axis for further use if needed
