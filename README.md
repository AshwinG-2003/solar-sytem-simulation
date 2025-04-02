# Solar System Simulation

A real-time 2D simulation of the solar system using Python and Pygame. This models planetary motion based on Newtonian gravity and allows user interaction to control various parameters.

## Features
- Simulates the orbits of planets around the Sun using gravitational forces.
- Real-time physics calculations with the `scipy.integrate.ode` solver.
- User controls to adjust simulation speed and gravitational constant.
- Ability to add new celestial bodies dynamically and observe their interactions.
- Zoom in/out functionality for better visualization.

## Installation
### Prerequisites
Ensure you have Python installed on your system. You also need the following dependencies:

```sh
pip install pygame numpy scipy
```

## Usage
Run the simulation with:
```sh
python solar-system.py
```

### Controls
- `SPACE` - Start the simulation
- `A` - Increase simulation speed
- `D` - Decrease simulation speed
- `W` - Increase gravitational constant
- `S` - Decrease gravitational constant
- `N` - Add a random celestial body
- `+/-` - Zoom in/out
- `ESC` - Exit the simulation

## How It Works
The simulation models planetary motion using Newtonian gravity:

**F = G * (m₁ * m₂) / r²**

where:
- `G` is the gravitational constant.
- `m1`, `m2` are the masses of two celestial bodies.
- `r` is the distance between them.

The equations of motion are solved using an ODE solver (`scipy.integrate.ode`).

