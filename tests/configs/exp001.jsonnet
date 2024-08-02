{
  shared: {
    max_epochs: 100,
  },
  train: {
    engine: {
      max_epochs: 'ref:max_epochs',
      output_dir: 'ref:output_dir',
    },
  },
  val: {
    engine: {
      max_epochs: 'ref:max_epochs',
      output_dir: 'ref:output_dir',
    },
  },
}
