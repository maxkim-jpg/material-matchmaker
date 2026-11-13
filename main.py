
from drafter import *
from dataclasses import dataclass, field

set_website_title("Material Matchmaker")
set_site_information(
    author="Max Kim",
    description="Find your perfect material",
    sources="Drafter docs, chatgpt, engineer wiki.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/maxkim-jpg/material-matchmaker"]
)
hide_debug_information()
set_website_framed(False)


# =====================================
# MATERIALS DATABASE
# =====================================

# Each material contains its density, heat resistance,
# and cost per kilogram as strings.
# Ranges are converted into averages later.

raw_materials = {
    "Acrylonitrile butadiene styrene (ABS)": ("1,030–1,070", "70–85", "2.3–3.4"),
    "Alumina (aluminium oxide, 99.5%)": ("3,850–3,950", "1,600–1,700", "11–34"),
    "Aluminium alloy 6061-T6": ("2,700", "150–200", "2.6–4"),
    "Aluminium alloy 7075-T6": ("2,810", "120–150", "4–6.8"),
    "Aramid fibre (Kevlar 49)": ("1,440", "150–200", "23–45"),
    "Aramid fibre composite (Kevlar/epoxy)": ("1,350–1,400", "120–180", "34–68"),
    "Ash (hardwood)": ("650–720", "100–120", "1.1–2.3"),
    "Bearing steel 100Cr6": ("7,810", "150–200", "1.7–3.4"),
    "Beech (hardwood)": ("680–750", "100–120", "0.9–2"),
    "Borosilicate glass": ("2,230", "450–500", "2.3–5.6"),
    "Carbon fibre reinforced polymer (CFRP), quasi-isotropic laminate": ("1,500–1,600", "120–180", "34–68"),
    "Carbon fibre reinforced polymer (CFRP), unidirectional": ("1,500–1,600", "120–180", "34–68"),
    "Cellulose acetate (CA)": ("1,270–1,310", "60–70", "3.4–5.6"),
    "Cold-work tool steel X153CrMoV12": ("7,700", "400–500", "5.6–14"),
    "Concrete C30/37": ("2,300–2,400", "200–300", "0.045–0.079"),
    "Cork": ("120–240", "120–140", "3.4–11"),
    "Epoxy resin (cast)": ("1,110–1,400", "80–170", "2.8–6.8"),
    "Ethylene propylene diene rubber (EPDM)": ("1,100–1,300", "130–160", "2.3–4.5"),
    "Expanded polystyrene (EPS)": ("15–35", "80", "2.3–4.5"),
    "Fired clay brick": ("1,600–2,000", "1,000–1,100", "0.23–0.45"),
    "Fused silica (quartz glass)": ("2,200", "950–1,100", "11–45"),
    "GFRP (glass fibre reinforced polymer)": ("1,750–1,970", "80–150", "3.4–17"),
    "Glass-filled polyamide PA66-GF30": ("1,350–1,370", "120–140", "4–5.1"),
    "Glued laminated timber GL24h": ("420", "100–120", "1.1–2.3"),
    "Gypsum plaster (set)": ("1,000–1,300", "80–100", "0.11–0.34"),
    "Hard ferrite magnet (strontium ferrite)": ("4,800–5,000", "250–300", "3.4–6.8"),
    "High-density polyethylene (PE-HD)": ("940–965", "80–120", "1.1–1.8"),
    "Low-density polyethylene (PE-LD)": ("917–930", "60–80", "1.1–1.8"),
    "Magnesium alloy AZ31B": ("1,770", "120–150", "3.4–5.6"),
    "Molybdenum": ("10,200", "1,100–1,600", "34–68"),
    "Natural rubber (NR)": ("920–1,000", "70–80", "1.7–3.4"),
    "Nickel alloy Inconel 625": ("8,440", "982", "40–68"),
    "Nickel superalloy Inconel 718": ("8,190", "650", "34–68"),
    "Nitrile rubber (NBR)": ("1,200–1,400", "100–120", "2.8–5.1"),
    "Oak (hardwood)": ("650–760", "100–120", "1.2–2.8"),
    "Polyamide 6 (PA6)": ("1,120–1,140", "80–100", "2.8–4"),
    "Polyamide 66 (PA66)": ("1,130–1,150", "80–120", "3.4–4.5"),
    "Polybutylene terephthalate (PBT)": ("1,300–1,310", "110–120", "2.8–4"),
    "Polycarbonate (PC)": ("1,190–1,210", "115–125", "3.4–4.5"),
    "Polyether ether ketone (PEEK)": ("1,300–1,320", "240–260", "79–120"),
    "Polyethylene terephthalate (PET)": ("1,330–1,390", "60–100", "1.4–2"),
    "Polylactic acid (PLA)": ("1,240–1,260", "50–60", "2.3–3.4"),
    "Polyoxymethylene (POM, acetal)": ("1,410–1,420", "90–100", "2.3–3.4"),
    "Polyphenylene sulfide PPS-GF40": ("1,640–1,670", "200–220", "5.6–11"),
    "Polypropylene (PP)": ("900–910", "100–110", "1.1–1.8"),
    "Polystyrene (PS)": ("1,040–1,050", "60–80", "1.6–2.5"),
    "Polytetrafluoroethylene (PTFE)": ("2,140–2,200", "260", "14–23"),
    "Precipitation-hardening stainless 17-4PH": ("7,780", "316", "6.8–11"),
    "Rigid polyurethane and polyisocyanurate foam (PUR/PIR)": ("30–40", "90–120", "3.4–6.8"),
    "Rigid polyvinyl chloride (PVC-U)": ("1,380–1,400", "60–65", "1.1–2.3"),
    "Scots pine (softwood)": ("500–550", "100–120", "0.56–1.1"),
    "Silicon carbide (sintered SiC)": ("3,100–3,210", "1,400–1,600", "17–56"),
    "Silicon nitride (Si3N4)": ("3,200–3,300", "1,200–1,300", "34–90"),
    "Silicone rubber (VMQ)": ("1,100–1,300", "200–230", "5.6–17"),
    "Soda-lime glass": ("2,500", "200–300", "0.56–1.7"),
    "Spruce (softwood)": ("400–470", "100–120", "0.56–1.1"),
    "Thermoplastic polyurethane (TPU)": ("1,100–1,250", "80–120", "4.5–7.9"),
    "Titanium alloy Ti-6Al-4V": ("4,430", "350–400", "23–40"),
    "Titanium grade 2": ("4,510", "300–400", "17–28"),
    "Tungsten": ("19,300", "1,500–2,500", "34–68"),
    "Unsaturated polyester resin (UP)": ("1,100–1,400", "70–150", "2.3–3.4"),
    "Zinc die-casting alloy Zamak 3": ("6,600", "50–100", "2.8–4.5")
}


def get_average(value):
    """
    Convert a material property string into a float.

    If the string contains a range, calculate its midpoint.
    If it contains one number, convert that number directly.

    Args:
        value (str): A single number or range of numbers.

    Returns:
        float: The numerical value or average of the range.
    """
    value = value.replace(",", "")
    value = value.replace("–", "-")

    numbers = value.split("-")

    if len(numbers) == 2:
        return (float(numbers[0]) + float(numbers[1])) / 2

    return float(value)


# Convert the raw material data into a usable dictionary.
# Density is converted from kg/m3 to g/cm3.
# Cost is converted from dollars/kg to dollars/lb.

materials = {}

for name, properties in raw_materials.items():
    density, heat, cost = properties

    materials[name] = {
        "density": round(get_average(density) / 1000, 4),
        "heat_resistance": round(get_average(heat), 2),
        "cost_per_pound": round(get_average(cost) / 2.20462, 2)
    }


# =====================================
# STATE DATACLASS
# =====================================

@dataclass
class State:
    """
    Store the user's preferences and material search information.

    Attributes:
        density (float): The user's desired density in g/cm3.
        heat_resistance (float): Desired heat resistance in Celsius.
        cost_per_pound (float): Desired cost in dollars per pound.
        matching_materials (list[str]): Material names ranked by score.
        scores (dict[str, int]): Match score for each material.
        selected_material_1 (str): First material chosen by the user.
        selected_material_2 (str): Second material chosen by the user.
    """
    density: float = 2.7
    heat_resistance: float = 175.0
    cost_per_pound: float = 1.5

    matching_materials: list[str] = field(default_factory=list)
    scores: dict[str, int] = field(default_factory=dict)

    selected_material_1: str = ""
    selected_material_2: str = ""


# =====================================
# MATCHING FUNCTIONS
# =====================================

def check_density(material, state):
    """
    Check whether a material's density matches the user's preference.

    The material passes if its density is within 20 percent
    of the user's desired density.

    Args:
        material (dict): Dictionary containing material properties.
        state (State): The user's current preferences.

    Returns:
        bool: True if density is within range, otherwise False.
    """
    difference = abs(material["density"] - state.density)
    tolerance = state.density * 0.20

    return difference <= tolerance


def check_heat(material, state):
    """
    Check whether a material's heat resistance matches the target.

    The material passes if its heat resistance is within
    20 degrees Celsius of the user's desired value.

    Args:
        material (dict): Dictionary containing material properties.
        state (State): The user's current preferences.

    Returns:
        bool: True if heat resistance is within range.
    """
    difference = abs(
        material["heat_resistance"] - state.heat_resistance
    )

    return difference <= 20


def check_cost(material, state):
    """
    Check whether a material's cost matches the user's preference.

    The material passes if its cost per pound is within
    20 percent of the user's desired cost.

    Args:
        material (dict): Dictionary containing material properties.
        state (State): The user's current preferences.

    Returns:
        bool: True if cost is within range, otherwise False.
    """
    difference = abs(
        material["cost_per_pound"] - state.cost_per_pound
    )
    tolerance = state.cost_per_pound * 0.20

    return difference <= tolerance


def calculate_score(material, state):
    """
    Calculate how closely a material matches the user's preferences.

    One point is awarded for each property within its
    acceptable range, giving a maximum score of three.

    Args:
        material (dict): Material properties to evaluate.
        state (State): The user's desired material properties.

    Returns:
        int: Match score between 0 and 3.
    """
    score = 0

    if check_density(material, state):
        score += 1

    if check_heat(material, state):
        score += 1

    if check_cost(material, state):
        score += 1

    return score


def find_matches(state):
    """
    Evaluate and rank all materials in the database.

    Calculates a score for every material and sorts the
    results from highest to lowest score. Materials with
    equal scores are sorted alphabetically.

    Updates the matching_materials and scores attributes
    in the user's State.

    Args:
        state (State): The current user's preferences.

    Returns:
        None: Results are saved directly into State.
    """
    results = []

    for name, material in materials.items():
        score = calculate_score(material, state)
        results.append((name, score))

    # Rank by score, highest first.
    # Alphabetical order breaks ties.
    results.sort(key=lambda item: (-item[1], item[0]))

    state.matching_materials = []
    state.scores = {}

    for name, score in results:
        state.matching_materials.append(name)
        state.scores[name] = score


def match_label(score):
    """
    Convert a numerical match score into a descriptive label.

    Args:
        score (int): The material's score from 0 to 3.

    Returns:
        str: Excellent Match, Good Match, Partial Match,
             or No Match.
    """
    if score == 3:
        return "Excellent Match"
    elif score == 2:
        return "Good Match"
    elif score == 1:
        return "Partial Match"
    else:
        return "No Match"


def status_text(passed):
    """
    Create a readable result for an individual property check.

    Args:
        passed (bool): Whether the material passed the check.

    Returns:
        str: PASS if the property matches, otherwise
             OUTSIDE RANGE.
    """
    if passed:
        return "PASS"
    else:
        return "OUTSIDE RANGE"


# =====================================
# PAGE 1: HOME
# =====================================

@route
def index(state: State) -> Page:
    """
    Display the homepage of Material Matchmaker.

    Introduces the website, explains the three searchable
    material properties, and provides navigation buttons.

    Args:
        state (State): The current application state.

    Returns:
        Page: The homepage with navigation options.
    """
    return Page(state, [
        Header("Material Matchmaker"),

        "Engineering Material Selection Tool",
        "\n",

        "Find materials with properties close "
        "to your desired values.",
        "\n",

        "Search by:",
        "1. Density (g/cm3)\n",
        "2. Heat Resistance (C)\n",
        "3. Cost per Pound ($/lb)\n",

        "\n",
        f"Materials available: {len(materials)}",
        "\n",

        Button("Find Materials", "search_page"),
        Button("Compare Materials", "compare_page"),
        Button("About the Website", "about_page")
    ])


# =====================================
# PAGE 2: SEARCH
# =====================================

@route
def search_page(state: State) -> Page:
    """
    Display the material search form.

    Allows users to enter their desired density,
    heat resistance, and cost per pound.

    The form uses values already stored in State.

    Args:
        state (State): Stores the current search preferences.

    Returns:
        Page: The search page containing three input fields.
    """
    return Page(state, [
        Header("Find Your Material"),

        "Enter your desired material properties.",
        "\n",

        "Desired Density (g/cm3):",
        TextBox("density", state.density, "number"),
        "\n",

        "Desired Heat Resistance (C):",
        TextBox(
            "heat_resistance",
            state.heat_resistance,
            "number"
        ),
        "\n",

        "Desired Cost per Pound ($/lb):",
        TextBox(
            "cost_per_pound",
            state.cost_per_pound,
            "number"
        ),
        "\n",

        "Materials will be compared using:",
        "Density: +/- 20%\n",
        "Heat Resistance: +/- 20 C\n",
        "Cost: +/- 20%\n",

        "\n",
        Button("Find Matches", "run_search"),
        Button("Home", "index")
    ])


# =====================================
# SEARCH SUBMISSION
# =====================================

@route
def run_search(
    state: State,
    density: float,
    heat_resistance: float,
    cost_per_pound: float
) -> Page:
    """
    Process the user's material search inputs.

    Validates the density and cost values, updates the
    user's State, clears previous material selections,
    and calculates new material matches.

    Args:
        state (State): The current application state.
        density (float): User's desired density in g/cm3.
        heat_resistance (float): Desired temperature in Celsius.
        cost_per_pound (float): Desired cost in dollars per pound.

    Returns:
        Page: The results page if inputs are valid,
              or an error page if an input is invalid.
    """
    if density <= 0:
        return Page(state, [
            Header("Invalid Density"),
            "Density must be greater than zero.",
            Button("Try Again", "search_page")
        ])

    if cost_per_pound < 0:
        return Page(state, [
            Header("Invalid Cost"),
            "Cost cannot be negative.",
            Button("Try Again", "search_page")
        ])

    state.density = density
    state.heat_resistance = heat_resistance
    state.cost_per_pound = cost_per_pound

    state.selected_material_1 = ""
    state.selected_material_2 = ""

    find_matches(state)

    return results_page(state)


# =====================================
# PAGE 3: RESULTS
# =====================================

@route
def results_page(state: State) -> Page:
    """
    Display all materials ranked by their matching scores.

    Shows how many materials received excellent or good
    scores and lists each material's properties.

    Users can select a material for additional details
    or navigate to the comparison page.

    Args:
        state (State): Contains the ranked results and scores.

    Returns:
        Page: A page displaying all ranked material results.
    """
    if not state.matching_materials:
        find_matches(state)

    excellent = 0
    good = 0

    for score in state.scores.values():
        if score == 3:
            excellent += 1
        elif score == 2:
            good += 1

    content = [
        Header("Material Search Results"),

        f"Materials searched: {len(materials)}",
        "\n",

        f"Excellent matches (3/3): {excellent}",
        "\n",

        f"Good matches (2/3): {good}",
        "\n",

        "Materials are ranked by their match score.",
        "\n"
    ]

    for name in state.matching_materials:
        material = materials[name]
        score = state.scores[name]

        content.append(Header(name, 3))

        content.append(
            f"Match Score: {score}/3 - {match_label(score)}"
        )
        content.append("\n")

        content.append(
            f"Density: {material['density']:.3f} g/cm3"
        )
        content.append("\n")

        content.append(
            f"Heat Resistance: "
            f"{material['heat_resistance']:.1f} C"
        )
        content.append("\n")

        content.append(
            f"Cost: ${material['cost_per_pound']:.2f}/lb"
        )
        content.append("\n")

        content.append(
            Button(
                "View Details",
                "choose_material",
                [Argument("name", name)]
            )
        )

        content.append("\n")

    content.extend([
        Button("Compare Materials", "compare_page"),
        Button("Edit Search", "search_page"),
        Button("Start Over", "reset_page"),
        Button("Home", "index")
    ])

    return Page(state, content)


# =====================================
# MATERIAL SELECTION
# =====================================

@route
def choose_material(state: State, name: str) -> Page:
    """
    Save the selected material and open its details page.

    Args:
        state (State): The current application state.
        name (str): Name of the material selected by the user.

    Returns:
        Page: The details page for the selected material.
    """
    state.selected_material_1 = name
    return material_page(state)


# =====================================
# PAGE 4: MATERIAL DETAILS
# =====================================

@route
def material_page(state: State) -> Page:
    """
    Display detailed information about a selected material.

    Shows the material's density, heat resistance, cost,
    individual property checks, and overall match score.

    If no valid material is selected, the user is sent
    back to the results page.

    Args:
        state (State): Contains the selected material and preferences.

    Returns:
        Page: The selected material's details page.
    """
    name = state.selected_material_1

    if name not in materials:
        return results_page(state)

    material = materials[name]
    score = calculate_score(material, state)

    density_ok = check_density(material, state)
    heat_ok = check_heat(material, state)
    cost_ok = check_cost(material, state)

    return Page(state, [
        Header(name),

        Header("Material Properties", 2),

        f"Density: {material['density']:.3f} g/cm3",
        "\n",

        f"Heat Resistance: "
        f"{material['heat_resistance']:.1f} C",
        "\n",

        f"Cost per Pound: "
        f"${material['cost_per_pound']:.2f}",
        "\n",

        Header("Requirement Checks", 2),

        f"Density: {status_text(density_ok)}",
        "\n",

        f"Heat Resistance: {status_text(heat_ok)}",
        "\n",

        f"Cost: {status_text(cost_ok)}",
        "\n",

        Header(f"Final Score: {score}/3", 2),
        match_label(score),

        "\n",

        Button("Back to Results", "results_page"),
        Button("Compare Materials", "compare_page"),
        Button("New Search", "search_page")
    ])


# =====================================
# PAGE 5: COMPARE MATERIALS
# =====================================

@route
def compare_page(state: State) -> Page:
    """
    Display a page for selecting two materials to compare.

    Retrieves and alphabetically sorts all material names.
    Previously selected materials are used when available.

    Args:
        state (State): Stores the selected comparison materials.

    Returns:
        Page: The material selection page or a message
              if no materials are available.
    """
    names = list(materials.keys())
    names.sort()

    if not names:
        return Page(state, [
            Header("No Materials Available"),
            Button("Home", "index")
        ])

    first = state.selected_material_1
    second = state.selected_material_2

    if first not in materials:
        first = names[0]

    if second not in materials:
        second = names[-1]

    return Page(state, [
        Header("Compare Two Materials"),

        "Choose the materials you want to compare.",
        "\n",

        "Material One:",
        SelectBox("first", names, first),
        "\n",

        "Material Two:",
        SelectBox("second", names, second),
        "\n",

        Button("Compare", "show_comparison"),
        Button("Back to Results", "results_page"),
        Button("Home", "index")
    ])


# =====================================
# COMPARISON RESULTS
# =====================================

@route
def show_comparison(
    state: State,
    first: str,
    second: str
) -> Page:
    """
    Compare the properties of two selected materials.

    Displays both materials' density, heat resistance,
    cost per pound, and overall match scores.

    Also identifies which material has the lower density,
    higher heat resistance, and lower cost.

    Args:
        state (State): The current application state.
        first (str): Name of the first selected material.
        second (str): Name of the second selected material.

    Returns:
        Page: A comparison page, or an error page
              if the same material is selected twice.
    """
    if first == second:
        return Page(state, [
            Header("Choose Different Materials"),
            "Please select two different materials.",
            Button("Try Again", "compare_page")
        ])

    state.selected_material_1 = first
    state.selected_material_2 = second

    a = materials[first]
    b = materials[second]

    score_a = calculate_score(a, state)
    score_b = calculate_score(b, state)

    return Page(state, [
        Header("Material Comparison"),

        Header(first, 2),

        f"Density: {a['density']:.3f} g/cm3",
        "\n",
        f"Heat Resistance: {a['heat_resistance']:.1f} C",
        "\n",
        f"Cost: ${a['cost_per_pound']:.2f}/lb",
        "\n",
        f"Match Score: {score_a}/3",
        "\n",

        Header(second, 2),

        f"Density: {b['density']:.3f} g/cm3",
        "\n",
        f"Heat Resistance: {b['heat_resistance']:.1f} C",
        "\n",
        f"Cost: ${b['cost_per_pound']:.2f}/lb",
        "\n",
        f"Match Score: {score_b}/3",
        "\n",

        Header("Comparison Summary", 2),

        f"Lower Density: "
        f"{first if a['density'] < b['density'] else second if b['density'] < a['density'] else 'Tie'}",
        "\n",

        f"Higher Heat Resistance: "
        f"{first if a['heat_resistance'] > b['heat_resistance'] else second if b['heat_resistance'] > a['heat_resistance'] else 'Tie'}",
        "\n",

        f"Lower Cost: "
        f"{first if a['cost_per_pound'] < b['cost_per_pound'] else second if b['cost_per_pound'] < a['cost_per_pound'] else 'Tie'}",
        "\n",

        Button("Compare Again", "compare_page"),
        Button("Back to Results", "results_page")
    ])


# =====================================
# PAGE 6: ABOUT
# =====================================

@route
def about_page(state: State) -> Page:
    """
    Explain the purpose and matching system of the website.

    Describes the three material properties, acceptable
    ranges, and the meaning of each match score.

    Args:
        state (State): The current application state.

    Returns:
        Page: An informational page about Material Matchmaker.
    """
    return Page(state, [
        Header("About Material Matchmaker"),

        "Material Matchmaker is designed to help "
        "users compare engineering materials.",
        "\n",

        "The program evaluates three properties:",
        "Density, Heat Resistance, and Cost.",
        "\n",

        Header("How Matching Works", 2),

        "Density must be within 20% "
        "of the user's desired value.",
        "\n",

        "Heat resistance must be within 20 C "
        "of the user's desired value.",
        "\n",

        "Cost must be within 20% "
        "of the user's desired value.",
        "\n",

        "Each matched property earns one point.",
        "\n",

        "3/3 = Excellent Match",
        "\n",
        "2/3 = Good Match",
        "\n",
        "1/3 = Partial Match",
        "\n",
        "0/3 = No Match",
        "\n",

        "These scores represent similarity to "
        "desired properties, not engineering safety.",
        "\n",

        "Property values are approximate reference "
        "values and should be verified for real designs.",

        Button("Home", "index")
    ])


# =====================================
# PAGE 7: RESET
# =====================================

@route
def reset_page(state: State) -> Page:
    """
    Reset the user's material search to its default settings.

    Creates a new State object, clearing previous search
    preferences, rankings, scores, and material selections.

    Args:
        state (State): The previous application state.

    Returns:
        Page: A confirmation page using the new State.
    """
    state = State()

    return Page(state, [
        Header("Search Reset"),

        "Your previous search has been cleared.",
        "\n",

        Button("Start New Search", "search_page"),
        Button("Home", "index")
    ])


# =====================================
# START THE WEBSITE
# =====================================

start_server(State())
