"""
Visualizer for cancer data clusters

Import PlotCluster class into your code and initialize with a list of clusters
"""

import math
import simplegui


# Constants
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 634

# URLS for various raw data sets
DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"


# List of 15 colors for clusters
COLORS = ['Aqua', 'Yellow', 'Blue', 'Fuchsia', 'Black', 'Green', 'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Brown', 'Teal']

# Helper functions


def circle_radius(pop):
    """
    Compute radius of circle whose area is proportional to population
    """
    return math.sqrt(pop) / 200
   

class PlotClusters:
    """
    Interactive frame to visualize cancer data
    """

    def __init__(self, data_table, cluster_list):
        """
        Create a frame and load the cancer data
        """
        self._frame = simplegui.create_frame("Cancer risk visualization", CANVAS_WIDTH, CANVAS_HEIGHT, 100)
        self._frame.set_canvas_background("White")
        self._frame.set_draw_handler(self.draw)
        self._toggle_label = self._frame.add_button("Draw centers", self.toggle_display)
        self._draw_centers = True
        self._data_table = data_table
        self._cluster_list = cluster_list
        self._fips_to_line = {}
        for line_idx in range(len(self._data_table)):
            self._fips_to_line[self._data_table[line_idx][0]] = line_idx
        self._USA_Counties = simplegui.load_image(MAP_URL)
        self._frame.start()
                                          
    
    def toggle_display(self):
        """
        Handler for button that toggles the display between clusters and center
        """
        if self._draw_centers:
            self._draw_centers = False
            self._toggle_label.set_text("Draw centers")
        else:
            self._draw_centers = True
            self._toggle_label.set_text("Draw counties")

    def draw(self, canvas):
        """
        Draw handler for visualizer
        """
        canvas.draw_image(self._USA_Counties, [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [CANVAS_WIDTH, CANVAS_HEIGHT], 
                                             [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2], [CANVAS_WIDTH, CANVAS_HEIGHT])

        for cluster_idx in range(len(self._cluster_list)):
            cluster = self._cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = self._data_table[self._fips_to_line[fips_code]]
                canvas.draw_circle([line[1], line[2]], circle_radius(line[3]), 1, cluster_color, cluster_color)

        if self._draw_centers:                
            for cluster_idx in range(len(self._cluster_list)):
                cluster = self._cluster_list[cluster_idx]
                cluster_color = COLORS[cluster_idx % len(COLORS)]
                cluster_center = (cluster.horiz_center(), cluster.vert_center())
                for fips_code in cluster.fips_codes():
                    line = self._data_table[self._fips_to_line[fips_code]]
                    canvas.draw_line([line[1], line[2]], cluster_center, 1, cluster_color)                
                cluster_pop = cluster.total_population()
                canvas.draw_circle(cluster_center, circle_radius(cluster_pop), 2, "Black")

        if self._draw_centers:                
            for cluster_idx in range(len(self._cluster_list)):
                cluster = self._cluster_list[cluster_idx]
                cluster_color = COLORS[cluster_idx % len(COLORS)]
                cluster_center = (cluster.horiz_center(), cluster.vert_center())
                cluster_pop = cluster.total_population()
                canvas.draw_circle(cluster_center, circle_radius(cluster_pop), 2, "Black")
                






    
    
    
