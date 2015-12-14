import os

build_dir = "build"
target = "vita.tex"

# Set the build directory
VariantDir(build_dir, ".", duplicate=False)

# Build the document
env = Environment()
latex_build = env.PDF(os.path.join(build_dir, target))
