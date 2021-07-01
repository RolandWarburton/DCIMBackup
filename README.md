# Mobile Processing Scripts

Read about how i create and use these scripts to manage my mobile phones photos [here!](https://blog.rolandw.dev/writing/automating_photo_backup/).

## GetGPSData

This script requires **exiftool** to be installed.

This script extracts GPS data and dumps it into a JSON file for a directory of JPGs. Typically you run this script first.

Scripts in the `./scatterplots` directory require the `location_data.json` that this script generates.

## Scatterplots Directory

This contains some scripts to display the data from `GetGPSData.py` in scatter plots.

## PhotoMap Directory

This contains a node project for displaying from `GetGPSData.py` as an interactive map using openstreetmap mapping data, mapbox browser intergration tools, and leafletjs to provide map markers.

To use this you need to optain an API key from mapbox to use their tools. There is a free tier for this that works great.

First install node dependencies.

```none
npm install
```

Then run `npm run start` and navigate to [localhost:3000](localhost:3000) in your browser.
