<template>
  <div>
    <h1>User Info</h1>
    <p v-if="user">Username: {{ user.username }}</p>
    <p v-if="user">Email: {{ user.email }}</p> 
    <!-- <button @click="onLogout">Logout</button> -->
  </div>
</template>

<script>
import axios from 'axios';
import router from '@/router';
const route = router
export default {
  data() {
    return {
      user:null
    };
  },
  async mounted() {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const response = await axios.get('http://127.0.0.1:8000/users/me', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching user info:', error);
      }
    }
  }
};
</script>
