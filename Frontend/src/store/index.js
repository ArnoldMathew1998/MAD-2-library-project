// src/store/index.js
import { createStore } from 'vuex';
import user from './modules/user';
import books from './modules/books'; 
import sections from './modules/sections';
import feedback from './modules/feedback';

export default createStore({
  modules: {
    user,
    books,
    sections,
    feedback,
  },
});
