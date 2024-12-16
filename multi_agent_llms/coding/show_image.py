# filename: show_image.py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load and display the image
img = mpimg.imread('stock_price.png')
plt.imshow(img)
plt.axis('off')  # Turn off axes
plt.show()