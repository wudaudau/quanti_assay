"""
It's the module to deal with SD serial concentration (conc.).
There are often 7 non-zero standard dilution (sd) points in the standard curve.
So we call the highest concentration of the standard dilution as sd7.
"""


def cal_sd7_dilution_factor(sd_vol:int, other_vol:int) -> float:
    """
    sd_vol: the volume of sd to prepare sd7
    other_vol: the volume of other standard pretients and diluant

    Calculate the dilution factor to prepare sd7.
    """

    sd7_dilution_factor = sd_vol / (sd_vol + other_vol)

    return sd7_dilution_factor

def cal_sd7_conc(sd_conc, sd7_dilution_factor) -> float:
    """
    sd_conc: the concentration of sd7
    sd7_dilution_factor: the dilution factor to prepare sd7.
    """
    return sd_conc * sd7_dilution_factor

def cal_sd_serie_conc(sd7_conc:float, serial_dilution_factor:int, sd_point_count=7) -> list:
    """
    sd7_conc: the concentration of sd7 (the highest sd)
    serial_dilution_factor: the serial dilution factor. often 2 or 4.
    sd_point_count: the number of sd points in the standard curve. default is 7.

    Calculate the concentrations of the other sd points. (round to 2)
    sorted from low to high.
    return [sd1_conc, sd2_conc, ...]
    """
    sd_concs = [sd7_conc]
    for i in range(1, sd_point_count):
        conc = round(sd_concs[i-1] / serial_dilution_factor, 2)
        sd_concs.append(conc)

    return sorted(sd_concs)


