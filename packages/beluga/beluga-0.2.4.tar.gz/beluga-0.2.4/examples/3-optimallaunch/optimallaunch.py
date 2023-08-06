import beluga
import logging
from math import pi, sqrt

BFR_mass = 4400000
BFR_thrust = 52.7*1000*1000
mu = 3.9860044188e14
re = 6.371*1000*1000
h = 120*1000
vc = sqrt(mu / (h + re))

ocp = beluga.OCP('optimallaunch')

# Define independent variables
ocp.independent('t', 's')

# Define equations of motion
ocp.state('x', 'v_x', 'm')
ocp.state('y', 'v_y', 'm')
ocp.state('v_x', 'F/mass*sin(alfa)', 'm/s')
ocp.state('v_y', 'F/mass*cos(alfa) - g', 'm/s')
ocp.state('mass', 0, 'kg')

# Define controls
ocp.control('alfa','rad')

# Define constants
ocp.constant('g', -9.80665, 'm/s^2')
ocp.constant('F', BFR_thrust, 'newton')
ocp.constant('mu', mu, 'm^3/s^(-2)')

# Define costs
ocp.path_cost('1', '1')

# Define constraints
ocp.constraints().initial('x-x_0', 'm')
ocp.constraints().initial('y-y_0', 'm')
ocp.constraints().initial('v_x-v_x_0', 'm/s')
ocp.constraints().initial('v_y-v_y_0', 'm/s')
ocp.constraints().initial('mass-mass_0', 'kg')
ocp.constraints().terminal('y-y_f', 'm')
ocp.constraints().terminal('v_x-v_x_f', 'm/s')
ocp.constraints().terminal('v_y-v_y_f', 'm/s')

# Use the "adjoined method" to solve for the constraints. (Default is False)
ocp.constraints().set_adjoined(False)

ocp.scale(m=1, s=1, kg=1, rad=1, newton=1)

bvp_solver = beluga.bvp_algorithm('Shooting',
                        derivative_method='fd',
                        tolerance=1e-4,
                        max_iterations=200,
                        max_error=100,
                        num_arcs=1,
                        num_cpus=1
             )

guess_maker = beluga.guess_generator('auto',
                start=[0,0,0,0,BFR_mass],          # Starting values for states in order
                direction='forward',
                costate_guess = 0.1,
                control_guess = [0],
                use_control_guess=True,
)

continuation_steps = beluga.init_continuation()

continuation_steps.add_step('bisection') \
                .num_cases(21) \
                .terminal('v_x', 0) \
                .terminal('y', h)

beluga.add_logger(logging_level=logging.DEBUG)

sol = beluga.solve(ocp,
             method='traditional',
             bvp_algorithm=bvp_solver,
             steps=continuation_steps,
             guess_generator=guess_maker)
