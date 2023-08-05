# Official Library for verifier.meetchopra.com

# Installation
```pip install git+https://github.com/email-verifier/verifier-py.git```

or

```git clone https://github.com/email-verifier/verifier-py.git```

# Usage
The library exposes 2 methods. `verify` for boolean response making it simple and `verifyRequest` for having the API response in return


Below is the example of how to use the library

```python
import verifier
import json


if verifier.verify('meet@hooktap.in', 'API_TOKEN'):
    print("Hurray! Email is right!")
else:
    print("Oh! Email is not real")
```