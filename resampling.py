import numpy as np
import SimpleITK as sitk
import os
from tqdm import tqdm
import nibabel as nib

images_array = []
labels_array = []
for image in os.listdir('data/CT_files/imagesTr'):
    full_path = os.path.join('data/CT_files/imagesTr/', image)
    images_array.append(full_path)

for label in os.listdir('data/CT_files/labelsTr'):
    full_path = os.path.join('data/CT_files/labelsTr/', label)
    labels_array.append(full_path)


for element in tqdm(range(len(images_array))):
    img_path = images_array[element]
    label_path = labels_array[element]

    img = sitk.ReadImage(img_path)
    label = sitk.ReadImage(label_path)

    img.SetOrigin((0,0,0))
    label.SetOrigin((0,0,0))
    # img.SetOrigin([0, 0, 0])
    # label.SetOrigin([0, 0, 0])

    # nii_img = nib.load(img_path)
    # nii_label = nib.load(label_path)

    # img_affine = nii_img.affine
    # label_affine = nii_label.affine

    new_spacing = np.array([0.95, 0.95, 2.5])

    orig_size = np.array(img.GetSize(), dtype=int)
    orig_spacing = img.GetSpacing()

    new_size = np.ceil(orig_size * (orig_spacing / new_spacing)).astype(int)
    new_size = [int(s) for s in new_size]
    # print(orig_size)
    # print(orig_spacing)
    # print(new_size)

    for ct, arr in enumerate([img, label]):
        resample = sitk.ResampleImageFilter()
        resample.SetOutputSpacing(new_spacing)
        resample.SetOutputOrigin(img.GetOrigin())
        resample.SetSize(new_size)
        if ct == 0:
            resample.SetInterpolator = sitk.sitkBSpline
            img_resampled = resample.Execute(arr)

            writer = sitk.ImageFileWriter()
            writer.SetFileName('data/CT_files/images_resampled/' + 'img_' + str(element) + '_' + str(ct) + '.nii.gz')
            writer.Execute(img_resampled)
        else:
            resample.SetInterpolator = sitk.sitkNearestNeighbor
            lbl_resampled = resample.Execute(arr)

            label_writer = sitk.ImageFileWriter()
            label_writer.SetFileName('data/CT_files/labels_resampled/' + 'seg_' + str(element) + '_' + str(ct) + '_label.nii.gz')
            label_writer.Execute(lbl_resampled)
