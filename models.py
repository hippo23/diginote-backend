from typing import Optional
from datetime import datetime
from sqlmodel import create_engine, SQLModel, Field

# Credits to Claude for this

# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# ---------------------------------------------------------------------------
# Node (filetree)
# ---------------------------------------------------------------------------

class Node(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="node.id")
    user_id: int = Field(foreign_key="user.id")
    type: str                               # folder | note | image
    name: str
    content: Optional[str] = None           # notes only
    image_path: Optional[str] = None        # images only
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# ---------------------------------------------------------------------------
# Deck
# ---------------------------------------------------------------------------

class Deck(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    node_id: Optional[int] = Field(default=None, foreign_key="node.id")
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ---------------------------------------------------------------------------
# Flashcard
# ---------------------------------------------------------------------------

class Flashcard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    deck_id: int = Field(foreign_key="deck.id")
    front: str
    back: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

class Summary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    node_id: int = Field(foreign_key="node.id")
    user_id: int = Field(foreign_key="user.id")
    content: str
    is_current: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
