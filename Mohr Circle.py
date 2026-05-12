import numpy as np
import matplotlib.pyplot as plt

def plot_3d_mohr_circle(stress_tensor):
    """
    Calculates and plots the 3D Mohr's Circles from a 3x3 stress tensor.
    
    Args:
        stress_tensor (numpy.ndarray): A 3x3 symmetric matrix representing the stress tensor.
    """
    # 1. Calculate principal stresses (eigenvalues of the stress tensor)
    # np.linalg.eigvalsh is used for Hermitian/Symmetric matrices
    principal_stresses = np.linalg.eigvalsh(stress_tensor)
    
    # 2. Sort principal stresses in descending order: sigma1 >= sigma2 >= sigma3
    principal_stresses = np.sort(principal_stresses)[::-1]
    sigma1, sigma2, sigma3 = principal_stresses
    
    # 3. Print the results
    print("-" * 30)
    print("--- Principal Stresses ---")
    print(f"σ1 (Maximum): {sigma1:.4f}")
    print(f"σ2 (Intermediate): {sigma2:.4f}")
    print(f"σ3 (Minimum): {sigma3:.4f}")
    
    # 4. Calculate centers and radii for the 3 circles
    # Circle 1 (Largest): between sigma1 and sigma3
    C1 = (sigma1 + sigma3) / 2
    R1 = (sigma1 - sigma3) / 2
    
    # Circle 2: between sigma1 and sigma2
    C2 = (sigma1 + sigma2) / 2
    R2 = (sigma1 - sigma2) / 2
    
    # Circle 3: between sigma2 and sigma3
    C3 = (sigma2 + sigma3) / 2
    R3 = (sigma2 - sigma3) / 2
    
    # Maximum shear stress
    tau_max = R1
    print(f"\nMaximum Shear Stress (τ_max): {tau_max:.4f}")
    print("-" * 30)
    
    # 5. Plot the circles
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create angles for drawing the circles (full circle)
    theta = np.linspace(0, 2 * np.pi, 200)
    
    # Helper function to plot a circle
    def draw_circle(ax, center, radius, color, label):
        x = center + radius * np.cos(theta)
        y = radius * np.sin(theta)
        ax.plot(x, y, color=color, label=label, linewidth=2)
        ax.plot(center, 0, marker='+', color=color, markersize=8) # Center marker

    # Draw the three circles
    draw_circle(ax, C1, R1, 'blue', "Circle 1 (σ1 - σ3)")
    draw_circle(ax, C2, R2, 'green', "Circle 2 (σ1 - σ2)")
    draw_circle(ax, C3, R3, 'red', "Circle 3 (σ2 - σ3)")
    
    # Formatting the plot
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('Normal Stress (σ)')
    ax.set_ylabel('Shear Stress (τ)')
    ax.set_title("3D Mohr's Circle")
    
    # Plot principal stress points on the x-axis
    ax.plot([sigma1, sigma2, sigma3], [0, 0, 0], 'ko', label="Principal Stresses")
    
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("=" * 40)
    print("   3D Mohr's Circle Calculator")
    print("=" * 40)
    print("Enter the 3D stress tensor components:")
    try:
        # Get input for the 6 independent components of the symmetric stress tensor
        sigma_xx = float(input("σ_xx [Normal stress x]: "))
        sigma_yy = float(input("σ_yy [Normal stress y]: "))
        sigma_zz = float(input("σ_zz [Normal stress z]: "))
        tau_xy = float(input("τ_xy [Shear stress xy]: "))
        tau_yz = float(input("τ_yz [Shear stress yz]: "))
        tau_zx = float(input("τ_zx [Shear stress zx]: "))
        
        # Construct the symmetric 3x3 stress matrix
        stress_matrix = np.array([
            [sigma_xx, tau_xy, tau_zx],
            [tau_xy, sigma_yy, tau_yz],
            [tau_zx, tau_yz, sigma_zz]
        ])
        
        print("\nInput Stress Tensor:")
        print(stress_matrix)
        print("\nCalculating & Plotting...")
        
        plot_3d_mohr_circle(stress_matrix)
        
    except ValueError:
        print("\n❌ Error: Please enter valid numerical values.")
    except ImportError:
        print("\n❌ Error: Required libraries not found. Please run:")
        print("pip install numpy matplotlib")