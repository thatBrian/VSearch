$(document).ready(function() {
  // constant variables
  // use underline to diff from d3js name
  var svg_height = 500,
    svg_width = 960,
    max_circle_radius = 60,
    link_distance = 200,
    charge_force_strength = -500;

  var main_node_id = 'red';
  change_title();
  function change_title() {
    console.log(document.getElementById('main-node-name'));
    document.getElementById('main-node-name').innerText = main_node_id;
  }
  // initialize svg element
  var svg = d3
    .select('svg')
    .attr('width', svg_width)
    .attr('height', svg_height);

  // size scale from 1 to 10
  var size_scale_func = d3
    .scaleLinear()
    .domain([0, 10])
    .range([0, max_circle_radius]);

  var color_scale_func = d3.scaleSequential(d3.interpolateCool).domain([0, 10]);

  // create force simulation
  var simulation = d3
    .forceSimulation()
    .force('charge', d3.forceManyBody().strength(charge_force_strength))
    .force(
      'link',
      d3
        .forceLink()
        .id(function(d) {
          return d.id;
        })
        .distance(link_distance)
    )
    .force('center', d3.forceCenter(svg_width / 2, svg_height / 2))
    .on('tick', ticked);

  // create group container
  var group = svg
    .append('g')
    .attr('height', svg_height)
    .attr('width', svg_width);

  // intialize elements on group
  var link = group.selectAll('.link'),
    node = group.selectAll('.node'),
    text = group.selectAll('.text');

  // binding data to elements
  axios.get('http://localhost:3000').then(function(res) {
    console.log(res);
  });
  d3.json('./graph.json', function(error, graph) {
    if (error) throw error;

    simulation.nodes(graph.nodes);
    simulation.force('link').links(graph.links);

    link = link
      .data(graph.links)
      .enter()
      .append('line')
      .attr('class', 'link');

    node = node
      .data(graph.nodes)
      .enter()
      .append('circle')
      .attr('class', 'node')
      .attr('r', function(d) {
        return size_scale_func(d.size);
      })
      .style('fill', function(d) {
        return color_scale_func(d.size);
      })
      .call(drag)
      .on('click', function(d) {
        d3.event.preventDefault();
        main_node_id = d.id;
        change_title();
        // d3.select(this)
        //   .transition()
        //   .delay(100)
        console.log('node clicked');
      });

    text = text
      .data(graph.nodes)
      .enter()
      .append('text')
      .attr('class', 'colorName')
      .attr('fill', 'black')
      .text(function(d) {
        return d.id;
      });
  });

  var drag = d3
    .drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended);

  function dragstarted() {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    if (d3.event.subject.id != main_node_id) {
      d3.event.subject.fx = d3.event.subject.x;
      d3.event.subject.fy = d3.event.subject.y;
    }
  }

  function dragged() {
    if (d3.event.subject.id != main_node_id) {
      d3.event.subject.fx = d3.event.x;
      d3.event.subject.fy = d3.event.y;
    }
  }

  function dragended() {
    if (!d3.event.active) simulation.alphaTarget(0);
    if (d3.event.subject.id != main_node_id) {
      d3.event.subject.fx = null;
      d3.event.subject.fy = null;
    }
  }

  svg.call(
    d3
      .zoom()
      .scaleExtent([1 / 2, 4])
      .on('zoom', zoomed)
  );

  function zoomed() {
    group.attr('transform', d3.event.transform);
  }

  // updating elements position
  function ticked() {
    link
      .attr('x1', function(d) {
        if (d.source.id != main_node_id) {
          return d.source.x;
        } else {
          return svg_width / 2;
        }
      })
      .attr('y1', function(d) {
        if (d.source.id != main_node_id) {
          return d.source.y;
        } else {
          return svg_height / 2;
        }
      })
      .attr('x2', function(d) {
        if (d.target.id != main_node_id) {
          return d.target.x;
        } else {
          return svg_width / 2;
        }
      })
      .attr('y2', function(d) {
        if (d.target.id != main_node_id) {
          return d.target.y;
        } else {
          return svg_height / 2;
        }
      });

    node
      .attr('cx', function(d) {
        if (d.id !== main_node_id) {
          return d.x;
        } else {
          return svg_width / 2;
        }
      })
      .attr('cy', function(d) {
        if (d.id !== main_node_id) {
          return d.y;
        } else {
          return svg_height / 2;
        }
      });

    text
      .attr('x', function(d) {
        if (d.id !== main_node_id) {
          return d.x;
        } else {
          return svg_width / 2;
        }
      })
      .attr('y', function(d) {
        if (d.id !== main_node_id) {
          return d.y;
        } else {
          return svg_height / 2;
        }
      });
  }
});
