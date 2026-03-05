# Pendulum Simulation & Numerical Methods Toolbox

This project is a **Python desktop application built with PySide6** that provides tools for exploring **pendulum dynamics and numerical analysis methods**.
The application includes interactive visualizations using **Matplotlib** and scientific computation with **NumPy and SciPy**.

The goal of the project is to help students understand numerical methods and physical simulations through experimentation and visualization.

---

## Requirements

The project was developed and tested with:

* Python 3.11
* pip

The required Python libraries are listed in `requirements.txt`.

---

# Features

## Pendulum Simulation

The application simulates the motion of a pendulum using numerical ODE solvers.

Users can specify:

* Pendulum length
* Initial angle
* Initial angular velocity
* Maximum simulation time
* Optional damping

The program compares two numerical solvers:

* `odeint`
* `solve_ivp (RK45)`

The simulation generates plots for:

* Pendulum angle over time
* Kinetic energy
* Potential energy
* Total energy

An optional error comparison can also be displayed.

### Optimal Pendulum Length

The program can compute the pendulum length that minimizes the time required for the pendulum to reach the lowest point using **scalar optimization**.

---

## Numerical Methods Toolbox

The toolbox allows experimentation with various numerical algorithms.

### Root Finding

* Bisection Method
* Newton–Raphson Method
* Secant Method
* Method comparison with convergence analysis

### Interpolation

* Linear Interpolation
* Cubic Spline Interpolation

### Numerical Differentiation

* Forward Difference
* Backward Difference
* Central Difference

Error vs step-size plots are generated when the analytical derivative is provided.

### Numerical Integration

* Trapezoidal Rule
* Simpson’s Rule
* NumPy `trapz`
* SciPy `quad`

### Linear Algebra

* Linear system solver (Ax = b)
* LU decomposition

### Optimization

* Scalar function minimization using SciPy

### Floating-Point Error Demonstration

Demonstrates how floating-point summation order can affect numerical accuracy and visualizes error accumulation.

---

# Technologies Used

* Python 3.11
* PySide6 (Qt for Python)
* NumPy
* SciPy
* Matplotlib
* Qt Designer

---

# Installation

Clone the repository:

```
git clone https://github.com/Sulyenman/Pendulum_Simulation
```

Navigate to the project directory:

```
cd Pendulum_Simulation
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Running the Application

Run the program with:

```
python widget.py
```

---

# Project Structure

```
widget.py        # Main application logic
ui_form.py       # Generated UI Python file
form.ui          # Qt Designer interface file
requirements.txt # Project dependencies
```

---

# Purpose

This project was created as an educational tool to demonstrate **numerical methods, optimization, and physical simulation** through an interactive desktop interface.

It was developed to practice building **scientific computing applications with Python and Qt**.
