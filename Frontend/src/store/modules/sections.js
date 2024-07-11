
const state = {
    sections: [],
   
  };
  
  const mutations = {
    setSections(state, sections) {
      state.sections = sections;
    },
    addSection(state, section) {
      state.sections.push(section);
    },
    updateSection(state, updatedSection) {
      const index = state.sections.findIndex(section => section.sec_id === updatedSection.sec_id);
      if (index !== -1) {
        state.sections.splice(index, 1, updatedSection);
      }
    },
    deleteSection(state, sec_id) {
      state.sections = state.sections.filter(section => section.sec_id !== sec_id);
    },
   
  };
  
  const actions = {
    async fetchSections({ commit }) {
      const token = localStorage.getItem('accessToken');
      if (token) {
        const roleUrl = 'http://127.0.0.1:5000/Api/Section';
        const requestOptions = {
          method: 'GET',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        };
  
        await fetch(roleUrl, requestOptions)
        .then(async response => {
            if (response.status === 404) {
              console.log("Resource not found");
                this.sections = []; 
            }
            else {
                const data = await response.json();
                commit('setSections', data);
            }
        })
        .catch(error => {
            console.error("There was an error fetching the books!", error);
            alert(error);
        });
      }
    },
    
    async addNewSection({ commit }, newSection) {
      const token = localStorage.getItem('accessToken');
      if (token) {
        const sectionUrl = 'http://127.0.0.1:5000/Api/Section';
        const requestOptions = {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(newSection)
        };

        await fetch(sectionUrl, requestOptions)
          .then(async response => response.json())
          .then(data => {
            commit('addSection', data);
          })
          .catch(error => {
            console.error("There was an error creating the new section!", error);
            alert(error);
            });
      }
    },
    async updateSection({ commit }, section) {
      const token = localStorage.getItem('accessToken');
      if (token) {
        const sectionUrl = `http://127.0.0.1:5000/Api/Section/${section.sec_id}`;
        const requestOptions = {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            sec_name: section.sec_name,
            description: section.description
          })
        };
  
       

        await fetch(sectionUrl, requestOptions)
                .then(response => response.json())
                .then(updatedSection => {
                    
                    commit('updateSection', updatedSection);
                })
                .catch(error => {
                    console.error("There was an error updating the section!", error);
                    alert(error);
                });
      }
    },
    async deleteSection({ commit }, sec_id) {
      const token = localStorage.getItem('accessToken');
      if (token) {
        const sectionUrl = `http://127.0.0.1:5000/Api/Section/${sec_id}`;
        const requestOptions = {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        };
  

        await fetch(sectionUrl, requestOptions)
        .then(commit('deleteSection', sec_id))
        .catch(error => {
        console.error("There was an error deleting the section!", error);
        alert(error);
        });
      }
    },
  };
  
  const getters = {
    allSections: (state) => state.sections,
    /* isAdmin: (state) => state.isAdmin, */
  };
  
  export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
  };
  