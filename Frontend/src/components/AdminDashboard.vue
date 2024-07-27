<template>
  <div class="container">
    <div class="card header">
      <h1>Admin Dashboard</h1>
      <button class="btn btn-outline-primary" @click="getReport">Export</button>
    </div>
    <div class="card summary-card total-sales">
      <div>${{ Total_Revenue }}</div>
      <div>Total Revenue</div>
    </div>
    <div class="card summary-card total-order">
      <div>{{ Total_Request }}</div>
      <div>Total Request</div>
    </div>
    <div class="card summary-card product-sold">
      <div>{{ Active_Users }}</div>
      <div>Total Active User</div>
    </div>

    <div class="card">
      <h2>Visitor Insights</h2>
      <img
        src="@/assets/admin/active_non_active_users.png"
        alt="Visitor Insights"
      />
    </div>
    <div class="card">
      <h2>Total Revenue</h2>
      <img src="@/assets/admin/total_revenue.png" alt="Total Revenue" />
    </div>
    <div class="card">
      <h2>Customer Satisfaction</h2>
      <img
        src="@/assets/admin/customer_satisfaction.png"
        alt="Customer Satisfaction"
      />
    </div>

    <div class="card">
      <h2>Top Products</h2>
      <img src="@/assets/admin/top_rated_books.png" alt="Top Products" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      Total_Revenue: 0,
      Total_Request: 0,
      Active_Users: 0,
    };
  },
  methods: {
    getStats() {
      // get stats
      const token = localStorage.getItem("accessToken");
      if (token) {
        const fetchUrl = "http://127.0.0.1:5000/admin/dashboard";
        const requestOptions = {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };

        fetch(fetchUrl, requestOptions).then((response) => {
          response
            .json()
            .then((data) => {
              this.Total_Revenue = data.total_revenue;
              this.Total_Request = data.total_requests;
              this.Active_Users = data.active_users;
            })
            .catch((error) => {
              console.log(error);
            });
        });
      }
    },
    getReport() {
      // get report
      const token = localStorage.getItem("accessToken");
      if (token) {
        const fetchUrl = "http://127.0.0.1:5000/generate_report";
        const requestOptions = {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        };

        fetch(fetchUrl, requestOptions).then((response) => {
          response
            .json()
            .then((data) => {
              const task_id = data.task_id;
              console.log(task_id);
              const interval = setInterval(async () => {
              const fetchUrl = `http://127.0.0.1:5000/generate_report/${task_id}`;
              const csv_res = await fetch(fetchUrl, requestOptions);
              if (csv_res.ok) {
                clearInterval(interval);
                window.location.href = `http://127.0.0.1:5000/generate_report/${task_id}`;
                this.task_id = null;
              }
              }, 1000);
            })
            .catch((error) => {
              console.log(error);
            });
        });
      }
    },
  },
  mounted() {
    this.getStats();
  },
};
</script>

<style scoped>
* {
  padding: 0;
}
body {
  background-color: #f8f9fd;
  padding: 20px;
}
.container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}
.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: calc(33.33% - 20px);
  min-width: 250px;
}
.card img {
  width: 100%;
  border-radius: 10px;
}
.card.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}
.summary-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.summary-card div {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.summary-card.total-sales {
  background-color: #ffe7e7;
}
.summary-card.total-order {
  background-color: #fff4e1;
}
.summary-card.product-sold {
  background-color: #edfff2;
}
.summary-card div:first-child {
  font-size: 1.5em;
  font-weight: bold;
}
.summary-card div:last-child {
  color: grey;
  font-size: 0.9em;
}
</style>
