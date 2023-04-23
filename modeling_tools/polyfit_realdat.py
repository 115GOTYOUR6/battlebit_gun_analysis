import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preset_arsenals import ARSENALS
from gen_realdam_dict import generate_real_damage_dict


def cubic_func(x, a, b, c, d):
    """Cubic function for curve fitting."""
    return a*x**3 + b*x**2 + c*x + d


def quad_func(x, a, b, c):
    """Quadratic function for curve fitting."""
    return a*x**2 + b*x + c


def perc_error(approx, exact):
    """Return the percentage error between approx and exact."""
    return abs(approx - exact)/exact*100

def int_to_alpha(i):
    return chr(ord('a')+i)


def print_model_coefficients_and_r_2(coefficients, r_2):
    for model in coefficients:
        print(model)
        print(f"R^2: {r_2[model]}")
        print_coeffs(coefficients[model])
        print()


def print_coeffs(coeffs):
    for ind, coeff in enumerate(coeffs):
        print(f"{int_to_alpha(ind)}: {coeff}")


def normalise_damage_values(real_damage_dict, gun):
    return np.array([i/gun.get_max_base_dam("bod_dam") for i in real_damage_dict[gun.name]["real_damage"]])


def plot_damage_scaling_vs_range_for_regressions_and_real(x, y, y_predictions):
    plt.plot(x, y, label="real")
    for model in y_predictions:
        plt.plot(x, y_predictions[model], label=model)
    plt.legend(loc="upper right")
    plt.ylabel("Damage Scaling Coefficient")
    plt.xlabel("Falloff Range (m)")
    plt.show()


def calculate_r_2_for_all_models(y, y_predict, reg_coeffs):
    y_hat = np.mean(y)
    r_2 = {}
    for model in reg_coeffs:
        residual_ss = sum((y - y_predict[model])**2)
        total_ss = sum((y - y_hat)**2)
        r_2[model] = 1 - (residual_ss/total_ss)
    return r_2

def enforce_last_point_is_end_of_falloff_range(min_damage_coefficient, falloff_start, falloff_end, fallof_range_x, fallof_range_y):
    if fallof_range_x[-1] != falloff_end - falloff_start:
        fallof_range_x.append(falloff_end - falloff_start)
        fallof_range_y.append(min_damage_coefficient)

def enforce_first_point_is_start_of_falloff(falloff_start, falloff_range_x, falloff_range_y, dist):
    if len(falloff_range_x) == 0 and dist > falloff_start:
        falloff_range_x.append(falloff_start - falloff_start)
        falloff_range_y.append(1)

def trim_range_to_falloff_range_and_normalise_x_y(name_of_gun_to_fit, gun,
                                                  real_damage_dict, x):
    falloff_start = gun._dam_prof[0][0]
    falloff_end = gun._dam_prof[1][0]
    falloff_range_x = []
    falloff_range_y = []
    for i, dist in enumerate(x):
        enforce_first_point_is_start_of_falloff(falloff_start, falloff_range_x, falloff_range_y, dist)
        if falloff_start <= dist <= falloff_end:
            falloff_range_x.append(dist - falloff_start)
            falloff_range_y.append(real_damage_dict[name_of_gun_to_fit]["real_damage"][i]/gun.get_max_base_dam("bod_dam"))
    enforce_last_point_is_end_of_falloff_range(gun._MIN_CO, falloff_start, falloff_end, falloff_range_x, falloff_range_y)
    return np.array(falloff_range_x), np.array(falloff_range_y)




parser = argparse.ArgumentParser(description="Fit a polynomial to real damage data.")
parser.add_argument("gun_to_fit", nargs="+", help="The gun to have its real"
                                                  " data fitted.")
parser.add_argument("--arsenal_name", default="ttk_dat",
                    help="The name of the arsenal to use.")
args = parser.parse_args()


name_of_gun_to_fit = args.guns_to_fit[0]
arsenal = ARSENALS[args.arsenal_name]()
gun = arsenal.get_weapon_by_name(name_of_gun_to_fit)
real_damage_dict = generate_real_damage_dict()
x = np.array(real_damage_dict[name_of_gun_to_fit]['dist'])
# we need to strip the damage values that don't occur in the gun's falloff range
# use the damage profile instance var

zero_aligned_x, normalised_y = trim_range_to_falloff_range_and_normalise_x_y(name_of_gun_to_fit, gun, real_damage_dict, x)
print(zero_aligned_x)
print(normalised_y)

# TODO: This shouldn't be hard coded; it should probably also be an object
y_predict = {}
reg_coeffs = {}
reg_covariance = {}
reg_coeffs["cub reg"], reg_covariance["cub reg"] = curve_fit(cubic_func, zero_aligned_x, normalised_y)
y_predict["cub reg"] = cubic_func(zero_aligned_x, *reg_coeffs["cub reg"])
reg_coeffs["quad reg"], reg_covariance["quad reg"] = curve_fit(quad_func, zero_aligned_x, normalised_y)
y_predict["quad reg"] = quad_func(zero_aligned_x, *reg_coeffs["quad reg"])

r_2 = calculate_r_2_for_all_models(normalised_y, y_predict, reg_coeffs)
print_model_coefficients_and_r_2(reg_coeffs, r_2)
# print_p_errs(y, y_predict)

plot_damage_scaling_vs_range_for_regressions_and_real(zero_aligned_x, normalised_y, y_predict)
