import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import base64
import dash_mantine_components as dmc

from io import BytesIO


def calculate_stress_matrix(
    s1: float, 
    s2: float, 
    s3: float
):
    """Calculate the stress matrix for the given principal stresses.
    Args:
        s1: The first principal stress.
        s2: The second principal stress.
        s3: The third principal stress.
    Returns:
        A 3x3 NumPy array representing the stress matrix.

    """
    stress_matrix = np.zeros((3, 3))
    stress_matrix[0, 0] = s1
    stress_matrix[1, 1] = s2
    stress_matrix[2, 2] = s3
    return stress_matrix

def calculate_rotation_matrix(
    alpha, 
    beta, 
    gamma
):
    """Calculate the rotation matrix for the given Euler angles.
    Args:
        alpha: First Euler angle (rotation about the x-axis).
        beta: Second Euler angle (rotation about the y-axis).
        gamma: Third Euler angle (rotation about the z-axis).
    Returns:
        A 3x3 NumPy array representing the rotation matrix.

    """
    a = np.deg2rad(alpha)
    b = np.deg2rad(beta)
    g = np.deg2rad(gamma)
    rotation_matrix = np.zeros((3, 3))
    cos_a = np.cos(a); cos_b = np.cos(b); cos_g = np.cos(g)
    sin_a = np.sin(a); sin_b = np.sin(b); sin_g = np.sin(g)
    rotation_matrix[0, 0] = cos_a * cos_b
    rotation_matrix[0, 1] = sin_a * cos_b
    rotation_matrix[0, 2] = -sin_b
    rotation_matrix[1, 0] = cos_a * sin_b * sin_g - sin_a * cos_g
    rotation_matrix[1, 1] = sin_a * sin_b * sin_g + cos_a * cos_g
    rotation_matrix[1, 2] = cos_b * sin_g
    rotation_matrix[2, 0] = cos_a * sin_b * cos_g + sin_a * sin_g
    rotation_matrix[2, 1] = sin_a * sin_b * cos_g - cos_a * sin_g
    rotation_matrix[2, 2] = cos_b * cos_g
    return rotation_matrix

def calculate_borehole_rotation_matrix(
    azimuth, 
    inclination
):
    """Calculate the borehole rotation matrix for the given azimuth and inclination.
    Args:
        azimuth: Azimuth angle in radians.
        inclination: Inclination angle in radians.
    Returns:
        A 3x3 NumPy array representing the borehole rotation matrix.

    """
    rotation_matrix = np.zeros((3, 3))
    cos_az = np.cos(azimuth); cos_inc = np.cos(inclination)
    sin_az = np.sin(azimuth); sin_inc = np.sin(inclination)
    rotation_matrix[0, 0] = -cos_az * cos_inc
    rotation_matrix[0, 1] = -sin_az * cos_inc
    rotation_matrix[0, 2] = sin_inc
    rotation_matrix[1, 0] = sin_az
    rotation_matrix[1, 1] = -cos_az
    rotation_matrix[1, 2] = 0
    rotation_matrix[2, 0] = cos_az * sin_inc
    rotation_matrix[2, 1] = sin_az * sin_inc
    rotation_matrix[2, 2] = cos_inc
    return rotation_matrix

def calculate_tangential_stress(
    stress_matrix, 
    theta, 
    poisson_ratio, 
    pressure_difference
):
    """Calculate the maximum and minimum tangential stresses for the given stress tensor.
    Args:
        stress_matrix: A 3x3 NumPy array representing the stress tensor.
        theta: Angle (in degrees) at which to calculate the stresses.
        poisson_ratio: Poisson's ratio of the material.
        pressure_difference: Pressure difference applied to the system.
    Returns:
        A tuple containing:
        - Maximum tangential stress.
        - Minimum tangential stress.
        - Shear stress.

    """
    cos_theta = np.cos(np.deg2rad(theta))
    sin_theta = np.sin(np.deg2rad(theta))
    cos_2theta = np.cos(2 * np.deg2rad(theta))
    sin_2theta = np.sin(2 * np.deg2rad(theta))
    s11 = stress_matrix[0, 0]
    s22 = stress_matrix[1, 1]
    s33 = stress_matrix[2, 2]
    s12 = stress_matrix[0, 1]
    s23 = stress_matrix[1, 2]
    s13 = stress_matrix[0, 2]
    szz = s33 - 2 * poisson_ratio * (s11 - s22) * cos_2theta - 4 * poisson_ratio * s12 * sin_2theta
    stt = s11 + s22 - 2 * (s11 - s22) * cos_2theta - 4 * s12 * sin_2theta - pressure_difference
    tau = 2 * (s23 * cos_theta - s13 * sin_theta)
    ts_max = 0.5 * (szz + stt + np.sqrt((szz - stt) ** 2 + 4 * tau ** 2))
    ts_min = 0.5 * (szz + stt - np.sqrt((szz - stt) ** 2 + 4 * tau ** 2))
    return ts_max, ts_min, tau, stt

def generate_plot(
    pore_pressure, 
    mud_pressure, 
    s1, 
    s2, 
    s3,
    poisson_ratio, 
    tensile_strength, 
    alpha_angle, 
    beta_angle, 
    gamma_angle, 
    specific_azimuth=270, 
    specific_inclination=60
):
    """Generate a polar plot of mud pressure required for tensile failure and convert it to a base64-encoded image.
    
    Returns:
        A base64-encoded string of the generated plot.

    """
    azimuth_list = np.radians(np.arange(0, 362, 2))
    inclination_list = np.radians(np.arange(0, 92, 2))
    azimuth_mesh, inclination_mesh = np.meshgrid(azimuth_list, inclination_list)
    theta = np.arange(0, 180, 0.1)
    mud_pressure_required = azimuth_mesh.copy() * 0.0
    # Adjust stresses by subtracting pore pressure
    s1 -= pore_pressure
    s2 -= pore_pressure
    s3 -= pore_pressure
    pressure_difference = pore_pressure - mud_pressure
    stress_matrix = calculate_stress_matrix(s1, s2, s3)
    rotation_matrix = calculate_rotation_matrix(alpha_angle, beta_angle, gamma_angle)
    for ia, azimuth in enumerate(azimuth_list):
        for ii, inclination in enumerate(inclination_list):
            borehole_rotation_matrix = calculate_borehole_rotation_matrix(azimuth, inclination)
            transformed_stress = (
                borehole_rotation_matrix @ rotation_matrix.T @ stress_matrix
                @ rotation_matrix @ borehole_rotation_matrix.T
            )
            _, _, _, stt = calculate_tangential_stress(
                transformed_stress, theta, poisson_ratio, pressure_difference
            )
            mud_pressure_required[ii, ia] = np.min(stt) - tensile_strength + pore_pressure
    fig, ax = plt.subplots(dpi=120, subplot_kw=dict(projection='polar'))
    contour = ax.contourf(azimuth_mesh, np.rad2deg(inclination_mesh), mud_pressure_required, 100, cmap='jet_r')
    ax.set_rmax(90)
    ax.set_rticks([0, 30, 60, 90])
    colorbar = fig.colorbar(contour, pad=0.15, shrink=0.75, format='%.0f')
    colorbar.set_label("Mud Pressure Required for Tensile Failure [MPa]")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    specific_azimuth_rad = np.radians(specific_azimuth)  # Convert azimuth to radians
    ax.plot(specific_azimuth_rad, specific_inclination, 'wo', markersize=8, markeredgecolor='k', label='Current well orientation')
    ax.legend(loc='upper right', bbox_to_anchor=(1.5, 1.1), frameon=False)
    plt.tight_layout()
    # Convert the plot to a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    return image_base64