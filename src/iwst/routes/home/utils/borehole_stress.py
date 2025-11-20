import numpy as np
import plotly.graph_objects as go
import dash_mantine_components as dmc

from typing import Tuple


def calculate_stress_matrix(
    s1: float, 
    s2: float, 
    s3: float
) -> np.ndarray:
    """Calculate the stress matrix for the given principal stresses.
    This function constructs a 3x3 diagonal stress matrix using the provided
    principal stresses. The matrix is zero everywhere except on the diagonal,
    where the principal stresses are placed.

    Args:
        s1: The first principal stress.
        s2: The second principal stress.
        s3: The third principal stress.

    Returns:
        A 3x3 NumPy array representing the stress matrix.

    """
    stress_matrix: np.ndarray = np.zeros((3, 3), dtype=float)
    stress_matrix[0, 0] = s1
    stress_matrix[1, 1] = s2
    stress_matrix[2, 2] = s3
    return stress_matrix

def calculate_rotation_matrix(
    alpha: float, 
    beta: float, 
    gamma: float
) -> np.ndarray:
    """Calculate the rotation matrix for the given Euler angles.
    This function constructs a 3x3 rotation matrix using the provided Euler angles.
    The angles represent rotations about the x-axis, y-axis, and z-axis, respectively.

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
    rotation_matrix: np.ndarray = np.zeros((3, 3), dtype=float)
    cos_a = np.cos(a)
    cos_b = np.cos(b)
    cos_g = np.cos(g)
    sin_a = np.sin(a)
    sin_b = np.sin(b)
    sin_g = np.sin(g)
    rotation_matrix[0, 0] = cos_a * cos_b
    rotation_matrix[0, 1] = sin_a * cos_b
    rotation_matrix[0, 2] = -sin_b
    rotation_matrix[1, 0] = (
        cos_a * sin_b * sin_g - sin_a * cos_g
    )
    rotation_matrix[1, 1] = (
        sin_a * sin_b * sin_g + cos_a * cos_g
    )
    rotation_matrix[1, 2] = cos_b * sin_g
    rotation_matrix[2, 0] = (
        cos_a * sin_b * cos_g + sin_a * sin_g
    )
    rotation_matrix[2, 1] = (
        sin_a * sin_b * cos_g - cos_a * sin_g
    )
    rotation_matrix[2, 2] = cos_b * cos_g
    return rotation_matrix

def calculate_rotation_matrix_azimuth_inclination(
    az: float, 
    ic: float
) -> np.ndarray:
    """Calculate the rotation matrix for azimuth and inclination angles.
    This function constructs a 3x3 rotation matrix using the provided azimuth
    and inclination angles. The matrix represents the orientation based on these angles.

    Args:
        az: Azimuth angle (in degrees).
        ic: Inclination angle (in degrees).

    Returns:
        A 3x3 NumPy array representing the rotation matrix.

    """
    azimuth_rad = np.deg2rad(az)  
    inclination_rad = np.deg2rad(ic)  
    rotation_matrix: np.ndarray = np.zeros((3, 3), dtype=float)
    cos_az = np.cos(azimuth_rad)
    cos_ic = np.cos(inclination_rad)
    sin_az = np.sin(azimuth_rad)
    sin_ic = np.sin(inclination_rad)
    rotation_matrix[0, 0] = -cos_az * cos_ic  
    rotation_matrix[0, 1] = -sin_az * cos_ic  
    rotation_matrix[0, 2] = sin_ic            
    rotation_matrix[1, 0] = sin_az        
    rotation_matrix[1, 1] = -cos_az           
    rotation_matrix[1, 2] = 0                
    rotation_matrix[2, 0] = cos_az * sin_ic   
    rotation_matrix[2, 1] = sin_az * sin_ic   
    rotation_matrix[2, 2] = cos_ic            
    return rotation_matrix

def calculate_tangential_stress(
    stress_matrix: np.ndarray, 
    theta: float, 
    poisson_ratio: float, 
    pressure_difference: float
) -> Tuple[float, float, float, float]:
    """Calculate the tangential stress components for the given stress tensor.
    This function computes the maximum and minimum tangential stresses, as well as
    the axium stresses, based on the provided stress matrix, angle, Poisson's ratio,
    and pressure difference.

    Args:
        stress_matrix: A 3x3 NumPy array representing the stress tensor.
        theta: Angle (in degrees) at which to calculate the stresses.
        poisson_ratio: Poisson's ratio of the material.
        pressure_difference: Pressure difference applied to the system.

    Returns:
        A tuple containing:
        - Maximum tangential stress.
        - Minimum tangential stress.
        - Axium stress in the z-direction (szz).
        - Axium stress in the tangential direction (stt).

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
    axium_zz = (
        s33 - 2 * poisson_ratio * (s11 - s22) * cos_2theta
        - 4 * poisson_ratio * s12 * sin_2theta
    )
    axium_tt = (
        s11 + s22 - 2 * (s11 - s22) * cos_2theta
        - 4 * s12 * sin_2theta - pressure_difference
    )
    shear_tau = 2 * (s23 * cos_theta - s13 * sin_theta)
    max_tangential_stress = (
        axium_zz + axium_tt + np.sqrt((axium_zz - axium_tt) ** 2 + 4 * shear_tau ** 2)
    ) / 2
    min_tangential_stress = (
        axium_zz + axium_tt - np.sqrt((axium_zz - axium_tt) ** 2 + 4 * shear_tau ** 2)
    ) / 2
    return max_tangential_stress, min_tangential_stress, axium_zz, axium_tt

def calculate_mohr_coulomb_circle(
    max_principal_stress: float, 
    min_principal_stress: float
) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate the Mohr-Coulomb failure circle for the given principal stresses.
    This function computes the x and y coordinates of the Mohr-Coulomb failure circle
    based on the maximum and minimum principal stresses.

    Args:
        max_principal_stress: Maximum principal stress.
        min_principal_stress: Minimum principal stress.

    Returns:
        A tuple containing:
        - x-coordinates of the Mohr-Coulomb circle.
        - y-coordinates of the Mohr-Coulomb circle.

    """
    step = 1e-4
    radius = (max_principal_stress - min_principal_stress) / 2
    x_coordinates = np.arange(-radius, radius + step, step)
    y_squared = radius**2 - x_coordinates**2
    y_squared[y_squared < 0] = 0.0
    y_coordinates = np.sqrt(y_squared)
    x_coordinates += min_principal_stress + radius
    return x_coordinates, y_coordinates

def plot_mohr_coulomb_failure(
    max_principal_stress: float, 
    intermediate_principal_stress: float, 
    min_principal_stress: float, 
    friction_coefficient: float
) -> float:
    """Plot the Mohr-Coulomb failure circles and calculate the Unconfined Compressive Strength (UCS).
    This function plots the Mohr-Coulomb failure circles for the given principal stresses
    and calculates the UCS based on the internal friction coefficient.

    Args:
        max_principal_stress: Maximum principal stress.
        intermediate_principal_stress: Intermediate principal stress.
        min_principal_stress: Minimum principal stress.
        friction_coefficient: Internal friction coefficient (Mu).

    Returns:
        Unconfined Compressive Strength (UCS).
        
    """
    x_coords_max_min, y_coords_max_min = calculate_mohr_coulomb_circle(
        max_principal_stress, min_principal_stress
    )
    x_coords_max_intermediate, y_coords_max_intermediate = calculate_mohr_coulomb_circle(
        max_principal_stress, intermediate_principal_stress
    )
    x_coords_intermediate_min, y_coords_intermediate_min = calculate_mohr_coulomb_circle(
        intermediate_principal_stress, min_principal_stress
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_coords_max_min, y=y_coords_max_min, mode='lines', name='Max-Min Circle'))
    fig.add_trace(go.Scatter(x=x_coords_max_intermediate, y=y_coords_max_intermediate, mode='lines', name='Max-Intermediate Circle'))
    fig.add_trace(go.Scatter(x=x_coords_intermediate_min, y=y_coords_intermediate_min, mode='lines', name='Intermediate-Min Circle'))
    ucs = (
        max_principal_stress - min_principal_stress
        * ((friction_coefficient**2 + 1)**0.5 + friction_coefficient)**2
    )
    intercept = (
        (max_principal_stress - min_principal_stress)
        / 2 / ((friction_coefficient**2 + 1)**0.5 + friction_coefficient)
    )
    x_failure = np.linspace(0, max_principal_stress * 1.5, 100)
    y_failure = x_failure * friction_coefficient + intercept
    fig.add_trace(go.Scatter(x=x_failure, y=y_failure, mode='lines', name='Failure Envelope', line=dict(color='grey')))
    fig.update_layout(
        xaxis_title=r'$S_n$ [MPa]',
        yaxis_title=r'$\tau$ [MPa]',
        legend_title='Legend',
        showlegend=True,
        xaxis_range=[0, max_principal_stress * 1.5],
        yaxis_range=[0, max_principal_stress],
        template='plotly_white'
    )
    return ucs