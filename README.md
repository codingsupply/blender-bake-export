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
### ⚙️ Requirements

- **Blender 4.4+** (developed and tested in Blender 4.4)
- **Cycles** render engine (the script switches to it automatically)
- Each selected mesh needs a **node-based material** whose *Base Color* is driven by an **Image Texture** node
- Only the **Base Color** channel is baked (Emit bake, no lighting/shadows)

### 🧰 Troubleshooting

| Message | Cause | Fix |
| --- | --- | --- |
| `Please save the .blend file first!` | The file was never saved | Save the `.blend` file, then run the script |
| `... has no node-based material!` | Object uses an old-style material | Assign a material with *Use Nodes* enabled |
| `No Principled BSDF found ...` | Material has no Principled BSDF node | Add one, or use a compatible material |
| `Base Color ... is not linked!` / `is not from an image texture node!` | Base Color comes from a flat color or procedural node | Plug an Image Texture into Base Color |

### 📄 License

MIT – see [LICENSE](LICENSE).
