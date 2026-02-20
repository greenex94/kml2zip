AgOpenGPS creates folders for each field. "find kmls.py" finds, copies, and renames kml files to their parent field folder name, and moves to a new collection folder. This is helpful in finding field.kml files in an AgOpenGPS document directory.

kml2zip.py Converts AgOpenGPS field.kml files into a field boundary that John Deere Ops Center will import and recognize.

"Client" (CLIENT_NAM), and "Farm" (FARM_NAME) are hard coded, as well as the script directory. Change as needed.

Must be used with QGIS.
1. Add vector layer. Open Field.kml and only import the boundary layer.
2. Preselect the imported boundary layer
3. Execute script kml2zip.py
4. Enter Field Name when prompted.
5. Upload zip file to OpsCenter
