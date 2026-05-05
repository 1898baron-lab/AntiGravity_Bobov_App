import ezdxf
import os

def generate_grill_dxfs():
    output_dir = r'C:/ANTIGRAVITY/1/obsidian_brain/1_PROJECTS/MANGAL/dxf/'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. bottom.dxf (600x300mm, grid of 10mm holes with 50mm spacing)
    doc_bottom = ezdxf.new('R2010')
    msp_bottom = doc_bottom.modelspace()
    msp_bottom.add_lwpolyline([(0, 0), (600, 0), (600, 300), (0, 300), (0, 0)])
    # Grid calculation: center holes at 25, 75, 125... to keep 50mm spacing
    for x in range(25, 600, 50):
        for y in range(25, 300, 50):
            msp_bottom.add_circle((x, y), radius=5)
    doc_bottom.saveas(os.path.join(output_dir, 'bottom.dxf'))

    # 2. side_long.dxf (600x200mm, with logo text 'MASTODONT' in the center)
    doc_long = ezdxf.new('R2010')
    msp_long = doc_long.modelspace()
    msp_long.add_lwpolyline([(0, 0), (600, 0), (600, 200), (0, 200), (0, 0)])
    # Note: ezdxf text requires fonts, for laser cutting it's better to use lines.
    # But for now we follow the model's logic.
    msp_long.add_text("MASTODONT", dxfattribs={'height': 40}).set_placement((200, 80))
    doc_long.saveas(os.path.join(output_dir, 'side_long.dxf'))

    # 3. side_short.dxf (300x200mm, include 4.2mm notches for 4mm steel assembly)
    doc_short = ezdxf.new('R2010')
    msp_short = doc_short.modelspace()
    msp_short.add_lwpolyline([(0, 0), (300, 0), (300, 200), (0, 200), (0, 0)])
    
    notch_dim = 4.2
    # Define 4 corner notches
    notches = [
        [(0, 0), (notch_dim, 0), (notch_dim, notch_dim), (0, notch_dim), (0, 0)],
        [(300, 0), (300 - notch_dim, 0), (300 - notch_dim, notch_dim), (300, notch_dim), (300, 0)],
        [(300, 200), (300 - notch_dim, 200), (300 - notch_dim, 200 - notch_dim), (300, 200 - notch_dim), (300, 200)],
        [(0, 200), (notch_dim, 200), (notch_dim, 200 - notch_dim), (0, 200 - notch_dim), (0, 200)]
    ]
    for points in notches:
        msp_short.add_lwpolyline(points)
    doc_short.saveas(os.path.join(output_dir, 'side_short.dxf'))

    # 4. leg.dxf (500x60mm)
    doc_leg = ezdxf.new('R2010')
    msp_leg = doc_leg.modelspace()
    msp_leg.add_lwpolyline([(0, 0), (500, 0), (500, 60), (0, 60), (0, 0)])
    doc_leg.saveas(os.path.join(output_dir, 'leg.dxf'))

    print(f"DXF files generated in: {output_dir}")

if __name__ == "__main__":
    generate_grill_dxfs()
