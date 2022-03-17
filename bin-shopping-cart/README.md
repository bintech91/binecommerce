# Authors

```
name: Thanh Tan Pham

email: phamtan15991@gmail.com
```

# Installation

## Poetry installation
https://python-poetry.org/docs/

## Project installation

1. Install dependencies

At path binecommerce/bin-shopping-cart/

```commandline
poetry install
```

2. Run project

```commandline
poetry run python main.py
```

3. Run unittest
```commandline
poetry run pytest
```

# API

## Get list products

### Request

```
GET /api/products
```

### Response

```
{
    "products": [
        {
            "product_id": string,
            "name": string,
            "price": number
        }
    ]
}
```

## Get product

### Request

```
GET /api/products/<product_id>
```

### Response

```
{
    "product_id": string,
    "name": string,
    "price": number
}
```


## Create new cart

### Request

```
POST /api/carts
```

### Response

```
{
    "cart_id": string
}
```

## Add cart items

### Request

```
POST /api/carts/<cart_id>/items/<product_id>

{
    "count": number
}
```

## Get cart items

### Request

```
GET /api/carts/<cart_id>/items
```

### Response

```
{
    "items": [
        {
            "product_id": string,
            "name": string,
            "price": number,
            "count": number
        }
    ]
}
```

## Get cart total

### Request

```
GET /api/carts/<cart_id>/total
```

### Response

```
{
    "total": number,
    "discount": number,
    "final": number
}
```

## Checkout cart

### Request

```
POST /api/carts/<cart_id>/checkout
```
