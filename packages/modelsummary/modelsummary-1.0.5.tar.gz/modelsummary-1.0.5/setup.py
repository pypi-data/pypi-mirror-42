import os
import io
from setuptools import setup

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read().strip()

setup_info = dict(
    name='modelsummary',
    version='1.0.5',
    author='Tae Hwan Jung(@graykode)',
    author_email='nlkey2022@gmail.com',
    url='https://github.com/graykode/modelsummary',
    description='All Model summary in PyTorch similar to `model.summary()` in Keras',
    long_description=long_description,
    license='MIT',
    install_requires=[ 'tqdm', 'torch', 'numpy'],
    keywords='pytorch model summary model.summary()',
)

setup(**setup_info)