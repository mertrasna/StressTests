from locust import HttpUser, task, between
import random
import uuid
import datetime
import string

# All the products we have in the system
products = [
    {"id": "03194d03-e05b-4767-8f3a-f03446192d0f", "name": "Matcha 100 g"},
    {"id": "0a366f28-c94a-4bd2-a3db-26a3086e7224", "name": "Anatolian Assam (loose)"},
    {"id": "1fc9be15-2f0c-4680-817f-f9b609faefea", "name": "Camomile (loose)"},
    {"id": "289ec905-1f69-4fbd-836a-07a5e3a9e7f1", "name": "Matcha 50 g"},
    {"id": "291ada5c-afb6-4762-a95b-4f1b626912be", "name": "Earl Grey (loose)"},
    {"id": "2cf76111-fe22-4b1b-992a-a94c75afe99e", "name": "Gunpowder Tea (15 bags)"},
    {"id": "2e02ae39-daec-4a5a-9811-0271de49e855", "name": "Assam (loose)"},
    {"id": "341ed9ef-ff73-47ed-9b78-16e2e118fa7f", "name": "Earl Grey Green (loose)"},
    {"id": "59f0f900-ba4e-48cb-82fc-d1d1cb46f8cf", "name": "House blend (20 bags)"},
    {"id": "5c14ef82-7652-4288-810e-30187a2fa38f", "name": "Sencha (25 bags)"},
    {"id": "5ccb3a10-7432-40c7-8291-854700753d0b", "name": "Sencha (15 bags)"},
    {"id": "7bbee0ae-7f42-4582-a274-a06fb3f0f2aa", "name": "Frisian Black Tee (loose)"},
    {"id": "7f090d65-ebb0-4785-a783-3b46cf18e8e8", "name": "Assam with Ginger (20 bags)"},
    {"id": "828a8074-b705-4500-bb71-8a322c28d143", "name": "Gunpowder Tea (25 bags)"},
    {"id": "841a77ea-cef9-4f3b-91fb-6990e830ef75", "name": "Ceylon (loose)"},
    {"id": "a8e1a5f6-1ed7-4834-a108-00f2ed8dfac8", "name": "Sencha (loose)"},
    {"id": "aa2d0cdd-e9d1-4959-931f-89e9513c3ac0", "name": "Matcha 30 g"},
    {"id": "aa82f73c-7a3e-4c7a-a1d5-1464b542fefe", "name": "Darjeeling (loose)"},
    {"id": "aec06326-6783-4e22-8e83-d28f2af25037", "name": "Earl Grey (20 bags)"},
    {"id": "b406a033-4659-4b1a-bee7-d92456711eff", "name": "Gunpowder Tea (loose)"},
    {"id": "b561f137-f0d5-4bae-84f5-848add95a5ff", "name": "Earl Grey Green (15 bags)"},
    {"id": "c3479ef7-fb3d-498b-bdb4-6a6455b87713", "name": "Earl Grey Green (25 bags)"},
    {"id": "d89a50e9-7a40-409c-8468-5d2148f54adf", "name": "Darjeeling (20 bags)"},
    {"id": "ec8d6427-3009-44e5-b819-aa3ae3a983f6", "name": "Assam (20 bags)"},
    {"id": "f1d7623a-40e8-4dc7-848c-d4e82d6b8fb5", "name": "Ceylon (20 bags)"}
]


card_types = ["VISA", "Maestro", "Mastercard"]
first_names = ["Mert", "Efe", "John", "David", "Eddie", "Alice"]
last_names = ["Doe", "Catovic", "Taylor", "Lars", "Rasna"]
streets = ["Herbal Way", "Prager Street", "Berliner Street", "Oolong Blvd"]


class MyUser(HttpUser):
    wait_time = between(1, 10) # to give users time to think
    session_id = None
    cart_filled = False  # State variable to track cart status
    order_confirmed = False  # State variable to track order confirmation

    def random_card_number(self):
        """Generate a random 16-digit card number."""
        return "".join(random.choices(string.digits, k=16))

    def random_checksum(self):
        """Generate a random alphanumeric checksum."""
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def random_address(self):
        """Generate a random address."""
        street_number = random.randint(100, 999)
        street_name = random.choice(streets)  #  global streets variable
        return f"{street_number} {street_name}"

    @task(1)
    def browse_items(self):
        if self.order_confirmed:
            self.session_id = None
            self.cart_filled = False
            self.order_confirmed = False

        """Task to browse all products."""
        if not self.session_id:  # only browse if session hasn't started
            response = self.client.get("/products")
            if response.status_code == 200:
                print("Successfully browsed products.")
                self.session_id = str(uuid.uuid4())  # start a new session with new id
    
    @task(1 )
    def add_to_cart(self):
        """Task to add items to the cart."""
        if self.session_id and not self.cart_filled:  # Only proceed if browsing is done
            cart_content = {
                "id": self.session_id,
                "content": {},
                "creationDate": datetime.datetime.now().isoformat()
            }

            # Add random products to the cart
            for _ in range(random.randint(1, 3)):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                cart_content["content"][product["id"]] = quantity

            response = self.client.post("/cart", json=cart_content)
            if response.status_code in [200, 201]:
                print(f"Cart created successfully: {cart_content}")
                self.cart_filled = True

    @task(1)
    def confirm_order(self):
        """Task to confirm the order."""
        if not (self.cart_filled and not self.order_confirmed):
            return

        # generating random order data
        card_owner = f"{random.choice(first_names)} {random.choice(last_names)}"  # Use global variables
        card_number = self.random_card_number()
        checksum = self.random_checksum()
        card_type = random.choice(card_types)  # Use global variable
        address = self.random_address()

        # Prepare order data
        order_data = {
            "cardNumber": card_number,
            "cardOwner": card_owner,
            "checksum": checksum,
            "sessionId": self.session_id,
            "lastName": card_owner.split()[-1],  # Extract last name from cardOwner
            "address1": address,
            "cardType": card_type
        }

        # Make the API request
        response = self.client.post("/confirm", json=order_data)
        if response.status_code in [200, 201]:
            print(f"Order confirmed successfully: {order_data}")
            self.order_confirmed = True
        else:
            print(f"Order confirmation failed: {response.text}")
