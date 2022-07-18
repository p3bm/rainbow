import os 
import numpy as np


class DataFile:
    """
    Class representing a chromatogram data file. 

    Args:
        path (str): Path of the file. 
        detector (str): Detector for the file. 
        xlabels (numpy.ndarray): 1D array with retention times (in minutes).
        ylabels (numpy.ndarray): 1D array with y-axis labels 
            (e.g. mz, wavelength). 
        data (numpy.ndarray): 2D array with data values (e.g. intensity).
        metadata (dict): Metadata for the file. 

    Attributes:
        name (str): Name of the file. 
        detector (str): Name of the detector. Options: UV, MS, FID, CAD, ELSD.
        xlabels (numpy.ndarray): 1D array with retention times (in minutes).
        ylabels (numpy.ndarray): 1D array with y-axis labels 
            (e.g. mz, wavelength). 
        data (numpy.ndarray): 2D array with data values (e.g. intensity).
            The rows correspond to the retention times and the columns 
            correspond to the y-axis labels.
        metadata (dict): Depends on the vendor and file format. 

    """
    def __init__(self, path, detector, xlabels, ylabels, data, metadata):
        self.name = os.path.basename(path)
        self.detector = detector 
        self.xlabels = xlabels 
        self.ylabels = ylabels
        self.data = data
        self.metadata = metadata

    def __repr__(self):
        return f"{self.name}"

    def get_info(self):
        """ 
        Returns a string summary of the DataFile. 

        """ 
        return f"\n{'-' * len(self.name)}\n" \
               f"{self.name}\n" \
               f"{'-' * len(self.name)}\n" \
               f"Detector: {self.detector}\n" \
               f"Xlabels: {self.xlabels}\n" \
               f"Ylabels: {self.ylabels}\n" \
               f"Data: {self.data}\n" \
               f"Metadata: {self.metadata}\n" 

    def extract_traces(self, labels=None):
        """
        Extracts data corresponding to the specified ylabel(s).

        Raises an exception if any ylabel(s) are invalid. 

        Args:
            labels (int/float/list, optional): Ylabel(s) to extract. 
        
        Returns:
            2D numpy array containing data for the specified ylabel(s). 
            The rows correspond to the ylabels and the columns corrrespond \
                to the retention times. 

        """

        if not labels:
            return self.data.T

        if isinstance(labels, int) or isinstance(labels, float):
            labels = [labels]

        if not isinstance(labels, list):
            raise Exception(f"Invalid type for labels.")

        indices = np.searchsorted(self.ylabels, labels)
        invalid_check = np.where(indices == len(labels))[0]
        if invalid_check.size > 0:
            raise Exception(f"Label {labels[i]} not in {filename}.")
        
        traces = self.data[:,indices].T

        return traces

    def export_csv(self, filename, labels=None, delim=','):
        """
        Outputs a CSV containing data for the specified ylabel(s).

        Args:
            filename (str): Filename for the output CSV.
            labels (int/float/list, optional): Ylabel(s) to export. 
            delim (str, optional): Delimiter used in the output CSV. 

        """
        f = open(filename, 'w+')
        f.write(self.to_csvstr(labels, delim))
        f.close()
    
    def to_csvstr(self, labels=None, delim=','):
        """
        Returns a string representation of a CSV containing data \
            for the specified ylabel(s).
        
        Args:
            labels (int/float/list, optional): Ylabel(s) to return.
            delim (str, optional): Delimiter used in the CSV representation.

        """
        str_traces_tp = self.extract_traces(labels).T.astype(str)

        if not labels:
            labels = self.ylabels.tolist()

        if isinstance(labels, int) or isinstance(labels, float):
            labels = [labels]

        if not isinstance(labels, list):
            raise Exception(f"Invalid type for labels.")

        str_labels = [str(label) for label in labels]

        csvstr = f"RT (min){delim}{f'{delim}'.join(str_labels)}\n"
        for i in range(self.xlabels.size):
            csvstr += f"{self.xlabels[i]}{delim}" \
                      f"{f'{delim}'.join(str_traces_tp[i])}\n"
        return csvstr

    def plot(self, label, **kwargs):
        """
        Shows a basic matplotlib plot for the specified ylabel.

        Args:
            label (int/float): Ylabel to be plotted. 
            **kwargs (optional): Keyword arguments for matplotlib.

        """
        import matplotlib.pyplot as plt
        plt.plot(self.xlabels, self.extract_traces(label).T, **kwargs)
        plt.show()