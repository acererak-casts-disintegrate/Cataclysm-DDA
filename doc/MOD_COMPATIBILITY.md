# Mod compatibility

Backported from upstream (CleverRaven/Cataclysm-DDA#76632).

## Summary

A mod can ship content that only loads when another mod is active. Files under a mod's `mod_interactions` folder are skipped unless they sit in a sub-folder named after the id of a mod in the current world.

## Layout

The sub-folder name must match the other mod's id exactly, including case. It is the `id` in that mod's `modinfo.json`, which is not always the folder name.

Example: Xedra Evolved (`xedra_evolved`) content that should only load alongside Defense Mode (`defense_mode`):

```
data/mods/Xedra_Evolved/mod_interactions/defense_mode/overmap_specials.json
```

Interaction files load after every active mod's own data, in mod load order.

## Limitations

Interaction files are loaded with the owning mod as their source. Redefining one of the owning mod's own ids inside its own `mod_interactions` folder therefore raises a duplicate-definition error. To change a mod's own content when another mod is present, put the override in the *other* mod's `mod_interactions` folder, under the first mod's id.
