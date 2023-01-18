# Supermarket-Markov-Simulation 🏪

![Simulation](./docs/simulation.gif)

This project is a Markov Chain simulation of a supermarket, modeling customer behavior. The simulation uses probability transitions to generate realistic customer actions, such as browsing, purchasing, entering, and leaving the store.

The simulation is implemented in Python, utilizing NumPy and Pandas for data manipulation, and cv2 for visualization. The project aims to provide insights into customer behavior and store operations, and can be easily modified to simulate different scenarios and store layouts.

<br>

# Notes

- The simulation transition matrix is based on real-world customer data. So while the amount of customers in the simulation is stochastic, the probability of the amount of customers in the store at any one moment represents the real-world probability.
- Customers start entering the store at 7:30AM and leave the store at around 23:15PM
- In the animation different customer are identified by a shape and a color
- Customers will always enter and exit though the store entrance and will always checkout before exiting the store.
