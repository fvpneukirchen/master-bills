function executeTable(theme, party) {
  fetch(`http://localhost:3000/bills/themed-bills/${theme}/parties/${party}`)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      document.querySelector("#table").innerHTML = "";
      updateTable(data);
    })
    .catch(function (err) {
      console.warn("Something went wrong.", err);
    });
}

function updateTable(data) {
  // const header = d3cloud.select("#table").append("div").attr("class", "well");
  // header.append("h3").text("Dynamic d3cloud Array of Tables Demo");

  // Container for array of tables
  const tableDiv = d3cloud
    .select("#table")
    .append("div")
    .attr("id", "tableContainer");

  // Select all divs in the table div, and then apply new data
  const divs = tableDiv
    .selectAll("div")
    // After .data() is executed below, divs becomes a d3cloud update selection
    .data(data, (d) => d.id);

  // Use the exit method of the d3cloud update selection to remove any deleted table div and contents (which would be absent in the data array just applied)
  divs.exit().remove();

  // Use the enter metod of the d3cloud update selection to add new ('entering') items present in the
  // data array just applied
  const divsEnter = divs
    .enter()
    .append("div")
    .attr("id", (d) => `${d.id}-Div`)
    .attr("class", "well");

  // Add title in new div(s)
  divsEnter.append("h5").text((d) => d.ementa);


  divs.selectAll("h5")
  .append("span").html("<br>")
  .append("a")
  .attr("href", (d) => d.url)
  .html((d) => `<br>${d.table}`);
  // .text((d) => ` ${d.table}`);
  // .text()
  // .append("br")
  // // .text((d) => d.ementa)
  // .text((d) => d.ementa);

  // Add table in new div(s)
  const tableEnter = divsEnter
    .append("table")
    .attr("id", (d) => d.id)
    .attr("class", "table table-condensed table-striped table-bordered");

  // Append table head in new table(s)
  tableEnter
    .append("thead")
    .append("tr")
    .selectAll("th")
    // Table column headers (here constant, but could be made dynamic)
    .data(["Nome", "Ordem"])
    .enter()
    .append("th")
    .text((d) => d);

  // Append table body in new table(s)
  tableEnter.append("tbody");

  // Select all tr elements in the divs update selection
  const tr = divs
    .select("table")
    .select("tbody")
    .selectAll("tr")
    // After the .data() is executed below, tr becomes a d3cloud update selection
    .data(
      (d) => d.rows, // Return inherited data item
      (d) => d.nome // 'key' function to disable default by-index evaluation
    );

  // Use the exit method of the update selection to remove table rows without associated data
  tr.exit().remove();

  // Use the enter method to add table rows corresponding to new data
  tr.enter().append("tr");

  // Bind data to table cells (td becomes update selection)
  const td = tr
    .selectAll("td")
    // After the .data() is executed below, the td becomes a d3cloud update selection
    .data((d) => {
      return d3cloud.values(d);
    }); // return inherited data item

  // Use the enter method of the update selection to add td elements
  td.enter().append("td");

  // Use the update selection to add/change the table cell text
  td.text((d) => d);
}