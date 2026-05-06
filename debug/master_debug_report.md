# Rhino / Grasshopper STL Generation — Master Debug Report

This report consolidates the most useful debugging information from the notebook.

## 1. Environment

- Python executable: `c:\Users\hecto\Desktop\bachelor-thesis\IDEAL-Propeller-Dataset\.venv311\Scripts\python.exe`
- Python version: `3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]`
- Rhino.Compute URL: `http://localhost:6500/`
- Grasshopper file: `C:\Users\hecto\Desktop\bachelor-thesis\IDEAL-Propeller-Dataset\grasshopper\Propeller_Raul_V1.2.gh`
- Grasshopper file exists: `True`
- Selected Grasshopper output name: `propeller_mesh`
- rhino3dm available: `True`
- compute-rhino3d available: `True`

## 2. Main constants

                    constant  value
                 SAMPLE_SIZE     10
                 SAMPLE_MODE random
                 RANDOM_SEED     42
      OVERWRITE_EXISTING_STL   True
  OVERWRITE_EXISTING_PREVIEW   True
         SAVE_PREVIEW_IMAGES   True
DISPLAY_PREVIEWS_IN_NOTEBOOK   True

## 3. Grasshopper input map

                     Grasshopper input      CSV column
                Radius of the Impeller          radius
                 Hight of the Impeller     ring height
           Thickness of the outer Ring  ring thickness
                      Amount of Blades     blade count
                 Thickness_i (% chord) inner thickness
            High-point_i (10ths chord)   inner max pos
                    Camber_i (% chord)    inner camber
                          Chord_i (mm)     inner chord
                      Angle_i (degree)     inner angle
Distance to middle NACA (times radius)  mid radial pos
                          Chord_m (mm)       mid_chord
                      Angle_m (degree)       mid angle
                 Thickness_o (% chord) outer thickness
            High-point_o (10ths chord)   outer max pos
                    Camber_o (% chord)    outer camber
                          Chord_o (mm)     outer chord
                      Angle_o (degree)     outer angle

## 4. Sampled configurations

 config_id  radius  blade count  mid radial pos
       106      62            4           0.449
       589      61            4           0.590
       705      68            5           0.542
      1055      60            4           0.306
      1501      76            5           0.381
      1600      77            4           0.690
      2413      76            4           0.691
      2468      74            4           0.363
      2586      67            5           0.390
      2653      60            5           0.458

## 5. Generation summary

 config_id  geometry_ok          stl_path                   preview_path  volume_mm3  volume_cm3  volume_m3  n_vertices  n_triangles selected_output_name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              error_message
       106        False  stl\prop_106.stl  previews\prop_106_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
       589        False  stl\prop_589.stl  previews\prop_589_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
       705        False  stl\prop_705.stl  previews\prop_705_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
      1055        False stl\prop_1055.stl previews\prop_1055_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
      1501        False stl\prop_1501.stl previews\prop_1501_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
      1600        False stl\prop_1600.stl previews\prop_1600_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
      2413        False stl\prop_2413.stl previews\prop_2413_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
      2468        False stl\prop_2468.stl previews\prop_2468_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
      2586        False stl\prop_2586.stl previews\prop_2586_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.
      2653        False stl\prop_2653.stl previews\prop_2653_preview.png         NaN         NaN        NaN         NaN          NaN       propeller_mesh No decodable mesh objects were found. Selected output: 'propeller_mesh'. Non-empty outputs: ['MeshLauncher']. Grasshopper errors: ['Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)', 'Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)', 'Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)', 'Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)', 'Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)']. Fix the .gh file so it exposes a real Mesh output, preferably named propeller_mesh.

## 6. Overall interpretation

No sampled configuration generated successfully. This usually means Grasshopper is not returning a decodable Rhino Mesh. Check whether the selected Grasshopper output is a real Mesh rather than a string, Brep, Panel output, or empty parameter.

## 7. Per-configuration Grasshopper errors

### config_id 106

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 589

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 705

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 1055

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 1501

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 1600

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 2413

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 2468

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 2586

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

### config_id 2653

- `Error running script: Object reference not set to an instance of an object. [89:1]: component "C# Script" (d7512d01-af72-4ce0-94be-46d6919e371b)`
- `Error running script: Object reference not set to an instance of an object. [103:1]: component "C# Script" (7bca56dc-58df-4d59-a218-f9ccf33a6699)`
- `Error running script: Object reference not set to an instance of an object. [105:1]: component "C# Script" (c2f07c9d-8130-4b21-88c5-6da98e0f75a7)`
- `Error running script: Object reference not set to an instance of an object. [47:1]: component "C# Script" (ae8dec44-ca52-400e-95bf-a781745cfd5a)`
- `Error running script: the JSON object must be str, bytes or bytearray, not NoneType [3:1]: component "Python 3 Script" (d2a9bec7-664a-4f55-a5cc-ef48f74e76d6)`

## 8. Per-configuration output summaries

### config_id 106

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 589

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 705

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 1055

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 1501

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 1600

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 2413

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 2468

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 2586

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

### config_id 2653

          ParamName  n_branches branch_names  n_items    item_types  max_data_length                                                                                                             data_preview
       MeshLauncher           1          {0}        1 System.String            21022 "RFJBQ08CAgEBAAAAoRfiHAHNHMwBF7IBEqABGiURaRKfARknE+gBDXMaJhKfARkmEWkTvgIRtwESuAISoAEaJRFpEp8BGScT7gERzAF3eHf//3+tCW/bftu
           MeshRing           1          {0}        0           NaN                0                                                                                                                      NaN
        MeshProfile           1          {0}        0           NaN                0                                                                                                                      NaN
          MeshFinal           1          {0}        0           NaN                0                                                                                                                      NaN
       InnerProfile           1          {0}        0           NaN                0                                                                                                                      NaN
      MiddleProfile           1          {0}        0           NaN                0                                                                                                                      NaN
       OuterProfile           1          {0}        0           NaN                0                                                                                                                      NaN
MeshSimpleInterface           1          {0}        0           NaN                0                                                                                                                      NaN
MeshUntrimmedBlades           1          {0}        0           NaN                0                                                                                                                      NaN

## 9. Per-configuration decode diagnostics

### config_id 106

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 589

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 705

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 1055

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 1501

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 1600

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 2413

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 2468

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 2586

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

### config_id 2653

   output_name  branch  item_index  item_type         route  success  is_mesh                                                                                                                                                                                        error
propeller_mesh     NaN         NaN        NaN output_lookup    False    False Output not found. Available outputs: ['MeshLauncher', 'MeshRing', 'MeshProfile', 'MeshFinal', 'InnerProfile', 'MiddleProfile', 'OuterProfile', 'MeshSimpleInterface', 'MeshUntrimmedBlades']

## 10. Most useful files to send

Send this file first:

- `debug\master_debug_report.md`

If needed, also send:

- the failing `.gh` file
- one `grasshopper_raw_config_*.json` file
- one `grasshopper_output_summary_config_*.csv` file
- one `grasshopper_decode_diagnostics_config_*.csv` file
