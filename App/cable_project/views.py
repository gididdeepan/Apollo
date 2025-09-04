# from django.shortcuts import render
# from harvest import main
# from django.http import JsonResponse
# import json
# from harvest import stop_harvester_loop
# from django.views.decorators.csrf import csrf_exempt
# from  Continuous_Tire import c_tire
# from django.views.decorators.http import require_http_methods
# from single_tire import s_tire
# import socket 
# from mac_id import c

# import os 
# from django.utils.timezone import now
# # try:
    
# #     HOST = '127.0.0.1'
# #     PORT = 6543

# #     # Create a socket object
# #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     client_socket.connect((HOST, PORT))
# #     print("connect the socket communication")
# # except:
# #     print("TCP IP is not connected ")

# @csrf_exempt
# def login(request):
#     # mac=c()
#     mac=27772739667
#     # print(mac)
#     return render(request,"login.html",{"mac_address":mac})

# def start_process(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Only POST requests allowed"}, status=405)

#     try:
        
#         data = json.loads(request.body)
#         # print("Received data:", data)
#         Frame=data.get('acquisitionMode')
#         stopMode=data.get('stopMode')
#         exposureTime=data.get('exposureTime')
#         threshold=data.get('threshold')
#         advance=data.get('advance')
#         profilePerImage=data.get('profilePerImage')
#         RisingEdge=data.get('External_trigger')
#         timedRate=data.get('timedRate')
#         encoderResolution=data.get('encoderResolution')
#         pulsePerProfile=data.get('pulsePerProfile')
#         triggerType=data.get('triggerType')
#         encoder_mode = data.get('encoderMode', 'OFF')
#         trigger_mode = data.get('triggerMode', 'OFF')
#         # print(f"Encoder Mode: {encoder_mode}")  # Will print "ON" or "OFF"
#         # print(f"Trigger Mode: {trigger_mode}")  # Will print "ON" or "OFF"
#         component = data.get("job_component")  # <-- Component value
#         # with open("job_selection.json", "w") as f:
#         #     json.dump({"job_selection": component}, f, indent=4)
#         # print(component)
#         receiver_ip = data.get("receiver_ip")
#         receiver_port = data.get("receiver_port")
#         sender_ip = data.get("sender_ip")
#         sender_port = data.get("sender_port")

#         # Print/log to check
#         print("Receiver IP:", receiver_ip, "Port:", receiver_port)
#         print("Sender IP:", sender_ip, "Port:", sender_port)
#         print(Frame,stopMode,exposureTime,threshold,advance,profilePerImage,RisingEdge,
#                  timedRate,encoderResolution,pulsePerProfile,triggerType,encoder_mode,trigger_mode,sender_ip,sender_port,receiver_ip,receiver_port)
#         try:
#             # print("process")
#             # main(**params)
            
#             main(Frame,stopMode,exposureTime,threshold,advance,profilePerImage,RisingEdge,
#                  timedRate,encoderResolution,pulsePerProfile,triggerType,encoder_mode,trigger_mode,sender_ip,sender_port,receiver_ip,receiver_port)
#             # while True:
#             # for i in range(10):
#             #     print("it come")
#             #     c_tire(i,client_socket)
#                 # s_tire()
#             # send shutdown signal
#             # client_socket.sendall(b"QUIT\n")
            

#             # close the client connection
#             # client_socket.close()
#             return JsonResponse({
#                 "status": "success", 
#                 "message": "Capture completed successfully"
#             })
#         except TimeoutError as e:  # Using built-in TimeoutError
#             return JsonResponse({
#                 "status": "error",
#                 "message": "Camera timeout - check connection",
#                 "error_code": "CAMERA_TIMEOUT"
#             }, status=408)
            
#         except IOError as e:  # For connection/device errors
#             return JsonResponse({
#                 "status": "error",
#                 "message": "Camera not connected or in use",
#                 "error_code": "CAMERA_NOT_FOUND"
#             }, status=503)
            
#         except Exception as e:
#             print(f"Acquisition error: {str(e)}")
#             return JsonResponse({
#                 "status": "error",
#                 "message": "Capture failed",
#                 "error_code": "CAPTURE_FAILED"
#             }, status=500)

#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON data"}, status=400)
#     except (KeyError, ValueError, TypeError) as e:
#         return JsonResponse({"error": f"Invalid parameter: {str(e)}"}, status=400)


# def stop_process(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         global stop_harvester
#         if data.get('message') == 'stop':
#             print("Stop command received")
#             # Your logic to stop the process goes here
#             stop_harvester_loop()
#             return JsonResponse({'status': 'stopped'})
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# def home(request):
  
#     return render(request, 'base.html')

# def page(request): 
#     return render(request, 'page.html')
# def viewer(request):
#     return render(request, 'viewer.html')
# @csrf_exempt
# @require_http_methods(["POST"])  # Only allow POST requests
# def save_corners(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # print(data)
            
#             selected_component = data.get("component")
#             # print("Selected Component:", selected_component)  # You’ll see this in your console
#             rectangle1 = data.get('rectangle1')
#             rectangle2 = data.get('rectangle2')
#             rectangle3 = data.get('rectangle3')
#             rectangle4 = data.get('rectangle4')
#             rectangle5 = data.get('rectangle5')
#             rectangle6 =  data.get('rectangle6')
#             rectangle7 =  data.get('rectangle7')
#             rectangle8 =  data.get('rectangle8')
#             rectangle9 =  data.get('rectangle9')
#             rectangle10 =  data.get('rectangle10')
#             # print(rectangle3)
#             # Validate data (example)
#             if not rectangle1 and not rectangle2 and not rectangle3 and not rectangle4 and not rectangle5 and not rectangle6 and not rectangle7 and not rectangle8 and not rectangle9 and not rectangle10:
#                 return JsonResponse(
#                     {"status": "error", "message": "No rectangles provided"},
#                     status=400
#                 )
            
#             # Process data (example)
#             # if rectangle1:
#             #     print("Rectangle 1:", rectangle1)
#             # if rectangle2:
#             #     print("Rectangle 2:", rectangle2)
            
#             # Process corners
#             # corners = data.get('corners', {})
#             # print("here")
            
#             rectangle_data = {
#                  'rectangle1': rectangle1,
#                  'rectangle2': rectangle2,
#                 'rectangle3': rectangle3,
#                 'rectangle4': rectangle4,
#                 'rectangle5' : rectangle5,
#                 'rectangle6':rectangle6,
#                 'rectangle7':rectangle7,
#                  'rectangle8':rectangle8,
#                  'rectangle9':rectangle9,
#                  'rectangle10':rectangle10,
#             }
#             # print("below")
#             # Process depth config
  
#             # Process tire filters (default to False if not provided)
#             depth_config = data.get('depth_config', {})
#             if selected_component=="job1":
               
#                 with open('First_object.json', 'w') as f:
#                     json.dump(rectangle_data, f, indent=4)    
                    
#                 with open('First_depth_config.json', 'w') as f:
#                     json.dump(depth_config, f, indent=4)
                
                
#             elif selected_component=="job2":
#                 with open('second_object.json', 'w') as f:
#                     json.dump(rectangle_data, f, indent=4)
#                 with open('second_depth_config.json', 'w') as f:
#                     json.dump(depth_config, f, indent=4)
                    
#             elif selected_component=="job3":
                
#                 with open('Third_object.json', 'w') as f:
#                     json.dump(rectangle_data, f, indent=4)
                
#                 with open('Third_depth_config.json', 'w') as f:
#                     json.dump(depth_config, f, indent=4)
#             # 2. Save Depth Config
#             with open('rectangle_coordinates.json', 'w') as f:
#                 json.dump(rectangle_data, f, indent=4)  
#             # depth_config = data.get('depth_config', {})
#             with open('depth_config.json', 'w') as f:
#                 json.dump(depth_config, f, indent=4)
#             # print("done")
#             results = s_tire()
#             # Here you would typically save to database or process the data
#             # print("Received data:", {
#             #     # 'corners': corners,
#             #     'depth_config': depth_config,
#             #     # 'tire_filters': tire_filters
#             # })
#             # return JsonResponse({"status": "success"})
#             range_values = {}
#             for i, rect in enumerate(results.get('roi_statistics', [])):
#                 range_values[f'rectangle{i+1}'] = {
#                     'range': rect['range']  # Only send range value
#                 }
            
#             return JsonResponse({
#                 'status': 'success',
#                 'range_values': range_values,
#                 'processing_time': results.get('processing_time', 0)
#             })
            
#         except json.JSONDecodeError:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': 'Invalid JSON data'
#             }, status=400)
#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': str(e)
#             }, status=400)
    
#     return JsonResponse({
#         'status': 'error',
#         'message': 'Only POST requests are allowed'
#     }, status=405)
    



# def monitor_view(request):
#     return render(request, "monitor.html")

# def job_summary_api(request):
#     summary_file = "job_summary.json"
#     job_summary = {}

#     if os.path.exists(summary_file):
#         with open(summary_file, "r") as f:
#             job_summary = json.load(f)

#     return JsonResponse({
#         "job_summary": job_summary,
#         "live_time": now().strftime("%Y-%m-%d %H:%M:%S")  
#     })


from django.shortcuts import render
from harvest import main
from django.http import JsonResponse
import json
from harvest import stop_harvester_loop
from django.views.decorators.csrf import csrf_exempt
from Continuous_Tire import c_tire
from django.views.decorators.http import require_http_methods
from single_tire import s_tire
import socket 
from mac_id import c
import os 
from django.conf import settings
from django.utils.timezone import now

@csrf_exempt
def login(request):
    try:
        mac = c()  # your function to get camera/mac
        if not mac:  # if function returns None or empty
            raise ValueError("No MAC found")
        return render(request, "login.html", {"mac_address": mac})
    except Exception as e:
        # Instead of breaking, show error message
        return render(request, "login.html", {"error": "Camera is not connected"})

def start_process(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)

    try:
        data = json.loads(request.body)
        Frame = data.get('acquisitionMode')
        stopMode = data.get('stopMode')
        exposureTime = data.get('exposureTime')
        threshold = data.get('threshold')
        advance = data.get('advance')
        profilePerImage = data.get('profilePerImage')
        RisingEdge = data.get('External_trigger')
        timedRate = data.get('timedRate')
        encoderResolution = data.get('encoderResolution')
        pulsePerProfile = data.get('pulsePerProfile')
        triggerType = data.get('triggerType')
        encoder_mode = data.get('encoderMode', 'OFF')
        trigger_mode = data.get('triggerMode', 'OFF')
        
        component = data.get("job_component")
        
        # FIXED: Use proper file paths with MEDIA_ROOT
        # job_file_path = os.path.join(settings.MEDIA_ROOT, "job_selection.json")
        # os.makedirs(os.path.dirname(job_file_path), exist_ok=True)
        
        # with open(job_file_path, "w") as f:
        #     json.dump({"job_selection": component}, f, indent=4)
        
        receiver_ip = data.get("receiver_ip")
        receiver_port = data.get("receiver_port")
        sender_ip = data.get("sender_ip")
        sender_port = data.get("sender_port")

        print("Receiver IP:", receiver_ip, "Port:", receiver_port)
        print("Sender IP:", sender_ip, "Port:", sender_port)
        
        try:
            main(Frame, stopMode, exposureTime, threshold, advance, profilePerImage, RisingEdge,
                 timedRate, encoderResolution, pulsePerProfile, triggerType, encoder_mode, 
                 trigger_mode, sender_ip, sender_port, receiver_ip, receiver_port)
            
            return JsonResponse({
                "status": "success", 
                "message": "Capture completed successfully"
            })
        except TimeoutError as e:
            return JsonResponse({
                "status": "error",
                "message": "Camera timeout - check connection",
                "error_code": "CAMERA_TIMEOUT"
            }, status=408)
        except IOError as e:
            return JsonResponse({
                "status": "error",
                "message": "Camera not connected or in use",
                "error_code": "CAMERA_NOT_FOUND"
            }, status=503)
        except Exception as e:
            print(f"Acquisition error: {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": "Capture failed",
                "error_code": "CAPTURE_FAILED"
            }, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except (KeyError, ValueError, TypeError) as e:
        return JsonResponse({"error": f"Invalid parameter: {str(e)}"}, status=400)

def stop_process(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        global stop_harvester
        if data.get('message') == 'stop':
            print("Stop command received")
            stop_harvester_loop()
            return JsonResponse({'status': 'stopped'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def home(request):
    return render(request, 'base.html')

def page(request): 
    return render(request, 'page.html')

def viewer(request):
    return render(request, 'viewer.html')

@csrf_exempt
@require_http_methods(["POST"])
def save_corners(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_component = data.get("component")
            
            rectangle1 = data.get('rectangle1')
            rectangle2 = data.get('rectangle2')
            rectangle3 = data.get('rectangle3')
            rectangle4 = data.get('rectangle4')
            rectangle5 = data.get('rectangle5')
            rectangle6 = data.get('rectangle6')
            rectangle7 = data.get('rectangle7')
            rectangle8 = data.get('rectangle8')
            rectangle9 = data.get('rectangle9')
            rectangle10 = data.get('rectangle10')
            
            if not any([rectangle1, rectangle2, rectangle3, rectangle4, rectangle5, 
                       rectangle6, rectangle7, rectangle8, rectangle9, rectangle10]):
                return JsonResponse(
                    {"status": "error", "message": "No rectangles provided"},
                    status=400
                )
            
            rectangle_data = {
                'rectangle1': rectangle1,
                'rectangle2': rectangle2,
                'rectangle3': rectangle3,
                'rectangle4': rectangle4,
                'rectangle5': rectangle5,
                'rectangle6': rectangle6,
                'rectangle7': rectangle7,
                'rectangle8': rectangle8,
                'rectangle9': rectangle9,
                'rectangle10': rectangle10,
            }
            
            depth_config = data.get('depth_config', {})
            
            # FIXED: Use proper file paths
            media_root = settings.MEDIA_ROOT
            
            if selected_component == "job1":
                first_obj_path = os.path.join(media_root, 'First_object.json')
                first_depth_path = os.path.join(media_root, 'First_depth_config.json')
                
                os.makedirs(os.path.dirname(first_obj_path), exist_ok=True)
                with open(first_obj_path, 'w') as f:
                    json.dump(rectangle_data, f, indent=4)
                with open(first_depth_path, 'w') as f:
                    json.dump(depth_config, f, indent=4)
                
            elif selected_component == "job2":
                second_obj_path = os.path.join(media_root, 'second_object.json')
                second_depth_path = os.path.join(media_root, 'second_depth_config.json')
                
                os.makedirs(os.path.dirname(second_obj_path), exist_ok=True)
                with open(second_obj_path, 'w') as f:
                    json.dump(rectangle_data, f, indent=4)
                with open(second_depth_path, 'w') as f:
                    json.dump(depth_config, f, indent=4)
                
            elif selected_component == "job3":
                third_obj_path = os.path.join(media_root, 'Third_object.json')
                third_depth_path = os.path.join(media_root, 'Third_depth_config.json')
                
                os.makedirs(os.path.dirname(third_obj_path), exist_ok=True)
                with open(third_obj_path, 'w') as f:
                    json.dump(rectangle_data, f, indent=4)
                with open(third_depth_path, 'w') as f:
                    json.dump(depth_config, f, indent=4)
            
            # Save general files
            rect_coords_path = os.path.join(media_root, 'rectangle_coordinates.json')
            depth_config_path = os.path.join(media_root, 'depth_config.json')
            
            os.makedirs(os.path.dirname(rect_coords_path), exist_ok=True)
            with open(rect_coords_path, 'w') as f:
                json.dump(rectangle_data, f, indent=4)
            with open(depth_config_path, 'w') as f:
                json.dump(depth_config, f, indent=4)
            print("go to single tire")
            
            results = s_tire()
            # print("succesfullly")
            range_values = {}
            for i, rect in enumerate(results.get('roi_statistics', [])):
                range_values[f'rectangle{i+1}'] = {
                    'range': rect['range']
                }
            
            return JsonResponse({
                'status': 'success',
                'range_values': range_values,
                'processing_time': results.get('processing_time', 0)
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST requests are allowed'
    }, status=405)

def monitor_view(request):
    return render(request, "monitor.html")

def job_summary_api(request):
    
    summary_file = os.path.join(settings.MEDIA_ROOT, "job_summary.json")
    job_summary = {
        "Component": "N/A",
        "JobCount": 0,
        "OK": 0,
        "FAIL": 0
    }

    if os.path.exists(summary_file):
        try:
            with open(summary_file, "r") as f:
                loaded_data = json.load(f)
                # Merge with default values to ensure all keys exist
                job_summary.update(loaded_data)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in job_summary.json")
        except Exception as e:
            print(f"Error reading job_summary.json: {e}")
    
    return JsonResponse({
        "job_summary": job_summary,
        "live_time": now().strftime("%Y-%m-%d %H:%M:%S")  
    })