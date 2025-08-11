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

DETAILED_SYLLABUS = {
    "math": {
        "Linear Equations and Inequalities": "Solving single-variable linear equations and inequalities. Includes interpreting slope and intercepts, and solving related word problems.",
        "Systems of Linear Equations": "Solving systems of two or more linear equations algebraically (substitution, elimination) and graphically. Determining whether a system has one solution, no solution, or infinitely many.",
        "Manipulating Algebraic Expressions": "Simplifying, factoring, and expanding expressions involving polynomials, rational terms, and exponents.",
        "Solving Literal Equations": "Rearranging formulas to isolate specific variables, often used in geometry, physics, and real-world contexts.",
        "Ratios, Proportions, Percents": "Solving problems involving proportional relationships, percent change, scaling, and direct/inverse variation.",
        "Data Interpretation (Tables, Charts, Graphs)": "Reading, analyzing, and drawing conclusions from tables, bar charts, line graphs, scatterplots, and other graphical data representations.",
        "Descriptive Statistics (Mean, Median, Mode, Range)": "Calculating and interpreting measures of central tendency and variability, and identifying effects of data changes.",
        "Probability and Inference": "Calculating simple and compound probabilities, and making predictions based on probability models.",
        "Quadratic Equations and Functions": "Solving quadratics by factoring, completing the square, or quadratic formula. Analyzing parabolas and interpreting vertex, intercepts, and axis of symmetry.",
        "Polynomials and Rational Expressions": "Adding, subtracting, multiplying, dividing, and factoring polynomials. Simplifying and solving rational expressions and equations.",
        "Exponential and Radical Equations": "Solving equations with exponential and radical terms, and interpreting exponential growth/decay.",
        "Function Notation, Domain, and Composition": "Evaluating and interpreting functions, determining domains and ranges, and working with composite and inverse functions.",
        "Angles, Circles, and Triangles": "Using angle relationships, circle theorems, and triangle properties to solve problems.",
        "Volume and Area Calculations": "Calculating the volume and surface area of 2D and 3D shapes including prisms, cylinders, cones, and spheres.",
        "Trigonometric Ratios (sin, cos, tan)": "Applying trigonometric ratios in right triangles, solving for sides and angles, and using special triangles."
    },
    "writing": {
        "Subject-Verb Agreement": "Matching singular/plural subjects with correct verb forms, even in sentences with interrupting phrases or inverted word order.",
        "Verb Tense and Mood Consistency": "Maintaining correct verb tense and mood throughout sentences and paragraphs, avoiding shifts that confuse meaning.",
        "Pronoun Clarity and Agreement": "Ensuring pronouns agree in number and gender with their antecedents, and avoiding ambiguous pronoun references.",
        "Modifier Placement and Usage": "Placing modifiers next to the words they describe, and avoiding misplaced or dangling modifiers.",
        "Sentence Boundaries (Fragments / Run-ons)": "Correcting sentence fragments and run-on sentences by adding, removing, or changing punctuation or conjunctions.",
        "Punctuation (Commas, Semicolons, Colons, Dashes)": "Using punctuation to join clauses, separate items, or set off non-essential information correctly.",
        "Clarity and Conciseness": "Eliminating redundancy, wordiness, and vague phrasing for clear, concise sentences.",
        "Logical Flow and Transitions": "Using appropriate transition words and sentence structures to connect ideas smoothly.",
        "Effective Word Choice": "Selecting precise, appropriate, and contextually accurate vocabulary.",
        "Goal-Oriented Revision": "Revising sentences or paragraphs to better achieve a specific rhetorical or stylistic goal."
    },
    "reading": {
        "Main Idea / Central Theme": "Identifying the main point or theme of a passage and differentiating it from supporting details.",
        "Inference from Text": "Drawing logical conclusions that are supported by evidence but not directly stated in the passage.",
        "Author’s Purpose / Point of View": "Determining why the author wrote the passage or a portion of it, and identifying their perspective.",
        "Vocabulary in Context": "Determining the meaning of a word or phrase as it is used in the specific context of the passage.",
        "Tone and Attitude": "Recognizing the author’s tone, mood, or attitude toward the subject matter.",
        "Text Structure / Logical Flow": "Understanding how ideas are organized and connected in a passage (cause-effect, compare-contrast, etc.).",
        "Evidence-Based Support": "Identifying the specific sentence or detail that supports an answer to a prior question."
    }
}

