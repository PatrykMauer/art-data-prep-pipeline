""""Numpy module."""
import numpy as np

unit_conversion_ratios = {
    'cm': 1.0,
    'mm': 0.1,
    'in': 2.54,
    'ft': 30.48,
    'yd': 91.44,
    'mi': 160934.4,
    'm': 100
}

# pylint: disable=C0301
REGEX_DIMENSIONS = r'(\d+(?:[,.]\d+)?)\s*[x,×]\s*(\d+(?:[,.]\d+)?)(?:\s*[x,×]\s*(\d+(?:[,.]\d+)?))?\s*(cm|mm|in|ft|yd|mi|m)'

REGEX_YEAR = r'(\d{4})'


def is_valid_number(s):
    """Check if a string is a valid number after replacing commas with periods."""
    try:
        float(s.replace(',', '.'))
        return True
    except ValueError:
        return False


def multiply_largest_dimensions(dimensions):
    """Calculates the area of two biggest dimensions after the unit conversion."""
    dimensions = str(dimensions)
    found_unit = False
    for unit, conversion_ratio in unit_conversion_ratios.items():
        if unit in dimensions:
            found_unit = True
            # Remove unit for calculation
            dimensions = dimensions.replace(unit, '')
            break

    # If no unit is found, assume cm or mm based on size
    if not found_unit:
        if '×' in dimensions:
            parts = dimensions.split('×')
        else:
            parts = dimensions.split('x')
        # Use cm if the largest dimension is less than 150, otherwise use mm
        try:
            float_dimensions = [float(part.replace(',', '.'))
                                for part in parts if is_valid_number(part)]
            if not float_dimensions or len(float_dimensions) < 2:
                return np.nan
            conversion_ratio = unit_conversion_ratios['cm'] if max(
                float_dimensions) < 150 else unit_conversion_ratios['mm']
        except ValueError:
            return np.nan

    else:
        if '×' in dimensions:
            parts = dimensions.split('×')
        else:
            parts = dimensions.split('x')

    # Validate each part of the dimensions
    valid_parts = [part for part in parts if is_valid_number(part)]
    if len(valid_parts) < 2:
        return np.nan

    try:
        # Convert all valid parts to floats and scale them
        scaled_parts = [float(part.replace(',', '.')) *
                        conversion_ratio for part in valid_parts]
        # Sort the dimensions to find the two largest
        scaled_parts.sort(reverse=True)
        # Calculate the product of the two largest dimensions
        return scaled_parts[0] * scaled_parts[1]
    except ValueError:
        return np.nan
