---
Savefile: "pred exp 3.2.1"
is_autosave_head: true
[add metadata as needed for tracking]
---
## Sim History
Taken basic structure and layout, and some solid predators from earlier Savefiles.
Concentric zones, mostly plant of diff characters, a little meat in case predator number boost needed
Lots of dumb "live meat" of two varieties - both color randomised
Added dense central plant zone, fine pellets for grazing. the "AntiPredator" zone - will be extremely hostile to predators or competitive species
Added "Color Selection Tower" dead centre of this to enforce protection zone
    - Zone majority overlap with AntiPredator central kill zone
    - insta-kill anything not pure magenta in color
    - small kill delay -- could be overwhelmed if very high numbers of mis-colored bibites in range
Added engineered bibite to AntiPredator zone - "Magentadeath"
    - indirect cause of death for predators
    - initially armored, but largely lost that in favour of growth and reproduction
    - lost of initial experimentation and tuning to simply get viable lineage (eat -> grow -> reproduce harder than it sounds!)
Added Creep lineage. Similar color, more aggressive, more highly evolved. Might be able to fake a way in and compete
Added more color selector towers to non-AntiPred areas - looking for greener predators and co-inhabitants.
    - much longer delays
    - select for *most* off-color, acts as a guiding force rather than hard wall
AntiPred interface full of meat, dead and dying bait. Predators try to encroach, but killed if venturing too far in.
3.2.2.2
Introduced GreenCreep
    - spin-off from some branch of creep
    - but *GREEN*, so directly selected for outside of AntiPred
    - same color as predators, might convey further survival advantage if preds use color vision
    - interesting to see how they go vs. regular almost-magenta creep. force them into middle?

would love way to ban or discourage red pheromone outside of AntiPred zone, but likely will be very advantageous to emit Red.
this may require occassional reboot of sim from selected lines with highly targetted neurosurgery applied. less drastic ideas also sought.

Some lessons / considerations -
    Nudges 
    Perturbations
    Overlapping gradients
    Contrasting signals - conceptual tensions create complexity
    zones, niches
    Engineer environment to drive behaviour, much easier than other way around
    Neurosurgery is damn hard. Simple survival is not so simple, let alone advanced behaviours. If selection occurs on genes instead of behaviour, complex brains quickly scramble.

3.2.2.3
added further eye-color selector (slow, permissive) to nudge magentadeath eyes towards warmer tones (currently green, same as creep eyes)

3.2.3
Greencreep established and original Creep (magenta) line has gone extinct.
Removing OuterReach color selector towers, allow pred/prey outside of AntiPred zone to drift again
(prediction: prey color will follow predator lead)
~40 - 50 individuals of each line remain - good pop size for efficient sim progression and moderate diversity


## 3.2.4
### Thoughts
evolution phases:
1. Natural selection - let the sim run
2. Artificial selection - modify the env
3. CRISPR - modify the organism

each tag is potentially at different stage
balance basic numbers
too many predators? meat decays faster
too many herbivores in a zone? reduce its biomass potential
too little speciation? add or nudge a niche in some way

convergence on basic genetic improvements - little speciation
stabilisation. Protected herbivores currently in this stage
expect behavioural based selection + speciation once basic lifecycle is well established
predators + unprotected berbivores both undergoing rapid speciation / presumably largely competition based


### Changes
various tweaks to resources. meat decay faster again, preds running wild
bigger more fertile AntiPred zone, less fertile killzone


# Purpose Note
multiple things are going on here -
1. Push all non-protected, reproductive lines to avoid red pheromone
    - ideally being blind to color of what is emitting it
    - protected species uses red pheromone strongly to signal danger
    - towers back it up with insta-death selection for invaders
2. Prevent all non-protected lines from outputting red pheromone
    - expect that copy-cat will be a good strategy, so need to identify if this occurs and plan reset

## Resets
*minor version bump -> 3.X*
will be used to re-create sim withou Bibites, gradually re-populate with engineered population, derived from previous version. Each species is introduced in turn, we confirm it can successfully inhabit the new world and maintain stable population size.

1. Protected species with color change (+ respective tower settings), to prevent reliance on BibiteColor vision (must use red pheromone signal)
2. Non-protected predator samples get minor brain surgery to prevent red pheromone output
3. (stretch) - reduce weights for predator color vision entirely (blue/green pheromone preferred for kin identification)
4. Prey species generation re-added, supplemental meat pellet generation if needed
5. Adjust meat decay, prey pop, etc to achieve stable predators in outer reach
4. Non-protected herbivore re-introduced. Color randomised perhaps?

## Alternate Path
just another thought here - what if instead we add a *2nd* protectorate, with different genetic color selection, same red pheromone bias?

# Decision - Multiple Protectorate Zones
each populated with red-pheromone emitting bibites of a specific genetic color, for selection by towers.

# 3.3.2
Multiple Protectorate Zones - IMPLEMENTED, appears stable
Added some more meat production zones also, carnivore safe harbor, where they can hopefully learn better kin identification
CHANGED: color settings for background (solid black now) + Zones (neutral grey/brown), with zone intensity showing biomass potential