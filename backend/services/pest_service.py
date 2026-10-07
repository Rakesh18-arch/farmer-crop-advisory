class PestService:
    """
    Expert Pest Management Advisory Engine.
    Correlates crop types, growth stages, and observed visual field symptoms
    to diagnose pest infestations with biological and IPM control measures.
    """

    PEST_KNOWLEDGEBASE = [
        {
            "crop": "Cotton",
            "growth_stage": "Flowering / Boll Formation",
            "symptom": "Flared square, rosette flowers, bored holes with excreta in developing bolls",
            "pest_name": "Pink Bollworm (Pectinophora gossypiella)",
            "severity": "HIGH",
            "biological_control": "Release Trichogramma bactrae egg parasitoids @ 60,000/acre weekly; install pink bollworm pheromone traps (Gossyplure) @ 8/acre.",
            "chemical_control": "Emamectin Benzoate 5% SG @ 4g/10L water or Chlorantraniliprole 18.5% SC @ 3ml/10L water.",
            "prevention": "Avoid ratoon cropping; cultivate short-duration varieties; destroy crop stalks immediately post-harvest."
        },
        {
            "crop": "Cotton",
            "growth_stage": "Vegetative",
            "symptom": "Upward leaf curling, honeydew excretion, black sooty mold on foliage",
            "pest_name": "Whitefly (Bemisia tabaci)",
            "severity": "MODERATE",
            "biological_control": "Install yellow sticky traps @ 10-15/acre; spray 5% Neem Seed Kernel Extract (NSKE) or Verticillium lecanii bio-agent @ 5g/L.",
            "chemical_control": "Diafenthiuron 50% WP @ 1.25g/L or Pyriproxyfen 10% EC @ 2ml/L water.",
            "prevention": "Avoid excess vegetative nitrogen; maintain border crops like maize or bajra."
        },
        {
            "crop": "Rice",
            "growth_stage": "Tillering / Reproductive",
            "symptom": "Dead hearts in vegetative stage and white ears/panicles at maturity",
            "pest_name": "Yellow Stem Borer (Scirpophaga incertulas)",
            "severity": "HIGH",
            "biological_control": "Install pheromone traps @ 5/acre; release egg parasitoid Trichogramma japonicum @ 40,000/acre.",
            "chemical_control": "Cartap Hydrochloride 4G @ 8 kg/acre or Chlorantraniliprole 0.4% G @ 4 kg/acre in standing water.",
            "prevention": "Clip seedling leaf tips before transplanting to eliminate egg masses."
        },
        {
            "crop": "Rice",
            "growth_stage": "Vegetative to Heading",
            "symptom": "Circular burnt patches of drying plants ('hopper burn') in the center of the field",
            "pest_name": "Brown Planthopper (Nilaparvata lugens)",
            "severity": "HIGH",
            "biological_control": "Conserve predatory mirid bugs and spiders; avoid indiscriminate broad-spectrum pyrethroid sprays.",
            "chemical_control": "Triflumuron + Pymetrozine 50% WG @ 0.6g/L or Dinotefuran 20% SG @ 0.4g/L directly directed at stem base.",
            "prevention": "Provide alleyways (passage lines) every 2-3 meters for aeration; alternate wetting and drying (AWD) water management."
        },
        {
            "crop": "Tomato",
            "growth_stage": "Vegetative to Fruiting",
            "symptom": "Serpentine silvery translucent mines/tunnels on leaves",
            "pest_name": "Serpentine Leafminer (Liriomyza trifolii)",
            "severity": "LOW",
            "biological_control": "Spray Neem oil (3000 ppm) @ 3 ml/L; conserve eulophid wasps (Diglyphus isaea).",
            "chemical_control": "Abamectin 1.9% EC @ 0.5 ml/L water.",
            "prevention": "Collect and burn heavily mined lower leaves; install yellow sticky sheets."
        },
        {
            "crop": "Tomato",
            "growth_stage": "Fruiting",
            "symptom": "Bored holes in fruits with caterpillar half inside the fruit body",
            "pest_name": "Fruit Borer (Helicoverpa armigera)",
            "severity": "HIGH",
            "biological_control": "Install Helilure pheromone traps @ 5/acre; spray HaNPV (Helicoverpa Nuclear Polyhedrosis Virus) @ 250 LE/acre in evening.",
            "chemical_control": "Flubendiamide 39.35% SC @ 0.3 ml/L or Indoxacarb 14.5% SC @ 1 ml/L water.",
            "prevention": "Plant African Marigold as a trap crop (1 row marigold for every 16 rows of tomato)."
        },
        {
            "crop": "Chilli",
            "growth_stage": "Vegetative to Flowering",
            "symptom": "Leaves curl upwards like a boat; crinkled margins, flower drop",
            "pest_name": "Chilli Thrips (Scirtothrips dorsalis)",
            "severity": "MODERATE",
            "biological_control": "Blue sticky traps @ 10/acre; spray Neem oil @ 5 ml/L or Lecanicillium lecanii @ 5g/L.",
            "chemical_control": "Fipronil 5% SC @ 2 ml/L or Spinetoram 11.7% SC @ 1 ml/L water.",
            "prevention": "Sprinkle clean water on foliage to disrupt thrip nymphs; avoid water stress."
        },
        {
            "crop": "Maize",
            "growth_stage": "Seedling to Whorl Stage",
            "symptom": "Severe leaf feeding in the central whorl, saw-dust-like frass on leaves",
            "pest_name": "Fall Armyworm (Spodoptera frugiperda)",
            "severity": "HIGH",
            "biological_control": "Apply dry sand/soil mixed with wood ash (9:1) into whorls; spray Bacillus thuringiensis (Bt) @ 2g/L.",
            "chemical_control": "Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L into central whorl.",
            "prevention": "Deep summer plowing to expose pupae to predatory birds; clean field cultivation."
        }
    ]

    @staticmethod
    def diagnose_pest(crop: str, growth_stage: str = None, symptom: str = None) -> dict:
        """Finds matching pest records based on user input parameters."""
        matches = []
        for record in PestService.PEST_KNOWLEDGEBASE:
            crop_match = crop.lower() in record["crop"].lower() or record["crop"].lower() in crop.lower()
            stage_match = True if not growth_stage else (growth_stage.lower() in record["growth_stage"].lower())
            symptom_match = True if not symptom else any(
                word in record["symptom"].lower() for word in symptom.lower().split() if len(word) > 3
            )

            if crop_match:
                score = (2 if crop_match else 0) + (1 if stage_match else 0) + (2 if symptom_match else 0)
                matches.append((score, record))

        matches.sort(key=lambda x: x[0], reverse=True)

        if matches and matches[0][0] >= 2:
            best = matches[0][1]
            return {
                "success": True,
                "crop": crop,
                "diagnosed_pest": best["pest_name"],
                "severity": best["severity"],
                "symptoms_confirmed": best["symptom"],
                "biological_control": best["biological_control"],
                "chemical_control": best["chemical_control"],
                "prevention": best["prevention"],
                "advice": f"Integrated Pest Management (IPM) is strongly advised. Prioritize biological measures and use chemical sprays only if pest population crosses the Economic Threshold Level (ETL)."
            }

        # Generic IPM fallback
        return {
            "success": True,
            "crop": crop,
            "diagnosed_pest": "Undetermined Sucking/Chewing Pest Complex",
            "severity": "MODERATE",
            "symptoms_confirmed": symptom or "Foliage chewing or sap sucking damage",
            "biological_control": "Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil 1500 ppm @ 5 ml/L water.",
            "chemical_control": "Consult local Krishi Vigyan Kendra (KVK) extension officer for precise species confirmation.",
            "prevention": "Install pheromone traps and maintain weed-free field boundaries.",
            "advice": "Monitor pest incidence weekly. Take photo and consult agricultural extension services."
        }

    @staticmethod
    def get_catalog() -> list:
        """Returns the complete list of managed pests across major Indian crops."""
        return PestService.PEST_KNOWLEDGEBASE
