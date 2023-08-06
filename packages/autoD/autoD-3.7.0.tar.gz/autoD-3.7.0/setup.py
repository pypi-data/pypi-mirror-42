import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
  name = 'autoD',
  packages = ['autoD'], 
  version = '3.7.0',
  description = 'A light-weight forward auto differentiation package',
  author = 'Wei Xuan, Chan',
  author_email = 'w.x.chan1986@gmail.com',
  license='MIT',
  url = 'https://github.com/WeiXuanChan/autoD',
  download_url = 'https://github.com/WeiXuanChan/autoD/archive/v3.7.0.tar.gz',
  keywords = ['differentiate', 'auto', 'forward'],
  classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
  #install_requires=['numpy'],
)
