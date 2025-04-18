from PIL import Image
import numpy as np
import io

def crop_transparent_image(image_data):
    """
    Crops transparent areas from an image.
    
    Args:
        image_data (bytes): The image data as bytes
        
    Returns:
        tuple: (BytesIO object of cropped image, original size tuple, cropped size tuple)
    """
    # Load image from binary data
    img = Image.open(io.BytesIO(image_data))
    
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
        
        # Get metadata
        original_size = img.size
        cropped_size = cropped.size
        
        # Save to memory buffer
        output = io.BytesIO()
        cropped.save(output, format=img.format if img.format else 'PNG')
        output.seek(0)
        
        return output, original_size, cropped_size
    else:
        # Image is entirely transparent
        output = io.BytesIO()
        img.save(output, format=img.format if img.format else 'PNG')
        output.seek(0)
        return output, img.size, img.size