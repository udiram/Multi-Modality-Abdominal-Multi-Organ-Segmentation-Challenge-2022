#!/usr/bin/env python
#########################################
#       nii2png for Python 3.7          #
#         NIfTI Image Converter         #
#                v0.2.9                 #
#                                       #
#     Written by Alexander Laurence     #
# http://Celestial.Tokyo/~AlexLaurence/ #
#    alexander.adamlaurence@gmail.com   #
#              09 May 2019              #
#              MIT License              #
#########################################

import scipy, numpy, shutil, os, nibabel
import sys, getopt
import scipy.misc
import imageio
from tqdm import tqdm

inputdir = 'data/AMOS22/labelsTr'
for file in tqdm(os.listdir(inputdir)):
    inputfile = os.path.join(inputdir, file)

    # print(inputfile)
    outputdir = "converteddirlabelsTr"
    outputfile = outputdir + "/" + inputfile.split(".")[0] + ".png"
    # print('Input file is ', inputdir + "/" + inputfile)
    # print('Output folder is ', outputfile)

    # set fn as your 4d nifti file
    image_array = nibabel.load(inputfile).get_data()
    # print(len(image_array.shape))


    # if 4D image inputted
    if len(image_array.shape) == 4:
        # set 4d array dimension values
        nx, ny, nz, nw = image_array.shape

        # set destination folder
        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
            # print("Created ouput directory: " + outputfile)

        # print('Reading NIfTI file...')

        total_volumes = image_array.shape[3]
        total_slices = image_array.shape[2]

        # iterate through volumes
        for current_volume in range(0, total_volumes):
            slice_counter = 0
            # iterate through slices
            for current_slice in range(0, total_slices):
                if (slice_counter % 1) == 0:
                    data = image_array[:, :, current_slice, current_volume]
                            
                    #alternate slices and save as png
                    # print('Saving image...')
                    image_name = inputfile[:-4] + "_t" + "{:0>3}".format(str(current_volume+1)) + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    imageio.imwrite(image_name, data)
                    # print('Saved.')

                    #move images to folder
                    # print('Moving files...')
                    src = image_name
                    shutil.move(src, outputfile)
                    slice_counter += 1
                    # print('Moved.')

        # print('Finished converting images')

    # else if 3D image inputted
    elif len(image_array.shape) == 3:
        # set 4d array dimension values
        nx, ny, nz = image_array.shape

        # set destination folder
        if not os.path.exists(outputfile):
            os.makedirs(outputfile)
            # print("Created ouput directory: " + outputfile)

        # print('Reading NIfTI file...')

        total_slices = image_array.shape[2]

        slice_counter = 0
        # iterate through slices
        for current_slice in range(0, total_slices):
            # alternate slices
            if (slice_counter % 1) == 0:
                data = image_array[:, :, current_slice]

                #alternate slices and save as png
                if (slice_counter % 1) == 0:
                    # print('Saving image...')
                    image_name = inputfile[:-4] + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
                    imageio.imwrite(image_name, data)
                    # print('Saved.')

                    #move images to folder
                    # print('Moving image...')
                    src = image_name
                    shutil.move(src, outputfile)
                    slice_counter += 1
                    # print('Moved.')

        # print('Finished converting images')
    else:
        print('Not a 3D or 4D Image. Please try again.')
