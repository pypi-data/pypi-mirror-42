from setuptools import setup, find_packages

setup(name = 'srfnef',
      version = '0.5a1',
      description = 'Scalable Reconstruction Framework -- Not Enough Functions',
      author = 'Minghao Guo',
      author_email = 'mh.guo0111@gmail.com',
      license = 'Apache',
      # packages = ['srfnef'],
      packages = find_packages(),
      install_requires = [
          'scipy',
          'matplotlib',
          'typing',
          'h5py',
          'click',
          'numpy',
          'tqdm',
          'numba',
          'deepdish',
      ],
      zip_safe = False)
