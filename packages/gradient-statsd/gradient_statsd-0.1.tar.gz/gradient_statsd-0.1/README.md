# Gradient-Statsd

Gradient-Statsd is a statsd agent allowing user defined metrics to be graphed within gradient jobs.
When creating a job on the gradient platform a user can specify a set of metrics strings. The user
can then use this package to write the same metrics strings in their jobs. The gradient platform 
will graph these metrics for you. 

# Usage
This client will automatically find the statsd server if it's being used via the gradient platform. We do provide a hostname and port override if you'd like to send metrics to your own statsd server. We require the environment variable `PS_JOB_ID` in order to tag the metrics correctly.

```
from gradient_statsd import Client
c = Client()
c.increment("myCustomMetric", 1)
```
