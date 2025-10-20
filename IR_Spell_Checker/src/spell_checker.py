# src/spell_checker.py
import json
import re

class SpellChecker:
    def __init__(self, index_path='src/te_word_counts.json'):
        """
        Initializes the spell checker by loading the Telugu index from disk.
        """
        print("Loading spell checker index from disk...")
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                self.WORDS = json.load(f)
            self.TOTAL_WORDS = sum(self.WORDS.values())
            print("Index loaded successfully.")
        except FileNotFoundError:
            print(f"ERROR: Index file not found at {index_path}")
            print("Please run '1_build_index.py' first to create the index file.")
            self.WORDS = {}
            self.TOTAL_WORDS = 0

    def probability(self, word):
        """Calculates the probability of a word."""
        return self.WORDS.get(word, 0) / self.TOTAL_WORDS

    def correction(self, word):
        """Finds the most probable spelling correction for a given word."""
        return max(self.candidates(word), key=self.probability)
    
    def candidates(self, word):
        """Generates a set of possible candidate corrections for a word."""
        known_words = self.known([word])
        if known_words: return known_words

        edit_distance_1 = self.known(self.edits1(word))
        if edit_distance_1: return edit_distance_1

        edit_distance_2 = self.known(self.edits2(word))
        if edit_distance_2: return edit_distance_2

        return {word}

    def known(self, words):
        """Filters a list to return only words present in our dictionary."""
        return set(w for w in words if w in self.WORDS)

    def edits1(self, word):
        """
        Generates all possible words that are one edit away.
        """
        # The Telugu alphabet
        letters = 'అఆఇఈఉఊఋఎఏఐఒఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయర్లవశషసహ'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        """Generates all possible words that are two edits away."""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def check_document(self, text):
        """
        Checks a full document, storing results in main memory.
        """
        words = re.findall(r'[\u0C00-\u0C7F]+', text.lower())
        
        results = {
            'source_text': text,
            'corrections': {}
        }
        
        if not self.WORDS: # Check if index loaded properly
            print("Cannot check document because the word index is empty.")
            return results

        for word in words:
            if word not in self.WORDS:
                possible_candidates = self.candidates(word)
                ranked_candidates = sorted(list(possible_candidates), key=self.probability, reverse=True)
                results['corrections'][word] = {
                    'best_guess': self.correction(word),
                    'candidates': ranked_candidates[:5] # Show top 5
                }
        return results