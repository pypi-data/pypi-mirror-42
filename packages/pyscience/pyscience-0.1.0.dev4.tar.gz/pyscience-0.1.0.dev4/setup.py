import setuptools
import pyscience

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyscience',
    version=pyscience.__version__,
    author='Manuel Alcaraz Zambrano',
    #author_email="",
    description='python science programming',
    long_description=long_description,
    long_description_content_type='text/markdown',
    #url='',
    license='MIT',
    packages=setuptools.find_packages(),
    package_data={
        'pyscience': ['chemistry/periodic_table.csv'],
    },
    python_requires='~=3.7',
    entry_points={
        'console_scripts': [
            'pyscience=pyscience:__main__.run',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ],
)
