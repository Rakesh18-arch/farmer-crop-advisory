class CalendarService:
    """
    Crop Calendar and Phenological Stage Engine.
    Generates actionable temporal timelines for sowing, fertilization,
    irrigation, pest surveillance, and harvest.
    """

    CROP_CALENDARS = {
        "Rice": {
            "sowing_period": "June - July (Kharif) / November - December (Rabi)",
            "harvest_period": "October - November (Kharif) / April - May (Rabi)",
            "total_duration_days": 130,
            "stages": [
                {"stage": "Nursery & Sowing", "days": "Day 1 - 20", "task": "Seed treatment with Carbendazim (2g/kg) and nursery bed preparation."},
                {"stage": "Transplanting", "days": "Day 21 - 30", "task": "Transplant 2-3 seedlings/hill with 20x15 cm spacing in puddle field."},
                {"stage": "Early Tillering & Basal Fertilizer", "days": "Day 31 - 45", "task": "Apply basal DAP and MOP. Maintain 2-3 cm standing water."},
                {"stage": "Panicle Initiation & Nitrogen Top-Dressing", "days": "Day 46 - 65", "task": "Broadcast 1st split Urea dose. Monitor for stem borer and gall midge."},
                {"stage": "Booting & Flowering", "days": "Day 66 - 85", "task": "Critical irrigation window. Avoid moisture stress. Apply second split Urea."},
                {"stage": "Grain Filling & Milk Stage", "days": "Day 86 - 110", "task": "Maintain shallow water. Inspect for brown planthopper and neck blast."},
                {"stage": "Dough & Ripening", "days": "Day 111 - 125", "task": "Drain field water 10 days before harvesting."},
                {"stage": "Harvesting", "days": "Day 126 - 135", "task": "Harvest when 85% of the panicles turn golden yellow."}
            ]
        },
        "Cotton": {
            "sowing_period": "May - June (Kharif)",
            "harvest_period": "November - January",
            "total_duration_days": 160,
            "stages": [
                {"stage": "Field Prep & Sowing", "days": "Day 1 - 15", "task": "Deep plowing; dibble delinted seeds at 90x60 cm spacing."},
                {"stage": "Germination & Gap Filling", "days": "Day 16 - 25", "task": "Thinning to single seedling per hill. Check for seedling root rot."},
                {"stage": "Squaring & Vegetative", "days": "Day 26 - 55", "task": "Inter-cultivation and weeding. Install pheromone traps for whitefly and thrips."},
                {"stage": "Peak Flowering", "days": "Day 56 - 90", "task": "Critical moisture requirement. Apply second dose of Nitrogen and Potassium."},
                {"stage": "Boll Formation & Development", "days": "Day 91 - 125", "task": "Surveillance for Pink Bollworm. Spray neem-based bio-pesticides if larvae observed."},
                {"stage": "Boll Bursting & Picking", "days": "Day 126 - 160", "task": "Pick clean open bolls during dry morning hours without leaf trash."}
            ]
        },
        "Wheat": {
            "sowing_period": "November (Rabi)",
            "harvest_period": "March - April",
            "total_duration_days": 120,
            "stages": [
                {"stage": "Sowing & Basal Dose", "days": "Day 1 - 10", "task": "Sow certified seed at 20 cm row spacing with basal NPK application."},
                {"stage": "Crown Root Initiation (CRI)", "days": "Day 20 - 25", "task": "CRITICAL 1st irrigation. Apply first split Urea dose."},
                {"stage": "Tillering Stage", "days": "Day 40 - 45", "task": "2nd irrigation. Apply herbicide for weed control if necessary."},
                {"stage": "Jointing Stage", "days": "Day 60 - 65", "task": "3rd irrigation. Monitor for yellow rust or powdery mildew."},
                {"stage": "Flowering / Anthesis", "days": "Day 80 - 85", "task": "4th irrigation. Ensure adequate soil moisture during pollination."},
                {"stage": "Milking & Dough Stage", "days": "Day 100 - 105", "task": "5th irrigation. Avoid irrigation during stormy days to prevent lodging."},
                {"stage": "Maturity & Harvesting", "days": "Day 115 - 125", "task": "Harvest with combine or sickle when straw turns brittle and dry."}
            ]
        },
        "Maize": {
            "sowing_period": "June - July (Kharif) / October - November (Rabi)",
            "harvest_period": "September - October / February - March",
            "total_duration_days": 105,
            "stages": [
                {"stage": "Sowing", "days": "Day 1 - 10", "task": "Ridge and furrow sowing at 60x20 cm. Basal DAP + MOP application."},
                {"stage": "Knee-High Stage", "days": "Day 25 - 35", "task": "Apply 1st split Urea dose. Check central whorl for Fall Armyworm."},
                {"stage": "Tasseling & Silking", "days": "Day 50 - 65", "task": "Most critical irrigation phase. Apply second split Nitrogen."},
                {"stage": "Grain Filling", "days": "Day 66 - 85", "task": "Maintain moisture. Guard against bird damage."},
                {"stage": "Harvesting", "days": "Day 95 - 105", "task": "Harvest when cob sheath turns papery white and grain moisture drops below 20%."}
            ]
        }
    }

    @staticmethod
    def get_crop_calendar(crop_name: str) -> dict:
        """Returns standard stage-by-stage calendar and tasks for specified crop."""
        normalized = crop_name.capitalize().strip()
        calendar_data = CalendarService.CROP_CALENDARS.get(normalized)

        if not calendar_data:
            # Generic 110-day crop calendar
            calendar_data = {
                "sowing_period": "Seasonal (Kharif/Rabi dependent)",
                "harvest_period": "90 - 120 days post sowing",
                "total_duration_days": 110,
                "stages": [
                    {"stage": "Seed Sowing & Germination", "days": "Day 1 - 15", "task": "Seedbed leveling, seed treatment, and initial irrigation."},
                    {"stage": "Active Vegetative Growth", "days": "Day 16 - 45", "task": "Weeding, first split fertilizer application, and light irrigation."},
                    {"stage": "Flowering & Pollination", "days": "Day 46 - 70", "task": "Critical watering window. Monitor for foliage sucking pests."},
                    {"stage": "Fruit / Grain Development", "days": "Day 71 - 95", "task": "Maintain balanced moisture; apply organic micronutrient spray."},
                    {"stage": "Ripening & Harvesting", "days": "Day 96 - 110", "task": "Suspend irrigation 10 days before harvest. Reap produce at maturity."}
                ]
            }

        return {
            "success": True,
            "crop_name": normalized,
            "calendar": calendar_data
        }
