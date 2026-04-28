from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/flashcard", tags=["auth"])

@router.post('/')
async def update_flashcard():
    # if the user wants to edit a question themselves
    ...

@router.get('/')
async def delete_flashcard():
    # if a user dislikes a generated flashcard, they can delete them
    ...
