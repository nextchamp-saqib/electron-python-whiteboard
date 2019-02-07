<template>
  <div class="container">
    <div v-if="!showRect" class="initialize">
      <p>Initializing.....Please Wait</p>
    </div>
    <div v-if="showRect" class="rectangle">
      <!-- <div class="one"></div>
      <div class="two"></div>
      <div class='three'></div>
      <div class="four"></div> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'CalibrationScreen',
  data() {
    return {
      showRect: false
    }
  },
  mounted() {
    setTimeout(() => {
      this.showRect = true
      const zerorpc = require('zerorpc')
      const client = new zerorpc.Client()
      client.connect("tcp://127.0.0.1:1122")

      client.invoke("startCalibrating", (error, res) => {
        if(error) {
          this.showRect = false
          console.error(error)
        } else {
          this.showRect = false
          console.log(res)
        }
      })

      // client.invoke("printSomethingFunc", (error, res) => {
      //   if(error) {
      //     // this.showRect = false
      //     console.error(error)
      //   } else {
      //     // this.showRect = false
      //     console.log(res)
      //   }
      // })

    }, 3000)
  }
}
</script>

<style scoped>
.container {
  flex-direction: column;
  justify-content: center;
  background-color: #242424;
  height: 100%;
  display: flex;
  /* align-items: center; */
}

.initialize{
  display: flex;
  align-items: center;
  background-color: #ababab;
  border: 1px solid rgba(0,0,0,0.2);
  box-shadow: 0px 0px 20px rgba(0,0,0,0.6);
  border-radius: 4px;
  width: 20vw;
  height: 10vh;
  text-align: center;
  font-size: 1.5vw;
}

.initialize > p {
  width: 100%;
}

.rectangle{
  display: block;
  position: relative;
  border: 1vw solid #ababab;
  /* border-radius: 12px; */
  width: 20vw;
  height: 20vh;
  animation-delay: 2s; 
  animation-name: expand;
  animation-timing-function: ease-out;
  animation-duration: 2s;
  animation-iteration-count: 10;
  animation-direction: alternate;
}

.one{
  border-bottom-right-radius:100%;
  top: -2px;
  left: -2px;
  position: absolute;
  width: 3vw;
  height: 4vh;
  background-color: #ababab;
}
.two{
  border-bottom-left-radius:100%;
  right: -2px;
  top: -2px;
  position: absolute;
  width: 3vw;
  height: 4vh;
  background-color: #ababab;
}
.three{
  border-top-left-radius:100%;
  position: absolute;
  right: -2px;
  bottom: -2px;
  width: 3vw;
  height: 4vh;
  background-color: #ababab;
}
.four{
  border-top-right-radius:100%;
  position: absolute;
  left: -2px;
  bottom: -2px;
  width: 3vw;
  height: 4vh;
  background-color: #ababab;
}

@keyframes expand{
  from {
    width: 20vw;
    height: 20vh;
  }
  to{
    width: 98vw;
    height: 96vh;
  }
}
</style>


