# V0.1.6

* Added job metadata feature. cli new argument: `--job-metadata` which points to JSON file with job metadata. This metadata, if provided, is used for naming PDF automatically
* Added tests for `cliriculum.deserializers` and fixed bad management of null values https://github.com/sondalex/cliriculum/issues/36.
* Fixed regression which constrained to use a profile picture in resume (related to previous point)

# V0.1.5.1

* Fixed https://github.com/sondalex/cliriculum/issues/16 . I.e support for Python > 3.9

## V0.1.5

* Added wrapper to chromium headless print. Now resume creation can be 100% automated. Solves https://github.com/sondalex/cliriculum/issues/10
* Fixed problem of files not being updated when setting overwrite to True https://github.com/sondalex/cliriculum/issues/13#issue-1558181130


## V0.1.4.2

* Added support for HTML blocks.

## V0.1.4.1

* Added custom stylesheet support

## V0.1.4

* Added profile picture support

## V0.1.3

* Fixed sidebar which would push main content on sidebar overflow.

## V0.1.2.2

* Fixed date icon padding in  style.css

## V0.1.2.1

* Changed style.css font size
* Fixed main box dimension in style.css

## V0.1.2

* Corrected error in make_resume function

## V0.1.1

* Added cli support
* Updated documentation
Some info
