from PIL import Image
import numpy as np
from colorama import Fore
import sys

class Ascii:
    def __init__(self, path):
        self.path = path
    
    def getWidth(self):
        """Returns the width of an image."""
        return Image.open(self.path).width
    
    def getHeight(self):
        """Returns the height of an image."""
        return Image.open(self.path).height

    def getMin(self, matrix):
        return min(map(min, matrix))

    def getMax(self, matrix):
        return max(map(max, matrix))

    def toMatrix(self, height, width):
        """
        Converts an Image into a matrix of tuples, where each tuple represents a pixel value.
        
        Utilizes the height and width of the image to loop through all
        rows and columns, append each value in a row to a list, and then
        append that list to create a matrix of tuples. Each tuple contains
        three values, one for Red, one for Green, and one for Blue.
        
        Parameters
        ----------
        height : (int)
            the height of the image
        width : (int)
            the width of the image

        Returns
        ----------
        A matrix representation of the image.
        """
        img = Image.open(self.path)
        pixels = list(img.getdata())                
        
        return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]       

    @classmethod   # won't be changed     
    def brightness(cls, matrix, eq):
        """
        Converts each tuple with the matrix into a 'brightness' value.

        Loops through the rows and columns of the matrix and converts
        each tuple into the brightness value (calculated as the luminosity)
        of the R, G, and B values in the tuple -> .21R + .72G + .07B

        Parameters
        ----------
        matrix : (2-d list)
            the matrix of pixel vaues
        eq : (str)
            the type of equation to use for converting a tuple of pixel values to brightness.

        Returns
        ----------
        Returns a matrix of brightness values
        """
        print("Construction brightness matrix...")
        if eq.lower() == "luminosity":
            return [list(map( lambda tup: .21*tup[0] + .72*tup[1] + .07*tup[2], l)) for l in matrix]
        elif eq.lower() == "average":
            return [list(map( lambda tup: (tup[0] + tup[1] + tup[2])/3, l)) for l in matrix]
        elif eq.lower() == "lightness":
            return [list(map( lambda tup: (max(tup) + min(tup))/2, l)) for l in matrix]
        else:
            return "Error: Try `lightness`, `average`, or `luminosity`."

    @classmethod # won't be changed
    def normalize(cls, brightness_matrix, maximum, minimum):
        """Takes a brightness matrix as input and normalizes the values between 0 and 1 (Min-Max Normalization)."""
        return [(val - minimum)/(maximum - minimum) for row in brightness_matrix for val in row]
    
    @classmethod # won't be changed
    def brightnessToAscii(cls, brightness_mat):
        """
        Returns each value in a brightness matrix mapped
        to its corresponding ASCII character.

        Parameters
        ----------
        brightness_mat : (matrix)
            the brightness matrix to convert to ASCII characters.

        Returns
        ----------
        A matrix of ASCII characters.
        """
        ASCII = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        abs_min = min(brightness_mat)
        abs_max = max(brightness_mat)
        # create 65 buckets to group character brightness into
        buckets = np.arange(abs_min, abs_max+0.1, (abs_max - abs_min)/len(ASCII))
        def asciiChar(min, max, brightness, ascii_chars, buckets):
            """
            assign an ascii character to a brightness value and return it.

            Parameters
            ----------
            min : (int)
                the minimum brightness
            max : (int)
                the maximum brightness
            brightness : (int)
                a brightness value
            ascii_chars : (string or any iterable)
                a string of ascii characters
            buckets : (list or any iterable of len(ascii_chars))
                a sorted list of evenly split values that range from
                min(brightness) to max(brightness)

            Returns
            ----------
            The ascii character assigned to the brightness value.
            """
            for val in buckets:
                if val < brightness:
                    pass
                else:
                    index_val = list(buckets).index(val)
                    return ASCII[index_val -1]
                
        s = ""
        for val in brightness_mat:
            s += asciiChar(abs_min, abs_max, val , ASCII, buckets) 
        return s

    def print_ascii_matrix(self, ascii_matrix, text_color):
        line = [p for row in ascii_matrix for p in row]
        print(text_color + "".join(line))
            

if __name__ == "__main__":
    jpg_name = sys.argv[2].lower().strip()    
    ascii_art = Ascii(jpg_name)
    
    # matrix where each  pixel is an RGB tuple.
    img_mat = ascii_art.toMatrix(height = ascii_art.getHeight(), width = ascii_art.getWidth())
    
    # ASCII is only converted with the overall brightness of each value.
    # So, now we will convert each tuple into a single value that signals how 'bright' each pixel is
    # and then normalize these values
    brightness_eq = sys.argv[3].lower().strip()
    bright_mat = ascii_art.brightness(matrix = img_mat, eq = brightness_eq)   
    print("Completed creating brightness matrix") 
    normalized_brightness_mat = ascii_art.normalize(bright_mat, maximum = ascii_art.getMax(bright_mat), minimum=ascii_art.getMin(bright_mat))
    print("Completed converting brightness -> normalized values")

    # Now, convert brightness matrix -> ASCII character matrix
    # We need to decide how to map brightnesses -> characters
    ascii_mat = ascii_art.brightnessToAscii(normalized_brightness_mat)
    print("Completed converting normalized values -> ascii")

    ascii_art.print_ascii_matrix(ascii_mat, Fore.GREEN)


    