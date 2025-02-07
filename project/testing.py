import os

# Get script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Paths
modules_path = os.path.join(script_dir, "..", "modules")  # Parent dir contains "modules"
model_path = os.path.join(script_dir, "stacking_model")  # Inside current dir

print("Modules Path:", modules_path)
print("Model Path:", model_path)
