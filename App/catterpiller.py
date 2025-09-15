# import numpy as np
# from PIL import Image

# # Load data
# data = np.load('./media/raw_data.npy')

# # Create binary mask
# mask = (data >= 145) & (data <= 152)
# binary_image = mask.astype(np.uint8) * 255

# # Save as image
# Image.fromarray(binary_image).save('mask_result.png')
import cv2
import numpy as np
import matplotlib.pyplot as plt 

# Load image (grayscale)
img = cv2.imread("mask_result.png", cv2.IMREAD_GRAYSCALE)

# Apply Gaussian blur (helps circle detection)
kernel = np.ones((5,5), np.uint8)

# Apply erosion (remove small white noise)
_, binary = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
eroded = cv2.erode(binary, kernel, iterations=1)

# Apply dilation (restore circle size, smooth edges)
dilated = cv2.dilate(eroded, kernel, iterations=2)

blurred = cv2.GaussianBlur(dilated, (9, 9), 2)

# Detect circles using Hough Transform
circles = cv2.HoughCircles(
    blurred, 
    cv2.HOUGH_GRADIENT, 
    dp=1, 
    minDist=30,     # minimum distance between circles
    param1=150,     # edge detection threshold
    param2=30,      # lower -> more false circles, higher -> stricter
    minRadius=10,   # minimum radius
    maxRadius=200   # maximum radius
)

# Convert original to color for visualization
output = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for (x, y, r) in circles[0, :]:
        # Draw the circle outline
        cv2.circle(output, (x, y), r, (0, 255, 0), 5)
        # Draw the center
        cv2.circle(output, (x, y), 3, (0, 0, 255), -1)
        print(f"Circle center: ({x}, {y}), radius: {r}")

# Show results
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.title("Original")
plt.imshow(img, cmap="gray")
plt.axis("off")

plt.subplot(1,2,2)
plt.title("Detected Circles")
plt.imshow(output)
plt.axis("off")

plt.show()

