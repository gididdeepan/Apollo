# import numpy as np
# import cv2
# import sys
# import time
# import json
# import csv
# # from scipy.signal import find_peaks, savgol_filter
# # from scipy.ndimage import gaussian_filter, maximum_filter, minimum_filter
# from scipy.ndimage import median_filter, gaussian_filter
# sys.stdout.reconfigure(encoding='utf-8')
# from datetime import datetime
# # def filter_noisy_extrema(values, coords, smooth, window=5, grad_threshold=5):
# #     """Reject peaks/downs that show sudden jumps (noise)."""
# #     clean_vals = []
# #     clean_coords = []
# #     for y, x in coords:
# #         # Extract local neighborhood
# #         y_min = max(0, y-window)
# #         y_max = min(smooth.shape[0], y+window+1)
# #         x_min = max(0, x-window)
# #         x_max = min(smooth.shape[1], x+window+1)
# #         local_patch = smooth[y_min:y_max, x_min:x_max]
        
# #         # Check local smoothness (max difference in patch)
# #         if np.ptp(local_patch) < grad_threshold:   # ptp = peak-to-peak (max-min)
# #             clean_vals.append(smooth[y, x])
# #             clean_coords.append((y, x))
    
# #     return np.array(clean_vals), clean_coords

# # count_value=1
# def s_tire():
#     # --- CONFIG FILES ---
#     depth_path = 'depth_config.json'
#     rec = 'rectangle_coordinates.json'
#     filter_path = 'tire_filters.json'
#     # --- Load rectangle coordinates ---
#     with open(rec, 'r') as f:
#         regions = json.load(f)
    
#     # Create list of ROIs (top-left and bottom-right coordinates)
#     rois = []
#     for rect_key in ['rectangle1', 'rectangle2', 'rectangle3','rectangle4','rectangle5',"rectangle6","rectangle7","rectangle8","rectangle9","rectangle10"]:
#         rect = regions.get(rect_key, {})
#         if rect:
#             top_left = (rect["topLeft"]["x"], rect["topLeft"]["y"])
#             bottom_right = (rect["bottomRight"]["x"], rect["bottomRight"]["y"])
#             # print("top_left",top_left)
#             # print("bottom_right",bottom_right)
#             rois.append({
#                 'name': rect_key,
#                 'top_left': top_left,
#                 'bottom_right': bottom_right,   
#                 'x_min': int(top_left[0]),
#                 'y_min': int(top_left[1]),
#                 'x_max': int(bottom_right[0]),
#                 'y_max': int(bottom_right[1])
#             })

#     # --- Load depth config ---
#     with open(depth_path, 'r') as f:
#         config = json.load(f)
#     y_pixel = float(config.get("y_pixel", 0.32))
#     minrange = float(config.get("minrange", 100))
#     maxrange = float(config.get("maxrange", 110))
#     dprange = float(config.get("dprange", 105.0))
#     filter_value = float(config.get("filter", 0.5))

#     # --- Load depth array ---
#     arr = np.load("raw_data.npy")
#     data = arr.copy()

#     # --- Resolution ---
#     x_resolution = 0.07805483  # mm/pixel
#     y_resolution = y_pixel     # mm/pixel

#     # start = time.time()

#     # --- Mask values outside valid range ---
#     filtered_arr = np.where((arr > maxrange) | (arr < minrange), 0, arr)
#     non_zero_values = filtered_arr[filtered_arr != 0]
#     if non_zero_values.size > 0:
#         min_val = np.min(non_zero_values)
#     else:
#         print("No values in range.")
#         return []

#     # --- Binary Threshold ---
#     binary_image = np.where(data > dprange, 255, 0).astype(np.uint8)
#     kernel = np.ones((3, 3), np.uint8)
#     binary_cleaned = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=2)

#     # --- Find contours ---
#     contours, _ = cv2.findContours(binary_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Load the RGB image for visualization
#     image = cv2.imread("./static/captured/two/ERL_refl - Copy.png")
#     if image is None:
#         print("Error: Could not load image")
#         return []

#     # Tolerance logic for dprange
#     tolerance = filter_value
#     lower_bound = dprange - tolerance
#     upper_bound = dprange + tolerance

#     # Process each ROI
#     roi_stats = []
#     Toler_value=[]
#     tyre_counter = 1
#     img_height, img_width = image.shape[:2]

#     for index, roi in enumerate(rois):
#         x_min, y_min = roi['x_min'], roi['y_min']
#         # print(x_min,y_min)
#         x_max, y_max = roi['x_max'], roi['y_max']
#         # cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
#         cv2.line(image, (x_min, 0), (x_min, img_height), (255, 0, 0), 3)  # Left boundary
#         cv2.line(image, (x_max, 0), (x_max, img_height), (255, 0, 0), 3)  # Right boundary
#         # Extract ROI from depth image
#         roi_depth = arr[y_min:y_max, x_min:x_max].copy()
#         # depth = np.load(npy_file)
#         # print(f"[INFO] Depth data loaded. Shape = {depth.shape}")

#        # Step 2: Remove invalid values (0, NaN, Inf)
       
#         # Apply min-max range: mask out-of-range values to 0
#         roi_depth[(roi_depth < minrange) | (roi_depth > maxrange)] = 0
#         depth_value = np.where((roi_depth == 0) | (np.isnan(roi_depth)) | (np.isinf(roi_depth)), np.nan, roi_depth)

#         filter_type = "median"
#         kernel_size = 5
#         sigma = 1

#         # Step 3: Noise filtering
#         if filter_type == "median":
#             depth_filtered = median_filter(np.nan_to_num(depth_value), size=kernel_size)
#             # print(f"[INFO] Median filter applied (kernel={kernel_size})")
#         elif filter_type == "gaussian":
#             depth_filtered = gaussian_filter(np.nan_to_num(depth_value), sigma=sigma)
#             # print(f"[INFO] Gaussian filter applied (sigma={sigma})")
#         else:
#             depth_filtered = depth_value
#             # print("[INFO] No filter applied")

#         # Step 4: Find min & max (ignoring NaNs)
#         min_val = np.nanmin(depth_filtered)
#         max_val = np.nanmax(depth_filtered)
        
#         min_coords = np.unravel_index(np.nanargmin(depth_filtered), depth_filtered.shape)
#         max_coords = np.unravel_index(np.nanargmax(depth_filtered), depth_filtered.shape)

#         # Step 5: Print resultsn
#         # print("min_val:", float(min_val))
#         # print("min_coords:", tuple(min_coords))
#         # print("max_val:", float(max_val))
#         # print("max_coords:", tuple(max_coords))
#         # print("subract value",max_val-min_val)
#         Correct_value=max_val-min_val
        
#         # Calculate ROI statistics and find min/max points
#          # Mark out-of-tolerance pixels in red
#         for y in range(roi_depth.shape[0]):
#             for x in range(roi_depth.shape[1]):
#                 val = roi_depth[y, x]
#                 if val == 0:
#                     continue  # skip masked or invalid depth
                 
#                 # if val < lower_bound or val > upper_bound:
#                 #     image[y + y_min, x + x_min] = [0, 0, 255]  # Red (BGR)
                    
#         roi_non_zero = roi_depth[roi_depth != 0]
#         if roi_non_zero.size > 0:
#              # Determine ROI rectangle color based on tolerance
#             region_key = f"Region_{index+1}_Tolernce"
#             region_dprange = float(config.get(region_key, dprange))  # fallback to global
#             # Find coordinates of min and max values
#             min_coords = np.unravel_index(np.argmin(roi_non_zero), roi_depth.shape)
#             # print("min_coords",min_coords)
            
#             max_coords = np.unravel_index(np.argmax(roi_non_zero), roi_depth.shape)
#             # print("max_coords",max_coords)
#             # Convert to global image coordinates
#             min_point = (x_min + min_coords[1], y_min + min_coords[0])
#             max_point = (x_min + max_coords[1], y_min + max_coords[0])
#              # Print only coordinates
#             # print(f"Min Point Coordinates: {min_point}")
#             # print(f"Max Point Coordinates: {max_point}")
#             roi_min = np.min(roi_non_zero)
#             # print("roi_min",roi_min)
#             roi_max = np.max(roi_non_zero)
#             # print("roi_max",roi_max)
#             # roi_range = roi_max - dprange
#             roi_mi=roi_min - dprange
#             #  # Calculate center of ROI for text placement
#             # if abs(roi_range) <= tolerance:  # Within tolerance → GREEN
#             #     rect_color = (0, 255, 0)  # Green (BGR)
#             # else:  # Out of tolerance → RED
#             #     rect_color = (0, 0, 255)  # Red (BGR) 
             
#             roi_range = roi_max - roi_min
#             final_value=Correct_value
#             # print("first come",roi_range)
#             lower_tolerance=region_dprange-tolerance
#             higher_tolerance=region_dprange+tolerance
#             # print("lower_tolerance",lower_tolerance)
#             # print("higher_tolerance",higher_tolerance)
            
#             # Check range against tolerance limits
#             if final_value < lower_tolerance or final_value > higher_tolerance:
#                 rect_color = (0, 0, 255)  # Red (BGR) → Out of tolerance
#                 cv2.line(image, (x_min, 0), (x_min, img_height), (0, 0, 255), 3)  # Left boundary
#                 cv2.line(image, (x_max, 0), (x_max, img_height), (0, 0, 255), 3)  # Right boundary
#             else:
#                 rect_color = (0, 255, 0)  # Green (BGR) → Within tolerance
#                 cv2.line(image, (x_min, 0), (x_min, img_height), (0, 255, 0), 3)  # Left boundary
#                 cv2.line(image, (x_max, 0), (x_max, img_height), (0, 255, 0), 3)  # Right boundary
           
                
#             center_x = (x_min + x_max) // 2
#             center_y = (y_min + y_max) // 2
#             text = f"{final_value:.2f}"
#             # print("text",text)
#             text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
#             text_x = center_x - text_size[0] // 2  # Center text horizontally
#             text_y = center_y + text_size[1] // 2  # Center text vertically
            
#             cv2.putText(
#                 image, text, (text_x, text_y),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, rect_color, 1, cv2.LINE_AA
#             )
            
#             # Draw circles at min and max points
#             cv2.circle(image, min_point, 5, (0, 255, 0), -1)  # Blue for min point
#             cv2.circle(image, min_point, 2, (255, 255, 255), -1)  # Blue for min point
#             cv2.circle(image, max_point, 5, (255, 0, 0), -1)  # Yellow for max point
#             cv2.circle(image, max_point, 2, (255, 255, 255), -1)  # Yellow for max point
            
#             # # Add text labels
#             # cv2.putText(image, f"Min: {roi_min:.2f}", (min_point[0]+10, min_point[1]), 
#             #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
#             # cv2.putText(image, f"Max: {roi_max:.2f}", (max_point[0]+10, max_point[1]), 
#             #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            
#             stats = {
#                 'name': roi['name'],
#                 'min': float(roi_min),
#                 'max': float(roi_max),
#                 'range': float(final_value),
#                 'min_point': {'x': int(min_point[0]), 'y': int(min_point[1])},
#                 'max_point': {'x': int(max_point[0]), 'y': int(max_point[1])}
#             }
            
#             roi_stats.append(stats)
#             current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             stat = {
#                 'name': f"region{index+1}",
#                 'upper_max': float(final_value),
#                 # 'lower_min': float(roi_mi),
#                 'datetime': current_dt
#             }
#             Toler_value.append(stat)
#             # print(f"{roi['name']} - Min: {roi_min:.2f}, Max: {roi_max:.2f}, Range: {final_value:.2f}")
            
#             # print(f"{roi['name']} - Min: {roi_min:.2f}, Max: {roi_max:.2f}, )
#         else:
#             print(f"{roi['name']} - No valid depth values")
    
#     # start_csv=time.time()
#     # csv_file = "roi_stats.csv"
#     # with open(csv_file, mode='a', newline='') as f:  # "a" = append
#     #     f.write(f"\ntyre {count_value}\n")  # block title
#     #     writer = csv.DictWriter(f, fieldnames=Toler_value[0].keys())
#     #     writer.writeheader()
#     #     writer.writerows(Toler_value)
 
#     # print(f"tyre {count_value} stats saved to {csv_file}")
    
#     # print("csv save time",time.time()-start_csv)
#     # Process contours and draw bounding boxes
#     results = []
#     for i, cnt in enumerate(contours):
#         if cv2.contourArea(cnt) < 3:
#             continue

#         rect = cv2.minAreaRect(cnt)
#         box = cv2.boxPoints(rect)
#         box = np.intp(box)
#         w, h = rect[1]

#         # Center of rotated rectangle
#         cx, cy = rect[0]
#         cx_int, cy_int = int(round(cx)), int(round(cy))
        
#         # Check if center is in any ROI
#         in_roi = False
#         for roi in rois:
#             if (roi['x_min'] <= cx_int <= roi['x_max'] and 
#                 roi['y_min'] <= cy_int <= roi['y_max']):
#                 in_roi = True
#                 break
        
#         if not in_roi:
#             continue

#         # Width/Height computation
#         if w > h:
#             width_mm = w * x_resolution
#             height_mm = h * y_resolution
#         else:
#             width_mm = w * y_resolution
#             height_mm = h * x_resolution

#         # Depth value at center
#         if 0 <= cy_int < arr.shape[0] and 0 <= cx_int < arr.shape[1]:
#             depth_val = filtered_arr[cy_int, cx_int] - min_val
#             # print("depth value ",depth_val)
            
#         else:
#             continue

#         result_data = {
#             "width_mm": round(float(width_mm), 2),
#             "height_mm": round(float(height_mm), 2),
#             "depth": round(float(depth_val), 2)
#         }
#         results.append(result_data)

#     # print("Processing time:", time.time() - start)

#     # --- Save outputs ---
#     cv2.imwrite("./static/captured/two/marked_outliers.png", image)
#     cv2.imwrite("./static/captured/two/rotated_bounding_boxes.png", image)
    
#     with open("results_summary.json", "w") as f:
#         json.dump({
#             'roi_statistics': roi_stats,
#             'detected_objects': results
#         }, f, indent=4)

#     return {
#         'roi_statistics': roi_stats,
#         'detected_objects': results
#     }



import numpy as np
import cv2
import sys
import time
import json
import csv
import os
from scipy.ndimage import median_filter, gaussian_filter
from datetime import datetime
from django.conf import settings

# sys.stdout.reconfigure(encoding='utf-8')

def s_tire():
    # --- CONFIG FILES ---
    # FIXED: Use proper file paths with MEDIA_ROOT
    print("above")
    media_root = settings.MEDIA_ROOT
    print("here",media_root)
    depth_path = os.path.join(media_root, 'depth_config.json')
    print("first")
    rec = os.path.join(media_root, 'rectangle_coordinates.json')
    print("Second")
    filter_path = os.path.join(media_root, 'tire_filters.json')
    print("thirsd")
    raw_data_path = os.path.join(settings.MEDIA_ROOT, 'raw_data.npy')
    print("raw_dtat reead")
    image_path = os.path.join(media_root, 'captured', 'two', 'ERL_refl.png')
    
    # Ensure directories exist
    os.makedirs(media_root, exist_ok=True)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    
    # --- Load rectangle coordinates ---
    try:
        with open(rec, 'r') as f:
            regions = json.load(f)
    except FileNotFoundError:
        print(f"Rectangle coordinates file not found: {rec}")
        return {'roi_statistics': [], 'detected_objects': []}

    # Create list of ROIs
    rois = []
    for rect_key in ['rectangle1', 'rectangle2', 'rectangle3', 'rectangle4', 'rectangle5', 
                    "rectangle6", "rectangle7", "rectangle8", "rectangle9", "rectangle10"]:
        rect = regions.get(rect_key, {})
        if rect:
            top_left = (rect["topLeft"]["x"], rect["topLeft"]["y"])
            bottom_right = (rect["bottomRight"]["x"], rect["bottomRight"]["y"])
            rois.append({
                'name': rect_key,
                'top_left': top_left,
                'bottom_right': bottom_right,   
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
        
    data = arr.copy()

    # --- Resolution ---
    x_resolution = 0.07805483  # mm/pixel
    y_resolution = y_pixel     # mm/pixel

    # --- Mask values outside valid range ---
    filtered_arr = np.where((arr > maxrange) | (arr < minrange), 0, arr)
    non_zero_values = filtered_arr[filtered_arr != 0]
    if non_zero_values.size > 0:
        min_val = np.min(non_zero_values)
    else:
        print("No values in range.")
        return {'roi_statistics': [], 'detected_objects': []}

    # --- Binary Threshold ---
    binary_image = np.where(data > dprange, 255, 0).astype(np.uint8)
    kernel = np.ones((3, 3), np.uint8)
    binary_cleaned = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=2)

    # --- Find contours ---
    contours, _ = cv2.findContours(binary_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Load the RGB image for visualization
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image: {image_path}")
            return {'roi_statistics': [], 'detected_objects': []}
    except Exception as e:
        print(f"Error loading image: {e}")
        return {'roi_statistics': [], 'detected_objects': []}

    # Tolerance logic for dprange
    tolerance = filter_value
    lower_bound = dprange - tolerance
    upper_bound = dprange + tolerance

    # Process each ROI
    roi_stats = []
    Toler_value = []
    img_height, img_width = image.shape[:2]

    for index, roi in enumerate(rois):
        x_min, y_min = roi['x_min'], roi['y_min']
        x_max, y_max = roi['x_max'], roi['y_max']
        
        # Draw ROI boundaries
        cv2.line(image, (x_min, 0), (x_min, img_height), (255, 0, 0), 3)
        cv2.line(image, (x_max, 0), (x_max, img_height), (255, 0, 0), 3)
        
        # Extract ROI from depth image
        roi_depth = arr[y_min:y_max, x_min:x_max].copy()
        
        # Apply min-max range: mask out-of-range values to 0
        roi_depth[(roi_depth < minrange) | (roi_depth > maxrange)] = 0
        depth_value = np.where((roi_depth == 0) | (np.isnan(roi_depth)) | (np.isinf(roi_depth)), np.nan, roi_depth)

        # Apply filter
        filter_type = "median"
        kernel_size = 5
        sigma = 1

        if filter_type == "median":
            depth_filtered = median_filter(np.nan_to_num(depth_value), size=kernel_size)
        elif filter_type == "gaussian":
            depth_filtered = gaussian_filter(np.nan_to_num(depth_value), sigma=sigma)
        else:
            depth_filtered = depth_value

        # Find min & max
        min_val_filtered = np.nanmin(depth_filtered)
        max_val_filtered = np.nanmax(depth_filtered)
        
        min_coords = np.unravel_index(np.nanargmin(depth_filtered), depth_filtered.shape)
        max_coords = np.unravel_index(np.nanargmax(depth_filtered), depth_filtered.shape)

        Correct_value = max_val_filtered - min_val_filtered
        
        # Process original ROI data for tolerance checking
        roi_non_zero = roi_depth[roi_depth != 0]
        if roi_non_zero.size > 0:
            region_key = f"Region_{index+1}_Tolernce"
            region_dprange = float(config.get(region_key, dprange))
            
            min_coords_orig = np.unravel_index(np.argmin(roi_non_zero), roi_depth.shape)
            max_coords_orig = np.unravel_index(np.argmax(roi_non_zero), roi_depth.shape)
            
            min_point = (x_min + min_coords_orig[1], y_min + min_coords_orig[0])
            max_point = (x_min + max_coords_orig[1], y_min + max_coords_orig[0])
            
            roi_min = np.min(roi_non_zero)
            roi_max = np.max(roi_non_zero)
            
            final_value = Correct_value
            lower_tolerance = region_dprange - tolerance
            higher_tolerance = region_dprange + tolerance
            
            # Check range against tolerance limits
            if final_value < lower_tolerance or final_value > higher_tolerance:
                rect_color = (0, 0, 255)  # Red
                cv2.line(image, (x_min, 0), (x_min, img_height), (0, 0, 255), 3)
                cv2.line(image, (x_max, 0), (x_max, img_height), (0, 0, 255), 3)
            else:
                rect_color = (0, 255, 0)  # Green
                cv2.line(image, (x_min, 0), (x_min, img_height), (0, 255, 0), 3)
                cv2.line(image, (x_max, 0), (x_max, img_height), (0, 255, 0), 3)
           
            center_x = (x_min + x_max) // 2
            center_y = (y_min + y_max) // 2
            text = f"{final_value:.2f}"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = center_x - text_size[0] // 2
            text_y = center_y + text_size[1] // 2
            
            cv2.putText(
                image, text, (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, rect_color, 1, cv2.LINE_AA
            )
            
            # Draw circles at min and max points
            cv2.circle(image, min_point, 5, (0, 255, 0), -1)
            cv2.circle(image, min_point, 2, (255, 255, 255), -1)
            cv2.circle(image, max_point, 5, (255, 0, 0), -1)
            cv2.circle(image, max_point, 2, (255, 255, 255), -1)
            
            stats = {
                'name': roi['name'],
                'min': float(roi_min),
                'max': float(roi_max),
                'range': float(final_value),
                'min_point': {'x': int(min_point[0]), 'y': int(min_point[1])},
                'max_point': {'x': int(max_point[0]), 'y': int(max_point[1])}
            }
            
            roi_stats.append(stats)
            current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            stat = {
                'name': f"region{index+1}",
                'upper_max': float(final_value),
                'datetime': current_dt
            }
            Toler_value.append(stat)
        else:
            print(f"{roi['name']} - No valid depth values")

    # Process contours and draw bounding boxes
    results = []
    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) < 3:
            continue

        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        w, h = rect[1]

        # Center of rotated rectangle
        cx, cy = rect[0]
        cx_int, cy_int = int(round(cx)), int(round(cy))
        
        # Check if center is in any ROI
        in_roi = False
        for roi in rois:
            if (roi['x_min'] <= cx_int <= roi['x_max'] and 
                roi['y_min'] <= cy_int <= roi['y_max']):
                in_roi = True
                break
        
        if not in_roi:
            continue

        # Width/Height computation
        if w > h:
            width_mm = w * x_resolution
            height_mm = h * y_resolution
        else:
            width_mm = w * y_resolution
            height_mm = h * x_resolution

        # Depth value at center
        if 0 <= cy_int < arr.shape[0] and 0 <= cx_int < arr.shape[1]:
            depth_val = filtered_arr[cy_int, cx_int] - min_val
        else:
            continue

        result_data = {
            "width_mm": round(float(width_mm), 2),
            "height_mm": round(float(height_mm), 2),
            "depth": round(float(depth_val), 2)
        }
        results.append(result_data)

    # --- Save outputs with proper paths ---
    marked_outliers_path = os.path.join(media_root, 'captured', 'two', 'marked_outliers.png')
    # rotated_boxes_path = os.path.join(media_root, 'captured', 'two', 'rotated_bounding_boxes.png')
    results_summary_path = os.path.join(media_root, 'results_summary.json')
    
    os.makedirs(os.path.dirname(marked_outliers_path), exist_ok=True)
    
    cv2.imwrite(marked_outliers_path, image)
    # cv2.imwrite(rotated_boxes_path, image)
    
    with open(results_summary_path, "w") as f:
        json.dump({
            'roi_statistics': roi_stats,
            'detected_objects': results
        }, f, indent=4)

    return {
        'roi_statistics': roi_stats,
        'detected_objects': results,
        'processing_time': time.time()  # You can calculate actual processing time if needed
    }