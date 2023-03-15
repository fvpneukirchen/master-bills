function executeChord(code) {
  fetch(`http://localhost:3000/bills/themed-bills/${code}/co-authors`)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data && data.length > 0) {
        document.querySelector("#chord").innerHTML = "";
        renderChord(data);
      } else {
        document.querySelector("#chord").innerHTML = "";
      }
    })
    .catch(function (err) {
      console.warn("Something went wrong.", err);
    });
}

const hierarchy = (data, delimiter = ".") => {
  let root;
  const map = new Map();
  data.forEach(function find(data) {
    const { name } = data;
    if (map.has(name)) return map.get(name);
    const i = name.lastIndexOf(delimiter);
    map.set(name, data);
    if (i >= 0) {
      find({ name: name.substring(0, i), children: [] }).children.push(data);
      data.name = name.substring(i + 1);
    } else {
      root = data;
    }
    return data;
  });
  return root;
};
const id = (node) => {
  return `${node.parent ? id(node.parent) + "." : ""}${node.data.name}`;
};

const party = (node) => {
  return id(node).split(".")[1];
};

function renderChord(dataEntry) {
  const data = hierarchy(dataEntry);
  function darkenColor(color, factor) {
    return d3.color(color).darker(factor);
  }

  const colorScale = d3.interpolateRainbow;
  const colorChord = (index, length) => {
    let ratio = index / (length - 1.0);
    return darkenColor(colorScale(ratio), 0.5);
  };

  const width = 954;
  const radius = width / 2.5;

  const colornone = "#ccc";
  const colorin = "#00f";
  const colorout = "#f00";

  const tree = unpkgd3v6.cluster().size([2 * Math.PI, radius - 100]);
  const line = unpkgd3v6
    .lineRadial()
    .curve(unpkgd3v6.curveBundle.beta(0.85))
    .radius((d) => d.y)
    .angle((d) => d.x);

  const bilink = (root) => {
    const map = new Map(root.leaves().map((d) => [id(d), d]));
    for (const d of root.leaves())
      (d.incoming = []),
        (d.outgoing = d.data.imports.map((i) => [d, map.get(i)]));
    for (const d of root.leaves())
      for (const o of d.outgoing) o[1].incoming.push(o);
    return root;
  };

  const root = tree(
    bilink(
      unpkgd3v6
        .hierarchy(data)
        .sort(
          (a, b) =>
            unpkgd3v6.ascending(a.height, b.height) ||
            unpkgd3v6.ascending(a.data.name, b.data.name)
        )
    )
  );

  const svg = unpkgd3v6
    .select("#chord")
    .append("svg")
    .attr("viewBox", [-width / 1.75, -width / 1.75, width , width]);

  const parties = Array.from(new Set(root.leaves().map((leaf) => party(leaf))));

  // console.log(parties);

  const node = svg
    .append("g")
    .attr("font-family", "sans-serif")
    .attr("font-size", 10)
    .selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr(
      "transform",
      (d) => `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`
    )
    .append("text")
    .attr("dy", "0.31em")
    .attr("x", (d) => (d.x < Math.PI ? 6 : -6))
    .attr("text-anchor", (d) => (d.x < Math.PI ? "start" : "end"))
    .attr("transform", (d) => (d.x >= Math.PI ? "rotate(180)" : null))
    .style("fill", (d) => {
      const p = party(d);
      const pIndex = parties.findIndex((item) => item === p);
      const color = colorChord(pIndex, parties.length);
      return color;
    })
    .text((d) => `${party(d)} - ${d.data.fullName}`)
    .each(function (d) {
      d.text = this;
    })
    .on("mouseover", overed)
    .on("mouseout", outed)
    .call((text) =>
      text.append("title").text(
        (d) => `${party(d)} - ${d.data.fullName}
  ${d.outgoing.length} vezes coautor(a)
  ${d.incoming.length} deputados(as) são coautores`
      )
    );

  const link = svg
    .append("g")
    .attr("stroke", colornone)
    .attr("fill", "none")
    .selectAll("path")
    .data(root.leaves().flatMap((leaf) => leaf.outgoing))
    .join("path")
    .style("mix-blend-mode", "multiply")
    .attr("d", ([i, o]) => line(i.path(o)))
    .each(function (d) {
      d.path = this;
    });

  function overed(event, d) {
    link.style("mix-blend-mode", null);
    unpkgd3v6.select(this).attr("font-weight", "bold");
    unpkgd3v6
      .selectAll(d.incoming.map((d) => d.path))
      .attr("stroke", colorin)
      .raise();
    unpkgd3v6
      .selectAll(d.incoming.map(([d]) => d.text))
      .attr("fill", colorin)
      .attr("font-weight", "bold");
    unpkgd3v6
      .selectAll(d.outgoing.map((d) => d.path))
      .attr("stroke", colorout)
      .raise();
    unpkgd3v6
      .selectAll(d.outgoing.map(([, d]) => d.text))
      .attr("fill", colorout)
      .attr("font-weight", "bold");
  }

  function outed(event, d) {
    link.style("mix-blend-mode", "multiply");
    unpkgd3v6.select(this).attr("font-weight", null);
    unpkgd3v6.selectAll(d.incoming.map((d) => d.path)).attr("stroke", null);
    unpkgd3v6
      .selectAll(d.incoming.map(([d]) => d.text))
      .attr("fill", null)
      .attr("font-weight", null);
    unpkgd3v6.selectAll(d.outgoing.map((d) => d.path)).attr("stroke", null);
    unpkgd3v6
      .selectAll(d.outgoing.map(([, d]) => d.text))
      .attr("fill", null)
      .attr("font-weight", null);
  }

  // return svg.node();
}