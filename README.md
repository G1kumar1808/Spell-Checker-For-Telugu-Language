# Assignment 1: Probabilistic Spell Checker for Telugu

**Course:** Information Retrieval(IR)
**Submitted By:**

- **Name:** `<Yerram Jeevankumar>`
- **Roll No:** `<S20230010271>`

To properly view the ouput.txt,please open it in notepad.So that you can view the text properly.

---

## 1. Project Overview

This project is an implementation of a probabilistic spell checker for the **Telugu language**, as required by the assignment. More weightage was given to an Indian language, and Telugu was chosen for this implementation.

The system is built following the principles outlined by Peter Norvig. It leverages a large text corpus from the Telugu Wikipedia to build a statistical language model. This model is then used to identify misspelled words and provide a ranked list of probable corrections.

The core functionalities directly address the assignment requirements:

- **(a, b)** It uses a large **Telugu Wikipedia dump** as its data source.
- **(d)** It generates a comprehensive spell-checker **index on secondary memory** (`te_word_counts.json`).
- **(c)** At runtime, it identifies misspelled words, generates candidates using **four edit operations** (Insertion, Deletion, Substitution, Transposition), and ranks them based on frequency (semantic probability).
- **(d)** The source text and candidate lists for misspelled words are held in **main memory** during operation.

---

## 2. How the System Works (Meeting Assignment Requirements)

This system is designed in two main phases: a one-time indexing phase and a runtime spell-checking phase.

### Phase 1: Building the Index on Secondary Memory

**(Addresses Assignment Points a, b, and d)**

- **Data Source:** The system uses the official **Telugu Wikipedia dump** (`tewiki-latest-pages-articles.xml`), a single large XML file containing all articles, as its corpus.
- **Indexing Process:** The `1_build_index.py` script is executed once. It parses this massive XML file, strips all wiki markup (like `[[links]]`, `{{templates}}`), and extracts every unique Telugu word.
- **Storage on Secondary Memory:** It then counts the frequency of each word and saves this entire word-frequency dictionary as a single JSON file named `te_word_counts.json`. This file acts as our **spell checker index and is stored permanently on secondary memory** (Hard Drive/SSD).

### Phase 2: Spell Checking and Memory Management

**(Addresses Assignment Points c and d)**

- **Loading into Main Memory:** When `main.py` is run, the `SpellChecker` class loads the entire `te_word_counts.json` index from the hard drive into a dictionary in **main memory (RAM)**. This allows for very fast lookups during the spell-checking process.
- **Identifying Misspelled Words:** When the user provides a sentence, each word in the sentence is checked against the dictionary loaded in memory. Any word not found in the dictionary is flagged as misspelled.
- **Generating Candidate Corrections:** For each misspelled word, the system generates a set of potential corrections using the following logic:
  1.  **Edit Distance 1:** It applies the four required edit operations (**Insertion, Deletion, Substitution, and Transposition**) to the misspelled word to create a large set of candidate words that are one "edit" away.
  2.  **Edit Distance 2:** If no valid candidates are found at distance 1, it repeats the process to find words that are two edits away.
  3.  **Filtering:** Only candidates that actually exist in our dictionary are considered valid.
- **Ranking by Semantics (Probability):** The list of valid candidates is then **ranked based on their frequency** in the original corpus. A higher frequency implies a higher probability of the word being the correct one, serving as a strong proxy for semantic likelihood. The system presents the word with the highest probability as the "Best Guess".
- **Main Memory Usage:** The user's input sentence (the source document) and the generated list of probable candidates for each misspelled word are all held temporarily in **main memory** for the duration of the check.

---

## 3. Module Descriptions

The source code is organized into three distinct Python modules:

### `1_build_index.py`

- **Purpose:** This is a one-time utility script to build the language model.
- **Functionality:** It reads the `tewiki-latest-pages-articles.xml` file, processes its content, and generates the `te_word_counts.json` index file.

### `spell_checker.py`

- **Purpose:** This is the core engine of the spell checker.
- **Functionality:** It contains the `SpellChecker` class. The class constructor loads the index from disk. It has methods to calculate word probabilities, generate candidate words using `edits1()` and `edits2()` operations, and process a full document to find errors.

### `main.py`

- **Purpose:** This is the user-facing application.
- **Functionality:** It provides a simple, clean command-line menu for the user. The user can choose to run pre-defined test cases or enter an interactive mode to check their own sentences. It creates an instance of the `SpellChecker` and uses it to perform the actual checks.

---

## 4. How to Run the Code

Follow these steps precisely to set up and run the project.

### Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### Step 1: Setup and Installation

1.  Unzip the `<S20230010271>-src.zip` file.
2.  Open a terminal or command prompt and navigate into the `src` folder.
3.  It is highly recommended to create and activate a virtual environment:
    ```bash
    # Create the environment
    python -m venv .venv
    # Activate it (on Windows)
    .\.venv\Scripts\activate
    # Or activate it (on Mac/Linux)
    source .venv/bin/activate
    ```
4.  Install the required library:
    ```bash
    pip install mwparserfromhell
    ```

### Step 2: Build the Index (One-Time Task)

This step is computationally intensive and can take a significant amount of time.

1.  **Download the Data:** Download the Telugu Wikipedia dump from [https://dumps.wikimedia.org/tewiki/latest/](https://dumps.wikimedia.org/tewiki/latest/). Find and download the file named `tewiki-latest-pages-articles.xml.bz2`.
2.  **Unzip the File:** Unzip the `.bz2` file. You will get a very large XML file named `tewiki-latest-pages-articles.xml`.
3.  **Place the File:** Create a folder named `data` inside the `src` folder, and move the `.xml` file into it. The final path should be `src/data/tewiki-latest-pages-articles.xml`.
4.  **Run the Script:** From your terminal (inside the `src` folder), run the index builder:
    ```bash
    python 1_build_index.py
    ```
    Wait for it to complete. It will create the `te_word_counts.json` file in the `src` folder.

> **Note:** As this step is time-consuming, a pre-built index is provided at the link below. You can download it and place it in the `src` folder to skip this step.

### Step 3: Run the Spell Checker

Once the `te_word_counts.json` file is present in the `src` folder, you can run the main application.

1.  From your terminal (inside the `src` folder), run the main script:
    ```bash
    python main.py
    ```
2.  A menu will appear, allowing you to run pre-defined test cases or enter interactive mode.

---

## 5. Data and Index Link

As per the instructions, the large corpus file and the generated index file are not included in the submission zip. They can be downloaded from the following link:

- **Link:** `https://github.com/G1kumar1808/Spell-Checker-For-Telugu-Language`

---
