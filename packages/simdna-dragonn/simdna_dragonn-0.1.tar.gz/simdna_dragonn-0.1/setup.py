from setuptools import setup

config = {
    'include_package_data': True,
    'description': 'Simulations of DNA for the Dragonn Package',
    'download_url': 'https://github.com/kundajelab/simdna_dragonn',
    'version': '0.1',
    'packages': ['simdna', 'simdna.resources'],
    'package_data': {'simdna.resources': ['encode_motifs.txt.gz',
                                          'HOCOMOCOv10_HUMAN_mono_homer_format_0.001.motif.gz']},
    'setup_requires': [],
    'install_requires': ['numpy>=1.15', 'matplotlib', 'scipy'],
    'dependency_links': [],
    'scripts': ['scripts/densityMotifSimulation.py',
                'scripts/emptyBackground.py',
                'scripts/motifGrammarSimulation.py'],
    'name': 'simdna_dragonn'
}

if __name__== '__main__':
    setup(**config)
