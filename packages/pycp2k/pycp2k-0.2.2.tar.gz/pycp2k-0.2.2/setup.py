from setuptools import setup, find_packages


def setup_manual():
    setup(
        name='pycp2k',
        version='0.2.2',
        description='A Python interface for CP2K.',
        long_description='A Python interface for CP2K.',
        url='https://github.com/SINGROUP/pycp2k.git',
        author='Lauri Himanen',
        author_email='lauri.himanen@gmail.com',
        license="Apache License 2.0",
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Scientific/Engineering :: Physics',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        keywords='cp2k CP2k pycp2k PYCP2K',
        python_requires='>=2.6, <4',
        packages=find_packages(),
        install_requires=[
            'future',
            'numpy',
            'ase',
        ]
    )

if __name__ == "__main__":
    setup_manual()
