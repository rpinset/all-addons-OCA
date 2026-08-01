This module installs `base_setup` and `base_geolocalize`.

After installation, configure the Google Maps API key under
**Settings > General Settings > Google Maps View**.

With demo data enabled, the module sets a placeholder value
`YOUR_GOOGLE_MAPS_API_KEY` on the `google.api_key_geocode` system
parameter. Replace it with a real key from your Google Cloud project
before using maps in a demo database.

Google APIs and services required for all features:

- Geocoding API
- Maps JavaScript API
- Places API

See the [Google documentation](https://developers.google.com/maps/documentation/javascript/get-api-key)
on how to get an API key.
