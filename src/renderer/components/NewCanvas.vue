<template>
  <div class="canvas-container">
    <canvas id="board" ref="board"></canvas>
  </div>
</template>

<script>
import { fabric } from 'fabric'

// todo: change canvas size according to window

export default {
  name: 'new-canvas',
  data () {
    return {
      mouseDown: false,
      canvas: null,
      eraserWidth: 5 + 15,
      canvasColor: "#242424",
      penWidth: 5,
      penColor: "#ababab",
      selectedPointer: 'pen',
      rectangles: [],
      ellipses: []
    }
  },
  mounted () {
    this.canvas = new fabric.Canvas('board', {
      backgroundColor: this.canvasColor,
      selection: false
    })
    this.canvas.setWidth(window.innerWidth)
    this.canvas.setHeight(window.innerHeight)
    this.$root.$on('eraserWidth', data => {
      this.eraserWidth = data + 5
      this.canvas.freeDrawingBrush.width = this.eraserWidth
    })
    this.$root.$on('penWidth', data => {
      this.penWidth = data
      this.canvas.freeDrawingBrush.width = this.penWidth
    })
    this.$root.$on('selectedPointer', data => {
      if (data === 'pen') {
        this.canvas.isDrawingMode = true
        this.canvas.freeDrawingBrush.color = this.penColor
        this.canvas.freeDrawingBrush.width = this.penWidth
      }
      if (data === 'eraser') {
        this.canvas.isDrawingMode = true
        this.canvas.freeDrawingBrush.color = this.canvasColor
        this.canvas.freeDrawingBrush.width = this.eraserWidth
      }
      if (data === 'rect') {
        this.canvas.isDrawingMode = false
      }
      if (data === 'circle') {
        this.canvas.isDrawingMode = false
      }
      this.selectedPointer = data
    })
    this.canvas.on('mouse:down', (e) => {
      this.mouseDown = true
      if (this.selectedPointer === 'rect') {
        this.rectangleHandler().down(e.pointer.x, e.pointer.y)
      }
      if (this.selectedPointer === 'circle') {
        this.ellipseHandler().down(e.pointer.x, e.pointer.y)
      }
    })
    this.canvas.on('mouse:move', (e) => {
      if (this.selectedPointer === 'rect' && this.mouseDown) {
        this.rectangleHandler().drag(e.pointer.x, e.pointer.y)
      }
      if (this.selectedPointer === 'circle' && this.mouseDown) {
        this.ellipseHandler().drag(e.pointer.x, e.pointer.y)
      }
    })
    this.canvas.on('mouse:up', (e) => {
      this.mouseDown = false
      this.canvas.forEachObject((o) => {
        o.selectable = false
      })
      if (this.selectedPointer === 'rect') {
        this.rectangleHandler().up()
      }
      if (this.selectedPointer === 'circle') {
        this.ellipseHandler().up()
      }
    })
  },
  methods: {
    ellipseHandler () {
      return {
        down: (x, y) => {
          const newEllipse = new fabric.Ellipse({
            left: x,
            top: y,
            originX: 'left',
            originY: 'top',
            rx: x,
            ry: y,
            angle: 0,
            fill: 'transparent',
            stroke: this.penColor,
            strokeWidth: this.penWidth,
            type: 'ellipse'
          })
          this.ellipses.push({
            ref: newEllipse,
            origin: {
              'x': x,
              'y': y
            }
          })
          this.canvas.add(newEllipse)
          this.canvas.renderAll()
        },
        drag: (x, y) => {
          const actEllipse = this.ellipses[this.ellipses.length - 1]
          let rx = Math.abs(actEllipse.origin.x - x) / 2
          let ry = Math.abs(actEllipse.origin.y - y) / 2
          if (rx > actEllipse.ref.strokeWidth) {
            rx -= actEllipse.ref.strokeWidth / 2
          }
          if (ry > actEllipse.ref.strokeWidth) {
            ry -= actEllipse.ref.strokeWidth / 2
          }

          actEllipse.ref.set({ rx: rx, ry: ry })

          if (actEllipse.origin.x > x) {
            actEllipse.ref.set({ originX: 'right' })
          } else {
            actEllipse.ref.set({ originX: 'left' })
          }
          if (actEllipse.origin.y > y) {
            actEllipse.ref.set({ originY: 'bottom' })
          } else {
            actEllipse.ref.set({ originY: 'top' })
          }
          this.canvas.renderAll()
        },
        up: () => {
        }
      }
    },
    rectangleHandler () {
      return {
        down: (x, y) => {
          const newRectangle = new fabric.Rect({
            left: x,
            top: y,
            width: 0,
            height: 0,
            stroke: this.penColor,
            strokeWidth: this.penWidth,
            fill: 'transparent'
          })
          this.rectangles.push({
            ref: newRectangle,
            origin: {
              'x': x,
              'y': y
            }
          })
          this.canvas.add(newRectangle)
          this.canvas.renderAll()
        },
        drag: (x, y) => {
          const actRect = this.rectangles[this.rectangles.length - 1]
          if (actRect.origin.x > x) {
            actRect.ref.set({ left: Math.abs(x) })
          }
          if (actRect.origin.y > y) {
            actRect.ref.set({ top: Math.abs(y) })
          }
          actRect.ref.set({ width: Math.abs(actRect.origin.x - x) })
          actRect.ref.set({ height: Math.abs(actRect.origin.y - y) })
          this.canvas.renderAll()
        },
        up: () => {
        }
      }
    }
  }
}
</script>

<style scoped>
.canvas-container{
  display: flex;
  align-items: center;
}

canvas{
    width: 100vw;
    height: 100vh; 
    margin: 0px;
}
</style>
