import os
import glob
import cv2
import sys, getopt
import numpy as np
import matplotlib.image as mpimg

# Define a function to compute binned color features
def bin_spatial(img, size=(32, 32)):
    # Resize the image and use ravel() to flat the array
    features = cv2.resize(img, size).ravel()
    return features

# Define a function to compute color histogram features
def color_hist(img, nbins=32, bins_range=(0, 256)):
    # Compute the histogram of the color channels separately
    channel1_hist = np.histogram(img[:,:,0], bins=nbins, range=bins_range)
    channel2_hist = np.histogram(img[:,:,1], bins=nbins, range=bins_range)
    channel3_hist = np.histogram(img[:,:,2], bins=nbins, range=bins_range)
    # Concatenate the histograms into a single feature vector
    features = np.concatenate((channel1_hist[0], channel2_hist[0], channel3_hist[0]))
    return features

# Define a function to extract features from a list of images
# Have this function call bin_spatial() and color_hist()
def extract_features(imgs, cspace='RGB', spatial_size=(32, 32), hist_bins=32, hist_range=(0, 256)):
    # Create a list to append feature vectors to
    features = []
    # Iterate through the list of images
    for file in imgs:
        # Read in each one by one
        img = mpimg.imread(file)
        # Apply color conversion if other than 'RGB'
        if cspace == 'HSV':
            feature_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        elif cspace == 'HSL':
            feature_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSL)
        elif cspace == 'YUV':
            feature_img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        elif cspace == 'LUV':
            feature_img = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
        else:
            feature_img = np.copy(img)
        # Apply bin_spatial() to get spatial color features
        spatial_features = bin_spatial(feature_img, size=spatial_size)
        # Apply color_hist() also with a color space option now
        hist_features = color_hist(img, nbins=hist_bins, bins_range=hist_range)
        # Append the new feature vector to the features list
        features.append(np.concatenate((spatial_features, hist_features)))
    # Return list of feature vectors
    return features

if __name__ == '__main__':
    # Parse command line arguments
    cspace = 'RGB'
    spatial_size=(32,32)
    hist_bins=32
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["cspace=", "spatial_size=", "hist_bins="])
    except getopt.GetoptError:
        print('main.py --cspace <cspace> --spatial_size <spatial_size> --hist_bins <hist_bins>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py --cspace <cspace> --spatial_size <spatial_size> --hist_bins <hist_bins>')
            sys.exit()
        elif opt in ("--cspace"):
            cspace = arg
        elif opt in ("--spatial_size"):
            spatial_size = arg
        elif opt in ("--hist_bins"):
            hist_bins = arg

    # Read in car and non-car images
    vehicles = []
    non_vehicles = []
    for file in glob.glob('vehicles/**/*.png'):
        vehicles.append(file)
    for file in glob.glob('non-vehicles/**/*.png'):
        non_vehicles.append(file)

    # Extract features from vehicles and non vehicles dataset
    print("Extract features from datasets with cspace={}, spatial_size={}, hist_bins={}".format(cspace, spatial_size, hist_bins))
    vehicles_features = extract_features(vehicles, cspace=cspace, spatial_size=spatial_size, hist_bins=hist_bins)
    non_vehicles_features = extract_features(non_vehicles, cspace=cspace, spatial_size=spatial_size, hist_bins=hist_bins)
