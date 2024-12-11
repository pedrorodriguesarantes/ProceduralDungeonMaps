import numpy as np
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter

class mapGenerator:
    def __init__(self, graph, custom_layout, margin_factor = 0.2):
        self.G = graph
        self.custom_layout = custom_layout
        self.margin_factor = margin_factor
    
    def getCoordinates(self):
        node_positions = np.array([pos for pos in self.custom_layout.values()])
        x_coords = node_positions[:, 0]
        y_coords = node_positions[:, 1]

        x_range = x_coords.max() - x_coords.min()
        y_range = y_coords.max() - y_coords.min()

        x_min = x_coords.min() - self.margin_factor * x_range
        x_max = x_coords.max() + self.margin_factor * x_range
        y_min = y_coords.min() - self.margin_factor * y_range
        y_max = y_coords.max() + self.margin_factor * y_range

        x_grid, y_grid = np.meshgrid(
            np.linspace(x_min, x_max, 200),
            np.linspace(y_min, y_max, 200)
        )

        return [x_coords, y_coords, x_range, y_range, x_grid, y_grid, node_positions]
    
    def islandContour(self):
        _, _, _, _, x_grid, y_grid, node_positions = self.getCoordinates()

        kde = gaussian_kde(node_positions.T, bw_method=0.215) 
        density = kde(np.vstack([x_grid.ravel(), y_grid.ravel()])).reshape(x_grid.shape)
        
        weight_map = np.random.uniform(0.5, 1.5, size=density.shape) 
        weight_map = gaussian_filter(weight_map, sigma=5) 
        
        noise_strength = 0.03
        noise = np.random.normal(scale=noise_strength * density.std(), size=density.shape)
        weighted_noise = noise * weight_map

        density_with_noise = density + weighted_noise
        density_with_noise = np.clip(density_with_noise, 0, None)
        density_with_noise = gaussian_filter(density_with_noise, sigma=0.1)
        
        contour_levels = np.linspace(density_with_noise.min(), density_with_noise.max(), 11)

        return [density_with_noise, contour_levels]