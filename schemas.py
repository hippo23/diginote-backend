# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------
class UserRegister(SQLModel):
    username: str
    email: str
    password: str

class UserLogin(SQLModel):
    username: str
    password: str

class UserChangePassword(SQLModel):
    old_password: str
    new_password: str

class UserPublic(SQLModel):
    id: int
    username: str
    email: str
    created_at: datetime

# ---------------------------------------------------------------------------
# Filetree
# ---------------------------------------------------------------------------
class NodeCreate(SQLModel):
    parent_id: Optional[int] = None
    type: str
    name: str
    content: Optional[str] = None
    image_path: Optional[str] = None

class NodeUpdate(SQLModel):
    name: Optional[str] = None
    content: Optional[str] = None
    image_path: Optional[str] = None
    parent_id: Optional[int] = None         

class NodeMove(SQLModel):
    parent_id: Optional[int]                

class NodePublic(SQLModel):
    id: int
    parent_id: Optional[int]
    user_id: int
    type: str
    name: str
    content: Optional[str]
    image_path: Optional[str]
    created_at: datetime
    updated_at: datetime

# ---------------------------------------------------------------------------
# Deck
# ---------------------------------------------------------------------------
class DeckCreate(SQLModel):
    name: str
    node_id: Optional[int] = None

class DeckUpdate(SQLModel):
    name: Optional[str] = None
    node_id: Optional[int] = None

class DeckPublic(SQLModel):
    id: int
    user_id: int
    node_id: Optional[int]
    name: str
    created_at: datetime

# ---------------------------------------------------------------------------
# Flashcards
# ---------------------------------------------------------------------------
class FlashcardCreate(SQLModel):
    front: str
    back: str

class FlashcardUpdate(SQLModel):
    front: Optional[str] = None
    back: Optional[str] = None

class FlashcardPublic(SQLModel):
    id: int
    deck_id: int
    front: str
    back: str
    created_at: datetime

class GenerateFlashcardsRequest(SQLModel):
    note_content: str
    num_cards: int = 10

class GenerateFlashcardsResponse(SQLModel):
    deck_id: int
    cards: list[FlashcardPublic]


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
class SummaryPublic(SQLModel):
    id: int
    node_id: int
    content: str
    is_current: bool
    created_at: datetime

class GenerateSummaryRequest(SQLModel):
    note_content: str

class GenerateSummaryResponse(SQLModel):
    summary: SummaryPublic
