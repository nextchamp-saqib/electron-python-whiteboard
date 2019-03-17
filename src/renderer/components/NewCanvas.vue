<template>
  <div class="my-canvas-container">
    <div class="firsthalf">
      <el-button class="right" :class="{'disable': plusD}" @click="newPage">
        <i
          class="fas"
          :class="{'fa-plus': pageNo == pages.length, 'fa-arrow-right': pageNo != pages.length}"
        ></i>
      </el-button>
      <el-button v-if="pages.length > 1" class="left" @click="prevPage(pageNo - 1 , pageNo)">
        <i class="fas fa-arrow-left"></i>
      </el-button>
      <div class="tabs">
        <div
          v-for="index in pages.length"
          :key="index"
          class="tab"
          :class="{'active': pageNo === index}"
          @click="prevPage(index, pageNo)"
        >{{index}}</div>
      </div>
      <canvas id="board" ref="board"></canvas>
    </div>
  </div>
</template>

<script>
import { fabric } from "fabric";
import jsPdf from "jspdf";

// todo: change canvas size according to window

export default {
  name: "new-canvas",
  data() {
    return {
      pageNo: 1,
      mouseDown: false,
      canvas: null,
      pages: [],
      eraserWidth: 5 + 15,
      canvasColor: "#242424",
      // canvasColor: "#ccc",
      penWidth: 5,
      // penColor: "#242424",
      penColor: "#ccc",
      selectedPointer: "pen",
      rectangles: [],
      ellipses: [],
      undoed: [],
      plusD: false
    };
  },
  async mounted() {
    await this.initializeBoard("board");
    this.$root.$emit("selectedPointer", "pen");
  },
  methods: {
    async initializeBoard(boardID) {
      let newCanvas = new fabric.Canvas(boardID, {
        backgroundColor: this.canvasColor,
        selection: false
      });
      this.canvas = newCanvas;
      // this.canvas.setWidth(window.innerWidth);
      // this.canvas.setHeight(window.innerHeight);
      this.canvas.setWidth(794);
      this.canvas.setHeight(561);
      this.pages.push(this.canvas._objects);
      this.$root.$on("eraserWidth", data => {
        this.eraserWidth = data + 5;
        this.canvas.freeDrawingBrush.width = this.eraserWidth;
      });
      this.$root.$on("penWidth", data => {
        this.penWidth = data;
        this.canvas.freeDrawingBrush.width = this.penWidth;
      });
      this.$root.$on("selectedPointer", data => {
        if (data === "pen") {
          this.canvas.isDrawingMode = true;
          this.canvas.freeDrawingBrush.color = this.penColor;
          this.canvas.freeDrawingBrush.width = this.penWidth;
        }
        if (data === "eraser") {
          this.canvas.isDrawingMode = true;
          this.canvas.freeDrawingBrush.color = this.canvasColor;
          this.canvas.freeDrawingBrush.width = this.eraserWidth;
        }
        if (data === "rect") {
          this.canvas.isDrawingMode = false;
        }
        if (data === "circle") {
          this.canvas.isDrawingMode = false;
        }
        if (data === "undo") {
          if (this.canvas._objects.length) {
            this.undoed.push(this.canvas._objects.pop());
            this.canvas.renderAll();
          }
        }
        if (data === "redo") {
          if (this.undoed.length) {
            this.canvas._objects.push(this.undoed.pop());
            this.canvas.renderAll();
          }
        }
        if (data === "clear") {
          this.canvas._objects = [];
          this.canvas.renderAll();
        }
        if (data === "save") {
          let images = [];
          let pdf = new jsPdf();
          this.canvas.isDrawingMode = false;
          let finalCanvas = this.$refs[boardID];
          this.pages[this.pageNo - 1] = this.canvas._objects;
          for (let i = 0; i < this.pages.length; i++) {
            this.canvas._objects = this.pages[i];
            this.canvas.backgroundColor = "#fff";
            this.canvas.renderAll();
            images.push(finalCanvas.toDataURL("image/jpeg", 1.0));
          }
          this.canvas.backgroundColor = this.canvasColor;
          this.canvas._objects = this.pages[this.pageNo - 1];
          this.canvas.renderAll();
          for (let i = 0; i < images.length; i++) {
            if (i % 2 === 0) {
              pdf.addImage(images[i], "JPEG", 0, 0);
            } else if (i % 2 === 1) {
              pdf.addImage(images[i], "JPEG", 0, 148.5);
              pdf.save("test" + i + ".pdf");
              pdf = new jsPdf();
            }
            if (i + 1 === images.length && i % 2 === 0) {
              pdf.save("test" + i + ".pdf");
              pdf = new jsPdf();
            }
          }
        }
        this.selectedPointer = data;
      });
      this.canvas.on("mouse:down", e => {
        this.mouseDown = true;
        if (this.selectedPointer === "rect") {
          this.rectangleHandler().down(e.pointer.x, e.pointer.y);
        }
        if (this.selectedPointer === "circle") {
          this.ellipseHandler().down(e.pointer.x, e.pointer.y);
        }
      });
      this.canvas.on("mouse:move", e => {
        if (this.selectedPointer === "rect" && this.mouseDown) {
          this.rectangleHandler().drag(e.pointer.x, e.pointer.y);
        }
        if (this.selectedPointer === "circle" && this.mouseDown) {
          this.ellipseHandler().drag(e.pointer.x, e.pointer.y);
        }
      });
      this.canvas.on("mouse:up", e => {
        this.mouseDown = false;
        this.canvas.forEachObject(o => {
          o.selectable = false;
        });
        if (this.selectedPointer === "rect") {
          this.rectangleHandler().up();
        }
        if (this.selectedPointer === "circle") {
          this.ellipseHandler().up();
        }
      });
    },
    newPage() {

      if (this.canvas._objects.length && this.pageNo === this.pages.length) {
        this.pages.push(this.canvas._objects);
        this.canvas._objects = [];
        this.canvas.renderAll();
        this.pageNo++;
      } else {
        this.prevPage(this.pageNo + 1, this.pageNo);
      }
    },
    prevPage(to, from) {
      this.pageNo = to;
      this.pages[from - 1] = this.canvas._objects;
      this.canvas._objects = this.pages[to - 1];
      this.canvas.renderAll();
    },
    ellipseHandler() {
      return {
        down: (x, y) => {
          const newEllipse = new fabric.Ellipse({
            left: x,
            top: y,
            originX: "left",
            originY: "top",
            rx: x,
            ry: y,
            angle: 0,
            fill: "transparent",
            stroke: this.penColor,
            strokeWidth: this.penWidth,
            type: "ellipse"
          });
          this.ellipses.push({
            ref: newEllipse,
            origin: {
              x: x,
              y: y
            }
          });
          this.canvas.add(newEllipse);
          this.canvas.renderAll();
        },
        drag: (x, y) => {
          const actEllipse = this.ellipses[this.ellipses.length - 1];
          let rx = Math.abs(actEllipse.origin.x - x) / 2;
          let ry = Math.abs(actEllipse.origin.y - y) / 2;
          if (rx > actEllipse.ref.strokeWidth) {
            rx -= actEllipse.ref.strokeWidth / 2;
          }
          if (ry > actEllipse.ref.strokeWidth) {
            ry -= actEllipse.ref.strokeWidth / 2;
          }

          actEllipse.ref.set({ rx: rx, ry: ry });

          if (actEllipse.origin.x > x) {
            actEllipse.ref.set({ originX: "right" });
          } else {
            actEllipse.ref.set({ originX: "left" });
          }
          if (actEllipse.origin.y > y) {
            actEllipse.ref.set({ originY: "bottom" });
          } else {
            actEllipse.ref.set({ originY: "top" });
          }
          this.canvas.renderAll();
        },
        up: () => {}
      };
    },
    rectangleHandler() {
      return {
        down: (x, y) => {
          const newRectangle = new fabric.Rect({
            left: x,
            top: y,
            width: 0,
            height: 0,
            stroke: this.penColor,
            strokeWidth: this.penWidth,
            fill: "transparent"
          });
          this.rectangles.push({
            ref: newRectangle,
            origin: {
              x: x,
              y: y
            }
          });
          this.canvas.add(newRectangle);
          this.canvas.renderAll();
        },
        drag: (x, y) => {
          const actRect = this.rectangles[this.rectangles.length - 1];
          if (actRect.origin.x > x) {
            actRect.ref.set({ left: Math.abs(x) });
          }
          if (actRect.origin.y > y) {
            actRect.ref.set({ top: Math.abs(y) });
          }
          actRect.ref.set({ width: Math.abs(actRect.origin.x - x) });
          actRect.ref.set({ height: Math.abs(actRect.origin.y - y) });
          this.canvas.renderAll();
        },
        up: () => {}
      };
    }
  }
};
</script>

<style scoped>
.my-canvas-container {
  display: flex;
  align-items: center;
  width: 100vw !important;
}

.firsthalf {
  width: 21cm !important;
  height: 14.85cm !important;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}

canvas {
  width: 21cm !important;
  height: 14.85cm !important;
}
.el-button {
  position: absolute;
  z-index: 15;
  margin: 0;
  box-shadow: 0px 0px 0px black;
  border-radius: 0;
  top: 50%;
  color: #fff;
  font-weight: bolder;
  background-color: #242424;
  transform: translateY(-50%);
}
.el-button.right {
  right: -63px;
}
.el-button.left {
  left: -62px;
}
.tabs {
  position: absolute;
  z-index: 16;
  top: -35px;
  display: flex;
}
.tab {
  background-color: #242424;
  padding: 4px 12px;
  border-right: 3px solid #ccc;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
  cursor: pointer;
  color: #fff;
  font-weight: bolder;
}
.tab:hover {
  background-color: #999;
}
.tab.active {
  padding: 4px 22px;
}

</style>
