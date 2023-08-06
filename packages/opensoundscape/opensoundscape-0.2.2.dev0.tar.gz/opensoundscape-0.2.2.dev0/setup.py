# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['opensoundscape']

package_data = \
{'': ['*'],
 'opensoundscape': ['config/*',
                    'init/*',
                    'model_fit/*',
                    'model_fit/model_fit_algo/template_matching/*',
                    'predict/*',
                    'predict/predict_algo/template_matching/*',
                    'scripts/*',
                    'spect_gen/*',
                    'spect_gen/spect_gen_algo/template_matching/*',
                    'utils/*',
                    'view/*']}

install_requires = \
['docopt==0.6.2',
 'librosa==0.6.2',
 'llvmlite==0.27.0',
 'matplotlib==3.0.2',
 'numba==0.42.0',
 'numpy==1.15.4',
 'pandas==0.23.4',
 'pymongo==3.7.2',
 'pyqt5>=5.12,<6.0',
 'scikit-image==0.14.1',
 'scipy==1.2.0',
 'toolz>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['opensoundscape = opensoundscape.console:run',
                     'opso_dump_cross_corrs = '
                     'opensoundscape.scripts.dump_cross_correlations:run',
                     'opso_find_high_cross_corrs = '
                     'opensoundscape.scripts.find_high_cross_correlations:run',
                     'opso_find_important_templates = '
                     'opensoundscape.scripts.find_important_templates:run',
                     'opso_generate_images = '
                     'opensoundscape.scripts.generate_images:run',
                     'opso_raven_selections_to_template_db = '
                     'opensoundscape.scripts.raven_selections_to_template_db:run']}

setup_kwargs = {
    'name': 'opensoundscape',
    'version': '0.2.2.dev0',
    'description': 'Open source, scalable acoustic classification for ecology and conservation',
    'long_description': '[![https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/1681)\n\n# OpenSoundscape\n\n## Quick start guide\n\n*Note: installation instructions are for MacOS systems only.*\n\n* Install [Anaconda for Python 3](https://www.anaconda.com/download/#macos) and [HomeBrew](https://brew.sh/).\n* Use HomeBrew to install a few other packages: `brew install libsamplerate mongodb git wget`\n* Set up the Python environment:\n\n        conda install -c conda-forge python=3.6 pip=18.0 pandas=0.23.4 numpy=1.15.1 matplotlib=2.1.2 docopt=0.6.2 scipy=1.0.0 scikit-image=0.13.1 pymongo=3.4.0 opencv=3.4.3 scikit-learn=0.20.0 #for dev: pytest==3.6.1 black==18.9b0\n\n\tpip install librosa==0.6.2 #for dev: pre-commit==1.12.0\n\n* Download data files, the [CLO-43SD-AUDIO](https://datadryad.org/resource/doi:10.5061/dryad.j2t92) dataset:\n\n        cd ~/Downloads\n        wget "https://datadryad.org/bitstream/handle/10255/dryad.111783/CLO-43SD-AUDIO.tar.gz"\n        tar -xzf CLO-43SD-AUDIO.tar.gz\n        rm CLO-43SD-AUDIO.tar.gz\n\n\n* Download our training & prediction split of a subset of the CLO-43SD dataset:\n\n        cd ~/Downloads/CLO-43SD-AUDIO/\n        wget https://raw.github.com/rhine3/opso-support/master/clo-43sd-train-small.csv\n        wget https://raw.github.com/rhine3/opso-support/master/clo-43sd-predict-small.csv\n\n\n* Download OpenSoundscape:\n\n        mkdir ~/Code && cd ~/Code\n        git clone https://github.com/jkitzes/opensoundscape\n\n\n* Download our config file, `opso-test-small.ini`\n\n        cd ~/Code/opensoundscape/\n        wget https://raw.github.com/rhine3/opso-support/master/opso-test-small.ini\n\n\n* Edit the `.ini` to reflect the absolute path of your `Downloads` folder, e.g. with `vim`: `vim opso-test-small.ini`\n* Start the MongoDB daemon in another terminal: `mongod --config /usr/local/etc/mongod.conf`\n* Run OpenSoundscape:\n\n        ./opensoundscape.py init -i opso-test-small.ini\n        ./opensoundscape.py spect_gen -i opso-test-small.ini > spect-gen-output-small.txt\n        ./opensoundscape.py model_fit -i opso-test-small.ini > model-fit-output-small.txt\n        ./opensoundscape.py predict -i opso-test-small.ini > predict-output-small.txt\n',
    'author': 'Justin Kitzes',
    'author_email': 'justin.kitzes@pitt.edu',
    'url': 'https://github.com/jkitzes/opensoundscape',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
