from setuptools import setup


setup(name='toree_proxy_kernel',
    version='0.1',
    description='Toree Client Proxy Kernel',
    long_description='A simple echo kernel for Jupyter/IPython, based on MetaKernel',
    py_modules=['toree_proxy_kernel'],
    install_requires=['metakernel', 'py4j'],
    classifiers = [
        'Framework :: IPython',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Shells',
    ]
)
