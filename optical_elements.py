import numpy as np
import math

class LinearPolarizer:
    def __init__(self):
        
        self.x = np.array([[1], [0]])
        self.y = np.array([[0], [1]])
    
    def horizontal_vertical(self, bit):
        if bit == 0:
            return self.x
        else:
            return self.y
    
    def diagonal_polarization(self, bit):
        jones = (1/np.sqrt(2))*np.array([[1,1],[1,-1]])
        
        if bit == 0:
            return np.dot(jones, self.x)
        else:
            return np.dot(jones, self.y)
    
    def general_polarization(self, angle, basis):
        """
            angle to be in degrees
        """
        angle = (math.pi/180) * (angle)
        jones = np.array([[np.cos(angle), np.sin(angle)], [np.sin(angle), -np.cos(angle)]])
        
        return np.dot(jones, basis)

class PolarizingBeamSplitter:
    def __init__(self):
        pass
    
    def measure(self, vector, basis):
        """
            basis  : basis chosen by bob to measure polarization encoded photon
                        0 -> horizontal/vertical 
                        1 -> diagonal
            vector : Jones vector for polarized photon
            
            returns a dictionary with probabilities of the encoded bit sent by Alice being 0 or 1
        """
        #horizontal-vertical can be clubbed into an identity matrix
        horizontal = np.array([[1, 0], [0, 0]])
        vertical = np.array([[0, 0], [0, 1]])
        plus_minus = (1/np.sqrt(2))*np.array([[1,1],[1,-1]])

        if basis == 0:
            zero = np.dot(horizontal, vector)[0]
            one = np.dot(vertical, vector)[1]
        
        elif basis == 1:
            zero = np.dot(plus_minus, vector)[0]
            one = np.dot(plus_minus, vector)[1]
        else:
            print("here")
            return None
            
        return {0: zero[0]**2, 1: one[0]**2}
