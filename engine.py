# ============================================================
# TRIPLE BOT – CHINA DEMO ENGINE (CLEAN VERSION)
# Deterministic | No Random | No External State
# ============================================================

import hashlib
import json


def evaluate_structure(design_input: dict, factor_input: dict):

    # ============================================================
    # INPUT
    # ============================================================

    foundation_area = float(design_input["foundation_area"])
    column_capacity = float(design_input["column_capacity"])
    load_per_storey = float(design_input["load_per_storey"])
    storeys = int(design_input["storeys"])

    soil_phi = float(factor_input["soil_phi"])
    column_phi = float(factor_input["column_phi"])
    load_factor = float(factor_input["load_factor"])

    # ============================================================
    # LOAD CALCULATION
    # ============================================================

    total_load = load_per_storey * storeys
    factored_load = total_load * load_factor

    # ============================================================
    # GB STYLE CAPACITY MODEL (DEMO LEVEL)
    # ============================================================

    GB_SOIL_BASE = 180  # kPa reference (demo constant)

    soil_capacity = foundation_area * GB_SOIL_BASE * soil_phi
    column_capacity_factored = column_capacity * column_phi

    # Governing mechanism
    if soil_capacity <= column_capacity_factored:
        governing_capacity = soil_capacity
        governing_mode = "SOIL_GB_STYLE"
    else:
        governing_capacity = column_capacity_factored
        governing_mode = "COLUMN_GB_STYLE"

    # ============================================================
    # UTILIZATION
    # ============================================================

    if governing_capacity == 0:
        utilization_ratio = 0
    else:
        utilization_ratio = factored_load / governing_capacity

    margin = governing_capacity - factored_load

    status = "SAFE" if utilization_ratio <= 1 else "UNSAFE"

    # ============================================================
    # TRANSPARENCY LAYER (NOT IP, JUST VALUES)
    # ============================================================

    transparency = {
        "soil_capacity": round(soil_capacity, 2),
        "column_capacity": round(column_capacity_factored, 2),
        "governing_capacity": round(governing_capacity, 2)
    }

    # ============================================================
    # DETERMINISTIC SIGNATURE
    # ============================================================

    signature_payload = {
        "foundation_area": foundation_area,
        "column_capacity": column_capacity,
        "load_per_storey": load_per_storey,
        "storeys": storeys,
        "soil_phi": soil_phi,
        "column_phi": column_phi,
        "load_factor": load_factor,
        "total_load": total_load,
        "factored_load": factored_load,
        "governing_capacity": governing_capacity,
        "utilization_ratio": utilization_ratio
    }

    payload_string = json.dumps(signature_payload, sort_keys=True)
    deterministic_hash = hashlib.sha256(payload_string.encode()).hexdigest()

    # ============================================================
    # OUTPUT
    # ============================================================

    return {
        "status": status,
        "utilization_ratio": round(utilization_ratio, 4),
        "governing_mode": governing_mode,
        "margin": round(margin, 2),
        "total_load": round(total_load, 2),
        "factored_load": round(factored_load, 2),
        "deterministic": True,
        "signature": deterministic_hash,
        "transparency": transparency
    }