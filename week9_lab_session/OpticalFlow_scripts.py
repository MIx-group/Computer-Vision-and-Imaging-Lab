#Step 1 We'll start by importing NumPy and OpenCV.
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def generate_hsv_color_matrix(size=300):
    """Generates a synthetic image visualizing the HSV color mapping."""
    
    # 1. Create a coordinate grid (U, V) where the center is (0, 0)
    # The grid ranges from -size/2 to +size/2
    X, Y = np.meshgrid(np.arange(size), np.arange(size))
    U = X - size / 2.0
    V = Y - size / 2.0
    
    # 2. Calculate Angle (Hue) and Magnitude (Value)
    # The functions cv.cartToPolar and cv.normalize are the same ones used in your flow code.
    mag, ang = cv.cartToPolar(U.astype(np.float32), V.astype(np.float32))
    
    # 3. Create the HSV image
    hsv = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Hue: Map the angle (0 to 2*pi) to 0-180 (OpenCV's standard Hue range)
    # Formula: ang * 180 / np.pi / 2
    hsv[..., 0] = (ang * 90 / np.pi).astype(np.uint8) 
    
    # Saturation: Set to full saturation (255)
    hsv[..., 1] = 255
    
    # Value: Map the magnitude (speed) to brightness (Value channel)
    # The center is darkest (zero magnitude), edges are brightest (max magnitude)
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)

    # 4. Convert to RGB for Matplotlib display
    return cv.cvtColor(hsv, cv.COLOR_HSV2RGB)


# Step 2: Capture video
cap = cv.VideoCapture(cv.samples.findFile("walking.mp4"))
# Step 2.1: showing the HSV colour matrix
color_matrix = generate_hsv_color_matrix(size=300)

plt.figure(figsize=(6, 6))
plt.imshow(color_matrix)
plt.title("HSV Color Matrix (Optical Flow Mapping)")
plt.xlabel("Direction (Hue)")
plt.ylabel("Speed (Brightness/Value)")
plt.axis('off')
plt.show()

# Step 3: Read the first frame and initialize variables
ret, frame1 = cap.read()
prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[..., 1] = 255



# Step 4: Process frames to calculate optical flow
while(1):
    ret, frame2 = cap.read()
    if not ret:
        cv.destroyAllWindows()
        print('No frames grabbed!')
        break

    next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
    
    # Visualize the flow
    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    
    # Display the frame
    cv.imshow('frame2', bgr)
    # Step 5: Handle key events
    k = cv.waitKey(30) & 0xff
    if k == 27:  # Esc key
        break
    elif k == ord('s'):  # 's' key to save frames
        cv.imwrite('opticalfb.png', frame2)
        cv.imwrite('opticalhsv.png', bgr)

    prvs = next  # Update previous frame

# Cleanup
cv.destroyAllWindows()



