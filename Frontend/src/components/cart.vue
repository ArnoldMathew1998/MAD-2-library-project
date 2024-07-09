<template>
    <div class="cart-dropdown" id="cartDropdown">
    <div class="cart-item">
        <h5>Evoshield</h5>
        <p>Standout Backpack</p>
        <p>Size: Large | Color: White</p>
        <p>$76.00</p>
    </div>
    <div class="cart-item">
        <h5>Evoshield</h5>
        <p>XVT™ Luxe Fitted Batting Helmet</p>
        <p>Size: Large | Color: White</p>
        <p>$79.99</p>
    </div>
    <!-- Add more cart items as needed -->
</div>
</template>

<style scoped>
.cart-dropdown {
            position: fixed;
            right: 0;
            top: 60px;
            width: 400px;
            max-height: 80%;
            overflow-y: auto;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            display: none;
            z-index: 1000;
        }
        .cart-dropdown.show {
            display: block;
        }
        .cart-item {
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
        }
        .cart-item:last-child {
            border-bottom: none;
        }
</style>