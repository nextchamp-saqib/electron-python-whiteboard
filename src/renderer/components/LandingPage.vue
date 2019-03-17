<template>
  <div id="wrapper">
    <h1 class="main-title">Interactive Board</h1>Live Snapshot:
    <div class="divider"/>
    <div class="calibration-screen">
      <img src="../../python/liveImage.jpg" alt srcset width="180px">
    </div>
    <div class="divider"/>Calibrated Snapshot:
    <div class="calibration-screen">
      <img src="../../python/wrapedImage.jpg" alt srcset width="180px">
    </div>
    <div class="divider"/>
    <div class="ip-input">
      <el-input placeholder="Enter IP Address" v-model="ipAddr" suffix-icon="el-icon-arrow-right"></el-input>
    </div>
    <div>
      <el-button @click="calibrate">Calibrate Screen</el-button>
    </div>
    <div>
      <el-button @click="newScreen">&nbsp;Drawing Board &nbsp;</el-button>
    </div>
    <div class="divider"/>
  </div>
</template>

<script>
export default {
  name: "landing-page",
  data() {
    return {
      ipAddr: "192.168.2.111"
    };
  },
  mounted() {
    document
      .getElementsByClassName("el-input__suffix")[0]
      .addEventListener("click", () => {
        this.sendIp();
      });
  },
  methods: {
    calibrate() {
      this.$router.push(`/calibration`);
    },
    newScreen() {
      this.$router.push(`/new`);
    },
    sendIp() {
      console.log("asd");
      const zerorpc = require("zerorpc");
      const client = new zerorpc.Client({
        timeout: 10000,
        heartbeatInterval: 300000
      });

      client.connect("tcp://127.0.0.1:1122");

      client.invoke("setIpAddress", this.ipAddr, (error, res) => {
        if (error) {
          // console.error(error);
          alert(error);
          client.close();
        } else {
          // console.error(res);
          alert(res);
          client.close();
        }
      });
    }
  }
};
</script>

<style scoped>
#wrapper {
  margin-left: auto;
  margin-right: auto;
  padding: 0.5rem;
  width: 25vw;
  text-align: center;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.6);
  background-color: #242424;
  color: #ccc;
}

.divider {
  margin: 0.7rem auto;
  width: 90%;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  border-color: #efefef;
}

.calibration-screen {
  width: 180px;
  height: 90px;
  margin: 1rem auto;
  margin-bottom: 2rem;
  /* border: 1px solid rgba(0,0,0,0.2); */
  /* box-shadow: 0px 0px 5px rgba(0,0,0,0.1); */
  background-color: #242424;
  color: #ccc;
}

div > .el-button {
  margin: 6px auto;
}
.ip-input {
  width: 155px;
  margin: 4px auto;
}
</style>

