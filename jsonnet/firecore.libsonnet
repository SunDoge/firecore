{
  linkedList(cfg)::
    local keys = std.objectFields(cfg);
    local nexts = [cfg[k].next for k in keys];
    local head = std.setDiff(keys, nexts)[0];
    local f(curr) = if cfg[curr].next != null then [cfg[curr]] + f(cfg[curr].next) else [cfg[curr]];
    f(head)
  ,

  abc: self.linkedList({
    d: { name: 'd', next:: null },
    a: { name: 'a', next:: 'b' },
    b: { name: 'b', next:: 'c' },
    c: { name: 'c', next:: 'd' },
  }),
}
