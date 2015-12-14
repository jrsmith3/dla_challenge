Joshua Ryan Smith's Curriculum Vitae
====================================
Featured on such sites as [Joshua's own site](https://jrsmith3.github.io)!

This repo contains two branches: 

* `master`: Hosts the CV in reStructuredText. This version is easily included in Joshua's aforementioned site.
* `pdf`: Hosts a LaTeX version of the CV. This version is derived from the rst via [pandoc](http://pandoc.org) conversion.


Converting from rst to LaTeX/PDF
--------------------------------
1. Create a new branch from master.
2. Convert the rst to LaTeX using pandoc, git add the LaTeX, git rm the rst, and commit the conversion.

        pandoc -o cv.tex cv.rst

3. Attempt to merge the new branch into pdf. Fix any merge conflicts.
4. Manually edit the resulting LaTeX until an acceptably formatted PDF is produced.

