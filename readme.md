

questions:
- should this be quite generic, ie specifying types for the data shapes that we need, but not actually trying to enumerate all the potential metrics?
  - eg "time series", "container", "scalar", etc.
  - and then the metric names just become suggestions/conventions? could have a list of common ones.
  - advantage is that this doesn't limit things to the canonical set of metrics, and you avoid hard questions of what should be included or not.
  - disadvantage is the typing is quite weak, and the client/server we provide here is rather weak.
  - how would apps actually interoperate on novel types?
    - i guess typically a producer would add something first - it's the source of the data
    - and then people would request in the consumer app that they add support for this new data field.
    - dashboarding software could also just display all discovered metrics, regardless of if they're known or not.
- alternatively you fully specify everything
  - means we could fully specify a client+server.
  - more immediately understandable.
  - most readily interoperable.
  - this is the model of apple/android health
    - isn't ideal tho, people end up trying stuff things in metadata fields or whatnot
- some hybrid? standard taxonomy, but apps can also push custom metric names?
  - typing is weirdish here.
  - is there any way to do this cleanly tho? this seems most natural. it's basically #1 but with the "canonical set" baked in somehow.
  - i mean in the client library, we could just have like "get_heart_rate(start, end)` and that calls `get_global_time_series(metric_name="heart rate", start, end)`.
  - or we could have a HeartRateTimeSeries(TimeSeries) where metric_name is pre-filled.



tbh i'm leaning towards just doing #1. it seems simple enough, along with a registry of the actual common structure.
