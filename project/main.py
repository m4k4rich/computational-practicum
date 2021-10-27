import sys
from PyQt5 import QtCore, QtWidgets
from interface import Ui_MainWindow
import math
import sys
import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

matplotlib.use('Qt5Agg')

class ODE():
    
    def __init__(self):
        pass

    def func(self, x,y):
    
        # function returning the value of differential => #
        try:
            return ((y/x) - y - x)
        except ZeroDivisionError:
            return None
    
    def exact_solution(self, x):
        return (x * ( ( math.pow(math.e,(1-x)) - 1) ))

class MplCanvas(FigureCanvasQTAgg):
    
    """
    ---------------------------------------------------------------------------------  
    MplCanvas is required in order to implement matplotlib, together with pyqt5
    to represent two graphs, one with function approximation and another with 
    local error
    ---------------------------------------------------------------------------------
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax1, self.ax2 = self.fig.subplots(2)
        self.ax1.grid()
        self.ax2.grid()
        self.ax1.set_title('Solution to differential equation')
        self.ax1.set_ylabel('y-axis')
        self.ax2.set_ylabel('y-axis with absolute error')
        self.ax2.set_xlabel('x-axis')
        self.ax2.set_title("Error visualisation")
        super(MplCanvas, self).__init__(self.fig)

class ODE_solver(QtWidgets.QMainWindow):

    """
    ---------------------------------------------------------------------------------
    ODE_solver class implements three methods for approximation of the differential.
    One method for visualisation of the 'approximation error'
    ---------------------------------------------------------------------------------
    """

    def __init__(self):    
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ODE = ODE()
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.verticalLayout_5.addWidget(self.canvas,1)
        self.init_UI()
    
    def init_UI(self):
        self.setWindowTitle("ODE Solver")

        # setting names for placeholders => #
        self.ui.lineEdit_2.setPlaceholderText("X_0")
        self.ui.lineEdit_3.setPlaceholderText("Y_0")
        self.ui.lineEdit_4.setPlaceholderText("step size")

        # binding of buttons to actions => #
        self.ui.pushButton_2.clicked.connect(lambda: self.solver(1)) # euler_method button
        self.ui.pushButton.clicked.connect(lambda: self.solver(2)) # improved_euler_method button
        self.ui.pushButton_3.clicked.connect(lambda: self.solver(3)) # runge_kutta_method button
        self.ui.pushButton_5.clicked.connect(lambda: self.solver(4)) # all methods button

        # button returning graphic for errors => #
        self.ui.pushButton_4.clicked.connect(lambda: self.solver(5))

    def solver(self, option):
        
        # fetching all necessary information => #
        initial_x = self.ui.lineEdit_2.text()
        initial_y = self.ui.lineEdit_3.text()
        step_quantity = self.ui.lineEdit_4.text()
        approximation_point = self.ui.lineEdit.text()
        initial_step = self.ui.lineEdit_5.text()
        final_step = self.ui.lineEdit_6.text()

        # calling a method based on the pressed button => #
        try:
            step = (float(approximation_point) - float(initial_x)) / float(step_quantity)
            initial_conditions = (float(initial_x), float(initial_y), step, float(approximation_point))

            if(option == 1):
                self.canvas.fig.clear()
                self.canvas.ax1, self.canvas.ax2 = self.canvas.fig.subplots(2)
                self.euler_method(initial_conditions, False, False)

            elif(option == 2):
                self.canvas.fig.clear()
                self.canvas.ax1, self.canvas.ax2 = self.canvas.fig.subplots(2)
                self.improved_euler_method(initial_conditions, False, False)

            elif(option == 3):
                self.canvas.fig.clear()
                self.canvas.ax1, self.canvas.ax2 = self.canvas.fig.subplots(2)
                self.runge_kutta_method(initial_conditions, False, False)

            elif(option == 4):
                self.canvas.fig.clear()
                self.canvas.ax1, self.canvas.ax2 = self.canvas.fig.subplots(2)
                self.euler_method(initial_conditions, True, False)
                self.improved_euler_method(initial_conditions, True, False)
                self.runge_kutta_method(initial_conditions, True, False)
                self.canvas.ax1.cla()
                self.canvas.ax2.cla()
            else:
                self.canvas.fig.clear()
                self.canvas.ax1 = self.canvas.fig.subplots(1)
                self.calculate_error(initial_conditions, float(initial_step), float(final_step))


        except ValueError:
            print("Please enter the integer!")

    def euler_slope(self, initial_x, initial_y, step):

        # this function provides the euler's slope used in two methods => #
        return (initial_y + (step * self.ODE.func(initial_x, initial_y)))

    def euler_method(self,initial_conditions, all, error):

        """

        ---------------------------------------------------------------------------------
            x_0 - initial_x
            y_0 - initial_y 
            N - step
            X - approximation_point
        ---------------------------------------------------------------------------------
            Euler method approximates the graphic.
            This method generates two graphs, one with approximated solutions
            And another one with the relation between step size on x-axis and approximation error on y-axis
            The error is computed with following equation: y(exact) - y(approximated) = error
            There is a clear correlation the higher the step, the higher the error.
        ---------------------------------------------------------------------------------

        """

        # "unpacking" provided initial conditions => #
        initial_x, initial_y, step, approximation_point = initial_conditions

        # arrays containing axes for exact function and approximated function => #
        x_axis=[]
        y_axis=[]
        exact_y = []
        error_y = []

        # initial conditions appended as we already know them => #
        x_axis.append(initial_x)
        y_axis.append(initial_y)
        exact_y.append(initial_y)
        error_y.append(0)

        # looping through in order to get consequetial y values => #
        while initial_x < approximation_point:

                if self.ODE.func(initial_x, initial_y) == None:
                    # check function for point of discontinuity => #
                    print("Point of discontinuit at: "+str(initial_x)+" and "+str(initial_y))
                    initial_x = initial_x + step
                    continue
                else:
                    initial_y = self.euler_slope(initial_x,initial_y,step)
                    initial_x = initial_x + step

                    x_axis.append(initial_x)
                    y_axis.append(initial_y)
                    exact_y.append(self.ODE.exact_solution(initial_x))
                    error_y.append(abs(initial_y - self.ODE.exact_solution(initial_x)))
        
        if error == True:
            print('something')
            return np.amax(error_y)
        else: 
            self.canvas.ax1.set_ylabel('y-axis')
            self.canvas.ax2.set_ylabel('y-axis with absolute error')
            self.canvas.ax2.set_xlabel('x-axis')
            self.canvas.ax1.grid()
            self.canvas.ax2.grid()
            self.canvas.ax1.set_title("Euler Method")
            self.canvas.ax1.plot(x_axis,exact_y,'b', label='Exact Solution')
            self.canvas.ax1.plot(x_axis, y_axis,'r', label='Euler Approximation')
            self.canvas.ax1.legend()

            self.canvas.ax2.plot(x_axis, error_y, label='Euler Approximation Error')
            self.canvas.ax2.legend()
            self.canvas.draw()
            if(all == True):
                pass
            else:
                self.canvas.ax1.cla()
                self.canvas.ax2.cla()
        
    def improved_euler_method(self, initial_conditions, all, error):

        """

        ---------------------------------------------------------------------------------
            The idea behind the improved euler method is based on two core principles.
            First, the usual euler method and the equation of tangent line that we find, whilst approximating
            And second, we take value of subsequent x and y, from original euler method and plug them to get 
            an equation for a new slope, which is different from the previous one. 
            Now, finally if we take these two slopes and find an average, we will have an approximation with
            much lower error behind it. 

            f(x_0, y_0) + f(x_0 + step_size, y_0 + step_size * f(x_0, y_0)) * 1/2

            Now, after deriving this formula, we plug it in our original euler formula, getting: 
            y_1 = y_0 + step_size * (f(x_0, y_0) + f(x_0 + step_size, y_0 + step_size * f(x_0, y_0)) * 1/2)
        ---------------------------------------------------------------------------------
            Average of the slopes direction fields - f(x_0, y_0) + f(x_0 + step_size, y_0 + step_size * f(x_0, y_0)) * 1/2
            Small horizontal increment - step_size 
            Current y-value - y_0
            Next y-value = y_1
        ---------------------------------------------------------------------------------

        """

        # "unpacking" provided initial conditions => #
        initial_x, initial_y, step, approximation_point = initial_conditions

        # arrays containing axes for exact function and approximated function => #
        x_axis=[]
        y_axis=[]
        exact_y = []
        error_y = []
        
        # initial conditions appended as we already know them => #
        x_axis.append(initial_x)
        y_axis.append(initial_y)
        exact_y.append(initial_y)
        error_y.append(0)

        # looping through in order to get consequetial y values => #
        while initial_x < approximation_point:
            if self.ODE.func(initial_x, initial_y) == None:
                    # check function for point of discontinuity => #
                    print("Point of discontinuit at: "+initial_x+" and "+initial_y)
            else:
                initial_y = initial_y + (step * (1/2 * (self.ODE.func(initial_x,initial_y) + self.ODE.func(initial_x+step,self.euler_slope(initial_x,initial_y,step)))))
                initial_x = initial_x + step
                x_axis.append(initial_x)
                y_axis.append(initial_y)
                exact_y.append(self.ODE.exact_solution(initial_x))
                error_y.append(abs(initial_y - self.ODE.exact_solution(initial_x)))

        if(error == True):
            return np.amax(error_y)
        else:
            self.canvas.ax1.set_title("Improved Euler method")
            if(all == False):
                    self.canvas.ax1.plot(x_axis,exact_y,'b', label='Exact Solution')
            self.canvas.ax1.plot(x_axis, y_axis,'g', label='Improved Euler Approximation')
            self.canvas.ax1.legend()
            self.canvas.ax1.set_ylabel('y-axis')
            self.canvas.ax2.set_ylabel('y-axis with absolute error')
            self.canvas.ax2.set_xlabel('x-axis')
            self.canvas.ax1.grid()
            self.canvas.ax2.grid()
            self.canvas.ax2.set_title("Relation between step number and error")
            self.canvas.ax2.plot(x_axis, error_y, label='Improved Euler Approximation Error')
            self.canvas.ax2.legend()

            # renew the canvas !
            self.canvas.draw()
            if(all == True):
                pass
            else:
                self.canvas.ax1.cla()
                self.canvas.ax2.cla()

    def runge_kutta_method(self, initial_conditions, all, error):

        """

        ---------------------------------------------------------------------------------
        In terms of x increment it repeats the idea from euler's method.
        But y value is updated in a different manner. It can be boiled down to equation.
        y_n+1 = y_n + 1/6 * step * (k_1 + 2*k_2 + 2*k_3 + k_4), where 
        k_1 = f(x_n, y_n)
        k_2 = f(x_n + step / 2, y_n + step * k_1 / 2)
        k_3 = f(x_n + step / 2, y_n + step * k_2 / 2)
        k_4 = f(x_n + step, y_n + step * k_3)
        ---------------------------------------------------------------------------------

        """

        # "unpacking" provided initial conditions => #
        initial_x, initial_y, step, approximation_point = initial_conditions

        # arrays containing axes for exact function and approximated function => #
        x_axis=[]
        y_axis=[]
        exact_y = []
        error_y = []

        # initial conditions appended as we already know them => #
        x_axis.append(initial_x)
        y_axis.append(initial_y)
        exact_y.append(initial_y)
        error_y.append(0)

        # looping through in order to get consequetial y values => #
        while initial_x < approximation_point:
            k_1 = self.ODE.func(initial_x, initial_y)
            k_2 = self.ODE.func(initial_x + (step/2), initial_y + ((k_1/2) * step))
            k_3 = self.ODE.func(initial_x + (step/2), initial_y + ((k_2/2) * step))
            k_4 = self.ODE.func(initial_x + step, initial_y + (step*k_3))

            initial_x = initial_x + step

            x_axis.append(initial_x)

            initial_y = initial_y + (1.0/6.0) * step * (k_1 +  2*k_2 + 2*k_3 + k_4)
            y_axis.append(initial_y)
            exact_y.append(self.ODE.exact_solution(initial_x))
            error_y.append(abs(initial_y - self.ODE.exact_solution(initial_x)))

        if(error == True):
            return np.amax(error_y)
        else:
            if(all == False):
                self.canvas.ax1.set_title("Runge-Kutta method")
                self.canvas.ax1.plot(x_axis,exact_y,'b', label='Exact Solution')

            # accessing the plotting object and plotting the graph => #
            self.canvas.ax1.set_ylabel('y-axis')
            self.canvas.ax2.set_ylabel('y-axis with absolute error')
            self.canvas.ax2.set_xlabel('x-axis')
            self.canvas.ax1.grid()
            self.canvas.ax2.grid()
            self.canvas.ax1.plot(x_axis, y_axis,'m', label='Runge-Kutta approximation')
            self.canvas.ax1.legend()
            self.canvas.ax2.plot(x_axis, error_y, label="Runge-Kutta Approximation Error")
            self.canvas.ax2.legend()

            # renew the canvas !
            self.canvas.draw()
            if(all == True):
                pass
            else:
                self.canvas.ax1.cla()
                self.canvas.ax2.cla()

    def calculate_error(self, initial_conditions, initial_step, final_step):
        # "unpacking" provided initial conditions => #
        initial_x, initial_y, step, approximation_point = initial_conditions

        euler_y=[]
        improved_euler_y=[]
        rk_y=[]
        axis_x=[]

        while initial_step < (final_step + 1):
            
            step = (float(approximation_point) - float(initial_x)) / float(initial_step)
            euler_y.append(self.euler_method((initial_x, initial_y, step, approximation_point), False, True))
            improved_euler_y.append(self.improved_euler_method((initial_x, initial_y, step, approximation_point), False, True))
            rk_y.append(self.runge_kutta_method((initial_x, initial_y, step, approximation_point), False, True))
            axis_x.append(initial_step)

            initial_step = initial_step + 1 
        
        self.canvas.ax1.grid()
        self.canvas.ax1.set_ylabel('Y-axis with absolute error')
        self.canvas.ax1.set_xlabel('Number of steps')
        self.canvas.ax1.plot(axis_x,euler_y,'b', label='Euler Approximation Error')
        self.canvas.ax1.plot(axis_x,improved_euler_y,'r', label='Improved Euler Approximation Error')
        self.canvas.ax1.plot(axis_x,rk_y,'g', label='Improved Runge-Kutta Approximation Error')
        self.canvas.ax1.legend()
        self.canvas.draw()
        self.canvas.ax1.cla()

if __name__ == "__main__":
    # turning on the applicaiton => #
    app = QtWidgets.QApplication([])
    application = ODE_solver()
    application.show()
    sys.exit(app.exec())
