from PIL import Image
import numpy as np

class Ascii:
    def __init__(self, path):
        self.path = path
    
    def getWidth(self):
        """Returns the width of an image."""
        return Image.open(self.path).width
    
    def getHeight(self):
        """Returns the height of an image."""
        return Image.open(self.path).height
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

        img_mat = [] # matrix of images pixels
        
        # loop through width of image
        for i in range(width):
            column = []    
            for j in range(height):
                column.append(img.getpixel((i, j))) # creating a column for the matrix
            img_mat.append(column) # add that column to the matrix           
        print(f"Successfully built a pixel matrix of height {height} and width {width}")
        return img_mat 
    @classmethod        
    def brightness(cls, matrix):
        """
        Converts each tuple with the matrix into a 'brightness' value.

        Loops through the rows and columns of the matrix and converts
        each tuple into the brightness value (calculated as the luminosity)
        of the R, G, and B values in the tuple -> .21R + .72G + .07B
        """
        # return [map(lambda R, G, B: .21*R + .72*G + .07*B, l) for l in matrix]
        print("Construction brightness matrix...")
        return [list(map( lambda tup: .21*tup[0] + .72*tup[2] + .07*tup[2], l)) for l in matrix]
    
    @classmethod
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
        abs_min = min(min(brightness_mat))
        abs_max = max(max(brightness_mat))
        # create 65 buckets to group character brightness into
        buckets = np.arange(abs_min, abs_max, (abs_max - abs_min)/len(ASCII))
        def bucketHelper(min, max, brightness, ascii_chars, buckets):
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
        ascii_str = []
        [ascii_str.append(str(bucketHelper(abs_min, abs_max, brightness, ASCII, buckets))) for val in brightness_mat for brightness in val]
        return "".join(ascii_str)
            
            

if __name__ == "__main__":
    ascii_art = Ascii("Ask-Logo-Small.jpg")
    
    # matrix where each pixel is an RGB tuple.
    img_mat = ascii_art.toMatrix(height = ascii_art.getHeight(), width = ascii_art.getWidth())
    
    # ASCII is only converned with the overall brightness of each value.
    # So, now we will convert each tuple into a single value that signals how 'bright' each pixel is
    bright_mat = ascii_art.brightness(matrix = img_mat)
    print(ascii_art.brightnessToAscii(bright_mat))

    # Now, convert brightness matrix -> ASCII character matrix
    # We need to decide how to map brightnesses -> characters
