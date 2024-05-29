# Structure Project

- Mantenimiento
  - app/ + **init**.py
  - models.py
  - service.py
    - confi/
      - local.py
      - qa.py
      - production.py
  - tests/
    - test_controller.py
    - test_service.py

## Operations

### Create User

```
curl -F "firstname=Juan" -F "lastname=perez" -F "age=20" -F "selectDepartment=eef11f69-ffe9-4078-ad09-16e31fe7f77c" -F "image=@cristiano.jpeg;type=image/jpeg" -X POST http://localhost:5002/employees

{
  "id": "27b79c53-edeb-4caf-9bcb-3725669eaa9d",
  "message": "Employee Created successfully!",
  "success": true
}

curl -X POST http://localhost:5002/employees
{
  "errors": [
    "firstname is required",
    "lastname is required",
    "age is required",
    "selectDepartment is required",
    "image is required"
  ],
  "message": "Error creating employee",
  "success": false
}

```