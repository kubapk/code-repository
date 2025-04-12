# -*- coding: utf-8 -*-
"""
________________TITLE________________
Assignment 2 - Z Boson
_____________________________________
This Python script combines and filters data of cross section for different
centre of mass energies. It then finds a best fit of the data to the function
for cross section by minimising chi square. This is used to determine the
best mass, width and lifetime of the Z_0 boson. Uncertainties are determined
using a contour plot of chi square.

Created on Tue 21 Nov 2023
Last updated on Tue 12 Dec 2023

@author: Kuba
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin
from scipy import constants

FILE_NAME_1 = "z_boson_data_1.csv"
FILE_NAME_2 = "z_boson_data_2.csv"
ELECTRON_POSITRON_WIDTH = 0.08391  # GeV
BOSON_MASS_START = 90  # GeV/c^2
BOSON_WIDTH_START = 3  # GeV


def read_data(file_name):
    """
    Reads in the data and removes any error, Nan, 0 or negative values. It
    also checks for potential errors with reading in file and halts code if an
    error is found. This includes if the file does not exist
    (FileNotFoundError) or if a delimiter is missing (ValueError).

    Parameters
    ----------
    file_name : string
        The name of the file.

    Returns
    -------
    data : list
    """
    try:
        data = np.genfromtxt(
            file_name, comments='%', delimiter=',', filling_values=100)

        data = [row for row in data if not np.any(row == 100)]
        data = [row for row in data if not np.any(np.isnan(row))]
        data = [row for row in data if not np.any(row <= 0)]

        return data

    except (FileNotFoundError, IOError, ValueError) as error_code:
        print("Error:", error_code)
        sys.exit()

    return None


def combine_data(data_1, data_2):
    """
    Combines data_1 and data_2 into 1 array and then orders the data so
    first column (centre of mass energy) is ascending.

    Parameters
    ----------
    data_1 : list
        Data read from file 1.
    data_2 : list
        Data read from file 2.

    Returns
    -------
    sorted_data : array
        Combination of data_1 and data_2

    """
    combined_data = np.vstack((data_1, data_2))

    sorted_data_indices = np.array(np.argsort(combined_data[:, 0]))
    sorted_data = combined_data[sorted_data_indices, :]

    return sorted_data


def cross_section_function(energy, boson_mass, boson_width):
    """
    Determines the cross section for the inputed energy, boson mass and
    boson width using the equation given by

    cross section = (12pi / boson_mass^2) *
    [energy^2 / (energy^2 - boson_mass^2)^2 + boson_mass^2 * boson_width^2] *
    electron_positron_width^2.

    It then converts this into nanobarns.

    Parameters
    ----------
    energy : array
        Centre of mass energy
    boson_mass : float
    boson_width : float

    Returns
    -------
    cross_section_nano_barns : array

    """

    part_one = (12*np.pi) / (boson_mass)**2
    part_two_numerator = (energy**2) * (ELECTRON_POSITRON_WIDTH**2)
    part_two_denominator = (energy**2 - boson_mass**2)**2 +\
        ((boson_mass**2) * (boson_width**2))

    part_two = part_two_numerator / part_two_denominator

    cross_section = part_one * part_two

    # Converting from GeV^{-2} to nanobarns (nb)
    cross_section_nano_barns = cross_section * 389.4 * 1000

    return cross_section_nano_barns


def chi_square(boson_parameters, energy_input, observation,
               observation_uncertainty):
    """
    Uses boson parameters and energy input to find the predicted equation
    from cross section function. Uses this with observation (cross section) and
    its uncertainty to calculate chi square.

    Parameters
    ----------
    boson_parameters : array
        Array with first element as boson mass and second element as boson
        width.
    energy_input : array
        Array containing values of centre of mass energy.
    observation : array
        Array containing values of cross section.
    observation_uncertainty : array
        Array containing values of uncertainty in each cross section.

    Returns
    -------
    array
        Chi square value

    """

    boson_mass_input = boson_parameters[0]
    boson_width_input = boson_parameters[1]

    prediction = cross_section_function(
        energy_input, boson_mass_input, boson_width_input)

    return np.sum((observation - prediction)**2 / observation_uncertainty**2)


def remove_outliers(data, best_boson_mass, best_boson_width):
    """
    Keeps points in the data set that are not outliers, which is set if the
    difference between the cross section for that point and the equivalent
    cross section for the best fit is less than or equal to 4 times the error
    on each data point.


    Parameters
    ----------
    data : array
        Data containing centre of mass energy, cross section and cross section
        error as separate columns.
    best_boson_mass : float
    best_boson_width : float

    Returns
    -------
    filtered_data : array
        Data with outliers removed.

    """
    best_fit_function = cross_section_function(
        data[:, 0], best_boson_mass, best_boson_width)

    fit_minus_point = np.abs(data[:, 1] - best_fit_function)

    # Outliers are those where fit_minus_point is greater than the own error
    # of the point
    not_outlier_indices = np.array(np.where(fit_minus_point <= data[:, 2]*4))

    not_outlier_indices = not_outlier_indices.flatten()

    filtered_data = data[not_outlier_indices, :]

    return filtered_data


def find_min_chi_square(boson_mass, boson_width, data):
    """
    Uses fmin function to minimise the chi square and finds boson mass and
    boson width at this minimum chi square.

    Parameters
    ----------
    boson_mass : float
    boson_width : float
    data : array
        Data containing centre of mass energy, cross section and cross section
        error as separate columns.

    Returns
    -------
    result : array
        Array containing boson mass and width as well as respective minimum
        chi square value.

    """

    result = fmin(chi_square, (boson_mass, boson_width), args=(
        data[:, 0], data[:, 1], data[:, 2]), xtol=0.0001,
        ftol=0.0001, full_output=True, disp=False)

    return result


def plot_result(data, parameters):
    """
    Plots the first column of data (centre of mass energy) against second
    column of data (cross section) with errors (third column of data). It
    then uses the centre of mass energies with the boson parameters to find
    the fit.

    Parameters
    ----------
    data : array
        Data containing centre of mass energy, cross section and cross section
        error as separate columns.
    parameters : array
        Array with first element as boson mass and second element as boson
        width.

    Returns
    -------
    None.

    """
    fig = plt.figure()

    axes = fig.add_subplot(111)

    axes.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2],
                  fmt='x', label="Filtered data")

    axes.plot(data[:, 0], cross_section_function(
        data[:, 0], parameters[0], parameters[1]), label="Best fit")

    axes.set_title('Cross section for different centre of mass energies')
    axes.set_xlabel('Centre of mass energy, E (GeV)')
    axes.set_ylabel(r'Cross section, $\sigma$ (nb)')

    axes.legend(loc='upper left')
    axes.grid()

    plt.savefig("Cross_section_fit.png")
    plt.show()
    plt.close()


def generate_data_range(initial_value, upper_multiplier, lower_multiplier,
                        length):
    """
    Generates an array around an initial value where upper and lower limits
    are determined using upper and lower multipliers added / subtracted to the
    initial value.


    Parameters
    ----------
    initial_value : float
    upper_multiplier : float
    lower_multiplier : float
    length : float
        Number of data points that should be in the array output.

    Returns
    -------
    data_range : array

    """

    data_range = np.linspace((initial_value - lower_multiplier*initial_value),
                             (initial_value + upper_multiplier*initial_value),
                             length)

    return data_range


def plot_chi_square_contour(data, best_boson_mass, best_boson_width,
                            min_chi_square):
    """
    Plots the boson mass against boson width and represents the chi square for
    both using contours. Plots contours for minimum chi square + 1 and
    minimum chi square + 2.

    Parameters
    ----------
    data : array
        Data containing centre of mass energy, cross section and cross section
        error as separate columns.
    best_boson_mass : float
        Boson mass as determined from minimum chi square.
    best_boson_width : float
        Boson width as determined from minimum chi square.
    min_chi_square : float

    Returns
    -------
    contour_plot : matplotlib.contour.QuadContourSet object

    """

    boson_mass_range = generate_data_range(
        best_boson_mass, 0.001, 0.001, len(data))
    boson_width_range = generate_data_range(
        best_boson_width, 0.01, 0.01, len(data))

    # Manually create chi_square_data
    chi_square_data = np.zeros((len(boson_mass_range), len(boson_width_range)))

    for i, mass_value in enumerate(boson_mass_range):
        for j, width_value in enumerate(boson_width_range):
            chi_square_data[i, j] = chi_square(
                [mass_value, width_value], data[:, 0], data[:, 1], data[:, 2])

    mass_mesh, width_mesh = np.meshgrid(boson_mass_range, boson_width_range)

    fig = plt.figure()
    axes = fig.add_subplot(111)

    # Center contour levels around (minimum chi-square + 1) and
    # (minimum chi-square + 2)
    contour_plot = axes.contour(mass_mesh, width_mesh, chi_square_data,
                                levels=[(min_chi_square + 1),
                                        (min_chi_square + 2.3)])
    min_chi_square_plot = axes.errorbar(best_boson_mass, best_boson_width,
                                        fmt='o', label=r'$\chi^2_{min}$')
    axes.set_title(r'$\chi^2$ contours against $Z^0$ boson mass and width')
    axes.clabel(contour_plot, fontsize=12, colors='r')
    axes.set_xlabel(r'Boson mass, $m_Z$ ($\frac{GeV}{c^2}$)', fontsize=12)
    axes.set_ylabel(r'Boson width, $\Gamma_Z$ (GeV)', fontsize=12)

    labels = [r'$\chi^2_{min}$+1', r'$\chi^2_{min}$+2.3', r'$\chi^2_{min}$']

    contours = contour_plot.legend_elements()[0]

    plots = [contours[0], contours[1], min_chi_square_plot]

    axes.legend(plots, labels, loc='upper right')

    plt.savefig("Chi_square_contour_plot.png")
    plt.show()
    plt.close()

    return contour_plot


def calculate_uncertainties(contour_plot, best_boson_mass, best_boson_width):
    """
    Calculates the uncertainties in the boson mass and boson width by finding
    the minimum and maximum of the minimum chi square + 1 contour on both axes.

    Parameters
    ----------
    contour_plot : matplotlib.contour.QuadContourSet object
        DESCRIPTION.
    best_boson_mass : float
        Boson mass as determined from minimum chi square.
    best_boson_width : float
        Boson width as determined from minimum chi square.

    Returns
    -------
    boson_mass_uncertainty : float
    boson_width_uncertainty : float

    """

    # Finds coordinates of first contour plot (index 0)
    contour_coordinates = contour_plot.allsegs[0][0]

    boson_mass_contour = contour_coordinates[:, 0]
    boson_width_contour = contour_coordinates[:, 1]

    boson_mass_upper_uncertainty = abs(
        np.max(boson_mass_contour) - best_boson_mass)
    boson_mass_lower_uncertainty = abs(
        np.min(boson_mass_contour) - best_boson_mass)

    boson_mass_uncertainty = (
        boson_mass_upper_uncertainty + boson_mass_lower_uncertainty) / 2

    boson_width_upper_uncertainty = abs(
        np.max(boson_width_contour) - best_boson_width)
    boson_width_lower_uncertainty = abs(
        np.min(boson_width_contour) - best_boson_width)

    boson_width_uncertainty = (
        boson_width_upper_uncertainty + boson_width_lower_uncertainty) / 2

    return boson_mass_uncertainty, boson_width_uncertainty


def calculate_lifetime_uncertainty(boson_parameters, lifetime,
                                   mass_uncertainty, width_uncertainty):
    """
    Calculates percentage uncertainty in lifetime by summing percentage
    uncertainty of boson mass and boson width. Multiplies this by lifetime to
    find lifetime uncertainty.

    Parameters
    ----------
    boson_parameters : array
        Array with first element as boson mass and second element as boson
        width
    lifetime : float
    mass_uncertainty : float
    width_uncertainty : float

    Returns
    -------
    lifetime_uncertainty : float

    """

    mass_percentage_uncertainty = mass_uncertainty / boson_parameters[0]
    width_percentage_uncertainty = width_uncertainty / boson_parameters[1]

    lifetime_percentage_uncertainty = mass_percentage_uncertainty + \
        width_percentage_uncertainty
    lifetime_uncertainty = lifetime_percentage_uncertainty * lifetime

    return lifetime_uncertainty


def format_lifetime(lifetime, lifetime_uncertainty):
    """
    Uses the powers in lifetime and lifetime uncertainty to write the lifetime
    uncertainty in the same power as the lifetime.

    Parameters
    ----------
    lifetime : float
    lifetime_uncertainty : float

    Returns
    -------
    lifetime_with_error : string
        Lifetime and its error written together in same power.

    """

    lifetime_split = str(lifetime).split('e')
    uncertainty_split = str(lifetime_uncertainty).split('e')

    power_difference = abs(
        float(lifetime_split[1]) - float(uncertainty_split[1]))

    matching_lifetime_uncertainty = float(uncertainty_split[0]) / \
        (10**power_difference)

    lifetime_with_error = (
        f"({float(lifetime_split[0]):3.2f} +/- "
        f"{float(matching_lifetime_uncertainty):3.2f})*10^{lifetime_split[1]}"
        f" s")

    return lifetime_with_error


def main():
    """
    Main function.

    Returns
    -------
    None.

    """

    data_1 = read_data(FILE_NAME_1)
    data_2 = read_data(FILE_NAME_2)

    all_data = combine_data(data_1, data_2)

    # Removing outliers using the intial guesses - a lot of outliers will be
    # removed
    data_no_outliers = remove_outliers(
        all_data, BOSON_MASS_START, BOSON_WIDTH_START)

    # Finding parameters using initial guess
    result = find_min_chi_square(BOSON_MASS_START, BOSON_WIDTH_START, all_data)

    # Finding better parameters using filtered data of initial parameters
    result = find_min_chi_square(result[0][0], result[0][1], data_no_outliers)

    # Removing outliers from all data using the new best parameters
    data_no_outliers = remove_outliers(all_data, result[0][0], result[0][1])

    # Compute result using newly, best filtered data
    result = find_min_chi_square(result[0][0], result[0][1], data_no_outliers)

    # Plot results
    plot_result(data_no_outliers, result[0])

    contours = plot_chi_square_contour(
        data_no_outliers, result[0][0], result[0][1], result[1])

    # Calculate boson lifetime using result
    boson_width_joules = result[0][1] * constants.e * 10**(9)
    boson_lifetime = constants.hbar / boson_width_joules

    # Calculate uncertainties in results
    boson_mass_uncertainty, boson_width_uncertainty = calculate_uncertainties(
        contours, result[0][0], result[0][1])

    boson_lifetime_uncertainty = calculate_lifetime_uncertainty(
        result[0], boson_lifetime, boson_mass_uncertainty,
        boson_width_uncertainty)

    lifetime_with_error = format_lifetime(
        boson_lifetime, boson_lifetime_uncertainty)

    print(f"\n FINAL RESULTS \n\
          Boson mass = {result[0][0]: .2f} +/-{boson_mass_uncertainty: .2f}"
          f" GeV/c^2\n\
          Boson width = {result[0][1]: .3f} +/-{boson_width_uncertainty: .3f}"
          f" GeV\n\
          Reduced chi squared={result[1] / (len(data_no_outliers)-2): .3f}\n\
          Boson lifetime = {lifetime_with_error} \n\
          Number of iterations={result[2]: d}\n\
          Number of function calls = {result[3]: d}")


if __name__ == "__main__":
    main()
