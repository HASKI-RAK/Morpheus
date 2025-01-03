class Config:
    def __init__(self):
        self.num_dist_info = {
            "cs": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "mcs": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "smir": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "smer": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "bfie": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "bfin": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "bfio": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "bfic": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
            "bfia": {
                "dist_type": "normal",
                "params": [5, 2],
                "possible_values": [1, 3, 5, 7, 9, 11],
            },
        }

        self.cat_dist_probs = {
            "AR": [0.5, 0.5],
            "SI": [0.5, 0.5],
            "VV": [0.5, 0.5],
            "SG": [0.5, 0.5],
        }
