# sktda-docs-config
Settings common across all scikit-tda doc sites

(soon) Install with 

```
pip install sktda_docs_config
```

and then add the following line to your docs' `conf.py` file:

```
from sktda_docs_config import *
```

You might also want to add the parameter to the `setup` function in your `setup.py`:

```
extras_require={
    'docs': [ # `pip install -e ".[docs]"`
        'sktda_docs_config'
    ]
},
```

this will make it so all required docs are installable with

```
pip install -e ".[docs]"    
```