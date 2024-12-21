from mp_api.client import MPRester
import pandas as pd

# Replace this with your Materials Project API key
API_KEY = "ZdS0JGpmF3Gm8W7mOr4dJbtSbU4YGy8R"
mpr = MPRester(API_KEY)

# Function to estimate thermal properties if missing
def estimate_properties(material):
    thermal_conductivity = getattr(material, 'thermal_conductivity', None)
    heat_capacity = getattr(material, 'heat_capacity', None)
    
    # Assign estimated values if missing
    if thermal_conductivity is None:
        thermal_conductivity = 0.2  # Default estimated value (W/m·K)
    if heat_capacity is None:
        heat_capacity = 1.5  # Default estimated value (J/g·K)
        
    return thermal_conductivity, heat_capacity

try:
    # Query for materials with fields commonly related to polymers
    polymer_data = mpr.materials.summary.search(
        elements=["C", "H", "O"],  # Elements commonly in polymers
        fields=[
            "material_id",
            "formula_pretty",
            "decomposition_energy_per_atom",
            "density",
            "thermal_conductivity",
            "heat_capacity",
        ]
    )

    # Convert data into a clean list of dictionaries
    processed_data = []
    for material in polymer_data:
        thermal_conductivity, heat_capacity = estimate_properties(material)
        processed_data.append({
            "Material ID": material.material_id,
            "Polymer Name (Formula)": material.formula_pretty,
            "Decomposition Energy (eV/atom)": getattr(material, 'decomposition_energy_per_atom', 'N/A'),
            "Density (g/cm³)": getattr(material, 'density', 'N/A'),
            "Thermal Conductivity (W/m·K)": thermal_conductivity,
            "Heat Capacity (J/g·K)": heat_capacity
        })

    # Convert the processed data to a DataFrame
    df = pd.DataFrame(processed_data)

    # Save the data to CSV
    csv_filename = "polymer_properties_with_estimations.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Data successfully saved to {csv_filename}")

    # Display a preview of the saved data
    print("Data Preview:")
    print(df.head())

except Exception as e:
    print("An error occurred:", e)
