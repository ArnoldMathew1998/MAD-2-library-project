const state = {
    checkoutItems: [],
};

const mutations = {
  addCheckoutItem(state, checkoutItem) {
    state.checkoutItems=checkoutItem;
  },
};  

const actions = {
  addCheckoutItem({ commit }, checkoutItem) {
    commit("addCheckoutItem", checkoutItem);
  },
};  

const getters = {
  checkoutItems: (state) => state.checkoutItems,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};