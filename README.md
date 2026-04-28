# DigiNote Backend

Hi yall! This is still barebones, right now there are only database schemas. But basically the breakdown is the following:

- Users (for authentication)
- Nodes (for the filetree in case we need folders)
- Decks (for the "questions" we'll be making, a deck will exist per node (pero if we want to keep it simple just limit it to singular note files)
- Flashcards (the actual question and answers we will be showing. It has a front and back field, one with the question, the other with the answer.
- Summary (a summary which can exist per node (pero again, per singular note file might better nalang)

