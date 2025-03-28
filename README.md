# Feasibility Study of Microfluidic Circuit by Simulation

## Project Description

This project aims to design a user-friendly user interface for ease of microfluidic circuit simulations. The Graphical User Interface (GUI) complements the "network simulation code" to calculate the hydraulic resistances, flowrates, flow times/speeds of channels and port pressures of a hydraulic network with multiple inlets and outlets.

**About**

A Python-based GUI designed to facilitate the simulation of microfluidic circuits. The GUI was developed using the Tkinter module and aims to simplify the parametrization process for microfluidic circuit simulations.

The GUI serves as an interface for:

* Displaying component information.
* Editing component information.
* Drawing the microfluidic circuit.
* Running simulations and displaying results.

## Features
* **Component Display**: View detailed information about each component in the circuit.
* **Component Editing**: Modify the parameters of the components directly through the interface.
* **Circuit Drawing**: Intuitive tools to draw and design the microfluidic circuit.
* **Simulation Results**: Display the results of the simulation, including flow rates and pressures.

## GUI Overview
### Main Interface
* **Component List**: Displays a list of all components in the circuit.
* **Canvas**: Area where the circuit is drawn.
* **Property Editor**: Panel for editing the properties of selected components.
* **Simulation Controls**: Buttons to run the simulation and view results.

### Component Types
* **Ports**: Define fluid inlets and outlets.
* **Channels**: Straight and bent channels connecting the ports.
* **Chambers**: Areas where fluids can mix.
* **Valves**: Control fluid flow between channels.

<img width="500" alt="interface" src="https://github.com/yeoxiongyun/microfluidic-GUI/assets/84406436/fff2bd2a-b1a9-4497-a504-bc5b0f75988f">
<img width="500" alt="interface" src="https://github.com/yeoxiongyun/microfluidic-GUI/assets/84406436/e2b30014-b780-4d42-b586-ce654ece8260">

### Example
Here is a simple example of how to use the GUI:

1. Add a port by clicking on the "Add Port" button.
2. Draw a channel connecting two ports by selecting the "Add Channel" tool and clicking on the canvas.
3. Edit the properties of the channel by selecting it and modifying its parameters in the Property Editor.
4. Simulate by clicking the "Run Simulation" button and view the results.



## License
Not allowed for commercial purposes. Only for academic research.
