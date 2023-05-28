import pandas as pd

# read hardware component excel sheet
hardware_components = pd.read_excel(
    'IEEE Hardware Inventory 2023-2024.xlsx',
    sheet_name='2022-2023 inventory',
)

size_list = hardware_components['name'].size
arr_item = [] # holds all item's full names
arr_item_name = [] # holds all item's names

# loop through the rows and get the item's: name, manufacturer, and model
for i in range(size_list):
    # if a field does not exist, replace with empty string
    name = "" if str(hardware_components['name'].iloc[i]) == "nan" else str(hardware_components['name'].iloc[i])
    manufacturer = "" if str(hardware_components['manufacturer'].iloc[i]) == "nan" else str(hardware_components['manufacturer'].iloc[i])
    model = "" if str(hardware_components['model_number'].iloc[i]) == "nan" else str(hardware_components['model_number'].iloc[i])
    arr_item.append(name + " " + manufacturer + " " + model) # append into arr
    arr_item_name.append(name)