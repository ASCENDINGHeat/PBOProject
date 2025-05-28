import os
import qt_material

# Get the directory where the qt_material package is installed
qt_material_path = os.path.dirname(qt_material.__file__)

# Construct the path to the themes directory
themes_path = os.path.join(qt_material_path, 'themes')

print(f"Qt-Material themes are located at: {themes_path}")

# You can also list the themes
from qt_material import list_themes
print("\nAvailable themes:")
for theme_file in list_themes():
    print(theme_file)