# 3D Printing in this fork

This mod ports the 3D printers and carbon fiber crafting of
[Cataclysm: Bright Nights](https://github.com/cataclysmbn/Cataclysm-BN), as they stood at Bright
Nights commit `4846cb7` (25 November 2026). Bright Nights keeps this content in its core game,
under the Creative Commons Attribution-ShareAlike 3.0 Unported licence, the same licence as
Cataclysm: Dark Days Ahead. Names, descriptions, recipes and loot placements follow Bright Nights
except where listed below; the JSON is written for this game's 0.I format, not copied.

## What it adds

* The 3D printer and advanced 3D printer, carried and run from a medium battery or a power cord,
  placed as appliances, mounted on vehicles as rigs, or kept in a workshop rig.  Both repair plastic
  and carbon fiber items; the advanced printer also repairs metal items.
* Carbon fiber filament, made from plastic by the advanced printer.
* Printed plastic containers, tools, a hard hat, a tonfa, boat hulls and magazines.
* Carbon fiber armor, swords and other blades, a jerrycan, a rifle, a machine pistol, a repeating
  crossbow and gunmods, and the core carbon fiber arrows, bolts, fishing spears and boat hull.
* Carbon fiber vehicle frames, walls, cargo space, plating and a bicycle.
* A 3D printing shop (`craft_shop_4`) and printers and filament in loot.

## Changes from Bright Nights

* **Metal printing**, which Bright Nights describes but never implemented.  The advanced printer
  sinters metal arrows, bolt points, nails, bearings, hinges, pipe fittings, lockpicks and steel
  magazines from scrap, and the steel edges of the carbon fiber blades.  Anything with a sharp edge
  or point also needs filing or grinding (`3d_printed_edge`), since a printer can't print one.
* **Power:** Bright Nights' grid-only furniture and fake tools become 0.I appliances, vehicle rigs,
  workshop slots and charging cords.  The printing shop's printers are furniture that turns into an
  appliance when examined.
* **Material:** the core `carbonfiber` material gains filament repairs and salvage, and bullet
  resistance equal to rigid Kevlar's (5 per millimetre).  Bright Nights' armor values would have made
  it the best ballistic material in the game.  The core carbon fiber items, which used rigid Kevlar
  as a stand-in, are made of it here.
* **Balance on 0.I's scale:** vehicle part durability and damage reduction are scaled to 0.I's steel
  parts (Bright Nights' frame values are 2.6 times 0.I's); the grip and stock take 5% and 8% off a
  gun's weight instead of 30% and 15%; armor keeps its leather straps and padding, with recipes that
  ask for them.
* **Mass:** every printed recipe uses at least as much material as the item weighs, checked by
  `printed_items_conserve_mass` in `tests/printing_3d_test.cpp`.
* **Equivalents:** the katar and jamadhar become the punch dagger and knuckle katar.
* **Generic Guns:** the carbon guns take generic ammunition and magazines, the printed magazine
  recipes print Generic Guns' magazines, and the carbon fiber lower receiver is blacklisted, as
  Generic Guns does with the core AR-15 receiver mods.

## Not ported

* Carbon fiber padding for clothing (`sew_advanced`), which 0.I's core game no longer uses.
* The carbon fiber STANAG magazine: 0.I lists each gun's magazines, so it would need every STANAG
  gun overridden.
* Printed rigid plastic sheets (a 15 kg, 12.5 L sheet from a 1.5 L printer), plastic string and
  rope, the plastic frame and bicycle, riot shields, carbon fiber shields and buckler, wings, the
  stab plate, enhanced and super motors, the 3D printing archive, CBM uncrafts, the AUG and G36
  conversions and the Saiga .410 magazine, which 0.I lacks or has made obsolete.
* The carbon fiber box, flat trunk, small box and manual turret mount; 0.I generates turret mounts
  for guns itself.
* Printers in core lab maps: the mod doesn't override core maps, so labs get printers and filament
  through their loot instead.
