from ionex_formatter.spatial import (
    SpatialRange,
    DecimalDigitReduceAccuracyError,
)


spatial = SpatialRange(0, 100, 5.0)
print(spatial.get_chunks(-5))

