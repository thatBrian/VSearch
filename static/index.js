$(document).ready(function() {
  var wiki_api_url =
    'https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&origin=*&search=';

  $('#search-form').submit(function(e) {
    e.preventDefault();
    console.log('search is called');
    var key_word = $('#search-input').val();
    var the_right_url = '';
    console.log(key_word);
    axios
      .get(wiki_api_url + key_word)
      .then(function(res) {
        the_right_url = res.data[3][0];
        var parsed = the_right_url.split('/');
        console.log(parsed[parsed.length - 1]);
        key_word = parsed[parsed.length - 1];
      })
      .then(function() {
        window.location = '/' + key_word;
      })
      .catch(function(err) {
        console.error(err);
      });
  });

  function change_img_src(main_node_title) {
    console.log(main_node_title);
    var gif_url = '';
    axios
      .get(
        'http://api.giphy.com/v1/gifs/search?api_key=RFiB4YCStEOA66u90FArIPVPXSgD8NV4&limit=1&q=' +
          main_node_title
      )
      .then(function(res) {
        console.log(res.data.data[0].images.preview_gif.url);
        gif_url = res.data.data[0].images.preview_gif.url;
        console.log(gif_url);
      })
      .then(function() {
        $('.card-img-top').attr('src', gif_url);
      })
      .catch(function(err) {
        console.error(err);
      });
  }
  // constant variables
  // use underline to diff from d3js name
  var svg_height = 700,
    svg_width = 1200,
    max_circle_radius = 100,
    link_distance = 400,
    charge_force_strength = -3000;

  var main_node_id = 'red';
  var main_node_title = 'red';
  var main_node_url = '';
  function change_title() {
    console.log(document.getElementById('main-node-name'));
    document.getElementById('main-node-name').innerText = main_node_title;
    change_img_src(main_node_title);
    axios
      .get(wiki_api_url + main_node_title)
      .then(function(res) {
        main_node_description = res.data[2][0];
        main_node_title = res.data[1][0];
        main_node_url = res.data[3][0];
        var parsed = main_node_url.split('/');
      })
      .then(function(parsed) {
        $('#card-content').text(main_node_description);
        var parsed = main_node_url.split('/');
        $('#card-btn').attr('href', parsed[parsed.length - 1]);
      })
      .catch(function(err) {
        console.error(err);
      });
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

  // // binding data to elements
  // axios.get('http://localhost:3000/search/Train').then(function(res) {
  //   console.log(res);
  // });
  var main_node_description = '';
  d3.json('./data.json', function(error, graph) {
    if (error) throw error;

    main_node_id = graph.id;
    main_node_title = graph.title;

    change_title();

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
        main_node_title = d.title;
        simulation.alpha(1);
        change_title();
        console.log('node clicked');
      });

    text = text
      .data(graph.nodes)
      .enter()
      .append('text')
      .attr('class', 'colorName')
      .attr('fill', 'black')
      .text(function(d) {
        return d.title;
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
      .scaleExtent([1 / 4, 4])
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
      })
      .style('fill', function(d) {
        if (d.id !== main_node_id) {
          return color_scale_func(d.size);
        } else {
          return 'pink';
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

function searchQuery() {
  console.log(document.getElementById('searchQuery').value);
}
