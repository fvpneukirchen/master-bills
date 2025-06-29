function executeSunburst() {
  fetch(`http://localhost:3000/bills/themed-bills/parties-count`)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      renderSunburst(data);
    })
    .catch(function (err) {
      console.warn("Something went wrong.", err);
    });
}

function renderSunburst(data) {
  const width = 932;
  const radius = width / 6;
  const format = unpkgd3v6.format(",d");
  const color = unpkgd3v6.scaleOrdinal(
    unpkgd3v6.quantize(unpkgd3v6.interpolateRainbow, data.children.length + 1)
  );

  const arc = unpkgd3v6
    .arc()
    .startAngle((d) => d.x0)
    .endAngle((d) => d.x1)
    .padAngle((d) => Math.min((d.x1 - d.x0) / 2, 0.005))
    .padRadius(radius * 1.5)
    .innerRadius((d) => d.y0 * radius)
    .outerRadius((d) => Math.max(d.y0 * radius, d.y1 * radius - 1));

  const partition = (data) => {
    const root = unpkgd3v6
      .hierarchy(data)
      .sum((d) => d.value)
      .sort((a, b) => b.value - a.value);
    return unpkgd3v6.partition().size([2 * Math.PI, root.height + 1])(root);
  };

  const root = partition(data);

  root.each((d) => (d.current = d));

  const svg = unpkgd3v6
    .select("#sunburst")
    .append("svg")
    .attr("viewBox", [0, 0, width, width])
    .style("font", "12px sans-serif");

  const g = svg
    .append("g")
    .attr("transform", `translate(${width / 2},${width / 2})`);

  const path = g
    .append("g")
    .selectAll("path")
    .data(root.descendants().slice(1))
    // .data(root.descendants())
    .join("path")
    .attr("fill", (d) => {
      while (d.depth > 1) d = d.parent;
      return color(d.data.name);
    })
    .attr("fill-opacity", (d) =>
      arcVisible(d.current) ? (d.children ? 0.6 : 0.4) : 0
    )
    .attr("pointer-events", (d) => (arcVisible(d.current) ? "auto" : "none"))

    .attr("d", (d) => arc(d.current));

  path
    // .filter((d) => d.children)
    .style("cursor", "pointer")
    .on("click", clicked);

  path.append("title").text(
    (d) =>
      `${d
        .ancestors()
        .map((d) => d.data.name)
        .reverse()
        .join("/")}\n${format(d.value)}`
  );

  const label = g
    .append("g")
    .attr("pointer-events", "none")
    .attr("text-anchor", "middle")
    .style("user-select", "none")
    .selectAll("text")
    .data(root.descendants().slice(1))
    .join("text")
    .attr("dy", "0.35em")
    .attr("fill-opacity", (d) => +labelVisible(d.current))
    .attr("transform", (d) => labelTransform(d.current))
    .text((d) => d.data.name);

  const parent = g
    .append("circle")
    .datum(root)
    .attr("r", radius)
    .attr("fill", "none")
    .attr("pointer-events", "all")
    .on("click", clicked);

  function clicked(event, p) {
    if (p.depth === 3) {
      const {name, cod} = p.parent.parent.data;
      const next = {
        data: { ...p.data, sigla: p.parent.data.name},
        theme: {
          name, cod
        }
      }
      console.log(next);
    } else {
      parent.datum(p.parent || root);

      root.each(
        (d) =>
          (d.target = {
            x0:
              Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) *
              2 *
              Math.PI,
            x1:
              Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) *
              2 *
              Math.PI,
            y0: Math.max(0, d.y0 - p.depth),
            y1: Math.max(0, d.y1 - p.depth),
          })
      );

      const t = g.transition().duration(750);

      // Transition the data on all arcs, even the ones that aren’t visible,
      // so that if this transition is interrupted, entering arcs will start
      // the next transition from the desired position.
      path
        .transition(t)
        .tween("data", (d) => {
          const i = unpkgd3v6.interpolate(d.current, d.target);
          return (t) => (d.current = i(t));
        })
        .filter(function (d) {
          return +this.getAttribute("fill-opacity") || arcVisible(d.target);
        })
        .attr("fill-opacity", (d) =>
          arcVisible(d.target) ? (d.children ? 0.6 : 0.4) : 0
        )
        .attr("pointer-events", (d) => (arcVisible(d.target) ? "auto" : "none"))

        .attrTween("d", (d) => () => arc(d.current));

      label
        .filter(function (d) {
          return +this.getAttribute("fill-opacity") || labelVisible(d.target);
        })
        .transition(t)
        .attr("fill-opacity", (d) => +labelVisible(d.target))
        .attrTween("transform", (d) => () => labelTransform(d.current));
    }
  }

  function arcVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && d.x1 > d.x0;
  }

  function labelVisible(d) {
    return d.y1 <= 3 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
  }

  function labelTransform(d) {
    const x = (((d.x0 + d.x1) / 2) * 180) / Math.PI;
    const y = (((d.y0 + d.y1) / 2) * radius);
    
    return `rotate(${x - 90}) translate(${y},0) rotate(${x < 180 ? 0 : 180}) `;
  }

  function textIdealLength(len) {
    // (textIdealLength(d.data.name.length))
    // if (len >= 40) return -50;
    // if (len >= 35) return -40;
    // if (len >= 30) return -25;
    // if (len >= 25) return -20;
    return 0;
  }

  // return svg.node();
}

setTimeout(function () {
  executeSunburst();
}, 3000);
