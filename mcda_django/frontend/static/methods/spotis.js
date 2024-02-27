import { DataFrame, InputField, DataInputField, WeightInputField, TypeInputField } from "../data_frame.js";

class BoundInputField extends InputField {
  constructor(name,placeholder) {
    super("number", name, "form-control");
    this.placeholder = placeholder;
  }
  create() {
    let input = super.create();
    input.placeholder = this.placeholder;
    return input;
  }
}

class SPOTISDataFrame extends DataFrame {
  constructor(init_row, init_col, container) {
    super(init_row, init_col);
    this.methodName = "spotis";
    this.renderTo(container);
  }
  _renderDataTable(parent){
    super._renderDataTable(parent);

    const trBounds = this.table.insertRow(3);
    trBounds.id = "bounds-row"; 
    const thBounds = document.createElement("th");
    thBounds.scope = "row";
    thBounds.innerText = "Bounds";
    trBounds.appendChild(thBounds);

    for (let i = 0; i < this.col; i++) {
      trBounds.appendChild(this.#createBoundsCell());
    }
  }
  #createBoundsCell(){
    let td = document.createElement("td");
    const lowerBoundInput = new BoundInputField("bound","lower");
    const upperBoundInput = new BoundInputField("bound","upper");
    td.appendChild(lowerBoundInput.create());
    td.appendChild(upperBoundInput.create());
    return td;
  }
  addCol() {
    this.col++;
    let thead = this.table.querySelector("thead");
    let trHead = thead.querySelector("tr");
    let th = document.createElement("th");
    th.scope = "col";
    th.innerText = `Cri-${this.col}`;
    trHead.appendChild(th);

    let trTypes = this.tbody.querySelector("tr");
    let td = document.createElement("td");
    let input = new TypeInputField("type");
    td.appendChild(input.create());
    trTypes.appendChild(td);

    let trWeights = this.tbody.querySelector("#weights-row");
    td = document.createElement("td");
    input = new WeightInputField("weight");
    td.appendChild(input.create());
    trWeights.appendChild(td);

    let trBounds = this.tbody.querySelector("#bounds-row");
    td = this.#createBoundsCell();
    trBounds.appendChild(td);

    for (let i = 0; i < this.row; i++) {
      let trData = this.tbody.querySelector(`tr:nth-child(${i + 4})`);
      td = document.createElement("td");
      input = new DataInputField("data");
      td.appendChild(input.create());
      trData.appendChild(td);
    }
  }
}

window.onload = () => {
  let df = new SPOTISDataFrame(5, 5, document.getElementById("content"));
};