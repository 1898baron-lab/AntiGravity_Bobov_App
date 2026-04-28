# DN170 Valve Weight Optimization - SEARCHING FOR 25kg
def find_sweet_spot(wall_t=0.005, gearbox_w=5.5):
    density_amg6 = 2650
    density_steel = 7900
    
    # 1. Main Housing (302 x 302 x 400 mm shell)
    w, h, d = 0.302, 0.302, 0.400
    surface_area = 2 * (w*h + h*d + w*d)
    weight_body = (surface_area * wall_t) * density_amg6
    
    # 2. Internal Cylinder (DN170, length 400mm)
    r_in = 0.172 / 2
    r_out = r_in + wall_t
    vol_cyl = 3.14159 * (r_out**2 - r_in**2) * 0.400
    weight_cyl = vol_cyl * density_amg6
    
    # 3. Disk (D=195mm, thickness 8mm instead of 10)
    r_disk = 0.195 / 2
    vol_disk = 3.14159 * (r_disk**2) * 0.008
    weight_disk = vol_disk * density_amg6
    
    # 4. Flanges (Optimized: Round D=280mm, thickness 10mm)
    r_f_out = 0.280 / 2
    r_f_in = 0.172 / 2
    vol_flanges = 2 * (3.14159 * (r_f_out**2 - r_f_in**2) * 0.010)
    weight_flanges = vol_flanges * density_amg6
    
    shaft_steel = 2.0 # Slightly lightened
    
    total = weight_body + weight_cyl + weight_disk + weight_flanges + gearbox_w + shaft_steel
    return {
        "Wall": wall_t * 1000,
        "Gearbox": gearbox_w,
        "Total": total,
        "Components": {
            "Body": weight_body,
            "Cyl": weight_cyl,
            "Disk": weight_disk,
            "Flanges": weight_flanges,
            "Shaft": shaft_steel
        }
    }

res = find_sweet_spot(0.005, 5.0) # 5mm wall, 5kg gearbox
print(f"--- OPTIMIZED DESIGN ---")
print(f"Wall Thickness: {res['Wall']} mm")
print(f"Gearbox Weight: {res['Gearbox']} kg")
print(f"TOTAL WEIGHT:   {res['Total']:.2f} kg")
print("\nBreakdown:")
for k, v in res['Components'].items():
    print(f"  {k:<10}: {v:.2f} kg")
