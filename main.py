import sys

import battleship.simulation as sim

if __name__ == '__main__':
    simulations = [
        sim.ManualVsManualSimulation(),
        sim.ManualVsRandomSimulation(),
        sim.RandomVsRandomSimulation(),
        sim.ManualVsAutomaticSimulation(),
        sim.RandomVsAutomaticSimulation(),
        sim.AutomaticVsAutomaticSimulation(),
    ]
    
    index = 0
    
    # read index from command line. Defaults to 0 (manual)
    if len(sys.argv) > 1:
        try:
            index = int(sys.argv[1])
        except ValueError:
            index = 0

    # Run multiple games at once to better assess the AI's performance
    results = 0
    total_plays = 10 ** 4

    for play in range(total_plays):
        simulation = simulations[index]
        if index == 4:
            results += simulation.run()
        else:
            simulation.run()

    print(f"BOB WON {results * 100 / total_plays}% OF THE TIME")

