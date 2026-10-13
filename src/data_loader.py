"""
Data Loader & Dataset Compiler for Legends of Runeterra - Path of Champions (PoC).
Parses the user CSV files, enriches with official mechanics, and provides a unified
database registry of Champions, Relics, Bosses, and Combos.
"""

import os
import csv
import json
from typing import Dict, List, Tuple, Set, Optional
from src.models import Relic, Champion, Boss, RelicCombo, Rarity, Archetype


class DatabaseRegistry:
    def __init__(
        self,
        champions: Dict[str, Champion],
        relics: Dict[str, Relic],
        bosses: Dict[str, Boss],
        combos: List[RelicCombo],
        synergy_matrix: Dict[str, Dict[str, float]],
    ):
        self.champions = champions
        self.relics = relics
        self.bosses = bosses
        self.combos = combos
        self.synergy_matrix = synergy_matrix

    def get_champion(self, name: str) -> Optional[Champion]:
        return self.champions.get(name)

    def get_relic(self, name: str) -> Optional[Relic]:
        return self.relics.get(name)

    def get_boss(self, name: str) -> Optional[Boss]:
        return self.bosses.get(name)

    def get_synergy(self, champion_name: str, relic_name: str) -> float:
        champ_dict = self.synergy_matrix.get(champion_name, {})
        return champ_dict.get(relic_name, 0.0)

    def to_dict(self) -> dict:
        return {
            "champions": {k: v.to_dict() for k, v in self.champions.items()},
            "relics": {k: v.to_dict() for k, v in self.relics.items()},
            "bosses": {k: v.to_dict() for k, v in self.bosses.items()},
            "combos": [
                {"relics": list(c.relics), "bonus": c.bonus, "description": c.description}
                for c in self.combos
            ],
            "synergies": self.synergy_matrix,
        }

    def save_json(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


# Default enriched database definition covering core mechanics, stackability, and tags
DEFAULT_RELICS_CATALOG: List[Relic] = [
    # Rare Relics
    Relic(
        name="The Loose Cannon's Payload",
        rarity=Rarity.RARE,
        base_score=2.0,
        stackable=False,
        description="When I'm summoned, discard your hand then replace it with Pow-Pows.",
        tags=("discard", "burn", "summon", "removal"),
    ),
    Relic(
        name="Luden's Tempest",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=True,
        description="All your spells and Skills deal 1 extra damage.",
        tags=("spell", "skill", "burn", "damage_boost"),
    ),
    Relic(
        name="The Scourge Stash",
        rarity=Rarity.RARE,
        base_score=5.0,
        stackable=False,
        description="Plunder: I cost 2 less.",
        tags=("plunder", "cost_reduction", "tempo"),
    ),
    Relic(
        name="Gatebreaker",
        rarity=Rarity.RARE,
        base_score=6.0,
        stackable=True,
        description="When I'm summoned, I strike the enemy Nexus.",
        tags=("strike", "nexus_damage", "summon", "burn"),
    ),
    Relic(
        name="Stalker's Blade",
        rarity=Rarity.RARE,
        base_score=6.5,
        stackable=True,
        description="When I'm summoned, I strike the strongest enemy.",
        tags=("strike", "removal", "summon", "control"),
    ),
    Relic(
        name="Tempest Blade",
        rarity=Rarity.RARE,
        base_score=5.0,
        stackable=False,
        description="When I level up, stun all enemies.",
        tags=("stun", "control", "board_clear", "level_up"),
    ),
    Relic(
        name="Yasuo's Windblade",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="Grant +1|+1 for each stunned enemy.",
        tags=("stun", "stat_buff", "scaling"),
    ),
    Relic(
        name="Crownguard Inheritance",
        rarity=Rarity.RARE,
        base_score=6.0,
        stackable=False,
        description="When I level up, Rally.",
        tags=("rally", "level_up", "aggro", "tempo"),
    ),
    Relic(
        name="Guardian's Orb",
        rarity=Rarity.RARE,
        base_score=6.0,
        stackable=True,
        description="When I'm summoned, grant 3 random Epic items to cards in deck.",
        tags=("summon", "value", "rng_buff", "scaling"),
    ),
    Relic(
        name="Galeforce",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="Scout. Round End: Recall me.",
        tags=("scout", "summon_repeat", "aggro", "recall"),
    ),
    Relic(
        name="Chemtech Duplicator",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="When you play a spell, if you have 6+ mana gems, cast a copy.",
        tags=("spell", "copy", "value", "late_game"),
    ),
    Relic(
        name="The Grand General's Counterplan",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="Round Start: Create a Fleeting copy of my champion spell.",
        tags=("spell", "card_generation", "value", "sustain"),
    ),
    Relic(
        name="Troll King's Crown",
        rarity=Rarity.RARE,
        base_score=6.5,
        stackable=False,
        description="Allies have Overwhelm.",
        tags=("overwhelm", "finisher", "board_buff", "aggro"),
    ),
    Relic(
        name="Archangel's Staff",
        rarity=Rarity.RARE,
        base_score=5.0,
        stackable=False,
        description="Round Start: Refill your spell mana.",
        tags=("spell_mana", "sustain", "spell"),
    ),
    Relic(
        name="Disciple of Shadows",
        rarity=Rarity.RARE,
        base_score=6.0,
        stackable=False,
        description="I cost 1 less for each ally. When summoned, deal 3 to all allies.",
        tags=("slay", "cost_reduction", "tempo", "sacrifice"),
    ),
    Relic(
        name="Corrupted Star Fragment",
        rarity=Rarity.RARE,
        base_score=6.5,
        stackable=False,
        description="Support: Kill supported ally and grant me its stats and positive keywords.",
        tags=("support", "stat_buff", "slay", "keyword_stack"),
    ),
    Relic(
        name="Succubus's Brand",
        rarity=Rarity.RARE,
        base_score=5.0,
        stackable=False,
        description="When I kill an enemy, summon a random Husk.",
        tags=("slay", "husk", "keyword_stack"),
    ),
    Relic(
        name="Bounty Hunter's Renown",
        rarity=Rarity.RARE,
        base_score=5.0,
        stackable=False,
        description="I have +1|+1 for each 200 gold you have.",
        tags=("stat_buff", "scaling", "gold"),
    ),
    Relic(
        name="Laurent Bladerack",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="Allies have Challenger.",
        tags=("challenger", "board_control", "combat"),
    ),
    Relic(
        name="Dreadway Chase Gun",
        rarity=Rarity.RARE,
        base_score=4.5,
        stackable=True,
        description="When I'm summoned, create 2 Warning Shots in hand.",
        tags=("burn", "spell", "plunder", "summon"),
    ),
    Relic(
        name="Swain's Ravenous Flock",
        rarity=Rarity.RARE,
        base_score=6.0,
        stackable=False,
        description="Deal 4 damage to damaged or stunned enemies on summon.",
        tags=("burn", "removal", "stun"),
    ),
    Relic(
        name="Lux's Incandescent Baton",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="Create a 0-cost Prismatic Barrier on round start.",
        tags=("barrier", "spell", "protection"),
    ),
    Relic(
        name="Spirit of the Buhru",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="1-cost allies have Overwhelm, Quick Attack, and Fury.",
        tags=("1_cost", "board_buff", "aggro", "overwhelm"),
    ),
    Relic(
        name="The Grandmaster's Ogre",
        rarity=Rarity.RARE,
        base_score=5.5,
        stackable=False,
        description="When I'm summoned, grant allies +1|+1 and Overwhelm.",
        tags=("board_buff", "stat_buff", "overwhelm"),
    ),

    # Epic Relics
    Relic(
        name="Chosen by the Stars",
        rarity=Rarity.EPIC,
        base_score=8.5,
        stackable=False,
        description="Fated, Empowered 10: Overwhelm, Regenerate, and Challenger.",
        tags=("fated", "stat_buff", "overwhelm", "regenerate", "challenger"),
    ),
    Relic(
        name="Echoing Spirit",
        rarity=Rarity.EPIC,
        base_score=8.0,
        stackable=False,
        description="Create 7 copies of me in your deck. Reduce my champion spell cost by 1.",
        tags=("draw", "copies", "spell", "cost_reduction"),
    ),
    Relic(
        name="The Beast Within",
        rarity=Rarity.EPIC,
        base_score=8.0,
        stackable=False,
        description="Allies with Subtypes have +1|+1 and Overwhelm.",
        tags=("subtype", "overwhelm", "stat_buff", "board_buff"),
    ),
    Relic(
        name="The Star Forge",
        rarity=Rarity.EPIC,
        base_score=9.0,
        stackable=False,
        description="Game Start: If I am Titanic, get +1 starting mana gem.",
        tags=("mana_gem", "titanic", "tempo", "ramp"),
    ),
    Relic(
        name="Epic: Spectral Scissors",
        rarity=Rarity.EPIC,
        base_score=8.0,
        stackable=False,
        description="Support: Summon an attacking Ephemeral exact copy of the supported ally.",
        tags=("support", "ephemeral", "copy", "aggro"),
    ),

    # Common Relics
    Relic(
        name="Everfrost",
        rarity=Rarity.COMMON,
        base_score=4.0,
        stackable=False,
        description="When I'm summoned, stun the strongest enemy.",
        tags=("stun", "control", "summon"),
    ),
    Relic(
        name="Lost Chapter",
        rarity=Rarity.COMMON,
        base_score=4.5,
        stackable=False,
        description="When I'm summoned, refill your spell mana.",
        tags=("spell_mana", "tempo", "summon"),
    ),
    Relic(
        name="Z-Drive Prototype",
        rarity=Rarity.COMMON,
        base_score=3.0,
        stackable=True,
        description="Start adventure with +2 rerolls.",
        tags=("reroll", "utility", "consistency"),
    ),
    Relic(
        name="Banshee's Veil",
        rarity=Rarity.COMMON,
        base_score=4.0,
        stackable=False,
        description="SpellShield.",
        tags=("spellshield", "protection", "anti_removal"),
    ),
    Relic(
        name="Warmog's Armor",
        rarity=Rarity.COMMON,
        base_score=3.5,
        stackable=False,
        description="Regeneration.",
        tags=("regenerate", "sustain"),
    ),
]

DEFAULT_BOSSES_CATALOG: List[Boss] = [
    Boss(
        name="Teemo",
        stars=1.0,
        map_type="World Adventure",
        threat_description="1-Star Map. Spams Puffcaps in your deck.",
        counter_tags={"burn", "aggro", "tempo"},
        vulnerable_tags={"burn", "aggro"},
        penalized_tags={"draw"},
    ),
    Boss(
        name="Lulu",
        stars=1.5,
        map_type="World Adventure",
        threat_description="1.5-Star Map. Transforms your blockers into 1/1 Pixels.",
        counter_tags={"spellshield", "burn", "summon", "removal"},
        vulnerable_tags={"strike", "burn"},
        penalized_tags={"stat_buff"},
    ),
    Boss(
        name="Gangplank",
        stars=2.0,
        map_type="World Adventure",
        threat_description="2-Star Map. Keg spams and high burn damage to Nexus.",
        counter_tags={"removal", "aggro", "burn", "spellshield"},
        vulnerable_tags={"removal", "tempo"},
        penalized_tags={"self_damage"},
    ),
    Boss(
        name="Thresh",
        stars=3.0,
        map_type="World Adventure",
        threat_description="3-Star Map. Captures your units and scales vaults.",
        counter_tags={"spellshield", "summon", "burn"},
        vulnerable_tags={"summon", "burn"},
        penalized_tags={"stat_buff"},
    ),
    Boss(
        name="Kai'Sa",
        stars=3.5,
        map_type="World Adventure",
        threat_description="3.5-Star Map. Spams evolved keywords on units.",
        counter_tags={"stun", "removal", "overwhelm"},
        vulnerable_tags={"stun", "board_clear"},
        penalized_tags={"slow_ramp"},
    ),
    Boss(
        name="Aurelion Sol",
        stars=4.0,
        map_type="World Adventure",
        threat_description="4-Star Map. Spams legendary powers and champions turn 1.",
        counter_tags={"otk", "nexus_damage", "strike", "rally", "fast_kill"},
        vulnerable_tags={"strike", "burn", "rally", "otk"},
        penalized_tags={"late_game", "rng_buff"},
    ),
    Boss(
        name="Lissandra",
        stars=5.0,
        map_type="World Adventure",
        threat_description="5-Star Map. Buries your units in Ice Tombs, increases card costs.",
        counter_tags={"spellshield", "overwhelm", "stat_buff", "instant_impact"},
        vulnerable_tags={"spellshield", "overwhelm", "stat_buff"},
        penalized_tags={"spell", "draw", "cheap_spam"},
    ),
    Boss(
        name="Swain",
        stars=5.5,
        map_type="World Adventure",
        threat_description="5.5-Star Map. Heavy board wipes and tactical direct Nexus damage.",
        counter_tags={"spellshield", "regenerate", "lifesteal", "tempo", "fast_kill"},
        vulnerable_tags={"strike", "fast_kill", "spellshield"},
        penalized_tags={"slow_ramp", "sacrifice"},
    ),
]

DEFAULT_COMBOS: List[RelicCombo] = [
    RelicCombo(
        relics=("The Loose Cannon's Payload", "Luden's Tempest"),
        bonus=4.0,
        description="Payload Pow-Pows deal +1 damage each, clearing board and burning Nexus.",
    ),
    RelicCombo(
        relics=("Stalker's Blade", "Gatebreaker"),
        bonus=3.5,
        description="Double summon strike: clears the strongest enemy and damages Nexus.",
    ),
    RelicCombo(
        relics=("Tempest Blade", "Crownguard Inheritance"),
        bonus=4.5,
        description="Level-up stuns entire enemy board and gives instant Rally for lethal.",
    ),
    RelicCombo(
        relics=("Disciple of Shadows", "Corrupted Star Fragment"),
        bonus=4.0,
        description="Cheap champion drop combined with consuming surviving allies for massive stats.",
    ),
    RelicCombo(
        relics=("The Star Forge", "Chosen by the Stars"),
        bonus=4.0,
        description="Early titanic mana acceleration straight into empowered fated keyword devastation.",
    ),
    RelicCombo(
        relics=("Guardian's Orb", "Guardian's Orb"),
        bonus=3.0,
        description="Exponential deck item stacking on multiple summon triggers.",
    ),
    RelicCombo(
        relics=("Echoing Spirit", "Lost Chapter"),
        bonus=3.0,
        description="Spell mana refill perfectly casts discounted champion spells repeatedly.",
    ),
    RelicCombo(
        relics=("Chemtech Duplicator", "The Grand General's Counterplan"),
        bonus=3.5,
        description="Generates champion spell each round and doubles it after 6 mana.",
    ),
]


def load_dataset(base_dir: str = ".") -> DatabaseRegistry:
    """
    Loads and compiles the database from CSV files if present,
    enriching with full game mechanics.
    """
    relics_dict: Dict[str, Relic] = {r.name: r for r in DEFAULT_RELICS_CATALOG}
    bosses_dict: Dict[str, Boss] = {b.name: b for b in DEFAULT_BOSSES_CATALOG}
    champions_dict: Dict[str, Champion] = {}
    synergy_matrix: Dict[str, Dict[str, float]] = {}

    # Paths to search
    csv_base_paths = [
        os.path.join(base_dir, "data", "lor_genetic_algorithm_base.csv"),
        os.path.join(base_dir, "lor_genetic_algorithm_base.csv"),
    ]
    csv_builds_paths = [
        os.path.join(base_dir, "data", "poe_legends_of_runeterra_builds.csv"),
        os.path.join(base_dir, "poe_legends_of_runeterra_builds.csv"),
    ]

    # 1. Parse base CSV
    for path in csv_base_paths:
        if os.path.exists(path):
            with open(path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    elem_type = row.get("Element_Type", "").strip()
                    name = row.get("Name", "").strip()
                    subtype = row.get("Subtype_Or_Rarity", "").strip()
                    desc = row.get("Core_Attribute_Or_Effect", "").strip()
                    diff = row.get("Difficulty_Or_Cost", "").strip()

                    if elem_type == "Champion":
                        # Map subtype to Archetype
                        arch = Archetype.AGGRESSIVE
                        if "Control" in subtype:
                            arch = Archetype.CONTROL
                        elif "Combo" in subtype:
                            arch = Archetype.COMBO
                        elif "Defensive" in subtype or "Celestial" in subtype:
                            arch = Archetype.DEFENSIVE

                        champions_dict[name] = Champion(
                            name=name,
                            archetype=arch,
                            difficulty=diff,
                            core_mechanic=desc,
                        )

                    elif elem_type == "Relic":
                        if name not in relics_dict:
                            rarity = Rarity.RARE
                            if "Epic" in subtype:
                                rarity = Rarity.EPIC
                            elif "Common" in subtype:
                                rarity = Rarity.COMMON
                            relics_dict[name] = Relic(
                                name=name,
                                rarity=rarity,
                                base_score=5.0,
                                stackable=(rarity != Rarity.EPIC),
                                description=desc,
                            )

                    elif elem_type == "Boss":
                        if name not in bosses_dict:
                            stars = 3.0
                            if "-Star" in diff:
                                try:
                                    stars = float(diff.replace("-Star", "").strip())
                                except ValueError:
                                    pass
                            bosses_dict[name] = Boss(
                                name=name,
                                stars=stars,
                                map_type=subtype,
                                threat_description=desc,
                            )
            break

    # 2. Parse builds CSV (Expert Data / Community Tier list)
    for path in csv_builds_paths:
        if os.path.exists(path):
            with open(path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    champ_name = row.get("Champion", "").strip()
                    tier = row.get("Tier", "A").strip()
                    bis1 = row.get("Best-in-Slot Relic 1", "").strip()
                    bis2 = row.get("Best-in-Slot Relic 2", "").strip()
                    bis3 = row.get("Best-in-Slot Relic 3", "").strip()
                    strategy = row.get("Core Strategy", "").strip()

                    bis_list = [r for r in [bis1, bis2, bis3] if r]

                    # Register relics if missing
                    for r_name in bis_list:
                        if r_name and r_name not in relics_dict:
                            relics_dict[r_name] = Relic(
                                name=r_name,
                                rarity=Rarity.RARE,
                                base_score=5.0,
                                stackable=False,
                                description="Community recommended relic.",
                            )

                    if champ_name in champions_dict:
                        champ = champions_dict[champ_name]
                        champ.tier = tier
                        champ.bis_relics = bis_list
                        if strategy:
                            champ.core_mechanic = strategy
                    else:
                        champions_dict[champ_name] = Champion(
                            name=champ_name,
                            archetype=Archetype.COMBO,
                            difficulty="Medium",
                            core_mechanic=strategy,
                            tier=tier,
                            bis_relics=bis_list,
                        )

                    # Populate synergy matrix from BiS expert recommendations
                    if champ_name not in synergy_matrix:
                        synergy_matrix[champ_name] = {}

                    # Tier multiplier
                    tier_bonus = 2.0 if "S" in tier else 1.0
                    if bis1:
                        synergy_matrix[champ_name][bis1] = 10.0 + tier_bonus
                    if bis2:
                        synergy_matrix[champ_name][bis2] = 8.5 + tier_bonus
                    if bis3:
                        synergy_matrix[champ_name][bis3] = 7.5 + tier_bonus
            break

    # Add all other known PoC champions to champions_dict to provide 50+ champions
    all_poc_champs = [
        ("Aatrox", Archetype.TITANIC, "World Ender discount with Darkin units"),
        ("Ahri", Archetype.COMBO, "Recall and re-summon with elusive strikes"),
        ("Annie", Archetype.SPELL_SPAM, "Fast burn spells and Tibbers stun"),
        ("Ashe", Archetype.CONTROL, "Frostbite lock and arrow overwhelms"),
        ("Aurelion Sol", Archetype.TITANIC, "Celestial invoke and massive cost reduction"),
        ("Bard", Archetype.KEYWORD_STACK, "Chimes keyword and stat amplification"),
        ("Caitlyn", Archetype.COMBO, "Flashbomb traps and targeted strikes"),
        ("Darius", Archetype.AGGRESSIVE, "Direct overwhelm attacks and attack rallies"),
        ("Diana", Archetype.AGGRESSIVE, "Nightfall cascading quick attacks"),
        ("Ekko", Archetype.COMBO, "Predicts and Chronobreak resurrection"),
        ("Elise", Archetype.AGGRESSIVE, "Spiderling swarm with fearsome and keywords"),
        ("Evelynn", Archetype.SLAY, "Husk leveling loop granting massive stats"),
        ("Garen", Archetype.AGGRESSIVE, "Round start strikes and automatic rallies"),
        ("Gnar", Archetype.TRANSFORM, "Pokey stick ping and Mega Gnar overwhelm"),
        ("Gwen", Archetype.AGGRESSIVE, "Hallowed stack lifesteal attacks"),
        ("Illaoi", Archetype.AGGRESSIVE, "Spawn tentacles and double strike power"),
        ("Jack", Archetype.COMBO, "Coin mana refill and prize fight"),
        ("Janna", Archetype.COMBO, "Cost reduction through card draw"),
        ("Jax", Archetype.AGGRESSIVE, "Equipped unit stats and quick strikes"),
        ("Jhin", Archetype.CONTROL, "Captive audience stun and lotus trap burn"),
        ("Jinx", Archetype.DISCARD_BURN, "Discard rockets and direct burn"),
        ("Kai'Sa", Archetype.KEYWORD_STACK, "Second skin keyword harvesting"),
        ("Kayn", Archetype.TRANSFORM, "Rhaast / Shadow Assassin transformation"),
        ("Kennen", Archetype.COMBO, "Mark of the storm stuns and lightning"),
        ("Kindred", Archetype.SLAY, "Prey mark execution each round"),
        ("Leblanc", Archetype.COMBO, "Mirror Image spam and repeated summons"),
        ("Lee Sin", Archetype.SPELL_SPAM, "Dragon's rage kick and barriers"),
        ("Leona", Archetype.CONTROL, "Daybreak chain stuns"),
        ("Lillia", Archetype.COMBO, "Sleep stasis and summon re-triggers"),
        ("Lux", Archetype.SPELL_SPAM, "Final Spark laser spam"),
        ("Lux: Illuminated", Archetype.AGGRESSIVE, "Spirit buffs and barrier creation"),
        ("Master Yi", Archetype.SPELL_SPAM, "Flow mechanic with 0-cost alpha strike"),
        ("Miss Fortune", Archetype.AGGRESSIVE, "Love tap bullet time ping on attacks"),
        ("Mordekaiser", Archetype.SLAY, "Realm of death resurrection"),
        ("Morgana", Archetype.CONTROL, "Shackle curses preventing enemy actions"),
        ("Nami", Archetype.SPELL_SPAM, "Spell cast buffing lowest health ally"),
        ("Nasus", Archetype.SLAY, "Siphoning strike slay scaling and sun disc"),
        ("Neeko", Archetype.KEYWORD_STACK, "Shapesplitter subtype array"),
        ("Nidalee", Archetype.TRANSFORM, "Ambush flip and overwhelm strike"),
        ("Nilah", Archetype.COMBO, "Fleeting card duplicates and slipstream"),
        ("Norra", Archetype.COMBO, "Mysterious portals summoning random units"),
        ("Ornn", Archetype.TITANIC, "Forge master equipment duplication"),
        ("Pyke", Archetype.AGGRESSIVE, "Lurker instant board sweep on kill"),
        ("Samira", Archetype.COMBO, "Style rank combo and 0-cost rally"),
        ("Sett", Archetype.COMBO, "Showstopper true damage obliterates"),
        ("Swain", Archetype.CONTROL, "Direct nexus ping and flock stuns"),
        ("Tahm Kench", Archetype.DEFENSIVE, "Acquired taste capture and health scaling"),
        ("Taliyah", Archetype.COMBO, "Landmark duplication and stone volley"),
        ("Teemo", Archetype.DISCARD_BURN, "Puffcap multiplier on nexus strikes"),
        ("Thresh", Archetype.SLAY, "Champion pull from deck on unit deaths"),
        ("Vayne", Archetype.AGGRESSIVE, "Tumble free attack generation"),
        ("Veigar", Archetype.CONTROL, "Darkness damage scaling and burst speed"),
        ("Vex", Archetype.CONTROL, "Gloom stacks reducing enemy stats"),
        ("Vi", Archetype.AGGRESSIVE, "Vault breaker huge attack punches"),
        ("Viego", Archetype.SLAY, "Encroaching mist scaling and possession"),
        ("Volibear", Archetype.TITANIC, "Sigil of the storm titanic drops"),
        ("Yasuo", Archetype.STUN_FREEZE, "Stun and recall board execution"),
        ("Yuumi", Archetype.KEYWORD_STACK, "Attach mechanic making untargetable hyper-carry"),
    ]

    for name, arch, mechanic in all_poc_champs:
        if name not in champions_dict:
            champions_dict[name] = Champion(
                name=name,
                archetype=arch,
                difficulty="Medium",
                core_mechanic=mechanic,
            )

    # 3. Setup Star Power Synergies
    for champ_name, champ in champions_dict.items():
        if champ_name not in synergy_matrix:
            synergy_matrix[champ_name] = {}

        # Heuristic archetype synergies
        for relic_name, relic in relics_dict.items():
            current_syn = synergy_matrix[champ_name].get(relic_name, 0.0)
            bonus = 0.0

            # Discard / Burn
            if champ.archetype == Archetype.DISCARD_BURN:
                if "discard" in relic.tags or "burn" in relic.tags:
                    bonus += 5.0
            # Stun / Freeze
            elif champ.archetype in (Archetype.STUN_FREEZE, Archetype.CONTROL):
                if "stun" in relic.tags or "removal" in relic.tags:
                    bonus += 4.5
            # Titanic / Big stats
            elif champ.archetype == Archetype.TITANIC:
                if "titanic" in relic.tags or "mana_gem" in relic.tags or "overwhelm" in relic.tags:
                    bonus += 6.0
            # Slay / Sacrifice
            elif champ.archetype == Archetype.SLAY:
                if "slay" in relic.tags or "stat_buff" in relic.tags:
                    bonus += 5.0
            # Spell spam
            elif champ.archetype == Archetype.SPELL_SPAM:
                if "spell" in relic.tags or "spell_mana" in relic.tags:
                    bonus += 5.0
            # Aggro / Rally
            elif champ.archetype == Archetype.AGGRESSIVE:
                if "rally" in relic.tags or "aggro" in relic.tags or "overwhelm" in relic.tags:
                    bonus += 4.0

            if bonus > 0 and current_syn == 0:
                synergy_matrix[champ_name][relic_name] = bonus

        # Define Star Power synergy profiles (1 to 6 stars)
        champ.star_power_synergies = {
            1: [r for r, val in synergy_matrix[champ_name].items() if val >= 5.0][:2],
            2: ["The Star Forge", "Gatebreaker", "Luden's Tempest", "Lost Chapter"],
            3: champ.bis_relics if champ.bis_relics else [r for r, val in synergy_matrix[champ_name].items() if val >= 7.0][:3],
            4: ["The Beast Within", "Chosen by the Stars"],
            5: ["The Star Forge", "Echoing Spirit"],
            6: ["Chosen by the Stars", "Epic: Spectral Scissors", "The Beast Within"],
        }

    registry = DatabaseRegistry(
        champions=champions_dict,
        relics=relics_dict,
        bosses=bosses_dict,
        combos=DEFAULT_COMBOS,
        synergy_matrix=synergy_matrix,
    )

    return registry
