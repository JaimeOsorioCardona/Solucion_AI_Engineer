"""
Clean and Optimized Router Module using Pure Python.

This module provides functionality to match drivers with packages based on proximity
using a spatial grid optimization (Spatial Hashing) since external libraries 
like scipy are unavailable in this environment.

Space complexity: O(N)
Time complexity: O(N + M) average case with uniform distribution.
"""

import math
import time
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict
from collections import defaultdict

@dataclass
class Driver:
    """Represents a driver with an ID and coordinates."""
    id: int
    x: int
    y: int

@dataclass
class Package:
    """Represents a package with an ID, coordinates, and priority."""
    id: int
    x: int
    y: int
    priority: str

@dataclass
class MatchResult:
    """Represents a match between a driver and a package."""
    driver_id: int
    package_id: int
    distance: float

def generate_data(num_drivers: int = 2000, num_packages: int = 5000) -> Tuple[List[Driver], List[Package]]:
    """
    Generates random data for drivers and packages.
    """
    random.seed(42) # For reproducibility
    drivers = [
        Driver(i, random.randint(0, 1000), random.randint(0, 1000))
        for i in range(num_drivers)
    ]
    packages = [
        Package(j, random.randint(0, 1000), random.randint(0, 1000), "high")
        for j in range(num_packages)
    ]
    return drivers, packages

def get_grid_key(x: int, y: int, cell_size: int) -> Tuple[int, int]:
    """Returns the grid key for a given coordinate."""
    return (int(x // cell_size), int(y // cell_size))

def find_matches_optimized(drivers: List[Driver], packages: List[Package], max_distance: float = 50.0) -> List[MatchResult]:
    """
    Finds matches between drivers and packages within a maximum distance
    using a spatial grid optimization.
    """
    start_time = time.time()
    print("Calculando (Optimized - Spatial Grid)...")

    # Use a grid cell size equal to or slightly larger than max_distance
    cell_size = int(max_distance)
    grid: Dict[Tuple[int, int], List[Package]] = defaultdict(list)

    # 1. Populate the grid with packages
    for pkg in packages:
        key = get_grid_key(pkg.x, pkg.y, cell_size)
        grid[key].append(pkg)

    matches: List[MatchResult] = []

    # 2. Query for each driver
    for driver in drivers:
        d_key = get_grid_key(driver.x, driver.y, cell_size)
        dx_grid, dy_grid = d_key
        
        # Check adjacent cells (3x3 grid around the driver's cell)
        # Since cell_size >= max_distance, we only need to check immediate neighbors
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_key = (dx_grid + i, dy_grid + j)
                if neighbor_key in grid:
                    for pkg in grid[neighbor_key]:
                        # Distance check
                        # Pre-check bounding box (optional, but good for heavy distance calculation)
                        if abs(driver.x - pkg.x) <= max_distance and abs(driver.y - pkg.y) <= max_distance:
                            dist_sq = (driver.x - pkg.x)**2 + (driver.y - pkg.y)**2
                            if dist_sq < max_distance**2:
                                matches.append(MatchResult(driver.id, pkg.id, math.sqrt(dist_sq)))

    end_time = time.time()
    print(f"Tiempo (Optimized): {end_time - start_time:.4f} seconds")
    return matches

def find_matches_brute_force(drivers: List[Driver], packages: List[Package], max_distance: float = 50.0) -> List[MatchResult]:
    """
    Original brute-force approach O(N*M) for benchmark comparison.
    """
    start_time = time.time()
    print("Calculando (Brute Force - Original O(N*M))...")

    matches: List[MatchResult] = []
    for driver in drivers:
        for pkg in packages:
            dist = math.sqrt((driver.x - pkg.x)**2 + (driver.y - pkg.y)**2)
            if dist < max_distance:
                matches.append(MatchResult(driver.id, pkg.id, dist))

    end_time = time.time()
    print(f"Tiempo (Brute Force): {end_time - start_time:.4f} seconds")
    return matches


def main() -> None:
    """Main execution function with performance comparison."""
    drivers, packages = generate_data()

    # Run brute-force (original approach)
    matches_bf = find_matches_brute_force(drivers, packages)
    print(f"Brute Force Matches: {len(matches_bf)}")

    print("---")

    # Run optimized calculation
    matches_opt = find_matches_optimized(drivers, packages)
    print(f"Optimized Matches:   {len(matches_opt)}")

    # Verify correctness: both must find the same number of matches
    assert len(matches_bf) == len(matches_opt), (
        f"Mismatch! Brute force found {len(matches_bf)}, optimized found {len(matches_opt)}"
    )
    print("\n✓ Both methods found the same number of matches. Optimization is correct.")

if __name__ == "__main__":
    main()
