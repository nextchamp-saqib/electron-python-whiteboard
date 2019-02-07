<template>
    <div class="navbar">
        <el-popover
            placement="top"
            width="160"
            v-model="penMenuOpen">
            <el-slider class="slider" v-model="penWidth"  @input="setPenWidth"></el-slider>
            <el-button slot="reference" @dblclick="showPenMenu" @click="select('pen')"><i class="fas fa-pen"></i></el-button>
        </el-popover>
        <el-popover
            placement="top"
            width="160"
            v-model="eraserMenuOpen">
            <el-slider class="slider" v-model="eraserWidth" @input="setEraserWidth"></el-slider>
            <el-button slot="reference" @dblclick="showEraserMenu" @click="select('eraser')"><i class="fas fa-eraser"></i></el-button>
        </el-popover>
        <el-popover
            placement="top"
            width="160"
            v-model="rectMenuOpen">
            <el-slider class="slider" v-model="rectWidth" @input="setRectWidth"></el-slider>
            <el-button slot="reference" @dblclick="showRectMenu" @click="select('rect')"><i class="fas fa-square"></i></el-button>
        </el-popover>
        <el-popover
            placement="top"
            width="160"
            v-model="circleMenuOpen">
            <el-slider class="slider" v-model="circleWidth" @input="setCircleWidth"></el-slider>
            <el-button slot="reference" @dblclick="showCircleMenu" @click="select('circle')"><i class="fas fa-circle"></i></el-button>
        </el-popover>
    </div>
</template>

<script>
export default {
  name: 'nav-bar',
  data () {
    return {
      penMenuOpen: false,
      penWidth: 50,
      eraserMenuOpen: false,
      eraserWidth: 50,
      rectMenuOpen: false,
      rectWidth: 50,
      circleMenuOpen: false,
      circleWidth: 50
    }
  },
  methods: {
    showPenMenu () {
    },
    showEraserMenu () {
    },
    showRectMenu () {
    },
    showCircleMenu () {
    },
    setPenWidth () {
      this.$root.$emit('penWidth', parseInt(this.penWidth / 10))
    },
    setEraserWidth () {
      this.$root.$emit('eraserWidth', parseInt(this.eraserWidth / 10))
    },
    setRectWidth () {
      this.$root.$emit('rectWidth', parseInt(this.rectWidth / 10))
    },
    setCircleWidth () {
      this.$root.$emit('circleWidth', parseInt(this.circleWidth / 10))
    },
    select (pointer) {
      this.$root.$emit('selectedPointer', pointer)
    }
  }
}
</script>

<style scoped>
.navbar {
    z-index: 10;
    position: fixed;
    display: flex;
    flex-direction: row;
    bottom: 0%;
    left: 25%;
    width: 50%;
    height: 50px;
    margin: 0% auto;
    background-color: #2D509F;
    padding: 0px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
}
span{
    align-self: center;
    height: 50px;
}
.el-button{
    background: none;
    height: 100%;
    color: aliceblue;
    border: none;
}
.el-button:hover{
    background-color: aliceblue;
    color: #2D509F;
    box-shadow: none;
    border-radius: 0;
}
</style>
