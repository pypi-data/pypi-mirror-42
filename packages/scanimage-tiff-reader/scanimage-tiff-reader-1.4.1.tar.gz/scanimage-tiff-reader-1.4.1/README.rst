.. image:: https://gitlab.com/vidriotech/scanimagetiffreader-python/badges/master/pipeline.svg
   :target: https://gitlab.com/vidriotech/scanimagetiffreader-python/commits/master
   :alt: Pipeline status

.. image:: https://gitlab.com/vidriotech/scanimagetiffreader-python/badges/master/coverage.svg
   :target: https://gitlab.com/vidriotech/scanimagetiffreader-python/commits/master
   :alt: Coverage

About
=====

For more information see the documentation_.

The ScanImageTiffReader reads data from Tiff_ and BigTiff_ files recorded 
using ScanImage_.  It was written with performance in mind and provides access 
to ScanImage-specific metadata. It is also available for Matlab_, Julia_ and C_.
There's also a `command line interface`_. This library should actually work with 
most tiff files, but as of now we don't support compressed or tiled data.

The library is pip-installable for 64-bit Windows, OS X, or Linux.  We test 
against python 3.6 and python 2.7.14.

Both ScanImage_ and this reader are products of `Vidrio Technologies`_.  If you
have questions or need support feel free to `submit an issue`_ or `contact us`_.

.. _documentation: https://vidriotech.gitlab.io/scanimagetiffreader-python/
.. _Tiff: https://en.wikipedia.org/wiki/Tagged_Image_File_Format
.. _BigTiff: http://bigtiff.org/
.. _ScanImage: http://scanimage.org
.. _scanimage.org: http://scanimage.org
.. _Matlab: https://vidriotech.gitlab.io/scanimagetiffreader-matlab
.. _Julia: https://vidriotech.gitlab.io/scanimagetiffreader-julia
.. _`Vidrio Technologies`: http://vidriotechnologies.com/
.. _`contact us`: https://vidriotechnologies.com/contact-support/
.. _`submit an issue`: https://gitlab.com/vidriotech/scanimagetiffreader-python/issues
.. _C: https://vidriotech.gitlab.io/scanimage-tiff-reader
.. _`command line interface`: https://vidriotech.gitlab.io/scanimage-tiff-reader

Examples
========

Python
``````

.. code-block:: python

    from ScanImageTiffReader import ScanImageTiffReader
    vol=ScanImageTiffReader("my.tif").data();
