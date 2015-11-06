import os

build_dir = "build"
target = "cover_letter.tex"

# Set the build directory
VariantDir(build_dir, ".")

# Build the document
env = Environment()
latex_build = env.PDF(os.path.join(build_dir, target))
