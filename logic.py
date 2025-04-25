def red_val_t(x, xc, temp_unit_index):
    if temp_unit_index == 0:
        return x / xc
    elif temp_unit_index == 1:
        return (x * (5 / 9)) / xc
    elif temp_unit_index == 2:
        return (x + 273.15) / xc
    elif temp_unit_index == 3:
        return ((x - 32) * (5 / 9) + 273.15) / xc

def red_val_p(y, yc, pressure_unit_index):
    if pressure_unit_index == 0:
        return y / yc
    elif pressure_unit_index == 1:
        return (y / 100000) / yc
    elif pressure_unit_index == 2:
        return (y * 1.10325) / yc
    elif pressure_unit_index == 3:
        return (y / 750) / yc

def pressure(z, pressure_unit_index):
    if pressure_unit_index == 0:
        return z * 100
    elif pressure_unit_index == 1:
        return z / 1000
    elif pressure_unit_index == 2:
        return z * 101.325
    elif pressure_unit_index == 3:
        return z / 7.501

def temp(q, temp_unit_index):
    if temp_unit_index == 0:
        return q
    elif temp_unit_index == 1:
        return q * (5 / 9)
    elif temp_unit_index == 2:
        return q + 273.15
    elif temp_unit_index == 3:
        return (q - 32) * (5 / 9) + 273.15

def red_h(h1, h2, h3, h4, h5, h6, h7, h8):
    return (1.987 * h1 * h2) * (h3 - (h4 * h5) + h6 * (h7 - (h4 * h8)))

def red_s(h1, h5, h6, h8):
    return -(1.987 * h1) * (h5 + (h6 * h8))

def red_v(h9, h10, h11, h12):
    return (8314 * h9 * (h10 - 1)) / (h11 * h12)
