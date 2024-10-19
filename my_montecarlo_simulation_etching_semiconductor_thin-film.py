# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 10:09:26 2024

@author: CosimoSpagnolo
"""

#montecarlo simulation etching semiconductor thin-film

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to get user input using a single pop-up window
def get_user_inputs():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    input_dialog = tk.Toplevel()
    input_dialog.title("Enter Etching Parameters")

    labels = [
        "Number of samples:",
        "SiO2 thickness mean (nm):",
        "SiO2 thickness std deviation (nm):",
        "SiO2 etch rate mean (nm/min):",
        "SiO2 etch rate std deviation (nm/min):",
        "SiNx thickness mean (nm):",
        "SiNx thickness std deviation (nm):",
        "SiNx etch rate mean (nm/min):",
        "SiNx etch rate std deviation (nm/min):",
        "Etch time (minutes):",
        "Limit 1 for SiO2 (nm):",
        "Limit 2 for SiNx (nm):"
    ]
    defaults = [
        10000, 400, 3, 400, 4, 350, 3, 26, 4, 70 / 60, 400 + (3 * 3), 350 - 26
    ]

    entries = []
    for i, label_text in enumerate(labels):
        label = tk.Label(input_dialog, text=label_text)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(input_dialog)
        entry.insert(0, str(defaults[i]))
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    def submit():
        inputs = {
            'num_samples': int(entries[0].get()),
            'thickness_SiO2_mean': float(entries[1].get()),
            'thickness_SiO2_std': float(entries[2].get()),
            'etch_rate_SiO2_mean': float(entries[3].get()),
            'etch_rate_SiO2_std': float(entries[4].get()),
            'thickness_SiNx_mean': float(entries[5].get()),
            'thickness_SiNx_std': float(entries[6].get()),
            'etch_rate_SiNx_mean': float(entries[7].get()),
            'etch_rate_SiNx_std': float(entries[8].get()),
            'etch_time': float(entries[9].get()),
            'limit_1': float(entries[10].get()),
            'limit_2': float(entries[11].get())
        }
        root.inputs = inputs
        input_dialog.destroy()

    submit_button = tk.Button(input_dialog, text="Submit", command=submit)
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    input_dialog.wait_window()
    return root.inputs

# Main code
if __name__ == "__main__":
    inputs = get_user_inputs()

    num_samples = inputs['num_samples']
    thickness_SiO2_mean = inputs['thickness_SiO2_mean']
    thickness_SiO2_std = inputs['thickness_SiO2_std']
    etch_rate_SiO2_mean = inputs['etch_rate_SiO2_mean']
    etch_rate_SiO2_std = inputs['etch_rate_SiO2_std']

    thickness_SiNx_mean = inputs['thickness_SiNx_mean']
    thickness_SiNx_std = inputs['thickness_SiNx_std']
    etch_rate_SiNx_mean = inputs['etch_rate_SiNx_mean']
    etch_rate_SiNx_std = inputs['etch_rate_SiNx_std']
    etch_time = inputs['etch_time']
    limit_1 = inputs['limit_1']
    limit_2 = inputs['limit_2']

    # Function to generate random samples
    def generate_random_samples(mean, std, num_samples):
        return np.random.normal(mean, std, num_samples)

    # Function to calculate remaining thickness after etching
    def calculate_remaining_thickness(initial_thickness, etch_rate, etch_time):
        etched_amount = etch_rate * etch_time
        return np.maximum(initial_thickness - etched_amount, 0)

    # Generate random samples
    thickness_SiO2 = generate_random_samples(thickness_SiO2_mean, thickness_SiO2_std, num_samples)
    thickness_SiNx = generate_random_samples(thickness_SiNx_mean, thickness_SiNx_std, num_samples)
    etch_rate_SiO2 = generate_random_samples(etch_rate_SiO2_mean, etch_rate_SiO2_std, num_samples)
    etch_rate_SiNx = generate_random_samples(etch_rate_SiNx_mean, etch_rate_SiNx_std, num_samples)

    # Calculate etched amounts and remaining thicknesses
    etched_SiO2 = etch_rate_SiO2 * etch_time
    remaining_SiO2 = calculate_remaining_thickness(thickness_SiO2, etch_rate_SiO2, etch_time)

    # Calculate etching for SiNx
    time_after_SiO2_etched = np.maximum(etch_time - thickness_SiO2 / etch_rate_SiO2, 0)
    etched_SiNx = etch_rate_SiNx * time_after_SiO2_etched
    remaining_SiNx = calculate_remaining_thickness(thickness_SiNx, etch_rate_SiNx, time_after_SiO2_etched)

    # Calculate mean values for plotting
    mean_remaining_SiO2 = np.mean(remaining_SiO2)
    mean_remaining_SiNx = np.mean(remaining_SiNx)
    total_remaining = remaining_SiO2 + remaining_SiNx
    mean_total = np.mean(total_remaining)
    std_total_remaining = np.std(total_remaining)

    # Function to plot histograms
    def plot_histogram(ax, data, bins, color, label, title, xlabel, ylabel, mean_line=None):
        ax.hist(data, bins=bins, alpha=0.5, color=color, label=label)
        if mean_line is not None:
            ax.axvline(mean_line, color='red', linestyle='--', label=f'Mean: {mean_line:.1f} nm')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)

    # Create first figure with subplots
    fig1, axs1 = plt.subplots(2, 2, figsize=(18, 10))

    # Plot initial and final structure
    axs1[0, 0].bar(0, thickness_SiNx_mean, width=0.5, color='lightgreen', edgecolor='k', label=f'SiNx: {thickness_SiNx_mean:.1f} nm')
    axs1[0, 0].bar(0, thickness_SiO2_mean, width=0.5, bottom=thickness_SiNx_mean, color='skyblue', edgecolor='k', label=f'SiO₂: {thickness_SiO2_mean:.1f} nm')
    axs1[0, 0].set_title('Initial Structure')
    axs1[0, 0].set_ylabel('Thickness (nm)')
    axs1[0, 0].set_xticks([])
    axs1[0, 0].legend()
    axs1[0, 0].grid(True, linestyle='--', alpha=0.7)

    axs1[0, 1].bar(0, mean_remaining_SiNx, width=0.5, color='lightgreen', edgecolor='k', label=f'SiNx: {mean_remaining_SiNx:.1f} nm')
    axs1[0, 1].bar(0, mean_remaining_SiO2, width=0.5, bottom=mean_remaining_SiNx, color='skyblue', edgecolor='k', label=f'SiO₂: {mean_remaining_SiO2:.1f} nm')
    axs1[0, 1].set_title('After Etching')
    axs1[0, 1].set_xticks([])
    axs1[0, 1].legend()
    axs1[0, 1].grid(True, linestyle='--', alpha=0.7)
    axs1[0, 1].set_ylim(0, thickness_SiO2_mean + thickness_SiNx_mean + 100)

    # Plot histograms for remaining thicknesses
    plot_histogram(axs1[1, 0], remaining_SiO2, bins=50, color='skyblue', label='SiO₂',
                   title='Distribution of Remaining SiO₂ Thickness', xlabel='Thickness (nm)', ylabel='Frequency', mean_line=mean_remaining_SiO2)
    plot_histogram(axs1[1, 1], total_remaining, bins=50, color='gray', label='Total thickness',
                   title='Distribution of Total Remaining Thickness', xlabel='Thickness (nm)', ylabel='Frequency', mean_line=mean_total)

    plt.tight_layout()
    plt.show()

    # Create second figure with additional plots
    fig2, axs2 = plt.subplots(2, 2, figsize=(18, 10))

    # SiO2 before and after etching
    plot_histogram(axs2[0, 0], thickness_SiO2, bins=50, color='blue', label='Initial SiO₂',
                   title='SiO₂ Thickness Before and After Etching', xlabel='Thickness (nm)', ylabel='Frequency')
    plot_histogram(axs2[0, 0], remaining_SiO2, bins=50, color='skyblue', label='Remaining SiO₂',
                   title='SiO₂ Thickness Before and After Etching', xlabel='Thickness (nm)', ylabel='Frequency')

    # SiNx before and after etching
    plot_histogram(axs2[0, 1], thickness_SiNx, bins=50, color='green', label='Initial SiNx',
                   title='SiNx Thickness Before and After Etching', xlabel='Thickness (nm)', ylabel='Frequency')
    plot_histogram(axs2[0, 1], remaining_SiNx, bins=50, color='lightgreen', label='Remaining SiNx',
                   title='SiNx Thickness Before and After Etching', xlabel='Thickness (nm)', ylabel='Frequency')

    # Total thickness before and after etching
    plot_histogram(axs2[1, 0], thickness_SiO2 + thickness_SiNx, bins=50, color='gray', label='Initial Total Thickness',
                   title='Total Thickness Before and After Etching', xlabel='Thickness (nm)', ylabel='Frequency')
    plot_histogram(axs2[1, 0], total_remaining, bins=50, color='darkgray', label='Remaining Total Thickness',
                   title='Total Thickness Before and After Etching', xlabel='Thickness (nm)', ylabel='Frequency')

    plt.tight_layout()
    plt.show()

    # Function to calculate the area under the remaining normal distribution for a given value
    def calculate_area_remaining(value, material='SiO2'):
        if material == 'SiO2':
            mean = mean_remaining_SiO2
            std = np.std(remaining_SiO2)
            color = 'blue'
        elif material == 'SiNx':
            mean = mean_remaining_SiNx
            std = np.std(remaining_SiNx)
            color = 'green'
        else:
            raise ValueError("Material must be 'SiO2' or 'SiNx'")

        # Calculate the cumulative distribution function (CDF) for the given value
        cdf_value = norm.cdf(value, mean, std)
        area_percentage = cdf_value * 100
        print(f"The area under the remaining normal distribution curve for {material} at value {value:.0f} nm is {area_percentage:.2f}%.")

        # Plot the normal distribution and add a vertical line for the given value
        x = np.linspace(mean - 4 * std, mean + 4 * std, 1000)
        y = norm.pdf(x, mean, std)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label=f'Normal Distribution of Remaining {material}', color=color)
        plt.axvline(value, color='red', linestyle='--', label=f'Value: {value:.0f} nm ({area_percentage:.2f}%)')
        plt.fill_between(x, 0, y, where=(x <= value), color=color, alpha=0.3)
        plt.title(f'Normal Distribution of Remaining {material} Thickness')
        plt.xlabel('Thickness (nm)')
        plt.ylabel('Probability Density')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()

    # Set limits to check area percentage for remaining thickness
    calculate_area_remaining(limit_1, material='SiO2')
    calculate_area_remaining(limit_2, material='SiNx')

    # Display final results in a pop-up window
    results_message = (
        f"After etching for {etch_time:.2f} minutes:\n"
        f"Remaining SiO₂ thickness: {mean_remaining_SiO2:.2f} nm ± {np.std(remaining_SiO2):.2f} nm\n"
        f"Remaining SiNx thickness: {mean_remaining_SiNx:.2f} nm ± {np.std(remaining_SiNx):.2f} nm\n"
        f"Total remaining thickness: Mean: {mean_total:.2f} nm, Std: {std_total_remaining:.2f} nm\n"
    )
    messagebox.showinfo("Etching Results", results_message)
    
    
    # Display final results in a pop-up window
    results_message = (
        f"Cosimo - October 2024"
    )
    messagebox.showinfo("Credits", results_message)

    
