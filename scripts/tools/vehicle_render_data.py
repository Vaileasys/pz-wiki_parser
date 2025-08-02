# Outputs a JSON file with rendering data (mesh and texture) to be used in blender project.

import os
from scripts.objects.vehicle import Vehicle
from scripts.core import file_loading
from scripts.utils import echo
from scripts.core.constants import OUTPUT_DIR

PATH = os.path.join(OUTPUT_DIR, "vehicle_render_data.json")

WHEEL_ORIGINS = {
    # "Name": (X, Y, Z, Scale) --scale is relative, based on wheel original size
    "Van": {
        "FrontLeft":  (-1.17,  2.75, -1.13),
        "RearLeft":   (-1.17, -1.68, -1.13),
        "FrontRight": (1.17,  2.75, -1.13),
        "RearRight":  (1.17, -1.68, -1.13),
    },
    "StepVan": {
        "FrontLeft":  (-1.17,  2.46, -1.44),
        "RearLeft":   (-1.17, -1.8, -1.44),
        "FrontRight": (1.17,  2.46, -1.44),
        "RearRight":  (1.17, -1.8, -1.44),
    },
    "PickUp": {
        "FrontLeft":  (-1.04,  2.46, -1.05),
        "RearLeft":   (-1.04, -1.84, -1.05),
        "FrontRight": (1.04,  2.46, -1.05),
        "RearRight":  (1.04, -1.84, -1.05),
    },
    "SmallCar02": {
        "FrontLeft":  (-1.00,  1.87, -1.00),
        "RearLeft":   (-1.00, -2.23, -1.00),
        "FrontRight": (1.00,  1.87, -1.00),
        "RearRight":  (1.00, -2.23, -1.00),
    },
    "CarSmall02": {
        "FrontLeft":  (-1.00,  1.87, -1.00),
        "RearLeft":   (-1.00, -2.23, -1.00),
        "FrontRight": (1.00,  1.87, -1.00),
        "RearRight":  (1.00, -2.23, -1.00),
    },
    "CarSmall": {
        "FrontLeft":  (-0.9,  1.61, -0.75),
        "RearLeft":   (-0.9, -1.82, -0.75),
        "FrontRight": (0.9,  1.61, -0.75),
        "RearRight":  (0.9, -1.82, -0.75),
    },
    "SmallCar": {
        "FrontLeft":  (-0.9,  1.61, -0.75),
        "RearLeft":   (-0.9, -1.82, -0.75),
        "FrontRight": (0.9,  1.61, -0.75),
        "RearRight":  (0.9, -1.82, -0.75),
    },
    "SportsCar": {
        "FrontLeft":  (-0.95,  1.9, -0.75),
        "RearLeft":   (-0.95, -1.82, -0.75),
        "FrontRight": (0.95,  1.9, -0.75),
        "RearRight":  (0.95, -1.82, -0.75),
    },
    "SUV": {
        "FrontLeft":  (-1.23,  2.22, -1.0),
        "RearLeft":   (-1.23, -1.84, -1.0),
        "FrontRight": (1.23,  2.22, -1.0),
        "RearRight":  (1.23, -1.84, -1.0),
    },
    "CarLuxury": {
        "FrontLeft":  (-1.25,  2.14, -0.93),
        "RearLeft":   (-1.25, -2.08, -0.93),
        "FrontRight": (1.25,  2.14, -0.93),
        "RearRight":  (1.25, -2.08, -0.93),
    },
    "ModernCar_Martin": {
        "FrontLeft":  (-0.88,  1.81, -0.93, 0.85),
        "RearLeft":   (-0.88, -1.53, -0.93, 0.85),
        "FrontRight": (0.88,  1.81, -0.93, 0.85),
        "RearRight":  (0.88, -1.53, -0.93, 0.85),
    },
    "ModernCar": {
        "FrontLeft":  (-1.1,  2.30, -0.93),
        "RearLeft":   (-1.1, -1.96, -0.93),
        "FrontRight": (1.1,  2.30, -0.93),
        "RearRight":  (1.1, -1.96, -0.93),
    },
    "OffRoad": {
        "FrontLeft":  (-1.04,  1.93, -0.93),
        "RearLeft":   (-1.04, -1.7, -0.93),
        "FrontRight": (1.04,  1.93, -0.93),
        "RearRight":  (1.04, -1.7, -0.93),
    },
    "Trailer_Horsebox": {
        "FrontLeft":  (-1.31,  -1.23, -1.65, 0.9),
        "RearLeft":   (-1.31, -2.22, -1.65, 0.9),
        "FrontRight": (1.31,  -1.23, -1.65, 0.9),
        "RearRight":  (1.31, -2.23, -1.65, 0.9),
    },
    "Trailer_Livestock": {
        "FrontLeft":  (-1.17,  -0.67, -1.25, 0.9),
        "RearLeft":   (-1.17, -1.66, -1.25, 0.9),
        "FrontRight": (1.17,  -0.67, -1.25, 0.9),
        "RearRight":  (1.17, -1.66, -1.25, 0.9),
    },
    "TrailerAdvert": {
        "FrontLeft":  (-0.8,  0, -1.71, 0.9),
        "RearLeft":   (-0.8, -1, -1.71, 0.9),
        "FrontRight": (0.8,  0, -1.71, 0.9),
        "RearRight":  (0.8, -1, -1.71, 0.9),
    },
    "Trailer": {
        "Left":  (-0.8,  -0.78, -0.8, 0.9),
        "Right": (0.8,  -0.78, -0.8, 0.9),
    },
    # Base.CarNormal
    "default": {
        "FrontLeft":  (-1.04,  2.67, -0.93),
        "RearLeft":   (-1.04, -1.96, -0.93),
        "FrontRight": (1.04,  2.67, -0.93),
        "RearRight":  (1.04, -1.96, -0.93),
    }
}

ADJUSTMENTS = {
    "trailer": {
        "location": [0, 0, -0.45],
        "camera": {
            "lens": 80
        }
    },
    "Base.ModernCar_Martin": {
        "location": [0, 0, -12.8],
        "camera": {
            "lens": 60
        }
    },
    "Base.SportsCar_ez": {
        "location": [0, 0.085, -1.1917],
        "camera": {
            "index": 4
        }
    },
    "Base.LuxuryCarBurnt": {
        "camera": {
            "lens": 50
        }
    }
}

def add_adjustments(vehicle_id, vehicle_data):
    if "burnt" in vehicle_id.lower():
        vehicle_data.setdefault("camera", {})["lens"] = 60

    if vehicle_id in ["Base.Trailer", "Base.TrailerCover"]:
        adjust_key = "trailer"
    else:
        adjust_key = vehicle_id

    if adjust_key in ADJUSTMENTS:
        vehicle_data = vehicle_data | ADJUSTMENTS.get(adjust_key, {})

    return vehicle_data


def main():
    vehicles = Vehicle.all()
    vehicle_data = {}

    for vehicle_id in vehicles:
        vehicle = Vehicle(vehicle_id)
        vehicle_data[vehicle_id] = {}
        vehicle_data[vehicle_id]["mesh"] = vehicle.get_mesh_path().split("|", 1)[0]
        vehicle_data[vehicle_id]["texture"] = vehicle.get_texture_path()

        wheel_origin = WHEEL_ORIGINS["default"]
        for prefix, origins in WHEEL_ORIGINS.items():
            if prefix != "default" and vehicle.id_type.startswith(prefix):
                wheel_origin = origins
                break
        vehicle_data[vehicle_id]["wheel"] = wheel_origin

        vehicle_data[vehicle_id] = add_adjustments(vehicle_id, vehicle_data[vehicle_id])

    file_loading.save_json(PATH, vehicle_data)
    echo.success(f"JSON file saved to '{PATH}'")

if __name__ == "__main__":
    main()