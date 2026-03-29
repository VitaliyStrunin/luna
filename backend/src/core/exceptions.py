class PaymentAlreadyExists(Exception):
    def __init__(self, idempotency_key: str):
        self.message = f"Payment with idempotency key '{idempotency_key}' already exists"
        super().__init__(self.message)
        

class PaymentNotFoundByID(Exception):
    def __init__(self, id: str):
        self.message = f"Payment not found by ID '{id}'"
        super().__init__(self.message)
    


class PaymentNotFoundByIdempotencyKey(Exception):
    def __init__(self, id: str):
        self.message = f"Payment not found by idempotency key '{id}'"
        super().__init__(self.message)
        