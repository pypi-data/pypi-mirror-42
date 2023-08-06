import os
import io
from setuptools import setup

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

long_description = read('README.md')

setup_info = dict(
    name='modelsummary',
    version='1.0.4',
    author='Tae Hwan Jung(@graykode)',
    author_email='nlkey2022@gmail.com',
    url='https://github.com/graykode/modelsummary',
    description='All Model summary in PyTorch similar to `model.summary()` in Keras',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[ 'tqdm', 'torch', 'numpy'],
    keywords='pytorch model summary model.summary()',
)

setup(**setup_info)