from vpython import sphere, vector, rate, color, mag, winput, button, scene, textures, graph, gcurve, label

# Function to update simulation parameters and restart the simulation
def update_parameters():
    try:
        # Update planet's initial position and velocity
        planet.pos = vector(float(pos_x_input.text), float(pos_y_input.text), 0)
        planet.velocity = vector(float(vel_x_input.text), float(vel_y_input.text), 0)
        
        # Update global parameters
        global dt, G, M
        dt = float(dt_input.text)
        G = float(G_input.text)
        M = float(M_input.text)
        
        # Reset the trail and graph
        planet.clear_trail()
        ke_distance_curve.delete()
    except ValueError:
        print("Please enter valid numerical values.")

# Create the sun
sun = sphere(pos=vector(0, 0, 0), radius=1, color=color.yellow)

# Create the planet with a reduced size, white trail, and Earth texture
planet = sphere(pos=vector(5, 0, 0), radius=0.25, make_trail=True, trail_color=color.white, texture=textures.earth)

# Default parameters
planet.velocity = vector(0, 1, 0)
dt = 0.01
G = 1
M = 10

# Display the force formula in the UI
scene.append_to_caption('Gravitational Force Formula: F = -G * M * m / r^2\n')

# UI for parameter input
scene.append_to_caption('\nPlanet Initial Position (x, y): ')
pos_x_input = winput(bind=update_parameters, text='5')
pos_y_input = winput(bind=update_parameters, text='0')

scene.append_to_caption('\nPlanet Initial Velocity (vx, vy): ')
vel_x_input = winput(bind=update_parameters, text='0')
vel_y_input = winput(bind=update_parameters, text='1')

scene.append_to_caption('\nTime Step (dt): ')
dt_input = winput(bind=update_parameters, text='0.01')

scene.append_to_caption('\nGravitational Constant (G): ')
G_input = winput(bind=update_parameters, text='1')

scene.append_to_caption('\nMass of the Sun (M): ')
M_input = winput(bind=update_parameters, text='10')

scene.append_to_caption('\n')
button(text='Update Parameters', bind=update_parameters)

# Create a graph for the kinetic energy of the planet against distance
ke_distance_graph = graph(title='Kinetic Energy vs Distance', xtitle='Distance', ytitle='Kinetic Energy', width=600, height=400)
ke_distance_curve = gcurve(graph=ke_distance_graph, color=color.red)

# Label to display escape velocity
escape_velocity_label = label(pos=vector(0, -3, 0), text='Escape Velocity: ', box=False, height=10, color=color.white)

# Simulation loop
while True:
    rate(100)  # Limit the animation to 100 frames per second

    # Calculate the gravitational force
    r = planet.pos - sun.pos
    force = -G * M * planet.pos / mag(r)**3

    # Update the velocity and position of the planet
    planet.velocity += force * dt
    planet.pos += planet.velocity * dt

    # Calculate the kinetic energy of the planet
    kinetic_energy = 0.5 * mag(planet.velocity)**2

    # Plot kinetic energy against the distance from the sun
    ke_distance_curve.plot(mag(r), kinetic_energy)

    # Calculate and display the escape velocity
    escape_velocity = (2 * G * M / mag(r))**0.5
    escape_velocity_label.text = f'Escape Velocity: {escape_velocity:.2f}'
