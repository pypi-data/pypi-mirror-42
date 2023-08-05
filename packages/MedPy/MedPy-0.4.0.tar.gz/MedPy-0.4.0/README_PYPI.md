# MedPy

[GitHub](https://github.com/loli/medpy/) | [Documentation](http://loli.github.io/medpy/) | [Tutorials](http://loli.github.io/medpy/) | [Issue tracker](https://github.com/loli/medpy/issues) | [Contact](oskar.maier@gmail.com)

**MedPy** is a library and script collection for medical image processing in Python, providing basic functionalities for **reading**, **writing** and **manipulating** large images of **arbitrary dimensionality**.
Its main contributions are n-dimensional versions of popular **image filters**, a collection of **image feature extractors**, ready to be used with [scikit-learn](http://scikit-learn.org), and an exhaustive n-dimensional **graph-cut** package.

* [Installation](#installation)
* [Getting started with the library](#getting-started-with-the-library)
* [Getting started with the scripts](#getting-started-with-the-scripts)
* [Read/write support for medical image formats](#read-write-support-for-medical-image-formats)
* [Requirements](#requirements)
* [License](#license)

## Installation

```bash
sudo apt-get install libboost-python-dev build-essential
pip3 install medpy
```

**MedPy** requires **Python 3** and officially supports Ubuntu as well as other Debian derivatives.
For installation instructions on other operating systems see the [documentation](http://loli.github.io/medpy/).
While the library itself is written purely in Python, the **graph-cut** extension comes in C++ and has it's own requirements. More details can be found in the [documentation](http://loli.github.io/medpy/).

### Using Python 2

**Python 2** is no longer supported. But you can still use the older releases.

```bash
pip install medpy==0.3.0
```

## Getting started with the library

If you already have a medical image whose format is support (see the [documentation](http://loli.github.io/medpy/>) for details), then good.
Otherwise, navigate to http://www.nitrc.org/projects/inia19, click on the *Download Now* button, unpack and look for the *inia19-t1.nii* file. Open it in your favorite medical image viewer (I personally fancy [itksnap](http://www.itksnap.org)) and beware: the INIA19 primate brain atlas.

Load the image

```python
from medpy.io import load
image_data, image_header = load('/path/to/image.xxx')
```

The data is stored in a numpy ndarray, the header is an object containing additional metadata, such as the voxel-spacing. Now lets take a look at some of the image metadata

```python
image_data.shape
```

`(168, 206, 128)`

```python
image_data.dtype
```

`dtype(float32)`

And the header gives us

```python
image_header.get_voxel_spacing()
```

`(0.5, 0.5, 0.5)`

```python
image_header.get_offset()
```

`(0.0, 0.0, 0.0)`

Now lets apply one of the **MedPy** filter, more exactly the [Otsu thresholding](https://en.wikipedia.org/wiki/Otsu%27s_method), which can be used for automatic background removal

```python
from medpy.filter import otsu
threshold = otsu(image_data)
output_data = image_data > threshold
```

And save the binary image, marking the foreground

```python
from medpy.io import save
save(output_data, '/path/to/otsu.xxx', image_header)
```

After taking a look at it, you might want to dive deeper with the tutorials found in the [documentation](http://loli.github.io/medpy/).

## Getting started with the scripts

**MedPy** comes with a range of read-to-use commandline scripts, which are all prefixed by `medpy_`.
To try these examples, first get an image as described in the previous section. Now call

```bash
medpy_info.py /path/to/image.xxx
```

will give you some details about the image. With

```bash
medpy_diff.py /path/to/image1.xxx /path/to/image2.xxx
```

you can compare two image. And

```bash
medpy_anisotropic_diffusion.py /path/to/image.xxx /path/to/output.xxx
```

lets you apply an edge preserving anisotropic diffusion filter. For a list of all scripts, see the [documentation](http://loli.github.io/medpy/).

## Read/write support for medical image formats

MedPy relies on SimpleITK, which enables the power of ITK for image loading and saving.
The supported image file formats should include at least the following. Note that not all might be supported by your machine.

**Medical formats:**

* ITK MetaImage (.mha/.raw, .mhd)
* Neuroimaging Informatics Technology Initiative (NIfTI) (.nia, .nii, .nii.gz, .hdr, .img, .img.gz)
* Analyze (plain, SPM99, SPM2) (.hdr/.img, .img.gz)
* Digital Imaging and Communications in Medicine (DICOM) (.dcm, .dicom)
* Digital Imaging and Communications in Medicine (DICOM) series (<directory>/)
* Nearly Raw Raster Data (Nrrd) (.nrrd, .nhdr) 
* Medical Imaging NetCDF (MINC) (.mnc, .MNC)
* Guys Image Processing Lab (GIPL) (.gipl, .gipl.gz)

**Microscopy formats:**

* Medical Research Council (MRC) (.mrc, .rec)
* Bio-Rad (.pic, .PIC)
* LSM (Zeiss) microscopy images (.tif, .TIF, .tiff, .TIFF, .lsm, .LSM)
* Stimulate / Signal Data (SDT) (.sdt)

**Visualization formats:**

* VTK images (.vtk)

**Other formats:**

* Portable Network Graphics (PNG) (.png, .PNG)
* Joint Photographic Experts Group (JPEG) (.jpg, .JPG, .jpeg, .JPEG)
* Tagged Image File Format (TIFF) (.tif, .TIF, .tiff, .TIFF)
* Windows bitmap (.bmp, .BMP)
* Hierarchical Data Format (HDF5) (.h5 , .hdf5 , .he5)
* MSX-DOS Screen-x (.ge4, .ge5)

## Requirements

MedPy comes with a number of dependencies and optional functionality that can require you to install additional packages.

### Main dependencies

* [scipy](http://www.scipy.org)
* [numpy](http://www.numpy.org)
* [SimpleITK](https://simpleitk.readthedocs.io)

### Optional functionalities

* compilation with `max-flow/min-cut` (enables the GraphCut functionalities)

## License

MedPy is distributed under the GNU General Public License, a version of which can be found in the LICENSE.txt file.
