# import json
# import numpy as np
# import cv2
# import csv
# import time
# from datetime import datetime
# import os 
# # from scipy.ndimage import gaussian_filter, maximum_filter, minimum_filter
# from scipy.ndimage import median_filter, gaussian_filter

# def c_tire(count_value,client_socket,arr,value):
#     # --- Load job selection ---
#     with open("job_selection.json", "r") as f:
#         job = json.load(f)
#     value=int(value)   
#     if value==1:
#         job_selected="Component1"
#     elif value==2:
#         job_selected="Component2"
#     elif value==3:
#         job_selected="Component3"
#     # job_selected = job.get("job_selection", "Component1")  # default fallback
#     # print("Current Job:", job_selected)
#     # # --- Map job selection to correct files ---
    
#     job_files = {
#         "Component1": {
#             "rect": "First_object.json",
#             "depth": "First_depth_config.json"
#         },
#         "Component2": {
#             "rect": "second_object.json",
#             "depth": "second_depth_config.json"
#         },
        
#         "Component3": {
#             "rect": "Third_object.json",
#             "depth": "Third_depth_config.json"
#         }
#     }

#     if job_selected not in job_files:
#         raise ValueError(f"Unknown job selection: {job_selected}")

#     rec = job_files[job_selected]["rect"]
#     depth_path = job_files[job_selected]["depth"]
#     # print("Using rectangle file:", rec)
#     # print("Using depth config file:", depth_path)

#     # --- Load rectangle coordinates ---
#     with open(rec, 'r') as f:
#         regions = json.load(f)
#     # print("load")
#     # Create list of ROIs (top-left and bottom-right coordinates)
#     rois = []
#     for rect_key in [
#         'rectangle1','rectangle2','rectangle3','rectangle4','rectangle5',
#         'rectangle6','rectangle7','rectangle8','rectangle9','rectangle10']:
#         rect = regions.get(rect_key, {})
#         if rect:
#             top_left = (rect["topLeft"]["x"], rect["topLeft"]["y"])
#             bottom_right = (rect["bottomRight"]["x"], rect["bottomRight"]["y"])
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
#     # arr = np.load("raw_data.npy")
#     data = arr.copy()

#     # --- Resolution ---
#     x_resolution = 0.07805483  # mm/pixel
#     y_resolution = y_pixel     # mm/pixel

#     start = time.time()

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
#     Toler_value = []
   
#     img_height, img_width = image.shape[:2]
#     pass_count = 0   # ROIs that are within tolerance
#     job_count = len(rois)  # total ROIs in the job
#     # print("job coount",job_count)
    
    
#     summary_file = "job_stats.json"

#     # Load existing summary file
#     if os.path.exists(summary_file) and os.path.getsize(summary_file) > 0:
#         with open(summary_file, "r") as f:
#             try:
#                 summary_data = json.load(f)
#             except json.JSONDecodeError:
#                 summary_data = {}
#     else:
#         summary_data = {}

#     # Ensure current component is in summary_data
#     if job_selected not in summary_data:
#         summary_data[job_selected] = {
#             "total_jobs": 0,
#             "ok_count": 0,
#             "fail_count": 0,
#             "last_update": None
#         }
    
#     summary_data[job_selected]["total_jobs"] += 1
    
    
    
#     for index, roi in enumerate(rois):
#         x_min, y_min = roi['x_min'], roi['y_min']
#         x_max, y_max = roi['x_max'], roi['y_max']

#         # draw vertical lines for boundaries
#         cv2.line(image, (x_min, 0), (x_min, img_height), (255, 0, 0), 3)
#         cv2.line(image, (x_max, 0), (x_max, img_height), (255, 0, 0), 3)

#         # Extract ROI from depth image
#         roi_depth = arr[y_min:y_max, x_min:x_max].copy()
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
#             print("[INFO] No filter applied")

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
        
#         roi_depth[(roi_depth < minrange) | (roi_depth > maxrange)] = 0
        
#         roi_non_zero = roi_depth[roi_depth != 0]
        
#         if roi_non_zero.size > 0:
#             region_key = f"Region_{index+1}_Tolernce"
#             region_dprange = float(config.get(region_key, dprange))  # fallback to global

#             min_coords = np.unravel_index(np.argmin(roi_non_zero), roi_depth.shape)
#             max_coords = np.unravel_index(np.argmax(roi_non_zero), roi_depth.shape)
#             min_point = (x_min + min_coords[1], y_min + min_coords[0])
#             max_point = (x_min + max_coords[1], y_min + max_coords[0])

#             roi_min = np.min(roi_non_zero)
#             roi_max = np.max(roi_non_zero)
#             roi_mi = roi_min - dprange
#             roi_range = roi_max - roi_min
#             # print(roi_range)
#             # print("first come")
#             lower_tolerance = region_dprange - tolerance
#             higher_tolerance = region_dprange + tolerance
#             # print("lower_tolerance", lower_tolerance)
#             # print("higher_tolerance", higher_tolerance)

#             # Check range against tolerance limits
#             if Correct_value < lower_tolerance or Correct_value > higher_tolerance:
#                 rect_color = (0, 0, 255)
#                 cv2.line(image, (x_min, 0), (x_min, img_height), (0, 0, 255), 3)
#                 cv2.line(image, (x_max, 0), (x_max, img_height), (0, 0, 255), 3)
#             else:
#                 rect_color = (0, 255, 0)
#                 cv2.line(image, (x_min, 0), (x_min, img_height), (0, 255, 0), 3)
#                 cv2.line(image, (x_max, 0), (x_max, img_height), (0, 255, 0), 3)
#                 pass_count += 1   
#             center_x = (x_min + x_max) // 2
#             center_y = (y_min + y_max) // 2
#             text = f"{Correct_value:.2f}"
#             text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
#             text_x = center_x - text_size[0] // 2
#             text_y = center_y + text_size[1] // 2
            
            
#             region_text = f"VALUE: {region_dprange:.2f}"
#             cv2.putText(image, region_text, (text_x- 25, text_y -  20),   # 15 pixels above
#                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
#             cv2.putText(image, text, (text_x, text_y),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, rect_color, 1, cv2.LINE_AA)

#             # Draw circles at min and max points
#             # cv2.circle(image, min_point, 5, (0, 255, 0), -1)
#             # cv2.circle(image, min_point, 2, (255, 255, 255), -1)
#             # cv2.circle(image, max_point, 5, (255, 0, 0), -1)
#             # cv2.circle(image, max_point, 2, (255, 255, 255), -1)
#             # stats = {
#             #     'name': roi['name'],
#             #     'min': float(roi_min),
#             #     'max': float(roi_max),
#             #     'range': float(roi_range),
#             #     'min_point': {'x': int(min_point[0]), 'y': int(min_point[1])},
#             #     'max_point': {'x': int(max_point[0]), 'y': int(max_point[1])}
#             # }
#             # roi_stats.append(stats)
#             # print("above")
#             current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            
#             stat = {
#                  'component':job_selected,
#                  'job': f"job{count_value}",
#                  'name': f"region{index+1}",
#                  'Value': float(Correct_value),
#                  'datetime': current_dt
#             }
            
#             Toler_value.append(stat)
#             message = json.dumps(stat) + "\n"   # <-- newline at end
#             client_socket.sendall(message.encode('utf-8'))
            
#             # print(f"{roi['name']} - Min: {roi_min:.2f}, Max: {roi_max:.2f}, Range: {roi_range:.2f}, Range: {roi_mi:.2f}")
#         else:
#             print(f"{roi['name']} - No valid depth values")
#     # --- after ROI loop ---
    
    
    
    
    
    
    
    
    
    
#     if pass_count == job_count:
#         result_msg = {"job": f"job{count_value}", "status": "OK"}
#         quality="pass"
#     else:
#         result_msg = {"job": f"job{count_value}", "status": "FAIL"}
#         quality="fail"
        
        
    

#     client_socket.sendall((json.dumps(result_msg) + "\n").encode('utf-8'))

#     # --- Save stats to CSV ---
#     start_csv = time.time()
#     wide_row = {
#         'component': job_selected,
#         'job': f"job{count_value}",
#         'status': result_msg['status'],        
#         'datetime': Toler_value[0]['datetime']
#     }
#     for stat in Toler_value:
#         region_name = stat['name']   # e.g. "region1"
#         wide_row[region_name] = stat['Value']
#     # print("come where ")
#     # ---- Save to CSV ----
#     today_date = datetime.now().strftime("%Y-%m-%d")
#     save_dir = r"C:\Apollo app"   # target folder

# # make sure folder exists
#     os.makedirs(save_dir, exist_ok=True)

#     csv_file = os.path.join(save_dir, f"{job_selected}_{today_date}.csv")

#     file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0
#     # collect fieldnames dynamically (component + all region names + status + datetime)
#     fieldnames = ['component', 'job'] + [f"region{i+1}" for i in range(len(Toler_value))] + ['status', 'datetime']

#     # write_header = not open(csv_file).read().strip()  # only write header if file is empty

#     with open(csv_file, mode='a', newline='') as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         if not file_exists:   # only write header if file is new
#             writer.writeheader()
#         writer.writerow(wide_row)

#     # print(f"CSV saved for job {count_value} with status {result_msg['status']}")
#     # print("csv save time", time.time() - start_csv)
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

   

#     # --- Save outputs ---
#     write_start=time.time()
#     cv2.imwrite("./static/captured/two/marked_outliers.png", image)
#     # print("end write",time.time()-write_start)
#     # cv2.imwrite("./static/captured/two/rotated_bounding_boxes.png", image)
#     # print("Processing time:", time.time() - start)
#     # with open("results_summary.json", "w") as f:
#     #     json.dump({
#     #         'roi_statistics': roi_stats,
#     #         'detected_objects': results
#     #     }, f, indent=4)

#     # return {
#     #     'roi_statistics': roi_stats,
#     #     'detected_objects': results
#     # }
    
#     return job_selected,quality

import json
import numpy as np
import cv2
import csv
import time
from datetime import datetime
import os 
from scipy.ndimage import median_filter, gaussian_filter
from django.conf import settings  # Add this import

def c_tire(count_value, client_socket, arr, value):
    # --- Use MEDIA_ROOT for all file paths ---
    media_root = settings.MEDIA_ROOT
    
    # --- Load job selection ---
    job_selection_path = os.path.join(media_root, "job_selection.json")
    with open(job_selection_path, "r") as f:
        job = json.load(f)
    
    value = int(value)   
    if value == 1:
        job_selected = "Component1"
    elif value == 2:
        job_selected = "Component2"
    elif value == 3:
        job_selected = "Component3"
    
    # --- Map job selection to correct files ---
    job_files = {
        "Component1": {
            "rect": "First_object.json",
            "depth": "First_depth_config.json"
        },
        "Component2": {
            "rect": "second_object.json",
            "depth": "second_depth_config.json"
        },
        "Component3": {
            "rect": "Third_object.json",
            "depth": "Third_depth_config.json"
        }
    }

    if job_selected not in job_files:
        raise ValueError(f"Unknown job selection: {job_selected}")

    # Use media_root for all file paths
    rec = os.path.join(media_root, job_files[job_selected]["rect"])
    depth_path = os.path.join(media_root, job_files[job_selected]["depth"])
    
    # --- Load rectangle coordinates ---
    with open(rec, 'r') as f:
        regions = json.load(f)
    
    # Create list of ROIs
    rois = []
    for rect_key in [
        'rectangle1','rectangle2','rectangle3','rectangle4','rectangle5',
        'rectangle6','rectangle7','rectangle8','rectangle9','rectangle10']:
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
    with open(depth_path, 'r') as f:
        config = json.load(f)
    
    y_pixel = float(config.get("y_pixel", 0.32))
    minrange = float(config.get("minrange", 100))
    maxrange = float(config.get("maxrange", 110))
    dprange = float(config.get("dprange", 105.0))
    filter_value = float(config.get("filter", 0.5))
    
    data = arr.copy()

    # --- Resolution ---
    x_resolution = 0.07805483  # mm/pixel
    y_resolution = y_pixel     # mm/pixel

    start = time.time()

    # --- Mask values outside valid range ---
    filtered_arr = np.where((arr > maxrange) | (arr < minrange), 0, arr)
    non_zero_values = filtered_arr[filtered_arr != 0]
    if non_zero_values.size > 0:
        min_val = np.min(non_zero_values)
    else:
        print("No values in range.")
        return []

    # --- Binary Threshold ---
    binary_image = np.where(data > dprange, 255, 0).astype(np.uint8)
    kernel = np.ones((3, 3), np.uint8)
    binary_cleaned = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=2)

    # --- Find contours ---
    contours, _ = cv2.findContours(binary_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # --- Load the RGB image from media root ---
    image_path = os.path.join(media_root, 'captured', 'two', 'ERL_refl.png')
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return []

    # Tolerance logic for dprange
    tolerance = filter_value
    lower_bound = dprange - tolerance
    upper_bound = dprange + tolerance

    # Process each ROI
    roi_stats = []
    Toler_value = []
    img_height, img_width = image.shape[:2]
    pass_count = 0   # ROIs that are within tolerance
    job_count = len(rois)  # total ROIs in the job
    
    # --- Use media_root for summary file ---
    summary_file = os.path.join(media_root, "job_stats.json")

    # Load existing summary file
    if os.path.exists(summary_file) and os.path.getsize(summary_file) > 0:
        with open(summary_file, "r") as f:
            try:
                summary_data = json.load(f)
            except json.JSONDecodeError:
                summary_data = {}
    else:
        summary_data = {}

    # Ensure current component is in summary_data
    if job_selected not in summary_data:
        summary_data[job_selected] = {
            "total_jobs": 0,
            "ok_count": 0,
            "fail_count": 0,
            "last_update": None
        }
    
    summary_data[job_selected]["total_jobs"] += 1
    
    for index, roi in enumerate(rois):
        x_min, y_min = roi['x_min'], roi['y_min']
        x_max, y_max = roi['x_max'], roi['y_max']

        # draw vertical lines for boundaries
        cv2.line(image, (x_min, 0), (x_min, img_height), (255, 0, 0), 3)
        cv2.line(image, (x_max, 0), (x_max, img_height), (255, 0, 0), 3)

        # Extract ROI from depth image
        roi_depth = arr[y_min:y_max, x_min:x_max].copy()
        depth_value = np.where((roi_depth == 0) | (np.isnan(roi_depth)) | (np.isinf(roi_depth)), np.nan, roi_depth)

        filter_type = "median"
        kernel_size = 5
        sigma = 1

        # Noise filtering
        if filter_type == "median":
            depth_filtered = median_filter(np.nan_to_num(depth_value), size=kernel_size)
        elif filter_type == "gaussian":
            depth_filtered = gaussian_filter(np.nan_to_num(depth_value), sigma=sigma)
        else:
            depth_filtered = depth_value

        # Find min & max
        min_val = np.nanmin(depth_filtered)
        max_val = np.nanmax(depth_filtered)
        
        min_coords = np.unravel_index(np.nanargmin(depth_filtered), depth_filtered.shape)
        max_coords = np.unravel_index(np.nanargmax(depth_filtered), depth_filtered.shape)

        Correct_value = max_val - min_val
        
        roi_depth[(roi_depth < minrange) | (roi_depth > maxrange)] = 0
        
        roi_non_zero = roi_depth[roi_depth != 0]
        
        if roi_non_zero.size > 0:
            region_key = f"Region_{index+1}_Tolernce"
            region_dprange = float(config.get(region_key, dprange))

            min_coords = np.unravel_index(np.argmin(roi_non_zero), roi_depth.shape)
            max_coords = np.unravel_index(np.argmax(roi_non_zero), roi_depth.shape)
            min_point = (x_min + min_coords[1], y_min + min_coords[0])
            max_point = (x_min + max_coords[1], y_min + max_coords[0])

            roi_min = np.min(roi_non_zero)
            roi_max = np.max(roi_non_zero)
            
            lower_tolerance = region_dprange - tolerance
            higher_tolerance = region_dprange + tolerance

            # Check range against tolerance limits
            if Correct_value < lower_tolerance or Correct_value > higher_tolerance:
                rect_color = (0, 0, 255)
                cv2.line(image, (x_min, 0), (x_min, img_height), (0, 0, 255), 3)
                cv2.line(image, (x_max, 0), (x_max, img_height), (0, 0, 255), 3)
            else:
                rect_color = (0, 255, 0)
                cv2.line(image, (x_min, 0), (x_min, img_height), (0, 255, 0), 3)
                cv2.line(image, (x_max, 0), (x_max, img_height), (0, 255, 0), 3)
                pass_count += 1   
                
            center_x = (x_min + x_max) // 2
            center_y = (y_min + y_max) // 2
            text = f"{Correct_value:.2f}"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            text_x = center_x - text_size[0] // 2
            text_y = center_y + text_size[1] // 2
            
            region_text = f"VALUE: {region_dprange:.2f}"
            cv2.putText(image, region_text, (text_x- 25, text_y -  20),
                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, text, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, rect_color, 1, cv2.LINE_AA)

            current_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            stat = {
                 'component': job_selected,
                 'job': f"job{count_value}",
                 'name': f"region{index+1}",
                 'Value': float(Correct_value),
                 'datetime': current_dt
            }
            
            Toler_value.append(stat)
            message = json.dumps(stat) + "\n"
            client_socket.sendall(message.encode('utf-8'))
        else:
            print(f"{roi['name']} - No valid depth values")
    
    # Determine result status
    if pass_count == job_count:
        result_msg = {"job": f"job{count_value}", "status": "OK"}
        quality = "pass"
        
        # Update summary data for OK
        summary_data[job_selected]["ok_count"] += 1
    else:
        result_msg = {"job": f"job{count_value}", "status": "FAIL"}
        quality = "fail"
        
        # Update summary data for FAIL
        summary_data[job_selected]["fail_count"] += 1

    # Update last update time
    summary_data[job_selected]["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save updated summary data
    with open(summary_file, "w") as f:
        json.dump(summary_data, f, indent=4)

    client_socket.sendall((json.dumps(result_msg) + "\n").encode('utf-8'))

    # --- Save stats to CSV ---
    wide_row = {
        'component': job_selected,
        'job': f"job{count_value}",
        'status': result_msg['status'],        
        'datetime': Toler_value[0]['datetime'] if Toler_value else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for stat in Toler_value:
        region_name = stat['name']
        wide_row[region_name] = stat['Value']
    
    # --- Use media_root for CSV storage ---
    today_date = datetime.now().strftime("%Y-%m-%d")
    save_dir = os.path.join(media_root, "reports")  # Save CSV in media_root/reports
    
    os.makedirs(save_dir, exist_ok=True)
    csv_file = os.path.join(save_dir, f"{job_selected}_{today_date}.csv")

    file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0
    fieldnames = ['component', 'job'] + [f"region{i+1}" for i in range(len(Toler_value))] + ['status', 'datetime']

    with open(csv_file, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(wide_row)

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

    # --- Save outputs to media root ---
    marked_outliers_path = os.path.join(media_root, 'captured', 'two', 'marked_outliers.png')
    os.makedirs(os.path.dirname(marked_outliers_path), exist_ok=True)
    cv2.imwrite(marked_outliers_path, image)

    return job_selected, quality