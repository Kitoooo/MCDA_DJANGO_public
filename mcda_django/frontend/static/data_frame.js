export class InputField {
  constructor(type, name, className) {
    this.type = type;
    this.name = name;
    this.className = className;
  }
  create() {
    let input = document.createElement("input");
    input.type = this.type;
    input.name = this.name;
    input.className = this.className;
    return input;
  }
}
export class TypeInputField extends InputField {
  constructor(name) {
    super("checkbox", name, "form-control");
  }
}
export class WeightInputField extends InputField {
  constructor(name) {
    super("number", name, "form-control");
  }
}
export class DataInputField extends InputField {
  constructor(name) {
    super("number", name, "form-control");
  }
}
class FileInputField extends InputField {
  constructor(name, onchange) {
    super("file", name, "form-control-file");
    this.onchange = onchange;
  }
  create() {
    let input = document.createElement("input");
    input.type = this.type;
    input.name = this.name;
    input.className = this.className;
    input.addEventListener("change", this.onchange);
    return input;
  }
}
class DataFrameManipulationButton {
  constructor(className, text, onclick) {
    this.className = className;
    this.text = text;
    this.onclick = onclick;
  }
  create() {
    let button = document.createElement("button");
    button.type = "button";
    button.className = this.className;
    button.innerText = this.text;
    button.addEventListener("click", this.onclick);
    return button;
  }
}

class DataFrameManipulationButtonGroup {
  constructor(text, buttons) {
    this.text = text;
    this.buttons = buttons;
  }
  create() {
    let container = document.createElement("div");
    container.className = "d-flex align-items-center mr-3 pl-2 mb-2";
    let title = document.createElement("span");
    title.innerText = this.text;
    title.className = "h5 mb-0 mr-2";
    container.appendChild(title);

    let buttonGroup = document.createElement("div");
    buttonGroup.className = "btn-group";
    buttonGroup.role = "group";
    this.buttons.forEach((button) => {
      buttonGroup.appendChild(button.create());
    });
    container.appendChild(buttonGroup);
    return container;
  }
}

export class DataFrame {
  constructor(init_row, init_col) {
    this.row = init_row < 2 ? 2 : init_row;
    this.col = init_col < 2 ? 2 : init_col;
    this.addCol = this.addCol.bind(this);
    this.delCol = this.delCol.bind(this);
    this.addRow = this.addRow.bind(this);
    this.delRow = this.delRow.bind(this);
    this.uploadFile = this.uploadFile.bind(this);
    this.methodName = undefined;
    this.submitButtonOnClick = this.submitButtonOnClick.bind(this);
    this.url = "http://127.0.0.1:8000/backend/api/";
  }
  _renderTopFrame(parent) {
    //render topFrame container
    let topFrameContainer = document.createElement("div");
    topFrameContainer.className = "d-flex flex-wrap sticky-top pt-1 bg-white";
    parent.appendChild(topFrameContainer);

    // Render the 2 button groups for rows and columns manipulation
    let rowBtns = new DataFrameManipulationButtonGroup("Rows", [
      new DataFrameManipulationButton("btn btn-danger", "-", this.delRow),
      new DataFrameManipulationButton("btn btn-success", "+", this.addRow),
    ]);
    topFrameContainer.appendChild(rowBtns.create());

    let colBtns = new DataFrameManipulationButtonGroup("Columns", [
      new DataFrameManipulationButton("btn btn-danger", "-", this.delCol),
      new DataFrameManipulationButton("btn btn-success", "+", this.addCol),
    ]);
    topFrameContainer.appendChild(colBtns.create());

    // Render file input field
    let fileInputContrainer = document.createElement("div");
    fileInputContrainer.className = "d-flex align-items-center mr-3 pl-2 mb-2";
    topFrameContainer.appendChild(fileInputContrainer);

    let fileUploadButton = new DataFrameManipulationButton(
      "btn btn-primary mr-3",
      "Upload",
      this.uploadFile
    ).create();
    fileUploadButton.disabled = true;
    fileInputContrainer.appendChild(fileUploadButton);

    this.fileInput = new FileInputField("file", (e) => {
      e.target.files[0]
        ? (fileUploadButton.disabled = false)
        : (fileUploadButton.disabled = true);
    }).create();
    fileInputContrainer.appendChild(this.fileInput);
  }

  _renderDataTable(parent) {
    // Render the table
    this.table = document.createElement("table");
    this.table.className = "table-responsive-sm table-bordered";
    parent.appendChild(this.table);

    // Render the table head
    let thead = document.createElement("thead");
    this.table.appendChild(thead);

    // Render the column headers
    let trHead = document.createElement("tr");
    thead.appendChild(trHead);
    for (let i = 0; i < this.col + 1; i++) {
      let th = document.createElement("th");
      th.scope = "col";
      th.contentEditable = true;
      i != 0 ? (th.innerText = `Cri-${i}`) : "";
      trHead.appendChild(th);
    }

    //Render the table body
    this.tbody = document.createElement("tbody");
    this.table.appendChild(this.tbody);

    //Render the types row
    let trTypes = document.createElement("tr");
    this.tbody.appendChild(trTypes);
    let thTypes = document.createElement("th");
    thTypes.scope = "row";
    thTypes.innerText = "Cost";
    trTypes.appendChild(thTypes);
    for (let i = 0; i < this.col; i++) {
      let td = document.createElement("td");
      let input = new TypeInputField("type");
      td.appendChild(input.create());
      trTypes.appendChild(td);
    }

    //Render the weights row
    let trWeights = document.createElement("tr");
    trWeights.id = "weights-row";
    this.tbody.appendChild(trWeights);
    let thWeights = document.createElement("th");
    thWeights.scope = "row";
    thWeights.innerText = "Weights";
    trWeights.appendChild(thWeights);
    for (let i = 0; i < this.col; i++) {
      let td = document.createElement("td");
      let input = new WeightInputField("weight");
      td.appendChild(input.create());
      trWeights.appendChild(td);
    }

    //Render the data rows
    for (let i = 0; i < this.row; i++) {
      let trData = document.createElement("tr");
      this.tbody.appendChild(trData);
      let thData = document.createElement("th");
      thData.scope = "row";
      thData.innerText = `Alt-${i + 1}`;
      thData.contentEditable = true;
      trData.appendChild(thData);

      for (let j = 0; j < this.col; j++) {
        let td = document.createElement("td");
        let input = new DataInputField("data");
        td.appendChild(input.create());
        trData.appendChild(td);
      }
    }
  }

  _renderBottomFrame(parent) {
    // Render the bottom frame
    let bottomFrameContainer = document.createElement("div");
    bottomFrameContainer.className =
      "d-flex pt-1 align-items-center justify-content-start";
    parent.appendChild(bottomFrameContainer);

    // Render result container
    this.resultContainer = document.createElement("div");
    parent.appendChild(this.resultContainer);

    // Render the submit button
    let submitButton = new DataFrameManipulationButton(
      "btn btn-primary mt-1 mb-1",
      "Submit",
      this.submitButtonOnClick
    ).create();
    bottomFrameContainer.appendChild(submitButton);
  }
  renderTo(parent_container) {
    // Render the container
    let dfContainer = document.createElement("div");
    dfContainer.className = "container";
    parent_container.appendChild(dfContainer);

    // Render the top frame
    this._renderTopFrame(dfContainer);

    // Render the data table
    this._renderDataTable(dfContainer);

    // Render the bottom frame
    this._renderBottomFrame(dfContainer);
  }

  addRow() {
    this.row++;
    let trData = document.createElement("tr");
    this.tbody.appendChild(trData);
    let thData = document.createElement("th");
    thData.scope = "row";
    thData.innerText = `Alt-${this.row}`;
    trData.appendChild(thData);

    for (let j = 0; j < this.col; j++) {
      let td = document.createElement("td");
      let input = new DataInputField("data");
      td.appendChild(input.create());
      trData.appendChild(td);
    }
  }

  delRow() {
    if (this.row > 2) {
      this.row--;
      this.tbody.removeChild(this.tbody.lastChild);
    }
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

    for (let i = 0; i < this.row; i++) {
      let trData = this.tbody.querySelector(`tr:nth-child(${i + 3})`);
      td = document.createElement("td");
      input = new DataInputField("data");
      td.appendChild(input.create());
      trData.appendChild(td);
    }
  }

  delCol() {
    if (this.col > 2) {
      this.col--;
      this.table.querySelector("thead tr").removeChild(this.table.querySelector("thead tr").lastChild);
      this.table.querySelectorAll("tbody tr").forEach((tr) => {
        tr.removeChild(tr.lastChild);
      });
    }
  }
  getTypes() {
    return Array.from(
      this.tbody.querySelectorAll("tr:first-child td input")
    ).map((input) => (input.checked ? -1 : 1));
  }

  getWeights() {
    return Array.from(
      this.tbody.querySelectorAll("tr:nth-child(2) td input")
    ).map((input) => parseFloat(input.value) || 0);
  }

  getData() {
    return Array.from(this.tbody.querySelectorAll("tr:nth-child(n+3)")).map(
      (tr) =>
        Array.from(tr.querySelectorAll("td input")).map(
          (input) => parseFloat(input.value) || 0
        )
    );
  }

  getJSONdata() {
    // Constructing the JSON object
    let json = {
      types: this.getTypes(),
      weights: this.getWeights(),
      data: this.getData(),
      meta: {
        criteries: this.col,
        alternatives: this.row,
      },
    };
    return json;
  }

  getCSVData() {
    // Array to hold each row's data
    let csvRows = [];

    // Add types (benefit/cost) row
    let types = Array.from(
      this.tbody.querySelectorAll("tr:first-child td input")
    ).map((input) => (input.checked ? -1 : 1));
    csvRows.push(types.join(","));

    // Add weights row
    let weights = Array.from(
      this.tbody.querySelectorAll("tr:nth-child(2) td input")
    ).map((input) => input.value);
    csvRows.push(weights.join(","));

    // Add data rows (input fields from the third row onwards)
    let dataRows = Array.from(
      this.tbody.querySelectorAll("tr:nth-child(n+3)")
    ).map((tr) =>
      Array.from(tr.querySelectorAll("td input"))
        .map((input) => input.value)
        .join(",")
    );
    csvRows = csvRows.concat(dataRows);

    // Convert array of rows into a single CSV string
    let csvString = csvRows.join("\n");

    return csvString;
  }

  uploadFile() {
    let inputFile = this.fileInput;
    let file = inputFile.files[0];
    let reader = new FileReader();
    reader.readAsText(file);
    reader.onload = () => {
      let data = reader.result;
      this.sendToApi(data, (status, response) => {
        this.responseManager(status, response);
      });
    };
    reader.onerror = function () {
      console.log(reader.error);
    };
  }

  sendToApi(data, callback) {
    let url = this.url + this.methodName;
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "text/csv");
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        callback(xhr.status, xhr.responseText);
      }
    };
    xhr.send(data);
  }

  submitButtonOnClick() {
    let data = this.getCSVData();
    this.sendToApi(data, (status, response) => {
      this.responseManager(status, response);
    });
  }

  responseManager(status, response) {
    //clear the result container
    this.resultContainer.innerHTML ="";
    //parse the response
    response = JSON.parse(response);
    if (status === 200) {
      // render the result table
      this.resultContainer.className = "alert alert-success d-flex";
      let table = document.createElement("table");
      table.className = "table table-responsive-sm table-bordered";
      this.resultContainer.appendChild(table);

      let thead = document.createElement("thead");
      table.appendChild(thead);

      let trHead = document.createElement("tr");
      thead.appendChild(trHead);
      let thAlts = document.createElement("th");
      thAlts.scope = "col";
      trHead.appendChild(thAlts);

      //render the column headers
      for (let i = 0; i < response.alts_number; i++) {
        let thAlts = document.createElement("th");
        thAlts.scope = "col";
        thAlts.innerText = `Alt-${i + 1}`;
        trHead.appendChild(thAlts);
      }

      let tbody = document.createElement("tbody");
      table.appendChild(tbody);

      let trPreferences = document.createElement("tr");
      tbody.appendChild(trPreferences);
      let th = document.createElement("th");
      th.scope = "row";
      th.innerText = "Preferences";
      trPreferences.appendChild(th);

      //render the preferences row values
      for (let i = 0; i < response.preferences.length; i++) {
        let td = document.createElement("td");
        td.innerText = response.preferences[i].toFixed(3);
        trPreferences.appendChild(td);
      }

      let trRanks = document.createElement("tr");
      tbody.appendChild(trRanks);
      th = document.createElement("th");
      th.scope = "row";
      th.innerText = "Ranks";
      trRanks.appendChild(th);
      
      //render the ranks row values
      for (let i = 0; i < response.ranks.length; i++) {
        let td = document.createElement("td");
        td.innerText = response.ranks[i];
        trRanks.appendChild(td);
      }
    }
    if (status === 400) {
      this.resultContainer.innerHTML = response.message;
      this.resultContainer.className = "alert alert-danger";
    }
  }
}
