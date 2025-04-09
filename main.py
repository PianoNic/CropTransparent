from PIL import Image
import numpy as np

def crop_transparent(input_path, output_path):
    # Open the image
    img = Image.open(input_path)
    
    # Convert to RGBA if it's not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Get the alpha channel
    alpha = np.array(img.getchannel('A'))
    
    # Find the non-transparent pixels
    non_transparent = np.where(alpha > 0)
    
    if len(non_transparent[0]) > 0:
        # Find the bounding box
        top = min(non_transparent[0])
        bottom = max(non_transparent[0])
        left = min(non_transparent[1])
        right = max(non_transparent[1])
        
        # Crop the image
        cropped = img.crop((left, top, right + 1, bottom + 1))
        
        # Save the result
        cropped.save(output_path)
        
        print(f"Image cropped and saved to {output_path}")
        print(f"Original size: {img.size}, Cropped size: {cropped.size}")
    else:
        print("Image is entirely transparent!")
        # Save a copy of the original
        img.save(output_path)

# Example usage
if __name__ == "__main__":
    input_file = "Industrial_Island_Step4.png"  # Replace with your input file
    output_file = "output.png"  # Replace with your desired output file
    crop_transparent(input_file, output_file)
