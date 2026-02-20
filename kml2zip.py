import os
import zipfile
import processing

from qgis.core import (
    QgsProject,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsField,
    edit
)

from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QInputDialog


# -----------------------------
# BASE DIRECTORY
# -----------------------------

base_dir = r"C:\Users\kevin\Desktop\OpsCenter imports\py gis script test"


# -----------------------------
# PROMPT FIELD NAME
# -----------------------------

field_name, ok = QInputDialog.getText(
    iface.mainWindow(),
    "Field Name Entry",
    "Enter FIELD_NAME:"
)

if not ok or not field_name:
    raise Exception("FIELD_NAME cancelled.")

safe_name = field_name.replace("/", "-").replace("\\", "-")


# -----------------------------
# FILE PATHS
# -----------------------------

raw_path = os.path.join(base_dir, f"{safe_name}_raw.shp")

attrib_path = os.path.join(
    base_dir,
    f"{safe_name}_attrib.shp"
)

final_path = os.path.join(
    base_dir,
    f"{safe_name}.shp"
)

zip_path = os.path.join(
    base_dir,
    f"{safe_name}.zip"
)


# -----------------------------
# GET ACTIVE LAYER
# -----------------------------

layer = iface.activeLayer()

if layer is None:
    raise Exception("Select boundary layer first.")

print("Using layer:", layer.name())


# -----------------------------
# EXPORT RAW SHAPEFILE
# -----------------------------

error = QgsVectorFileWriter.writeAsVectorFormat(
    layer,
    raw_path,
    "UTF-8",
    layer.crs(),
    "ESRI Shapefile"
)

if error[0] != QgsVectorFileWriter.NoError:
    raise Exception("Raw export failed.")

print("Raw shapefile exported.")


raw_layer = QgsVectorLayer(raw_path, "raw", "ogr")

provider = raw_layer.dataProvider()


# -----------------------------
# DELETE ALL BUT NAME
# -----------------------------

delete_indexes = []

for i, field in enumerate(raw_layer.fields()):

    if field.name() != "Name":
        delete_indexes.append(i)

provider.deleteAttributes(delete_indexes)

raw_layer.updateFields()


# -----------------------------
# ADD OPS CENTER FIELDS
# -----------------------------

provider.addAttributes([

    QgsField("CLIENT_NAM", QVariant.String),
    QgsField("FARM_NAME", QVariant.String),
    QgsField("FIELD_NAME", QVariant.String),
    QgsField("POLYGONTYP", QVariant.LongLong)

])

raw_layer.updateFields()


# -----------------------------
# POPULATE ATTRIBUTES
# -----------------------------

with edit(raw_layer):

    for feature in raw_layer.getFeatures():

        feature["CLIENT_NAM"] = "Zwieg"
        feature["FARM_NAME"] = "Main"
        feature["FIELD_NAME"] = field_name

        raw_layer.updateFeature(feature)

print("Attributes populated.")


# -----------------------------
# SAVE ATTRIBUTED INTERMEDIATE
# -----------------------------

error = QgsVectorFileWriter.writeAsVectorFormat(
    raw_layer,
    attrib_path,
    "UTF-8",
    raw_layer.crs(),
    "ESRI Shapefile"
)

if error[0] != QgsVectorFileWriter.NoError:
    raise Exception("Attrib export failed.")


attrib_layer = QgsVectorLayer(
    attrib_path,
    "attrib",
    "ogr"
)


# -----------------------------
# SIMPLIFY (FINAL OUTPUT)
# -----------------------------

print("Simplifying geometry...")

processing.run(
    "native:simplifygeometries",
    {
        'INPUT': attrib_layer,
        'METHOD': 0,
        'TOLERANCE': 0.00001,
        'OUTPUT': final_path
    }
)

print("Simplified FINAL shapefile created.")


final_layer = QgsVectorLayer(
    final_path,
    safe_name,
    "ogr"
)

QgsProject.instance().addMapLayer(final_layer)


# -----------------------------
# CREATE ZIP PACKAGE
# -----------------------------

print("Creating ZIP package...")

required_exts = [".shp", ".shx", ".dbf", ".prj"]

# remove existing zip if exists
if os.path.exists(zip_path):
    os.remove(zip_path)

with zipfile.ZipFile(zip_path, 'w',
                     compression=zipfile.ZIP_DEFLATED) as z:

    for ext in required_exts:

        file_path = final_path.replace(".shp", ext)

        if os.path.exists(file_path):

            z.write(
                file_path,
                os.path.basename(file_path)
            )

print("ZIP package created:", zip_path)

print("SUCCESS — Ops Center upload ZIP ready.")