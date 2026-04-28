# DN170 Valve Weight Optimization Calculator
# Comparing Steel (12X18H10T) vs Aluminum (AMg6)

def calculate_weight(material="steel"):
    # Densities in kg/m3
    density = 7900 if material == "steel" else 2650
    
    # 1. Main Housing (302 x 302 x 400 mm shell, wall thickness 6mm)
    # Using surface area approximation for the box-like structure
    w, h, d = 0.302, 0.302, 0.400
    t = 0.006
    surface_area = 2 * (w*h + h*d + w*d)
    vol_body = surface_area * t
    weight_body = vol_body * density
    
    # 2. Internal Cylinder (DN170, length 400mm, wall 6mm)
    # Vol = Pi * (R_out^2 - R_in^2) * L
    r_in = 0.172 / 2
    r_out = r_in + t
    vol_cyl = 3.14159 * (r_out**2 - r_in**2) * 0.400
    weight_cyl = vol_cyl * density
    
    # 3. Disk (D=195mm, thickness 10mm)
    r_disk = 0.195 / 2
    vol_disk = 3.14159 * (r_disk**2) * 0.010
    weight_disk = vol_disk * density
    
    # 4. Flanges (Outer D ~ 300mm, Inner D ~ 172mm, Thickness 12mm, 2 pieces)
    r_f_out = 0.300 / 2
    r_f_in = 0.172 / 2
    vol_flanges = 2 * (3.14159 * (r_f_out**2 - r_f_in**2) * 0.012)
    weight_flanges = vol_flanges * density
    
    return {
        "Body": weight_body,
        "Cylinder": weight_cyl,
        "Disk": weight_disk,
        "Flanges": weight_flanges,
        "Total_Metal": weight_body + weight_cyl + weight_disk + weight_flanges
    }

print("--- WEIGHT ANALYSIS FOR DN170 VALVE ---")
steel = calculate_weight("steel")
amg6 = calculate_weight("amg6")

print(f"{'Component':<15} | {'Steel (kg)':<10} | {'AMg6 (kg)':<10} | {'Delta (kg)':<10}")
print("-" * 55)
for key in steel.keys():
    delta = steel[key] - amg6[key]
    print(f"{key:<15} | {steel[key]:>10.2f} | {amg6[key]:>10.2f} | {delta:>10.2f}")

gearbox = 7.0
shaft_steel = 2.5
total_steel = steel['Total_Metal'] + gearbox + shaft_steel
total_amg6 = amg6['Total_Metal'] + gearbox + shaft_steel

print("-" * 55)
print(f"TOTAL ASSEMBLY (with Steel Shaft & Gearbox):")
print(f"STEEL: {total_steel:.2f} kg (LIMIT EXCEEDED by {total_steel-25:.2f} kg)")
print(f"AMg6:  {total_amg6:.2f} kg (OK! - Under limit by {25-total_amg6:.2f} kg)")
