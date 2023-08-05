PyuMetric
=========

A Python Package to unify time series data sources.

[![Build Status](https://travis-ci.org/silverbackhq/pyumetric.svg?branch=master)](https://travis-ci.org/silverbackhq/pyumetric)
[![PyPI version](https://badge.fury.io/py/pyumetric.svg)](https://badge.fury.io/py/pyumetric)

Installation
------------
To install PyuMetric run this command:
```
pip3 install pyumetric
```

Usage
-----
After installing the library, Read the following usage criteria:

```python
from pyumetric import NewRelic_Provider


new_relic = NewRelic_Provider("api_key_here")
# Get apps list
new_relic.get_apps()
# Get app info (12345 is the app id)
new_relic.get_app(12345)
# Get all metric list
new_relic.get_metrics(12345)
# Get Metrics list with a filter (Apdex)
new_relic.get_metrics(12345, "Apdex")
# Get Metric Values from 2019-02-01T01:00:00+00:00 to 2019-02-14T11:03:20+00:00
new_relic.get_metric(244202213, ["WebTransaction"], ["average_response_time"], "2019-02-01T01:00:00+00:00", "2019-02-14T11:03:20+00:00", False)
```

Misc
====

Changelog
---------
Version 0.0.2:
```
Initial Release.
```

Acknowledgements
----------------

© 2019, Silverback. Released under [MIT License](https://opensource.org/licenses/mit-license.php).

**PyuMetric** is authored and maintained by [@silverbackhq](http://github.com/silverbackhq).
