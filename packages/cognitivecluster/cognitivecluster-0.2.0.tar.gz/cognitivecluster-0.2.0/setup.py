# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cognitivecluster']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0',
 'pandas>=0.24.1,<0.25.0',
 'scikit-learn>=0.20.2,<0.21.0',
 'tensorflow-hub>=0.2.0,<0.3.0',
 'tensorflow>=1.12,<2.0']

setup_kwargs = {
    'name': 'cognitivecluster',
    'version': '0.2.0',
    'description': 'A library to cluster partners based on metacognitive diversity',
    'long_description': "# Cognitive Cluster\n\n[![Build Status](https://travis-ci.org/mjs2600/cognitivecluster.svg?branch=master)](https://travis-ci.org/mjs2600/cognitivecluster)\n\nCognitive Cluster is a library for clustering written metacognitive exercises based on document embeddings.\nThis is useful for creating cross-cluster partnerships to increase the diversity of problem solving techniques in teams.\n\n## Installation\n\nTo instal `cognitivecluster`, run `pip install cognitivecluster`. The library currently only supports Python 3.6. This is a limitation in TensorFlow, as soon as Python 3.7 support is released, I will update this library to add 3.7 support.\n\n## Usage\n\nTo cluster people based on writing samples, pass either a Numpy array or a Pandas series to `cognitivecluster.sentence_vector_clusters`.\n\n### Examples\n\n```python\n>>> import cognitivecluster\n>>> cognitivecluster.sentence_vector_clusters(np_sentence_array)\narray([0, 0, 1, 1, 2, 2], dtype=int32)\n>>> df['cluster'] = cognitivecluster.sentence_vector_clusters(df.metacognitive_exercises)\n>>> df\n  metacognitive_exercises  cluster\n0          I like carrots        0\n1         I like potatoes        0\n2              I am a cat        1\n3              I am a dog        1\n4          This is a test        2\n5      This is a sequence        2\n```\n",
    'author': 'Michael Simpson',
    'author_email': 'michael@snthesis.com',
    'url': 'https://github.com/mjs2600/cognitivecluster',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
