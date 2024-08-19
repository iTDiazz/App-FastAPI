from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title='Trading App'
)

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Bob'},
    {'id': 2, 'role': 'investor', 'name': 'Kai'},
    {'id': 3, 'role': 'trader', 'name': 'John'},
    {'id': 4, 'role': 'investor', 'name': 'Homer', 'degree': [
        {'id': 1, 'created_at': '2024-08-18T17:48:30', 'type_degree': 'expert'}
    ]}
]

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: str

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = None  # по умолчанию None

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = next((user for user in fake_users if user['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

fake_trades = [
    {'id_operation': 1, 'wallet': 'MoneyBank', 'crypto_money': 'BTC'},
    {'id_operation': 2, 'wallet': 'CryptoBank', 'crypto_money': 'ETH'},
    {'id_operation': 3, 'wallet': 'RichBank', 'crypto_money': 'TON'},
    {'id_operation': 4, 'wallet': 'BigBank', 'crypto_money': 'NOT'}
]

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=8)
    side: str
    price: float = Field(ge=0)
    amount: float

@app.post('/trades')
async def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}