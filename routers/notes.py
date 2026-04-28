import requests
import re
from schemas import NodeCreate, NodeUpdate, NodePublic
from database import SessionDep
from routers.auth import CurrentUser
from models import Node
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text

router = APIRouter(prefix="/notes", tags=["notes"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_tree(nodes: list, parent_id=0):
    return [
        {**dict(node), "children": build_tree(nodes, node["id"])}
        for node in nodes if node["parent_id"] == parent_id
    ]

def clean_markdown(text: str) -> str:
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text, flags=re.DOTALL)
    text = re.sub(r'- \[x\]|- \[ \]', '-', text)
    text = re.sub(r'>\s*', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def summarize_block(content: str):
    url = "http://143.55.45.86:42528/v1/chat/completions"
    cleaned = clean_markdown(content)
    instruction = f"Summarize the key points of this text.\n\n{cleaned}"
    headers = {
        "Authorization": "Bearer 5013404055a67b396ee4292a62005121b3d77c19e10502c7be0a398d1a74d994",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "qwen3-summarizer",
        "messages": [{"role": "user", "content": instruction}]
    }
    res = requests.post(url, headers=headers, json=payload, verify=False)
    return res.json()["choices"][0]["message"]["content"]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/tree")
async def get_tree(current_user: CurrentUser, session: SessionDep):
    result = session.exec(text("""
        WITH RECURSIVE tree AS (
            SELECT * FROM node WHERE (parent_id = 0) AND
                user_id = :user_id
            UNION ALL
            SELECT n.* FROM node n
            JOIN tree t ON n.parent_id = t.id
            WHERE n.user_id = :user_id
        )
        SELECT * FROM tree
    """).bindparams(user_id=current_user.id))

    nodes = [dict(row) for row in result.mappings()]
    return build_tree(nodes)

@router.post("/", response_model=NodePublic)
async def create_node(data: NodeCreate, current_user: CurrentUser, session: SessionDep):
    # when you add a node, it should automaticaly generate a summary
    node = Node(**data.model_dump(), user_id=current_user.id)
    session.add(node)
    session.commit()
    session.refresh(node)
    return node

@router.patch("/{node_id}", response_model=NodePublic)
async def update_node(node_id: int, data: NodeUpdate, current_user: CurrentUser, session: SessionDep):
    node = session.get(Node, node_id)

    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    if node.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="This resource does not belong to you.")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(node, key, value)

    session.add(node)
    session.commit()
    session.refresh(node)
    return node

@router.delete("/{node_id}")
async def delete_node(node_id: int, current_user: CurrentUser, session: SessionDep):
    node = session.get(Node, node_id)

    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    if node.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="This resource does not belong to you.")

    session.delete(node)
    session.commit()
    return {"message": "Deleted"}

@router.get("/{node_id}/summary")
async def summarize_node(node_id: int, current_user: CurrentUser, session: SessionDep):
    node = session.get(Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    if node.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="This resource does not belong to you.")
    if not node.content:
        raise HTTPException(status_code=400, detail="Node has no content to summarize.")
    
    result = summarize_block(node.content)
    return {"message": result}
