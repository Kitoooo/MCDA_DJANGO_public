import { DataFrame } from "../data_frame.js";

class TOPSISDataFrame extends DataFrame {
  constructor(init_row, init_col, container) {
    super(init_row, init_col);
    this.methodName = "topsis";
    this.renderTo(container);
  }
}

window.onload = () => {
  let df = new TOPSISDataFrame(5, 5, document.getElementById("content"));
};