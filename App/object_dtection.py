# import numpy as np
# import cv2
# import matplotlib.pyplot as plt

# # --- Load original image ---
# orig_img = cv2.imread(r"C:\APP\App\media\captured\two\ERL_refl.png", cv2.IMREAD_GRAYSCALE)

# # --- Load numpy array (for processing) ---
# arr = np.load("./media/raw_data.npy")

# # Create binary mask (151 <= value <= 155 → white, others → black)
# binary_img = np.where((arr >= 152) & (arr <= 156), 255, 0).astype(np.uint8)

# # Define kernel for morphology
# kernel = np.ones((4, 4), np.uint8)

# # Apply erosion and dilation
# eroded = cv2.erode(binary_img, kernel, iterations=1)
# dilated = cv2.dilate(eroded, kernel, iterations=1)

# # Find contours
# contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Convert to BGR for drawing
# output = cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR)

# # Set size conditions
# min_w, min_h = 20, 20
# max_w, max_h = 2000, 2000

# # Draw rectangles and centers
# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)

#     if min_w <= w <= max_w and min_h <= h <= max_h:
#         cx, cy = x + w // 2, y + h // 2
#         cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 5)
#         cv2.circle(output, (cx, cy), 4, (0, 0, 255), 5)
#         print(f"Object center: x={cx}, y={cy}, w={w}, h={h}")

# # Save processed result
# cv2.imwrite("detected_objects.png", output)

# # --- Show Original and Processed Side by Side ---
# plt.figure(figsize=(12, 6))

# plt.subplot(1, 2, 1)
# plt.imshow(orig_img, cmap="gray")
# plt.title("Original Image")
# plt.axis("off")

# plt.subplot(1, 2, 2)
# plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
# plt.title("Detected Objects with Rectangles")
# plt.axis("off")

# plt.tight_layout()
# plt.show()


import numpy as np
import cv2
import matplotlib.pyplot as plt
import os, json, time
from django.conf import settings


def caterpillar():
    media_root = settings.MEDIA_ROOT

    # --- Load paths ---
    depth_path = os.path.join(media_root, 'depth_config.json')
    rec = os.path.join(media_root, 'rectangle_coordinates.json')
    filter_path = os.path.join(media_root, 'tire_filters.json')
    raw_data_path = os.path.join(media_root, 'raw_data.npy')
    image_path = os.path.join(media_root, 'captured', 'two', 'ERL_refl.png')

    # --- Load original image ---
    orig_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # --- Load rectangle definitions ---
    try:
        with open(rec, "r") as f:
            regions = json.load(f)
    except FileNotFoundError:
        print(f"Rectangle config not found: {rec}")
        return

    rois = []
    for rect_key in [
        'rectangle1', 'rectangle2', 'rectangle3', 'rectangle4', 'rectangle5',
        "rectangle6", "rectangle7", "rectangle8", "rectangle9", "rectangle10"
    ]:
        rect = regions.get(rect_key, {})
        if rect:
            top_left = (rect["topLeft"]["x"], rect["topLeft"]["y"])
            bottom_right = (rect["bottomRight"]["x"], rect["bottomRight"]["y"])
            rois.append({
                'name': rect_key,
                'x_min': int(top_left[0]),
                'y_min': int(top_left[1]),
                'x_max': int(bottom_right[0]),
                'y_max': int(bottom_right[1])
            })

    # --- Load depth config ---
    try:
        with open(depth_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Depth config file not found: {depth_path}")
        return {'roi_statistics': [], 'detected_objects': []}

    y_pixel = float(config.get("y_pixel", 0.32))
    minrange = float(config.get("minrange", 100))
    maxrange = float(config.get("maxrange", 110))
    dprange = float(config.get("dprange", 105.0))
    filter_value = float(config.get("filter", 0.5))

    # --- Load depth array ---
    try:
        arr = np.load(raw_data_path)
    except FileNotFoundError:
        print(f"Raw data file not found: {raw_data_path}")
        return {'roi_statistics': [], 'detected_objects': []}

    # --- Processing ---
    output = cv2.cvtColor(orig_img, cv2.COLOR_GRAY2BGR)
    detected_objects = []

    for roi in rois:
        roi_arr = arr[roi['y_min']:roi['y_max'], roi['x_min']:roi['x_max']]

        # Threshold (example: 152–156, adjust if needed)
        binary_img = np.where((roi_arr >= minrange) & (roi_arr <= maxrange), 255, 0).astype(np.uint8)

        # Morphology
        kernel = np.ones((4, 4), np.uint8)
        processed = cv2.dilate(cv2.erode(binary_img, kernel, iterations=1), kernel, iterations=1)

        # Find contours in ROI
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            # Shift coords back to original image system
            x += roi['x_min']
            y += roi['y_min']

            if 20 <= w <= 2000 and 20 <= h <= 2000:
                cx, cy = x + w // 2, y + h // 2
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.circle(output, (cx, cy), 4, (0, 0, 255), -1)
                print(f"[{roi['name']}] center=({cx},{cy}), w={w}, h={h}")

                detected_objects.append({
                    "roi": roi['name'],
                    "center_x": cx,
                    "center_y": cy,
                    "width": w,
                    "height": h
                })

    # Save result
    cv2.imwrite("detected_objects.png", output)

    # # Show comparison
    # plt.figure(figsize=(12, 6))
    # plt.subplot(1, 2, 1)
    # plt.imshow(orig_img, cmap="gray")
    # plt.title("Original Image")
    # plt.axis("off")

    # plt.subplot(1, 2, 2)
    # plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    # plt.title("Detected Objects (within ROIs)")
    # plt.axis("off")
    # plt.show()

    return {"detected_objects": detected_objects}
# caterpillar()