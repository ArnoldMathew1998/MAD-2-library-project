<template>
    <div>
      <table class="table">
        <thead class="table-secondary">
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Description</th>
            <th scope="col">CREATED DATE</th>

            <th scope="col">View</th>
            <th v-if="isAdmin" scope="col">Edit</th>
            <th v-if="isAdmin" scope="col">Delete</th>
          </tr>
        </thead>
    
        <tbody v-if="sections.length > 0">
            <tr v-for="(section, index) in sections" :key="section.sec_id" :class="{ 'table-secondary': index % 2 === 1 }">
            <th scope="row">{{ index+1 }}</th>
            <td>{{ section.sec_name }}</td>
            <td>{{ section.description }}</td>
            <td>
              <div class="date-time">
                <span class="date">{{ formatDate(section.date_created) }}</span>
                <span class="time">{{ formatTime(section.date_created) }}</span>
              </div>
            </td>
           <td class="link-info link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable" @click="viewSection(section.sec_id)">Click</td>
           <td v-if="isAdmin" class="link-warning link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable" @click="editSection(section, index)">Edit</td>
            <td v-if="isAdmin" class="link-danger link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover clickable" @click="confirmDeleteSection(section.sec_id)">Delete</td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="isAdmin" class="text-end mt-3">
        <button class="btn btn-primary" @click="showAddSectionModal = true">+ Add New Section</button>
      </div>
      
      <div v-if="showAddSectionModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="CloseAddSection()">&times;</span>
          <h2>Add New Section</h2>
          <form form @submit.prevent="newSection.sec_id ? updateSection() : addNewSection()">
            <div class="form-group">
              <label for="sec_name">Section Name</label>
              <input type="text" id="sec_name" v-model="newSection.sec_name" required>
            </div>
            <div class="form-group">
              <label for="description">Description</label>
              <input type="text" id="description" v-model="newSection.description" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sections:[],
        searchQuery: '',
        isAdmin: false,
        showAddSectionModal: false,
        currentSectionIndex: null,
        newSection: {
            sec_id:'',
            sec_name: '',
            description: ''
        }
      };
    },

    methods: {
        CloseAddSection(){
            this.showAddSectionModal=false;
            this.newSection.sec_id='';
            this.newSection.sec_name='';
            this.newSection.description='';
            this.currentSectionIndex = null;

        },
      async fetchSections() {
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
                    this.sections = data;
                }
            })
            .catch(error => {
                console.error("There was an error fetching the books!", error);
                alert(error);
            });
            
        }
        },
      async fetchUserRole() {
        const token = localStorage.getItem('accessToken');
        if (token) {
          const roleUrl = 'http://127.0.0.1:5000/Api/user/role';
          const requestOptions = {
            method: 'GET',
            headers: { 
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          };
          
          await fetch(roleUrl, requestOptions)
            .then(async response => response.json())
            .then(data =>{ 
                if (data.role=="admin"){
                    this.isAdmin=true;
                }})
            .catch(error => {
            console.error("There was an error fetching the user role!", error);
            alert(error);
            });
        }
        },
      async addNewSection() { 
        const token = localStorage.getItem('accessToken');
        if (token) {
          const sectionUrl = 'http://127.0.0.1:5000/Api/Section';
          const requestOptions = {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(this.newSection)
          };
          
          await fetch(sectionUrl, requestOptions)
          .then(async response => response.json())
          .then(data => {
            console.log(data)
            this.sections.push(data);
            
            this.showAddSectionModal = false;
            
            this.newSection.sec_name = '';
            this.newSection.description = '';
          })
          .catch(error => {
            console.error("There was an error creating the new section!", error);
            alert(error);
            });
            }
        },
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
        },
      formatTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleTimeString();
        },
      viewSection(sec_id) {
        this.$router.push({ name: 'Book', params: { section_id: sec_id } });
        },

        async editSection(section,index) {
        // Populate form with existing section details
        this.newSection.sec_id = section.sec_id;
        this.newSection.sec_name = section.sec_name;
        this.newSection.description = section.description;
        this.currentSectionIndex = index;
        // Show the modal for editing
        this.showAddSectionModal = true;
        },

        async updateSection() {
            const token = localStorage.getItem('accessToken');
            if (token) {
                const sectionUrl = `http://127.0.0.1:5000/Api/Section/${this.newSection.sec_id}`;
                const requestOptions = {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    sec_name: this.newSection.sec_name,
                    description: this.newSection.description
                })
                };

                await fetch(sectionUrl, requestOptions)
                .then(response => response.json())
                .then(updatedSection => {
                    
                    this.sections.splice(this.currentSectionIndex, 1, updatedSection);
                    this.CloseAddSection();
                })
                .catch(error => {
                    console.error("There was an error updating the section!", error);
                    alert(error);
                });
            }
            },
      confirmDeleteSection(sec_id) {
        if (confirm("Are you sure you want to delete this section?")) {
            this.deleteSection(sec_id);
        }
        },

    async deleteSection(sec_id) {
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
                .then(() => this.sections = this.sections.filter(section => section.sec_id !== sec_id))
                .catch(error => {
                console.error("There was an error deleting the section!", error);
                alert(error);
                });
    }
  }
    },
    async mounted() {
      await this.fetchSections();
      await this.fetchUserRole();
    }
  };
  </script>
  
  <style scoped>
  .input-group>.form-control {
    width: 20rem; /* Adjust width as needed */
  }
  .date-time {
    display: flex;
    flex-direction: column;
  }
  .date-time .time {
    font-size: 0.85em;
    color: gray;
  }
  .modal {
    display: block; /* Show the modal */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
  }
  
  .modal-content {
    background-color: #fefefe;
    margin: 15% auto; /* 15% from the top and centered */
    padding: 20px;
    border: 1px solid #888;
    width: 80%; /* Could be more or less, depending on screen size */
  }
  
  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
.clickable {
  cursor: pointer;
}
  </style>
  