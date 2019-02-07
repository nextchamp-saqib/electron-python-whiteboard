<template>
  <div id="wrapper">
    <h1 class="main-title">Interactive Board</h1>
    <div class="divider" />
    <div class="calibration-screen">
      <img src="../../python/frame.jpg" alt="" srcset="" width="180px">
    </div>
    <div>
      <el-button @click="calibrate">Calibrate Screen</el-button>
    </div>
    <div>
      <el-button @click="newScreen">&nbsp;Drawing Board &nbsp;</el-button>
    </div>
    <div class="divider" />
  </div>
</template>

<script>
export default {
  name: 'landing-page',
  methods: {
    calibrate () {
      this.$router.push(`/calibration`)
    },
    newScreen () {
      this.$router.push(`/new`)
    }
  }
}
</script>

<style scoped>
#wrapper{
  margin-left: auto;
  margin-right: auto;
  padding: 0.5rem;
  width: 25vw;
  text-align: center;
  box-shadow: 0px 0px 20px rgba(0,0,0,0.6);
  background-color: #ababab;
}

.divider{
  margin: 1rem auto;
  width: 90%;
  border-bottom: 1px solid rgba(0,0,0,0.1);
  border-color: #efefef;
}

.calibration-screen{
  width: 180px;
  height: 180px;
  margin: 1rem auto;
  border: 1px solid rgba(0,0,0,0.2);
  box-shadow: 0px 0px 5px rgba(0,0,0,0.1);
  background-color: #efefef;
}

div > .el-button {
  margin-bottom: 12px;
}
</style>

