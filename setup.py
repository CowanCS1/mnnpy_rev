from os import cpu_count
from setuptools import setup
from pathlib import Path
from setuptools import Extension
# x86-64-v2 (any x86 CPU from about 2009), not -march=native: a wheel built with native carries
# the build machine's instruction set, and one built on an AVX-512 machine died with SIGILL
# ("illegal hardware instruction") on CPUs without it. Check a machine with:
# ld-linux-x86-64.so.2 --help
try:
    from Cython.Build import cythonize
    extm = cythonize([Extension('mnnpy._utils',
                      ['mnnpy/_utils.pyx'],
                      extra_compile_args = ['-O2', '-ffast-math', '-march=x86-64-v2', '-fopenmp'],
                      extra_link_args=['-fopenmp'])])
except ImportError:
    print('Building with c.')
    extm = [Extension('mnnpy._utils', 
            ['mnnpy/_utils.c'],
            extra_compile_args = ['-O2', '-ffast-math', '-march=x86-64-v2', '-fopenmp'],
            extra_link_args=['-fopenmp'])]

req_path = Path('requirements.txt')
with req_path.open() as requirements:
    requires = [l.strip() for l in requirements]

setup(name='mnnpy_rev',  # maintained fork of chriscainx/mnnpy; import name stays `mnnpy`
      version='0.1.12',
      description='Mutual nearest neighbors correction in python.',
      long_description='Correcting batch effects in single-cell expression datasets using the mutual nearest neighbors method.',
      url='http://github.com/chriscainx/mnnpy',
      author='Chris Kang',
      author_email='kbxchrs@gmail.com',
      license='BSD 3',
      packages=['mnnpy'],
      install_requires=requires,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      python_requires='>=3.4',
      py_modules=['irlb', 'mnn', 'utils'],
      ext_modules=extm,
      zip_safe=False)
