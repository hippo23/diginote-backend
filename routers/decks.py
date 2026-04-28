from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/deck", tags=["auth"])

@router.post('/')
async def create_deck():
    # this will autogenerate a deck of flashcards for the node that
    # you selected
    ...

@router.post('/refresh')
async def refresh_deck():
    # if a user dislikes a set of questions
    # as a whole, then they can just call this
    # to regenerate it
    ...

@router.get('/')
async def get_deck():
    # should retrieve all flashcards
    ...

@router.get('/')
async def delete_deck():
    # just delete the entire deck
    ...
