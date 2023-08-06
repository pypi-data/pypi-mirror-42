"""
Metadata for the cosmology fields.
"""

def generate_cosmology(a: float, gamma: float):
    """
    Generates the cosmology dictionaries with the
    a-factors given for each particle field.

    Gives comoving -> physical.
    """

    # TODO
    UNKNOWN = 1.0

    shared = {
        "coordinates": a,
        "masses": None, 
        "particle_ids": None,
        "velocities": UNKNOWN,
        "potential": UNKNOWN
    }

    baryon = {
        "element_abundance": None,
        "maximal_temperature": None,
        "maximal_temperature_scale_factor": None,
        "iron_mass_frac_from_sn1a": None,
        "metal_mass_frac_from_agb": None,
        "metal_mass_frac_from_snii": None,
        "metal_mass_frac_from_sn1a": None,
        "metallicity": None,
        "smoothed_element_abundance": None,
        "smoothed_iron_mass_frac_from_sn1a": None,
        "smoothed_metallicity": None,
        "total_mass_from_agb": None, 
        "total_mass_from_snii": None,
    }

    gas = {
        "denisty": a**(-3),
        "entropy": None,
        "internal_energy": a**(-3.0 * (gamma - 1)),
        "smoothing_length": a,
        "pressure": a**(-3.0 * gamma),
        "diffusion": None,
        "sfr": None,
        "temperature": None,
        "viscosity": None,
        "specific_sfr": None,
        "material_id": None,
        "diffusion": None,
        "viscosity": None,
        **shared,
        **baryon,
    }

    dark_matter = {**shared}

    stars = {
        "birth_density": gas["density"],
        "birth_time": None,
        "initial_masses": None,
        "new_star_flag": None,
        **shared,
        **baryon,
    }

    black_holes = {**shared}

    return {
        "gas": gas,
        "dark_matter": dark_matter,
        "stars": stars,
        "black_holes": black_holes,
    }