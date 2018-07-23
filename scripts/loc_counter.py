
from pycount.core import Counter

COUNTER = Counter('C://Users//bctech//Desktop//MaxSondereggerCode//Raiders',
                  ignore=["venv", "__pycache__", "README.md", ".idea"])
COUNTER.discover()
COUNTER.count()
print(COUNTER.results)
