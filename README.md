# The Toilet That Wanted Revenge

A colorful 3D cartoon project targeting **Blender 2.79b**.

## Build with GitHub Actions

1. Open the **Actions** tab.
2. Select **Build Blender movie project**.
3. Click **Run workflow** (or let it run after a push to `main`).
4. When the run completes, download the artifact named
   `The-Toilet-That-Wanted-Revenge-Blender279`.

The artifact contains an editable `.blend` project.

## Local build

Run Blender 2.79b in background mode:

```sh
BLEND_OUTPUT=dist/The_Toilet_That_Wanted_Revenge.blend \
  blender --background --factory-startup --python build_movie.py
```

## Current production status

The builder creates the colorful character models, four environments, camera, lighting,
seven-act 50-minute timeline, keyframed character movement, title cards, and visual
dialogue captions. This is currently an **animated animatic foundation**, not a finished
50-minute rendered film. Recorded voice acting, music, detailed sound design, and the
final feature render remain production work.

The target is Blender 2.79b to match the older macOS computer.


Latest compatibility fix: the scene builder now uses Blender 2.79's `World.horizon_color` property.
