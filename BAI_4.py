from fastapi import FastAPI,HTTPException
from pydantic import Field,BaseModel


class product_schema(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]


@app.put("/products/{product_id}")
def update_product_by_list(product_id: int, product_data: product_schema):
    target_product = None
    
    for item in products:
        if item["code"] == product_data.code and item["id"] != product_id:
            raise HTTPException(status_code=400, detail="Product code already exists")
        
        if item["id"] == product_id:
            target_product = item

    if target_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    target_product.update(product_data.model_dump())
    
    return target_product


#ưu điểm , dễ hiểu  dễ sửa
# , hiệu năng kém  , tốc độ tìm kiếm chậm , phù hợp cho bài tập nhỏ , tối ưu ram