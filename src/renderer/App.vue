<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'white-board'
  }
</script>

<style>
@import '~@fortawesome/fontawesome-free/css/all.min.css';

body{
  font-family: 'Catamaran', sans-serif;
  padding: 0;
  margin: 0;
  overflow: hidden;
  height: 100vh;
  background-color: #ccc;
}

#app {
  height: 100%;
  display: flex;
  align-items: center;
}
</style>
