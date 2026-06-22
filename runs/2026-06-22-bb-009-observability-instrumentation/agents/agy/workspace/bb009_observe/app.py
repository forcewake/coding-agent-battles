from fastapi import FastAPI
app = FastAPI()
app.state.events = []

@app.get('/items/{item_id}')
def get_item(item_id: str):
    return {'item_id': item_id}
