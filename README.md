# Blender Sushi Scene

A procedural sushi scene created with Blender's Python API. The script builds sushi pieces and a serving setup, while demonstrating core modeling techniques such as subdivision, extrusion, insetting, materials, modifiers, and linked duplication.

## Requirements

- Blender 3.x or 4.x
- No external Python packages

## Create the scene

1. Open Blender and switch to the **Scripting** workspace.
2. Open `blender.py` in the Text Editor.
3. Click **Run Script**.
4. Inspect the generated scene, then save it with **File > Save As** to create a `.blend` file.

> **Warning:** Running the script deletes all objects in the current scene before creating the sushi scene. Run it in a new Blender file or save a copy of your current work first. The script does not save the `.blend` file automatically.

## What's in the scene

The script creates:

- A wooden serving board, plate, soy dish, and soy sauce
- Sushi with rice, nori, and salmon materials
- A camera and sunlight
- A 4-by-2 array of sushi pieces and a linked duplicate

## Techniques demonstrated

| Technique | How it is used |
| --- | --- |
| Subdivide | Adds a grid of geometry to the base sushi mesh. |
| Extrude | Raises the top faces to form the salmon topping. |
| Extrude along normals | Forms the nori band around the sushi. |
| Materials | Colors the rice, nori, salmon, board, plate, and soy sauce. |
| Stacked modifiers | Uses a Bevel modifier followed by two Array modifiers on the main sushi object. |
| Inset | Creates a border on the sushi top before the salmon is extruded. |
| Linked duplication | Creates a second object that shares the sushi mesh data. |

## Assignment submission

Save your completed work as a Blender `.blend` file, or submit a `.jpg` screenshot that clearly shows the scene and the modifier stack. Name your submission using this format:

```text
Name_Surname_Title_version
```

For example: `John_Doe_SushiHomework_v1`
