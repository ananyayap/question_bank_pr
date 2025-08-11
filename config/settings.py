import os
from dotenv import load_dotenv

load_dotenv()

# Firestore settings
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Predefined SAT sections and difficulty levels
SECTIONS = ["math", "reading", "writing"]
DIFFICULTIES = ["easy", "medium", "hard"]


SECTION_TAGS = {
    "reading": [
        "Main Idea / Central Theme",
        "Inference from Text",
        "Author's Purpose / Point of View",
        "Vocabulary in Context",
        "Tone and Attitude",
        "Text Structure / Logical Flow",
        "Evidence-Based Support",
        "Logical Flow and Transitions",
        "Effective Word Choice",
        "Goal-Oriented Revision"
    ],
    "writing": [
        "Subject-Verb Agreement",
        "Verb Tense and Mood Consistency",
        "Pronoun Clarity and Agreement",
        "Modifier Placement and Usage",
        "Sentence Boundaries (Fragments / Run-ons)",
        "Punctuation (Commas, Semicolons, Colons, Dashes)",
        "Clarity and Conciseness",
        "Logical Flow and Transitions",
        "Effective Word Choice",
        "Goal-Oriented Revision"
    ],
    "math": [
        "Linear Equations and Inequalities",
        "Systems of Linear Equations",
        "Manipulating Algebraic Expressions",
        "Solving Literal Equations",
        "Ratios, Proportions, Percents",
        "Data Interpretation (Tables, Charts, Graphs)",
        "Descriptive Statistics (Mean, Median, Mode, Range)",
        "Probability and Inference",
        "Quadratic Equations and Functions",
        "Polynomials and Rational Expressions",
        "Exponential and Radical Equations",
        "Function Notation, Domain, and Composition",
        "Angles, Circles, and Triangles",
        "Volume and Area Calculations",
        "Trigonometric Ratios (sin, cos, tan)"
    ]
}

