## Blender Texture Bake & FBX Export Script

This script automates texture baking (Base Color only via EMIT) and FBX export for selected mesh objects in Blender 4.4+.  
It generates low-resolution (e.g. 512x512) baked PNG textures, replaces materials with simplified versions, and exports optimized FBX files with embedded textures.

✔️ Ideal for game asset optimization (e.g. Unity / mobile use)  
✔️ Automatically unwraps UVs if missing  
✔️ Keeps your original textures untouched  
✔️ Very low memory usage for baked textures

### ✅ How to Use
1. Open your `.blend` file and save it (must be saved first)
2. Select all mesh objects you want to export
3. Run the script in the Scripting tab or as a Blender Text block
4. Done! An `Export/` folder will be created **next to your `.blend` file**, containing:
   - One baked `.png` texture per object
   - One `.fbx` file per object with the baked texture embedded

No configuration needed. Fast, clean, and optimized export for real-time engines.
