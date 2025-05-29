import numpy as np


ROOFTOP_CLASSES = [25,14] 
PANEL_AREA_M2 = 1.7 
PIXEL_TO_METER_RATIO = 0.25  # Assume each pixel covers 0.25 sq meter (adjust as needed)

def calculate_rooftop_area(mask: np.ndarray):
    rooftop_pixels = sum(np.sum(mask == cid) for cid in ROOFTOP_CLASSES)
    rooftop_area_m2 = rooftop_pixels * PIXEL_TO_METER_RATIO
    return rooftop_area_m2

def estimate_solar_capacity(area_m2, panel_wattage, panel_area):
    num_panels = int(area_m2 // panel_area)
    estimated_kw = round(num_panels * (panel_wattage / 1000), 2)  # W to kW
    return num_panels, estimated_kw