
from harvesters.core import Harvester
import numpy as np
from PIL import Image
import numpy as np
import socket
# from taiyer import tai
import json
# from continous_tire import c_tire
import time
import orjson
from Continuous_Tire import c_tire
import os
def wait_for_trigger(HOST, PORT):
    """Waits for a TCP client to send trigger value."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[INFO] Waiting for TCP trigger on {HOST}:{PORT} ...")
        conn, addr = s.accept()
        with conn:
            print(f"[INFO] Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                trigger_value = data.decode().strip()
                print(f"[INFO] Received trigger: {trigger_value}")
                # if trigger_value == "1":   # <-- condition to capture
                #     return True
                if trigger_value :   # <-- condition to capture
                    return trigger_value
    return False

# def sender_socket(sender_ip,sender_port):
#     try:
        
#         HOST = sender_ip
#         PORT = int(sender_port)
        
#         # Create a socket object
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect((HOST, PORT))
#         print("connect the socket communication")
#     except:
#         print("TCP IP is not connected ")
#     return client_socket

# try:

# except:
#     print("Harvest is not connected")
    

OUTPUT_FOLDER = "./"
BASE_FILE_NAME = "ERL"

stop_harvester = False
# # ocr = PaddleOCR(use_angle_cls=True, lang='en')

def stop_harvester_loop():
    global stop_harvester
    stop_harvester = True

def save_range_image_to_disk(component, file_name):
    if component.data_format == 'Coord3D_C16':
        range_data = component.data.astype(np.float32)
        range_image = Image.fromarray(range_data, 'F')  # Convert to float image
        converted_range_image = range_image.convert('L')
        converted_range_image.save(f"{OUTPUT_FOLDER}\\{file_name}")
        # print(f"Saved range image to {OUTPUT_FOLDER}\\{file_name}")
    else:
        raise Exception(f"Cannot save range image to file {file_name} due to bad data format {component.data_format}")

def save_image_to_disk(component, file_name):
    if component.data_format == 'Mono8':
        # y_mm_per_pixel=3
        img_buffer = component.data.reshape(component.height, component.width)
        # img = Image.fromarray(img_buffer, mode="L")
        
        img = Image.fromarray(img_buffer).convert("L")
        img_buffer = img.resize((component.width, component.height), Image.NEAREST)  # Resize if needed
        # img_buffer.save(f"{OUTPUT_FOLDER}/{file_name}")
        output_path = os.path.join(OUTPUT_FOLDER, file_name)

        # Delete if file already exists
        if os.path.exists(output_path):
            os.remove(output_path)

        # Save new file
        img_buffer.save(output_path)
        
        # new_height = int(component.height * y_mm_per_pixel)
        
        # # Resize only in Y-direction (height)
        # stretched_img = img.resize((component.width, new_height), Image.NEAREST)
        
        # stretched_img.save(f"{OUTPUT_FOLDER}/{file_name}")
        
# def save_image_to_disk(component, file_name,pulses_per_mm):
   
#     if component.data_format == 'Mono8':
#        img_buffer = component.data.reshape(component.height, component.width)
#        height_factor=(pulses_per_mm)
#        y_resolution_factor=int(component.height*height_factor)
#     #    print(len(y_resolution_factor))
#     #    print("New Y Resolution:", y_resolution_factor)
#        img = Image.fromarray(img_buffer, mode="L")
#        img_buffer = img.resize((component.width,y_resolution_factor), Image.NEAREST)
#        img_buffer.save(f"{OUTPUT_FOLDER}/{file_name}")

def main(Frame,stopMode,exposureTime,threshold,advance,profilePerImage,RisingEdge,timedRate,encoderResolution,pulsePerProfile,triggerType,encoder_mode,trigger_mode,sender_ip,sender_port,receiver_ip,receiver_port):
    try:
        h = Harvester()
        cti_file = "SICKGigEVisionTL.cti"
        h.add_file(cti_file)
        h.update()
        # print(h.device_info_list)
        ia = h.create(0)
        # Acuqa_mode = "Continuous"
        # print("start harvest")
        node_map = ia.remote_device.node_map
        node_map.AcquisitionMode.value = Frame
        node_map.DeviceScanType.value = 'Linescan3D'
        node_map.AcquisitionLineRate.value =timedRate#2000
        node_map.RegionSelector.value = 'Scan3dExtraction1'
        node_map.Height.value =profilePerImage#380
        node_map.RegionSelector.value = 'Region1'
        node_map.ExposureTime.value = exposureTime#100
        node_map.DetectionThreshold.value = threshold#50
        node_map.AcquisitionStopMode.value = stopMode
        
        # if Trigger=="Free_Running/External_Trigger":
        #     ex_on='On'
        #     en_off="Off"
        #     pulses_per_mm=float(y_value)
        node_map.TriggerSelector.value = 'FrameStart'
        # print(type(trigger_mode))
        node_map.TriggerMode.value = trigger_mode
        #RisingEdge
        #LevelHigh
        node_map.TriggerActivation.value = RisingEdge
        
        # node_map.TriggerSelector.value = 'LineStart'
        # # node_map.TriggerMode.value = en_off
        # EncoderDivider=1
        # node_map.EncoderDivider.value = EncoderDivider  # Set Encoder Divider
        # node_map.EncoderMode.value = "FourPhase"  # Now enable FourPhase
        # node_map.TriggerSource.value='Encoder'
        # EncoderResolution=float(y_value)
        # node_map.EncoderResolution.value=encoderResolution
       
        # if Trigger=="External_Trigger/Encoder":
        #     ex_on='On'
        #     en_off="On"
        # pulses_per_mm=(EncoderDivider*encoderResolution/0.1)
        # pulses_per_mm=EncoderResolution
        
        #PositionUP
        #positionDown
        #DirectionUP
        #DirectionDown
        #Motion
        # node_map.EncoderOutputMode.value='triggerType'
        #PositionUP
        #positionDown
        #DirectionUP
        #DirectionDown
        #Motion
        # print("pulses_per_mm",pulses_per_mm)
        # PresetMedium
        # PresetSoft
        # PresetAggressive
        # print(advance)
        node_map.MultiSlopeMode.value=advance
        # print("check")
        node_map.MultiSlopeKneePointCount.value=1
        global stop_harvester
        if Frame=="SingleFrame":
            # print("start Acquisition")
            ia.start()
            try:
                #   if wait_for_trigger():
                    buffer = ia.fetch()
                    payload = buffer.payload
                    component = payload.components[0]
                    # data_format = component.data_format
                    component_1 = payload.components[1]
                    width = component.width
                    height = component.height
                    cordord16 = component.data.reshape(height,width)
                    # np.save("raw_data.npy", cordord16)
                    mono8= component_1.data.reshape(height,width)
                    mono8 = mono8.astype(np.uint8)
                    # np.save("2d_grayscale.npy", mono8)
                    # np.savetxt("2d_grayscale.txt", mono8, fmt="%d")
                    cordord16 = cordord16.astype(np.float32)
                    arr = cordord16 * 0.002399454 + 39.67811
                    # arr = cordord16 * 0.007099454 + 39.67811
                    # arr = cordord16 * 0.0625
                    arr[arr == 39.67811] = 0
                    # np.savez_compressed("./static/cordord16.npz", data=arr)
                    filename = "raw_data.npy"

                    # Delete old file if it exists
                    if os.path.exists(filename):
                        os.remove(filename)

                    # Save new array
                    np.save(filename, arr)
                    # print("tai")
                    # tai(arr)
                    # value=tai(arr)
                    # s.sendall(str(value).encode())
                    
    
                    # Load depth data from a .npy file (replace with your file path)
                    # depth_map = np.load("bun_depth.npy")  # shape should be (500, 500)
                    # np.save("./static/data.npy", arr)10
                    cordord16_list = arr.tolist()


                    # # Save to JSON file\
                    
                    # np.savetxt("data.txt", arr, fmt="%.6f")
                    # C:\ocr_vision\cable_project\static\captured\mes\image_refl2.png   
                    save_image_to_disk(buffer.payload.components[1], "./static/captured/two/ERL_refl - Copy.png")
                    # save_range_image_to_disk(buffer.payload.components[0], f"{BASE_FILE_NAME}_range_image.png")
                    
                    # print("image saved")
                    # h.reset()
                    # ia.stop()
                    # ia.destroy()
                    # h.reset()
                    start = time.time()
                    # with open("./static/cordord16.json", "w") as f:
                    #     json.dump(cordord16_list, f)
                    # # print("json going")
                    # print(f"orjson: {time.time() - start:.2f} seconds")
                    # start = time.time()
                    file_path = "./static/cordord18.json"
                    # delete if already exists
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    if os.path.exists(file_path):
                        os.remove(file_path)

                    with open(file_path, "wb") as f:
                        f.write(orjson.dumps(cordord16_list))

                    # print(f"orjson: {time.time() - start:.2f} seconds")
                    buffer.queue()
                    # return cordord16_list
            except:
                ia.stop()
                ia.destroy()
                h.reset()   
            finally :
                # s.close()
                ia.stop()
                ia.destroy()
                h.reset()
        if Frame=="Continuous":
            # sender_socket(sender_ip,sender_port)
            try:
                # if wait_for_trigger:
                value =wait_for_trigger(receiver_ip,int(receiver_port))
            except:
                # print("wrong Data")
                h.reset()
            
            try:
        
                HOST = sender_ip
                PORT = int(sender_port)
                
                # Create a socket object
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((HOST, PORT))
                print("connect the socket communication")
            except:
                h.reset()
                print("TCP IP is not connected ")
            print("start Continuous Acquisition")
            summary_file = "job_summary.json"

            if os.path.exists(summary_file):
                os.remove(summary_file)

            job_summary = {}
            ia.start()
            try:
                frame_count = 0
                while not stop_harvester:
                # while True:
                    # print("enter")
                    buffer = ia.fetch()
                    payload = buffer.payload
                    component = payload.components[0]
                    # data_format = component.data_format
                    component_1 = payload.components[1]
                    width = component.width
                    height = component.height
                    cordord16 = component.data.reshape(height,width)
                    
                    # np.save("raw_data.npy", cordord16)
                    mono8= component_1.data.reshape(height,width)
                    
                    mono8 = mono8.astype(np.uint8)
                    # np.save("2d_grayscale.npy", mono8)
                    # np.savetxt("2d_grayscale.txt", mono8, fmt="%d")
                    
                    cordord16 = cordord16.astype(np.float32)
                    
                    arr = cordord16 * 0.002399454 + 39.67811
                    arr[arr == 39.67811] = 0
                    # np.save("raw_data.npy", arr)
                    # print("tai")
                    # c_tire(arr,client_socket)
    
                    # Load depth data from a .npy file (replace with your file path)
                    # depth_map = np.load("bun_depth.npy")  # shape should be (500, 500)
                    
                    
                    
                    # np.save("./static/data.npy", arr)
                    # cordord16_list = arr.tolist()
                    

                    # # Save to JSON file
                    
                    # with open("./static/cordord16.json", "w") as f:
                    #     json.dump(cordord16_list, f)
                    # np.savetxt("data.txt", arr, fmt="%.6f")
                    # C:\ocr_vision\cable_project\static\captured\mes\image_refl2.png   
                    save_image_to_disk(buffer.payload.components[1], "./static/captured/two/ERL_refl - Copy.png")
                    buffer.queue()
                    # print("end process")
                    # address=sender_socket()
                    # start=time.time()
                    job_selected,quality=c_tire(frame_count,client_socket,arr,value)
                    # print(time.time()-start)
                    frame_count += 1
                    # ---------------- JSON update directly here ----------------
                    if job_selected not in job_summary:
                        job_summary[job_selected] = {"JobCount": 0, "OK": 0, "FAIL": 0}

                    # Increment total jobs
                    job_summary[job_selected]["JobCount"] += 1

                    # Increment OK / FAIL counts
                    if quality == "pass":
                        job_summary[job_selected]["OK"] += 1
                        # print("ok")
                    elif quality == "fail":
                        job_summary[job_selected]["FAIL"] += 1
                        # print("fail")

                    # -------- Save JSON after each update in required format --------
                    with open(summary_file, "w") as f:
                        latest_summary = {
                            "Component": job_selected,
                            "JobCount": job_summary[job_selected]["JobCount"],
                            "OK": job_summary[job_selected]["OK"],
                            "FAIL": job_summary[job_selected]["FAIL"]
                        }
                        json.dump(latest_summary, f, indent=4)
                                
            except:
                stop_harvester = False 
                ia.stop()
                ia.destroy()
                h.reset()
            finally:
                # ia.stop()
                # ia.destroy()
                # h.reset() 
                ia.destroy()
                ia.stop()
                h.reset() 
                stop_harvester = False              
                # print("properly work")
              
        # if Frame=="Continuous":
            # ocr = PaddleOCR(use_angle_cls=True, lang='en')
            # print("please connect TCP/IP client")
            # host = '127.0.0.1'
            # port = 6543
            # s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            # s.bind((host, port))
            # s.listen()
            # print(f"Server started and listening on {host}:{port}")  
            # conn, addr = s.accept()
            # print("Now start the Acquisition")
            # ia.start()
        
            # try:
            #     while not stop_harvester:      
                    
            #         buffer = ia.fetch()
            #         payload = buffer.payload
            #         component = payload.components[0]
            #         # data_format = component.data_format
            #         component_1 = payload.components[1]
            #         width = component.width
            #         height = component.height
            #         cordord16 = component.data.reshape(height,width)
            #         mono8= component_1.data.reshape(height,width)
                    
            #         mono8 = mono8.astype(np.uint8)
            #         np.save("2d_grayscale.npy", mono8)
            #         # np.savetxt("2d_grayscale.txt", mono8, fmt="%d")                    
            #         cordord16 = cordord16.astype(np.float32)
            #         arr = cordord16 * 0.002399454 + 39.67811
            #         arr[arr == 39.67811] = 0
            #         np.save("data.npy", arr)
            #         # np.savetxt("data.txt", arr, fmt="%.6f")
            #         # img_save=time.time()
            #         save_image_to_disk(buffer.payload.components[1], "./static/captured/ERL_refl.png")
            #         # print("image_save_time",time.time()-img_save)
            #         # C:\ocr_vision\cable_project\static\captured\mes\ERL_refl.png
            #         # total_time=time.time()
                    
            # if stop_harvester:
            #     ia.stop()
                # ia.destroy()
                # h.reset()    
                # buffer.queue()
    finally :
        ia.stop()
        ia.destroy()
        h.reset()
        # print("Aquasition Finish")
            
# def stop_harvester_loop():
#     global stop_harvester
#     stop_harvester = True
# if __name__ == "__main__":
#     main()