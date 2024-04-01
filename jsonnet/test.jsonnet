local datasets = {
  remote: {
    path: 234,
  },
  'local': {
    path: 123,
  },
};


function(place) {
  dataset: datasets[place],
  batch_size: {
    'local': 32,
    remote: 64,
  }[place],
  place: place,
}
