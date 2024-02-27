import { DataFrame } from "../data_frame.js";

class COPRASDataFrame extends DataFrame {
  constructor(init_row, init_col, container) {
    super(init_row, init_col);
    this.methodName = "copras";
    this.renderTo(container);
  }
}

window.onload = () => {
  let df = new COPRASDataFrame(5, 5, document.getElementById("content"));
};