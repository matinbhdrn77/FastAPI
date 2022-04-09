from typing import Dict, Optional
from fastapi import Body, FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_post = [{'title': "first title", 'content': 'first content', 'id': 1}, {
    'title': "second title", 'content': 'second content', 'id': 2}]


def find_post(id):
    for post in my_post:
        if post['id'] == id:
            return post

def find_index(id):
    for i, post in enumerate(my_post):
        if post['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_post}

# @app.post("/createpost")
# def create_post(payload: Dict = Body(...)):
#     print(payload)
#     return {"data": f"title: {payload['title']} content: {payload['content']}"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    my_post.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post details": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    post = my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)