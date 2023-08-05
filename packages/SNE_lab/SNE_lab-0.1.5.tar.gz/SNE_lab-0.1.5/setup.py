from distutils.core import setup
setup(
    name='SNE_lab',
    packages=[
        'SNE_lab',
        'SNE_lab.dataloaders',
        "SNE_lab.poolers",
        "SNE_lab.statevalidators",
        "SNE_lab.updator"
    ],
    version='0.1.5',
    description='Structured Neural Embedding model for research',
    long_description='This module aims to implement Structured Neural Embedding, a novel multi-task multi-label predictor, upon NumPy. It runs on MovieLens100K, MovieLens1M, Youtube, and Ego-net (Facebook)\'s network datasets. The original purpose of it was to serve as one of the baseline models in the paper Deep Energy Factorization Model for Demographic Prediction (Chih-Te Lai, Po-Kai Chang, et al). Give SNE-lab a try if either you need a handy implementation or you want a quick overview on multi-task multi-label prediction!',
    url='https://github.com/LplusKira/SNE_lab',
    author='Po-Kai Chang',
    author_email='pokaichangtwn@gmail.com',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Education",
        "Topic :: Utilities",
    ],
)
