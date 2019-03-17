<template>
  <div class="container">
    <div v-if="!showRect" class="initialize">
      <p>Initializing.....Please Wait</p>
    </div>
    <div v-if="showRect" class="rectangle">
      <!-- <div class="one"></div>
      <div class="two"></div>
      <div class='three'></div>
      <div class="four"></div>-->
    </div>
  </div>
</template>

<script>
export default {
  name: "CalibrationScreen",
  data() {
    return {
      showRect: false
    };
  },
  mounted() {
    setTimeout(() => {
      this.showRect = true;
      const zerorpc = require("zerorpc");
      const client = new zerorpc.Client({
        timeout: 10000,
        heartbeatInterval: 300000
      });

      client.connect("tcp://127.0.0.1:1122");

      client.invoke("startCalibrating", (error, res) => {
        if (error) {
          this.showRect = false;
          console.error(error);
          client.close();
        } else {
          this.showRect = false;
          this.$router.replace({ name: "new-screen" });
          console.log(res);
          client.invoke("listenForIR", (error, res) => {
            if (error) {
              console.error(error);
            } else {
              console.log(res);
              client.close();
            }
          });
        }
      });
    }, 3000);
  }
};
</script>

<style scoped>
.container {
  flex-direction: column;
  justify-content: center;
  /* background-color: #ccc; */
  background-color: #242424;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
}

.initialize {
  display: flex;
  align-items: center;
  /* background-color: #242424; */
  background-color: #ccc;

  border: 1px solid rgba(0, 0, 0, 0.2);
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.6);
  border-radius: 4px;
  width: 20vw;
  height: 10vh;
  text-align: center;
  font-size: 1.5vw;
  color: #ccc;
}

.initialize > p {
  width: 100%;
}

.rectangle {
  display: block;
  position: relative;
  border: 1vw solid #242424;
  /* border-radius: 12px; */
  border: 1vw solid #ccc;
  width: 20vw;
  height: 20vh;
  animation-delay: 2s;
  animation-name: expand;
  animation-timing-function: ease-out;
  animation-duration: 2s;
  animation-iteration-count: 10;
  animation-direction: alternate;
}

@keyframes expand {
  from {
    width: 20vw;
    height: 20vh;
  }
  to {
    /* width: 98vw;
    height: 96vh; */
    width: 96vw;
    height: 94vh;
  }
}
</style>


