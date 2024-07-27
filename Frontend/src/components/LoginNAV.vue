<template>
  <nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-fluid">
      <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
        <div class="d-flex align-items-center">
          <RouterLink to="/Profile" class="d-flex align-items-center">
            <img :src="resolvedImagePath(user.profile_photo)" alt="Avatar" :class="{'profile-icon': !isActive('/Profile'), 'profile-icon-active': isActive('/Profile')}" />  
          </RouterLink>
        </div>

        <ul class="navbar-nav">
          <li class="nav-item">
            <RouterLink to="/Home" class="nav-link active" aria-current="page">
              <i :class="{'bi bi-house': !isActive('/Home'), 'bi bi-house-fill': isActive('/Home'), 'text-red': isActive('/Home') }">Home</i>
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink to="/Section" class="nav-link active" aria-current="page">
              <i :class="{'bi bi-collection': !isActive('/Section'), 'bi bi-collection-fill': isActive('/Section'), 'text-red': isActive('/Section') }">Section</i>
            </RouterLink>
          </li>
          <li class="nav-item" v-if="!isAdmin">
            <RouterLink to="/MyBooks" class="nav-link active" aria-current="page">
              <i :class="{'bi bi-book': !isActive('/MyBooks'), 'bi bi-book-fill': isActive('/MyBooks'), 'text-red': isActive('/MyBooks') }">My Books</i>
            </RouterLink>
          </li>
          <li class="nav-item" v-if="isAdmin">
            <RouterLink to="/MyBooks" class="nav-link active" aria-current="page">
              <i :class="{'bi bi-send-dash': !isActive('/MyBooks'), 'bi bi-send-dash-fill': isActive('/MyBooks'), 'text-red': isActive('/MyBooks') }">Status</i>
            </RouterLink>
          </li>
          <li class="nav-item position-relative" v-if="!isAdmin">
            <span class="nav-link active clickable" @click="toggleCart">
              <i :class="{'bi bi-cart': !isCartVisible, 'bi bi-cart-fill': isCartVisible, 'text-red': isCartVisible }">Cart</i>
            </span>
            <CartDropdown :isVisible="isCartVisible" :cartItems="cartItems" class="dropdown-menu" />
          </li>
          <li class="nav-item" v-if="isAdmin">
            <RouterLink to="/Dashboard" class="nav-link active" aria-current="page">
              <i :class="{'bi bi-database-dash': !isActive('/Dashboard'), 'bi bi-database-fill-check': isActive('/Dashboard'), 'text-red': isActive('/Dashboard') }">Dashboard</i>
            </RouterLink>
          </li>
          <li class="nav-item position-relative" v-if="!isAdmin">
            <span class="nav-link active clickable" @click="toggleWishlist">
              <i :class="{'bi bi-heart': !isWishlistVisible, 'bi bi-heart-fill': isWishlistVisible, 'text-red': isWishlistVisible }">Wishlist</i>
            </span>
            <WishlistDropdown :isVisible="isWishlistVisible" :wishlistItems="wishlistItems" class="dropdown-menu" />
          </li>
        </ul>
        <div>
          <span class="clickable" @click="logout">
            <i class="bi bi-box-arrow-right">Sign out</i>
          </span>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import WishlistDropdown from "@/components/WishlistContent.vue";
import CartDropdown from "@/components/CartContent.vue"; // Adjust the path accordingly

export default {
  components: {
    CartDropdown,
    WishlistDropdown,
  },
  data() {
    return {
      isCartVisible: false,
      isWishlistVisible: false,
    };
  },
  computed: {
    isAdmin() {
      return localStorage.getItem("isAdmin") === "true";
    },
    user() {
      return this.$store.getters["user/user"];
    },
    cartItems() {
     return this.$store.getters["cartitem/cartItems"]; 
     
    },
    wishlistItems() {
      return this.$store.getters["wishlist/wishItems"];
    },
  },
  methods: {
    resolvedImagePath(imagePath) {
      if (imagePath == null) {
        return require("@/assets/book_image/default.jpg");
      }
      return require(`@/assets/book_image/${imagePath}`);
    },
    async fetchUser() {
      const user_id = localStorage.getItem("user_id");
      await this.$store.dispatch("user/getUser", user_id);
    },
    logout() {
  this.$store.dispatch("user/logout");
  this.$router.push("/SignIn");
  
},

    toggleCart() {
      this.isCartVisible = !this.isCartVisible;
    },
    toggleWishlist() {
      this.isWishlistVisible = !this.isWishlistVisible;
    },
    isActive(route) {
      return this.$route.path === route;
    },
    async fetchCart() {
      await this.$store.dispatch("cartitem/loadCartWithBookDetails");
    },
    async fetchWishlist() {
      await this.$store.dispatch("wishlist/loadwishWithBookDetails");
    },
  },
  async created() {
    await this.fetchUser();
    await this.fetchCart();
    await this.fetchWishlist();
  },
};
</script>

<style scoped>
.navbar-custom {
  background: linear-gradient(90deg, #efc2cf, #b5cacd 52%, #edb294);
}
.navbar-nav .nav-link {
  color: black;
  font-weight: bold;
}
.navbar-nav .nav-link:hover {
  color: darkgray;
}
.icon {
  font-size: 1.5rem;
  margin-right: 15px;
  color: black;
}
.profile-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid white;
  background-color: #ff0000;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.2rem;
}
.profile-icon:hover,
.profile-icon.isActive {
  background-color: rgba(255, 0, 0, 0.748);
}
.clickable {
  cursor: pointer;
}
.text-red {
  color: rgba(255, 0, 0, 0.748) !important;
}
.profile-icon-active {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid rgb(227, 14, 14);
  background-color: #ff0000;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 1.2rem;
}
.relative {
  position: relative;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  background: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  width: 250px;
  display: none;
}
.nav-item.position-relative:hover .dropdown-menu,
.nav-item.position-relative .dropdown-menu-active {
  display: block;
}
</style>
