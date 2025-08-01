from PIL import Image
from PIL.Image import Image as PILImage
import numpy as np
import io

def crop_transparent_image(image_data, output_format='PNG'):
    """Crops transparent areas from an image."""
    img = Image.open(io.BytesIO(image_data))
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    alpha = np.array(img.getchannel('A'))
    non_transparent = np.where(alpha > 0)
    
    if len(non_transparent[0]) > 0:
        top = min(non_transparent[0])
        bottom = max(non_transparent[0])
        left = min(non_transparent[1])
        right = max(non_transparent[1])
        
        cropped = img.crop((left, top, right + 1, bottom + 1))
        original_size = img.size
        cropped_size = cropped.size
        
        # Ensure PNG format for transparent images
        output = io.BytesIO()
        cropped.save(output, format='PNG')
        output.seek(0)
        
        return output, original_size, cropped_size, 'PNG'
    else:
        output = io.BytesIO()
        img.save(output, format='PNG')
        output.seek(0)
        return output, img.size, img.size, 'PNG'

def crop_by_background_color(image_data, threshold=30, corner_offset=5, output_format=None):
    """Crops background areas based on corner color sampling."""
    img = Image.open(io.BytesIO(image_data))
    original_format = img.format
    
    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGB')
    
    width, height = img.size
    corner_colors = []
    offset = min(corner_offset, width//4, height//4)
    
    corners = [
        (offset, offset),
        (width - offset - 1, offset),
        (offset, height - offset - 1),
        (width - offset - 1, height - offset - 1)
    ]
    
    for x, y in corners:
        if img.mode == 'RGBA':
            r, g, b, a = img.getpixel((x, y))
            corner_colors.append((r, g, b))
        else:
            corner_colors.append(img.getpixel((x, y)))
    
    avg_r = sum(color[0] for color in corner_colors) // len(corner_colors)
    avg_g = sum(color[1] for color in corner_colors) // len(corner_colors)
    avg_b = sum(color[2] for color in corner_colors) // len(corner_colors)
    background_color = (avg_r, avg_g, avg_b)
    
    img_array = np.array(img)
    if img.mode == 'RGBA':
        img_rgb = img_array[:, :, :3]
    else:
        img_rgb = img_array
    
    # Vectorized color distance calculation
    bg_color_array = np.array(background_color)
    diff = img_rgb.astype(np.float32) - bg_color_array
    distances = np.sqrt(np.sum(diff**2, axis=2))
    mask = distances > threshold
    
    non_bg_coords = np.where(mask)
    
    if len(non_bg_coords[0]) > 0:
        top = min(non_bg_coords[0])
        bottom = max(non_bg_coords[0])
        left = min(non_bg_coords[1])
        right = max(non_bg_coords[1])
        
        cropped = img.crop((left, top, right + 1, bottom + 1))
        original_size = img.size
        cropped_size = cropped.size
        
        # Determine output format
        if output_format is None:
            output_format = original_format if original_format in ['JPEG', 'PNG', 'WEBP', 'GIF'] else 'PNG'
        
        # Convert to RGB for JPEG format
        if output_format == 'JPEG' and cropped.mode in ['RGBA', 'LA']:
            # Create a white background for JPEG
            white_bg = Image.new('RGB', cropped.size)
            # Create a white background using PIL's putdata
            white_pixels = [(255, 255, 255)] * (cropped.size[0] * cropped.size[1])
            white_bg.putdata(white_pixels)
            
            if cropped.mode == 'RGBA':
                white_bg.paste(cropped, mask=cropped.split()[-1])  # Use alpha channel as mask
            else:
                white_bg.paste(cropped)
            cropped = white_bg
        
        output = io.BytesIO()
        save_kwargs = {'format': output_format}
        if output_format == 'JPEG':
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True
        
        cropped.save(output, **save_kwargs)
        output.seek(0)
        
        return output, original_size, cropped_size, background_color, output_format
    else:
        # Convert to RGB for JPEG format
        if output_format == 'JPEG' and img.mode in ['RGBA', 'LA']:
            rgb_img = Image.new('RGB', img.size)
            # Create white background using putdata
            white_pixels = [(255, 255, 255)] * (img.size[0] * img.size[1])
            rgb_img.putdata(white_pixels)
            
            if img.mode == 'RGBA':
                rgb_img.paste(img, mask=img.split()[-1])
            else:
                rgb_img.paste(img)
            img = rgb_img
        
        output = io.BytesIO()
        save_kwargs = {'format': output_format if output_format else (original_format if original_format in ['JPEG', 'PNG', 'WEBP', 'GIF'] else 'PNG')}
        if output_format == 'JPEG':
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True
        
        img.save(output, **save_kwargs)
        output.seek(0)
        return output, img.size, img.size, background_color, save_kwargs['format']

def auto_crop_image(image_data, threshold=30, corner_offset=5):
    """Automatically chooses between transparent or color background cropping."""
    img = Image.open(io.BytesIO(image_data))
    original_format = img.format
    
    has_alpha = img.mode in ['RGBA', 'LA'] or 'transparency' in img.info
    
    if has_alpha:
        if img.mode != 'RGBA':
            img_rgba = img.convert('RGBA')
        else:
            img_rgba = img
        
        alpha = np.array(img_rgba.getchannel('A'))
        unique_alpha = np.unique(alpha)
        has_meaningful_transparency = len(unique_alpha) > 1 and np.min(alpha) < 255
        has_transparent_pixels = np.any(alpha == 0)
        
        if has_meaningful_transparency or has_transparent_pixels:
            output, original_size, cropped_size, output_format = crop_transparent_image(image_data)
            return output, original_size, cropped_size, "transparent", None, output_format
    
    # Determine output format for non-transparent images
    output_format = original_format if original_format in ['JPEG', 'PNG', 'WEBP', 'GIF'] else 'PNG'
    
    output, original_size, cropped_size, background_color, final_format = crop_by_background_color(
        image_data, threshold, corner_offset, output_format
    )
    return output, original_size, cropped_size, "color_background", background_color, final_format