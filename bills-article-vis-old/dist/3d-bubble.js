const defaultLimit = 32;
// setup controls
// const satInput = document.querySelector("#sat");
// const lumInput = document.querySelector("#lum");
// const limitSelect = document.querySelector("#limit");
// const shuffleSelect = document.querySelector("#shuffle");
const options = [
  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
  23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
];
// options.forEach((val, i) => (limitSelect.options[i] = new Option(val)));
// limitSelect.selectedIndex = defaultLimit - 1;
// const bgSelect = document.querySelector("#bg");
// bgSelect.selectedIndex = 0;
// limitSelect.addEventListener("change", execute);
// bgSelect.addEventListener("change", execute);
// shuffleSelect.addEventListener("change", render);

function execute() {
  document.querySelector("#chart").innerHTML = "";

  fetch("http://localhost:3000/bills/themed-bills")
    .then(function (response) {
      // The API call was successful!
      return response.json();
    })
    .then(function (data) {
      // This is the JSON from our response
      // console.log(data);
      render(data);
    })
    .catch(function (err) {
      // There was an error
      console.warn("Something went wrong.", err);
    });
}

function render(jsonChildren) {
  let idx = 0;
  // const limit = limitSelect.selectedIndex + 1;
  const limit = 32;
  // const bgColor = bgSelect.options[bgSelect.selectedIndex].value;
  const bgColor = "#e0e0e0";
  // const doShuffle = shuffleSelect.selectedIndex === 1;
  const doShuffle = false;
  document.querySelector("#chart").innerHTML = "";

  const json = { children: jsonChildren.slice(0, limit) };

  if (doShuffle) {
    json.children = _.shuffle(json.children);
  }

  const values = json.children.map((d) => d.value);
  const min = Math.min.apply(null, values);
  const max = Math.max.apply(null, values);
  const total = json.children.length;

  document.body.style.backgroundColor = bgColor;

  const DIAMETER = 600;
  // color = d3.scaleOrdinal(d3.schemeCategory20c);

  const bubble = d3.pack().size([DIAMETER, DIAMETER]).padding(0);

  function darkenColor(color, factor) {
    return d3.color(color).darker(factor);
  }

  const colorScale = d3.interpolateRainbow;
  const colorBubble = (index, length) => {
    let ratio = index / (length - 1.0);
    return darkenColor(colorScale(ratio), 0.2);
  };

  const tip = d3
    .tip()
    .attr("class", "d3-tip-outer")
    .offset([-38, 0])
    .html((d, i) => {
      const item = json.children[i];
      // const color = getColor(i, values.length);
      const color = colorBubble(i, json.children.length);
      return `<div class="d3-tip" style="background-color: ${color}">${item.name} (${item.value})</div><div class="d3-stem" style="border-color: ${color} transparent transparent transparent"></div>`;
    });

  const margin = {
    left: 25,
    right: 25,
    top: 25,
    bottom: 25,
  };

  const svg = d3
    .select("#chart")
    .append("h3").html(`<div style="text-align:center;">Quantidade de Projetos de Lei elaborados por tema</div>`)
    .append("svg")
    .attr("viewBox", "0 0 " + (DIAMETER + margin.right) + " " + DIAMETER)
    .attr("width", DIAMETER + margin.right)
    .attr("height", DIAMETER)
    .attr("class", "chart-svg");

  const root = d3.hierarchy(json).sum(function (d) {
    return d.value;
  });

  bubble(root);

  const node = svg
    .selectAll(".node")
    .data(root.children)
    .enter()
    .append("g")
    .attr("class", "node")
    .attr("transform", function (d) {
      return "translate(" + d.x + " " + d.y + ")";
    })
    .append("g")
    .attr("class", "graph");

  node
    .append("circle")
    .attr("r", function (d) {
      return d.r;
    })
    // .style("fill", getItemColor)
    .style("fill", (d,i) => colorBubble(i, json.children.length))
    .on("mouseover", tip.show)
    .on("mouseout", tip.hide);

  node.call(tip);

  node
    .append("text")
    .attr("dy", "0.2em")
    .style("text-anchor", "middle")
    .style("font-family", "Roboto")
    .style("font-size", getFontSizeForItem)
    .text(getLabel)
    .style("fill", "#ffffff")
    .style("pointer-events", "none");

  node
    .append("text")
    .attr("dy", "1.3em")
    .style("text-anchor", "middle")
    .style("font-family", "Roboto")
    .style("font-weight", "100")
    .style("font-size", getFontSizeForItem)
    .text(getValueText)
    .style("fill", "#ffffff")
    .style("pointer-events", "none");

  node.on("click", (d) => {
    executeSankey(d.data.cod);
    setTimeout(function(){
      executeChord(d.data.cod);
    }, 2000);
    
  });

  function getLabel(item) {
    // if (item.data.value < max / 3.3) {
    // if (item.data.value < max / 50) {
    //   return "";
    // }
    return truncate(item.data.name);
  }

  function getValueText(item) {
    // if (item.data.value < max / 3.3) {
    if (item.data.value < max / 50) {
      return "";
    }
    return item.data.value;
  }

  function truncate(label) {
    const max = 11;
    if (label.length > max) {
      label = label.slice(0, max) + "...";
    }
    return label;
  }

  function getFontSizeForItem(item) {
    return getFontSize(item.data.value, min, max);
  }

  function getFontSize(value, min, max) {
    const minPx = 6;
    const maxPx = 30;
    const pxRange = maxPx - minPx;
    const dataRange = max - min;
    const ratio = pxRange / dataRange;
    const size = Math.min(maxPx, Math.round(value * ratio) + minPx);
    return `${size}px`;
  }
}

execute();
