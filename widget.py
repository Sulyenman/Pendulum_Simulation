import sys
import math
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout
from PySide6.QtWidgets import QLineEdit, QComboBox, QPushButton, QTextEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time



# Canvas class
class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3):
        self.fig = Figure(figsize=(width, height))
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.fig.tight_layout()


# Main window
class PendulumApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        file = QFile("form.ui")
        if not file.open(QIODevice.ReadOnly):
            QMessageBox.critical(self, "Error", f"Cannot open UI file: {file.errorString()}")
            sys.exit(1)

        self.ui = loader.load(file, self)
        file.close()

        self.setWindowTitle("Pendulum Simulation")
        self.resize(1100, 600)
        self.setup_ui()





    def setup_ui(self):
        # Pendulum Inputs
        self.length_input = self.ui.findChild(type(self.ui.length_input), "length_input")
        self.angle_input = self.ui.findChild(type(self.ui.angle_input), "angle_input")
        self.omega_input = self.ui.findChild(type(self.ui.omega_input), "omega_input")
        self.time_input = self.ui.findChild(type(self.ui.time_input), "time_input")
        self.simulate_button = self.ui.findChild(type(self.ui.simulate_button), "simulate_button")

        # Plot containers from UI
        main_plot_widget = self.ui.findChild(type(self.ui.angle_plot_widget), "angle_plot_widget")
        energy_plot_widget = self.ui.findChild(type(self.ui.energy_plot_widget), "energy_plot_widget")
        aux_plot_widget = self.ui.findChild(type(self.ui.convergence_plot_widget), "convergence_plot_widget")

        # Matplotlib canvases
        self.main_plot_canvas = MatplotlibCanvas(self)    # Used for pendulum angle and toolbox method plots
        self.energy_canvas = MatplotlibCanvas(self)       # Only used for energy plots
        self.aux_plot_canvas = MatplotlibCanvas(self)     # Used for convergence, error analysis, toolbox graphs

        # Layouts for plot widgets
        main_layout = QVBoxLayout(main_plot_widget)
        main_layout.addWidget(self.main_plot_canvas)

        energy_layout = QVBoxLayout(energy_plot_widget)
        energy_layout.addWidget(self.energy_canvas)

        aux_layout = QVBoxLayout(aux_plot_widget)
        aux_layout.addWidget(self.aux_plot_canvas)

        # Checkbox and result label setup
        self.error_checkbox = self.ui.findChild(type(self.ui.error_compare_checkbox), "error_compare_checkbox")
        self.damping_checkbox = self.ui.findChild(type(self.ui.damping_checkbox), "damping_checkbox")
        self.find_opt_button = self.ui.findChild(type(self.ui.find_optimal_length_button), "find_optimal_length_button")
        self.optimal_result_label = self.ui.findChild(type(self.ui.optimal_length_result_label), "optimal_length_result_label")

        self.simulate_button.clicked.connect(self.simulate_pendulum)
        self.find_opt_button.clicked.connect(self.find_optimal_length)

        # Toolbox input elements
        self.func_input = self.ui.findChild(QLineEdit, "func_input")
        self.param1_input = self.ui.findChild(QLineEdit, "param1_input")
        self.param2_input = self.ui.findChild(QLineEdit, "param2_input")
        self.method_select = self.ui.findChild(QComboBox, "method_select")
        self.run_method_button = self.ui.findChild(QPushButton, "run_method_button")
        self.toolbox_output = self.ui.findChild(QTextEdit, "toolbox_output")



        self.run_method_button.clicked.connect(self.run_selected_method)



        self.method_select.addItems([
            "Root Finding - Bisection",
            "Root Finding - Newton-Raphson",
            "Root Finding - Secant",
            "Root Finding - Compare All Methods",

            "Interpolation - Linear",
            "Interpolation - Cubic Spline",

            "Numerical Differentiation - Forward",
            "Numerical Differentiation - Backward",
            "Numerical Differentiation - Central",

            "Numerical Integration - Trapezoidal",
            "Numerical Integration - Simpson",
            "Numerical Integration - trapz (SciPy)",
            "Numerical Integration - quad (SciPy)",

            "Linear System Solver",
            "Linear System - LU Decomposition",

            "Optimization - Scalar Minimization",

            "Floating-Point - Error Accumulation Demo",
            ])


    def custom_bisection(self, f, a, b, tol=1e-6, max_iter=100):
        if f(a) * f(b) >= 0:
            raise ValueError("f(a) and f(b) must have opposite signs")
        errors = []
        for i in range(max_iter):
            c = (a + b) / 2
            error = abs(b - a) / 2
            errors.append(error)
            if abs(f(c)) < tol or error < tol:
                return c, i + 1, errors
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        raise RuntimeError("Max iterations reached in bisection")

    def custom_newton_raphson(self, f, x0, tol=1e-6, max_iter=100):
        errors = []
        def f_prime(x):
            h = 1e-5
            return (f(x + h) - f(x - h)) / (2 * h)
        for i in range(max_iter):
            fx = f(x0)
            dfx = f_prime(x0)
            if dfx == 0:
                raise ZeroDivisionError("Derivative zero.")
            x1 = x0 - fx / dfx
            error = abs(x1 - x0)
            errors.append(error)
            if abs(fx) < tol or error < tol:
                return x1, i + 1, errors
            x0 = x1
        raise RuntimeError("Max iterations reached in Newton-Raphson")


    def custom_secant(self, f, x0, x1, tol=1e-6, max_iter=100):
        errors = []
        for i in range(max_iter):
            fx0 = f(x0)
            fx1 = f(x1)
            if fx1 - fx0 == 0:
                raise ZeroDivisionError("Divide by zero in Secant")
            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            error = abs(x2 - x1)
            errors.append(error)
            if abs(fx1) < tol or error < tol:
                return x2, i + 1, errors
            x0, x1 = x1, x2
        raise RuntimeError("Max iterations reached in Secant")



    def simulate_pendulum(self):
        try:
            L = float(self.length_input.text())
            theta0_deg = float(self.angle_input.text())
            omega0 = float(self.omega_input.text())
            t_max = float(self.time_input.text())
        except:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers.")
            return

        g = 9.81
        theta0_rad = math.radians(theta0_deg)
        y0 = [theta0_rad, omega0]

        # Damping value
        damping = 0.1 if (self.damping_checkbox.isChecked()) else 0.0

        # Define ODE
        def ode(y, t):
            return [y[1], - (g / L) * math.sin(y[0]) - damping * y[1]]

        t = np.linspace(0, t_max, 500)

        # Solve with odeint
        start_odeint = time.time()
        sol_odeint = odeint(ode, y0, t)
        end_odeint = time.time()
        theta_odeint = sol_odeint[:, 0]
        omega_odeint = sol_odeint[:, 1]

        # Solve with solve_ivp (RK45)
        start_rk = time.time()
        sol_rk = solve_ivp(lambda t, y: ode(y, t), [0, t_max], y0, t_eval=t, method='RK45')
        end_rk = time.time()
        theta_rk = sol_rk.y[0]

        # Plot angle comparison
        self.main_plot_canvas.axes.clear()
        self.main_plot_canvas.axes.plot(t, theta_odeint, label="θ(t) - odeint", color="blue")
        self.main_plot_canvas.axes.plot(t, theta_rk, '--', label="θ(t) - RK45", color="magenta")

        # Optional: error comparison with fewer points
        if self.error_checkbox and self.error_checkbox.isChecked():
            t_low = np.linspace(0, t_max, 100)
            sol_low = odeint(ode, y0, t_low)
            theta_low = sol_low[:, 0]
            self.main_plot_canvas.axes.plot(t_low, theta_low, ':', label="θ(t) - 100 pts", color="gray", linewidth=2)

        self.main_plot_canvas.axes.set_title("Pendulum Motion - Solver Comparison")
        self.main_plot_canvas.axes.set_xlabel("Time (s)")
        self.main_plot_canvas.axes.set_ylabel("Angle (rad)")
        self.main_plot_canvas.axes.grid(True)
        self.main_plot_canvas.axes.legend()
        self.main_plot_canvas.fig.tight_layout()
        self.main_plot_canvas.draw()

        # Energy using odeint result
        m = 1.0
        KE = 0.5 * m * (L * omega_odeint) ** 2
        PE = m * g * L * (1 - np.cos(theta_odeint))
        total_E = KE + PE

        self.energy_canvas.axes.clear()
        self.energy_canvas.axes.plot(t, KE, label="Kinetic", color="green")
        self.energy_canvas.axes.plot(t, PE, label="Potential", color="orange")
        self.energy_canvas.axes.plot(t, total_E, label="Total", color="red")
        self.energy_canvas.axes.set_title("Pendulum Energy (odeint)")
        self.energy_canvas.axes.set_xlabel("Time (s)")
        self.energy_canvas.axes.set_ylabel("Energy (J)")
        self.energy_canvas.axes.grid(True)
        self.energy_canvas.axes.legend()
        self.energy_canvas.fig.tight_layout()
        self.energy_canvas.draw()

        # Optional: print times to terminal
        print(f"odeint time: {end_odeint - start_odeint:.6f}s")
        print(f"RK45 time:   {end_rk - start_rk:.6f}s")


    def find_optimal_length(self):
        try:
            angle0 = float(self.angle_input.text())
            omega0 = float(self.omega_input.text())
            t_max = float(self.time_input.text())
        except:
            QMessageBox.warning(self, "Input Error", "Enter valid initial conditions.")
            return

        g = 9.81
        theta0_rad = math.radians(angle0)
        y0 = [theta0_rad, omega0]

        def time_to_bottom(length):
            if length <= 0: return 1000  # invalid
            def ode(y, t):
                return [y[1], - (g / length) * math.sin(y[0])]

            t_vals = np.linspace(0, t_max, 1000)
            sol = odeint(ode, y0, t_vals)
            angles = sol[:, 0]

            for i, theta in enumerate(angles):
                if abs(theta) < 0.01:
                    return t_vals[i]  # reached near bottom
            return t_max  # didn’t reach

        from scipy.optimize import minimize_scalar
        result = minimize_scalar(time_to_bottom, bounds=(0.1, 5), method='bounded')

        if result.success:
            L_opt = result.x
            T_opt = result.fun
            self.optimal_result_label.setText(f"Optimal Length: {L_opt:.3f} m\nTime to bottom: {T_opt:.2f} s")
        else:
            self.optimal_result_label.setText("Optimization failed.")


    def run_selected_method(self):
        from scipy.interpolate import interp1d
        from scipy.linalg import lu

        f_str = self.func_input.text()
        method = self.method_select.currentText()
        self.main_plot_canvas.axes.clear()
        self.energy_canvas.axes.clear()
        self.main_plot_canvas.draw()
        self.energy_canvas.draw()

        output = ""

        # Safe function parsing only for methods that need a function
        f = None
        if any(kw in method for kw in [
            "Root Finding", "Interpolation - Linear", "Numerical Differentiation", "Numerical Integration", "Optimization"
        ]):
            try:
                f = lambda x: eval(f_str, {"x": x, "np": np, "math": math})
            except Exception as e:
                self.toolbox_output.setText(f"Invalid function input: {e}")
                return

        # Parse exact derivative if provided (used for error plots in differentiation)
        deriv_str = self.param2_input.text()
        try:
            f_prime_exact = lambda x: eval(deriv_str, {"x": x, "np": np, "math": math})
        except:
            f_prime_exact = None

        #  Input parsing
        a_text = self.param1_input.text()
        b_text = self.param2_input.text()
        a = b = None

        try:
            if method in ["Interpolation - Linear"]:
                a = float(a_text) if a_text else None

            elif method in [
                "Linear System Solver",
                "Linear System - LU Decomposition",
                "Interpolation - Cubic Spline"
            ]:
                pass  # Skip float conversion, use eval in respective blocks

            else:
                a = float(a_text) if a_text else None
                b = float(b_text) if b_text else None

        except:
            self.toolbox_output.setText(" Invalid parameter input.")
            return


        try:
            if method == "Root Finding - Bisection":
                if a is None or b is None:
                    output = " Bisection requires a and b."
                else:
                    try:
                        root, iters, errors = self.custom_bisection(f, a, b)
                        output = f"Bisection Root: {root:.12f} in {iters} iterations"

                        # Plot function
                        x_vals = np.linspace(a, b, 400)
                        y_vals = [f(x) for x in x_vals]
                        self.plot_result(x_vals, y_vals, label="f(x)", title="Bisection - Function Plot", ylabel="f(x)")

                        # Mark root
                        self.main_plot_canvas.axes.plot([root], [f(root)], 'ro', label="Root")
                        self.main_plot_canvas.axes.legend()
                        self.main_plot_canvas.draw()

                        # Plot convergence
                        self.aux_plot_canvas.axes.clear()
                        self.aux_plot_canvas.axes.plot(range(1, len(errors)+1), errors, marker='o', color='blue')
                        self.aux_plot_canvas.axes.set_yscale("log")
                        self.aux_plot_canvas.axes.set_title("Bisection Convergence")
                        self.aux_plot_canvas.axes.set_xlabel("Iteration")
                        self.aux_plot_canvas.axes.set_ylabel("Absolute Error")
                        self.aux_plot_canvas.axes.grid(True)
                        self.aux_plot_canvas.draw()

                    except Exception as e:
                        output = f"Error: {str(e)}"



            elif method == "Root Finding - Newton-Raphson":
                if a is None:
                    output = "Newton-Raphson requires x₀ (a)."
                else:
                    try:
                        root, iters, errors = self.custom_newton_raphson(f, a)
                        output = f"Newton-Raphson Root: {root:.12f} in {iters} iterations"

                        x_vals = np.linspace(a - 5, a + 5, 400)
                        y_vals = [f(x) for x in x_vals]
                        self.plot_result(x_vals, y_vals, label="f(x)", title="Newton-Raphson - Function Plot", ylabel="f(x)")
                        self.main_plot_canvas.axes.plot([root], [f(root)], 'ro', label="Root")
                        self.main_plot_canvas.axes.legend()
                        self.main_plot_canvas.draw()

                        self.aux_plot_canvas.axes.clear()
                        self.aux_plot_canvas.axes.plot(range(1, len(errors)+1), errors, marker='s', color='green')
                        self.aux_plot_canvas.axes.set_yscale("log")
                        self.aux_plot_canvas.axes.set_title("Newton-Raphson Convergence")
                        self.aux_plot_canvas.axes.set_xlabel("Iteration")
                        self.aux_plot_canvas.axes.set_ylabel("Absolute Error")
                        self.aux_plot_canvas.axes.grid(True)
                        self.aux_plot_canvas.draw()

                    except Exception as e:
                        output = f"Error: {str(e)}"



            elif method == "Root Finding - Secant":
                if a is None or b is None:
                    output = "Secant requires x₀ (a) and x₁ (b)."
                else:
                    try:
                        root, iters, errors = self.custom_secant(f, a, b)
                        output = f"Secant Root: {root:.12f} in {iters} iterations"

                        x_vals = np.linspace(min(a, b) - 2, max(a, b) + 2, 400)
                        y_vals = [f(x) for x in x_vals]
                        self.plot_result(x_vals, y_vals, label="f(x)", title="Secant - Function Plot", ylabel="f(x)")
                        self.main_plot_canvas.axes.plot([root], [f(root)], 'ro', label="Root")
                        self.main_plot_canvas.axes.legend()
                        self.main_plot_canvas.draw()

                        self.aux_plot_canvas.axes.clear()
                        self.aux_plot_canvas.axes.plot(range(1, len(errors)+1), errors, marker='^', color='purple')
                        self.aux_plot_canvas.axes.set_yscale("log")
                        self.aux_plot_canvas.axes.set_title("Secant Convergence")
                        self.aux_plot_canvas.axes.set_xlabel("Iteration")
                        self.aux_plot_canvas.axes.set_ylabel("Absolute Error")
                        self.aux_plot_canvas.axes.grid(True)
                        self.aux_plot_canvas.draw()

                    except Exception as e:
                        output = f"Error: {str(e)}"



            elif method == "Root Finding - Compare All Methods":
                if a is None or b is None:
                    output = "Comparison requires a and b. 'a' is x0, 'b' is x1."
                else:
                    results = []

                    # --- Bisection ---
                    try:
                        root, iters, errors = self.custom_bisection(f, a, b)
                        final_error = errors[-1] if errors else "N/A"
                        results.append(("Bisection", root, iters, f"{final_error:.2e}"))
                    except Exception as e:
                        results.append(("Bisection", "-", "-", f"Error: {e}"))

                    # --- Newton-Raphson ---
                    try:
                        root, iters, errors = self.custom_newton_raphson(f, a)
                        final_error = errors[-1] if errors else "N/A"
                        results.append(("Newton-Raphson", root, iters, f"{final_error:.2e}"))
                    except Exception as e:
                        results.append(("Newton-Raphson", "-", "-", f"Error: {e}"))

                    # --- Secant ---
                    try:
                        root, iters, errors = self.custom_secant(f, a, b)
                        final_error = errors[-1] if errors else "N/A"
                        results.append(("Secant", root, iters, f"{final_error:.2e}"))
                    except Exception as e:
                        results.append(("Secant", "-", "-", f"Error: {e}"))

                    # Format the output
                    output = "Root Finding Method Comparison:\n"
                    output += f"{'Method':<18}{'Root':<20}{'Iter':<10}{'Final Error':<14}\n"
                    output += "-" * 62 + "\n"
                    for name, root, iters, err in results:
                        root_str = f"{root:.12f}" if isinstance(root, float) else root
                        iters_str = str(iters) if isinstance(iters, int) else "-"
                        output += f"{name:<18}{root_str:<20}{iters_str:<10}{err:<14}\n"




            elif method == "Interpolation - Linear":
                try:
                        f = lambda x: eval(f_str, {"x": x, "np": np, "math": math})
                except:
                    self.toolbox_output.setText("Invalid function input.")
                    return


                if a is None:
                    output = "Provide an x value for interpolation."
                else:
                    x_data = np.array([0, 1, 2, 3, 4])
                    y_data = f(x_data)
                    linear_f = interp1d(x_data, y_data)
                    y_interp = linear_f(a)
                    output = f"Linear Interpolation at x = {a}: {y_interp:.4f}"
                    self.plot_interpolation_result(x_data, y_data, linear_f, "Linear")




            elif method == "Interpolation - Cubic Spline":
                try:
                    x_data = np.array(eval(f_str))
                    y_data = np.array(eval(self.param1_input.text()))
                    if len(x_data) != len(y_data):
                        output = "x and y must have the same length."
                    elif len(x_data) < 2:
                        output = "Need at least two data points."
                    else:
                        x_eval = float(self.param2_input.text()) if self.param2_input.text() else None

                        from scipy.interpolate import CubicSpline
                        cs = CubicSpline(x_data, y_data)

                        if x_eval is not None:
                            y_interp = cs(x_eval)
                            output = f"Cubic Spline Interpolation at x = {x_eval}: {y_interp:.6f}"
                        else:
                            output = "Cubic Spline interpolation curve plotted."

                        # Plot the curve and points
                        x_dense = np.linspace(x_data[0], x_data[-1], 200)
                        y_dense = cs(x_dense)

                        self.aux_plot_canvas.axes.clear()
                        self.aux_plot_canvas.axes.plot(x_data, y_data, 'o', label="Data Points", color="black")
                        self.aux_plot_canvas.axes.plot(x_dense, y_dense, '-', label="Cubic Spline", color="purple")
                        self.aux_plot_canvas.axes.set_title("Cubic Spline Interpolation")
                        self.aux_plot_canvas.axes.set_xlabel("x")
                        self.aux_plot_canvas.axes.set_ylabel("f(x)")
                        self.aux_plot_canvas.axes.grid(True)
                        self.aux_plot_canvas.axes.legend()
                        self.aux_plot_canvas.draw()


                except Exception as e:
                    output = f" Invalid input: {str(e)}"


            elif method == "Numerical Differentiation - Forward":
                if a is None or b is None:
                    output = "Provide x and h for differentiation."
                else:
                    df_dx = (f(a + b) - f(a)) / b
                    output = f"Forward Derivative at x = {a}: {df_dx:.12f}"

                    #plot error vs h
                    if f_prime_exact:
                        exact = f_prime_exact(a)
                        h_vals = np.logspace(-5, -1, 20)
                        errors = [abs((f(a + h) - f(a)) / h - exact) for h in h_vals]

                        self.aux_plot_canvas.axes.clear()
                        self.aux_plot_canvas.axes.plot(h_vals, errors, marker='s', color='orange')
                        self.aux_plot_canvas.axes.set_xscale("log")
                        self.aux_plot_canvas.axes.set_yscale("log")
                        self.aux_plot_canvas.axes.set_title("Forward Difference Error vs h")
                        self.aux_plot_canvas.axes.set_xlabel("Step size (h)")
                        self.aux_plot_canvas.axes.set_ylabel("Absolute Error")
                        self.aux_plot_canvas.axes.grid(True)
                        self.aux_plot_canvas.draw()



            elif method == "Numerical Differentiation - Backward":
                if a is None or b is None:
                    output = " Provide x and h for differentiation."
                else:
                    df_dx = (f(a) - f(a - b)) / b
                    output = f"Backward Derivative at x = {a}: {df_dx:.12f}"

                    # Plot error vs h
                    if f_prime_exact:
                        exact = f_prime_exact(a)
                        h_vals = np.logspace(-5, -1, 20)
                        errors = [abs((f(a) - f(a - h)) / h - exact) for h in h_vals]

                        self.aux_plot_canvas.axes.clear()
                        self.aux_plot_canvas.axes.plot(h_vals, errors, marker='^', color='green')
                        self.aux_plot_canvas.axes.set_xscale("log")
                        self.aux_plot_canvas.axes.set_yscale("log")
                        self.aux_plot_canvas.axes.set_title("Backward Difference Error vs h")
                        self.aux_plot_canvas.axes.set_xlabel("Step size (h)")
                        self.aux_plot_canvas.axes.set_ylabel("Absolute Error")
                        self.aux_plot_canvas.axes.grid(True)
                        self.aux_plot_canvas.draw()


            elif method == "Numerical Differentiation - Central":
                if a is None or b is None:
                    output = "Provide x and h for differentiation."
                else:
                    df_dx = (f(a + b) - f(a - b)) / (2 * b)
                    output = f"Central Derivative at x = {a}: {df_dx:.12f}"


                    if f_prime_exact:
                        exact = f_prime_exact(a)
                        h_vals = np.logspace(-5, -1, 20)
                        errors = [(abs((f(a + h) - f(a - h)) / (2*h) - exact)) for h in h_vals]

                        self.aux_plot_canvas.axes.clear()
                        self.aux_plot_canvas.axes.plot(h_vals, errors, marker='o')
                        self.aux_plot_canvas.axes.set_xscale("log")
                        self.aux_plot_canvas.axes.set_yscale("log")
                        self.aux_plot_canvas.axes.set_title("Central Difference Error vs h")
                        self.aux_plot_canvas.axes.set_xlabel("Step size (h)")
                        self.aux_plot_canvas.axes.set_ylabel("Absolute Error")
                        self.aux_plot_canvas.axes.grid(True)
                        self.aux_plot_canvas.draw()



            elif method == "Linear System Solver":
                try:
                    # Expecting user to input matrix A and vector b in func_input and param1_input respectively
                    A = eval(f_str, {"np": np, "math": math})  # Matrix A from function input
                    b_vec = eval(a_text, {"np": np, "math": math})  # Vector b from parameter 1

                    A = np.array(A, dtype=float)
                    b_vec = np.array(b_vec, dtype=float)

                    if A.shape[0] != A.shape[1]:
                        output = " Matrix A must be square."
                    elif A.shape[0] != b_vec.shape[0]:
                        output = "Dimensions of A and b do not match."
                    else:
                        x = np.linalg.solve(A, b_vec)
                        output = (
                            "Solving Ax = b using NumPy's `linalg.solve`\n\n"
                            f"Matrix A:\n{A}\n\n"
                            f"Vector b:\n{b_vec}\n\n"
                            f"Solution x:\n{x.round(4)}"
                        )
                except Exception as e:
                    output = f"Error: {str(e)}"

            elif method == "Linear System - LU Decomposition":
                try:
                    # Matrix A expected in func_input
                    A = eval(f_str, {"np": np, "math": math})
                    A = np.array(A, dtype=float)

                    P, L, U = lu(A)

                    output = (
                        "LU Decomposition (A = LU)\n\n"
                        f"Matrix A:\n{A}\n\n"
                        f"L:\n{np.round(L, 3)}\n\n"
                        f"U:\n{np.round(U, 3)}"
                    )
                except Exception as e:
                    output = f"Error: {str(e)}"



            elif method == "Numerical Integration - Trapezoidal":
                if a is None or b is None:
                    output = " Provide a and b for integration."
                else:
                    N = 1000
                    x_vals = np.linspace(a, b, N + 1)
                    y_vals = f(x_vals)
                    h = (b - a) / N
                    result = (h / 2) * (y_vals[0] + 2 * np.sum(y_vals[1:-1]) + y_vals[-1])
                    output = f"Trapezoidal Rule Result: {result:.6f}"
                    self.plot_result(x_vals, y_vals, label="f(x)", title="Trapezoidal Integration", ylabel="f(x)")



            elif method == "Numerical Integration - Simpson":
                if a is None or b is None:
                    output = "Provide a and b for integration."
                else:
                    from scipy.integrate import simpson
                    N = 1000
                    x_vals = np.linspace(a, b, N + 1)
                    y_vals = f(x_vals)
                    result = simpson(y_vals, x_vals)
                    output = f"Simpson’s Rule Result: {result:.6f}"
                    self.plot_result(x_vals, y_vals, label="f(x)", title="Simpson Integration", ylabel="f(x)")



            elif method == "Numerical Integration - trapz (SciPy)":
                if a is None or b is None:
                    output = "Provide a and b for integration."
                else:
                    N = 1000
                    x_vals = np.linspace(a, b, N + 1)
                    try:
                        y_vals = f(x_vals)  # Works if f supports vectorized input
                    except:
                        y_vals = np.array([f(x) for x in x_vals])  # Fallback

                    result = np.trapz(y_vals, x_vals)
                    output = f"NumPy trapz Result: {result:.6f}"
                    self.plot_result(x_vals, y_vals, label="f(x)", title="NumPy trapz Integration", ylabel="f(x)")




            elif method == "Numerical Integration - quad (SciPy)":
                if a is None or b is None:
                    output = " Provide a and b for integration."
                else:
                    from scipy.integrate import quad
                    result, err = quad(f, a, b)
                    output = f"SciPy quad Result: {result:.6f}\nEstimated Error: {err:.2e}"
                    x_vals = np.linspace(a, b, 500)
                    y_vals = f(x_vals)
                    self.plot_result(x_vals, y_vals, label="f(x)", title="quad Integration", ylabel="f(x)")





            elif method == "Optimization - Scalar Minimization":
                if a is None or b is None:
                    output = " Provide a and b as bounds for optimization."
                else:
                    try:
                        from scipy.optimize import minimize_scalar
                        result = minimize_scalar(f, bounds=(a, b), method='bounded')

                        if result.success:
                            output = (
                                f"Scalar Minimization Result:\n\n"
                                f"Minimum x: {result.x:.6f}\n"
                                f"f(x): {result.fun:.6f}\n"
                                f"Iterations: {result.nit}\n"
                                f"Status: {result.message}"
                            )

                            # Plot the function over the interval
                            x_vals = np.linspace(a, b, 400)
                            y_vals = [f(x) for x in x_vals]
                            self.plot_result(
                                x_vals, y_vals,
                                label="f(x)", title="Scalar Minimization", ylabel="f(x)"
                            )
                            self.main_plot_canvas.axes.plot(result.x, result.fun, 'ro', label="Minimum")
                            self.main_plot_canvas.axes.legend()
                            self.main_plot_canvas.draw()
                        else:
                            output = f"Optimization failed: {result.message}"
                    except Exception as e:
                        output = f"Error: {str(e)}"


            elif method == "Floating-Point - Error Accumulation Demo":
                try:
                    N = 1000000  # 1 million small values
                    small_value = 1e-8

                    # Increasing order sum
                    inc_sum = 0.0
                    for _ in range(N):
                        inc_sum += small_value

                    # Decreasing order sum
                    values = [small_value] * N
                    dec_sum = sum(reversed(values))

                    # Expected
                    expected = N * small_value

                    output = (
                    "Floating-Point Error Accumulation Demo\n\n"
                    f"Summing {small_value} for {N} times:\n\n"
                    f"Expected sum:           {expected:.12f}\n"
                    f"Sum (increasing order): {inc_sum:.12f}\n"
                    f"Sum (decreasing order): {dec_sum:.12f}\n\n"
                    f"Error (increasing):     {abs(expected - inc_sum):.2e}\n"
                    f"Error (decreasing):     {abs(expected - dec_sum):.2e}"
                    )

                    # Optional plot of cumulative error over number of terms
                    self.aux_plot_canvas.axes.clear()
                    counts = np.linspace(10, N, 50, dtype=int)
                    inc_errors = []
                    dec_errors = []

                    for count in counts:
                        inc = sum(small_value for _ in range(count))
                        dec = sum(small_value for _ in reversed(range(count)))
                        inc_errors.append(abs(count * small_value - inc))
                        dec_errors.append(abs(count * small_value - dec))

                    self.aux_plot_canvas.axes.plot(counts, inc_errors, label="Increasing Order", color="red")
                    self.aux_plot_canvas.axes.plot(counts, dec_errors, label="Decreasing Order", color="blue")
                    self.aux_plot_canvas.axes.set_title("Floating-Point Summation Error")
                    self.aux_plot_canvas.axes.set_xlabel("Number of Terms")
                    self.aux_plot_canvas.axes.set_ylabel("Absolute Error")
                    self.aux_plot_canvas.axes.set_yscale("log")
                    self.aux_plot_canvas.axes.grid(True)
                    self.aux_plot_canvas.axes.legend()
                    self.aux_plot_canvas.draw()

                except Exception as e:
                    output = f"Error: {str(e)}"


            else:
                output = "Method not supported."


        except Exception as e:
            output = f"Error: {str(e)}"

        self.toolbox_output.setText(output)


    def plot_result(self, x, y, label="Result", title="Plot", xlabel="x", ylabel="y"):
        self.aux_plot_canvas.axes.clear()
        self.aux_plot_canvas.axes.plot(x, y, label=label, linewidth=2)
        self.aux_plot_canvas.axes.set_title(title)
        self.aux_plot_canvas.axes.set_xlabel(xlabel)
        self.aux_plot_canvas.axes.set_ylabel(ylabel)
        self.aux_plot_canvas.axes.grid(True)
        self.aux_plot_canvas.axes.legend()
        self.aux_plot_canvas.draw()

    def plot_interpolation_result(self, x_data, y_data, interp_func, method_name):
        x_dense = np.linspace(x_data[0], x_data[-1], 200)
        y_dense = interp_func(x_dense)

        self.aux_plot_canvas.axes.clear()
        self.aux_plot_canvas.axes.plot(x_data, y_data, 'o', label="Data Points", color="black")
        self.aux_plot_canvas.axes.plot(x_dense, y_dense, '-', label=method_name, linewidth=2, color="blue")

        self.aux_plot_canvas.axes.set_title(f"{method_name} Interpolation")
        self.aux_plot_canvas.axes.set_xlabel("x")
        self.aux_plot_canvas.axes.set_ylabel("f(x)")
        self.aux_plot_canvas.axes.grid(True)
        self.aux_plot_canvas.axes.legend()
        self.aux_plot_canvas.draw()








# Run app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PendulumApp()
    window.show()
    sys.exit(app.exec())
