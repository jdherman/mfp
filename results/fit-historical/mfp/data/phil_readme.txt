File naming conventions for rhessys output
out<scenario>.<watershed>_<output_scale>.<time_interval>

Scenarios:
NA - No Action
NAfire - No Action + Fire
TA - Treatment Alternative
TAfire - Treatment Alternative + Fire

Watershed:
frm (French Meadows)

Output_scale:
Basin (entire watershed)

Time_interval (1980-2015):
daily
monthly
yearly (calendar)


frm_inflows_cms.csv
Daily inflows to French Meadows Reservoir from the Middle Fork American River in cubic meters/second. Columns are named by scenarios defined above.


New info October 2017 - new model runs

Sure - the fire scenarios don't completely map because I used the entire basin (97.5 km2) burned, but I used the extreme weather + east wind fire simulations (most significant effects) previously so the closest would be:

new = old
control = NA
treatment = TA
eelt_75 ~ TAfire
eeln_75 ~ NAfire

I added the no-treatment column headers to the list below too.

Column headers are....
date (10/1/1980-9/30/2015)
control (no treatment vegetation condition)
treatment (post-treatment vegetation condition)
welt_8 (west wind, extreme weather, landscape treatment, 8 km2 burn area)
welt_50 (west wind, extreme weather, landscape treatment, 50 km2 burn area)
welt_75 (west wind, extreme weather, landscape treatment, 75 km2 burn area)
wmlt_8 (west wind, moderate weather, landscape treatment, 8 km2 burn area)
wmlt_50 (west wind, moderate weather, landscape treatment, 50 km2 burn area)
wmlt_75 (west wind, moderate weather, landscape treatment, 75 km2 burn area)
eelt_8 (east wind, extreme weather, landscape treatment, 8 km2 burn area)
eelt_50 (east wind, extreme weather, landscape treatment, 50 km2 burn area)
eelt_75 (east wind, extreme weather, landscape treatment, 75 km2 burn area)
emlt_8 (east wind, moderate weather, landscape treatment, 8 km2 burn area)
emlt_50 (east wind, moderate weather, landscape treatment, 50 km2 burn area)
emlt_75 (east wind, moderate weather, landscape treatment, 75 km2 burn area)
weln_8 (west wind, extreme weather, landscape no-treatment, 8 km2 burn area)
weln_50 (west wind, extreme weather, landscape no-treatment, 50 km2 burn area)
weln_75 (west wind, extreme weather, landscape no-treatment, 75 km2 burn area)
wmln_8 (west wind, moderate weather, landscape no-treatment, 8 km2 burn area)
wmln_50 (west wind, moderate weather, landscape no-treatment, 50 km2 burn area)
wmln_75 (west wind, moderate weather, landscape no-treatment, 75 km2 burn area)
eeln_8 (east wind, extreme weather, landscape no-treatment, 8 km2 burn area)
eeln_50 (east wind, extreme weather, landscape no-treatment, 50 km2 burn area)
eeln_75 (east wind, extreme weather, landscape no-treatment, 75 km2 burn area)
emln_8 (east wind, moderate weather, landscape no-treatment, 8 km2 burn area)
emln_50 (east wind, moderate weather, landscape no-treatment, 50 km2 burn area)
emln_75 (east wind, moderate weather, landscape no-treatment, 75 km2 burn area)