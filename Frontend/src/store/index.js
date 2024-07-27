import { createStore } from 'vuex';
import user from './modules/user';
import books from './modules/books'; 
import sections from './modules/sections';
import feedback from './modules/feedback';
import cartitem from './modules/cartitem';
import wishlist from './modules/wishlist';
import checkout from './modules/checkout';
import userLog from './modules/userLog';
import searchbook from './modules/searchbook';
import myorder from './modules/myorder';

export default createStore({
  modules: {
    user,
    books,
    sections,
    feedback,
    cartitem,
    wishlist,
    checkout,
    userLog,
    searchbook,
    myorder,
  },
});
