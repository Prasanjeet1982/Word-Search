from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

class WordSearchGenerator:
    """
    Word Search Generator class that generates word search puzzles.
    """

    def __init__(self, size):
        """
        Initialize the WordSearchGenerator.

        Args:
            size (int): Size of the word search grid.
        """
        if size <= 0:
            raise ValueError("Size must be a positive integer.")
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]

    def insert_word(self, word):
        """
        Insert a word into the word search grid.

        Args:
            word (str): The word to be inserted.

        Returns:
            bool: True if the word was successfully inserted, False otherwise.
        """
        # ... (same as before)

    def fill_empty_cells(self):
        """
        Fill empty cells in the word search grid with random letters.
        """
        # ... (same as before)

    def generate(self, words):
        """
        Generate a word search puzzle.

        Args:
            words (list): List of words to insert into the grid.

        Raises:
            ValueError: If input words are not valid.

        Returns:
            None
        """
        if not isinstance(words, list) or not all(isinstance(word, str) for word in words):
            raise ValueError("Words must be a list of strings.")
        
        for word in words:
            word = word.upper()
            inserted = self.insert_word(word)
            if not inserted:
                print(f"Could not insert word: {word}")

        self.fill_empty_cells()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Render the index page.

    Args:
        request (Request): The incoming request.

    Returns:
        TemplateResponse: The index page template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(request: Request, words: str = Form(...), size: int = Form(...)):
    """
    Generate and display a word search puzzle.

    Args:
        request (Request): The incoming request.
        words (str): Comma-separated list of words.
        size (int): Size of the word search grid.

    Returns:
        TemplateResponse: The word search page template with the generated grid or an error message.
    """
    try:
        words = words.split(",")
        word_search = WordSearchGenerator(size)
        word_search.generate(words)
        return templates.TemplateResponse("word_search.html", {"request": request, "grid": word_search.grid})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error_message": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
