{
  linkedList(cfg)::
    local keys = std.objectFields(cfg);
    local tail = [k for k in keys if cfg[k].next == null][0];  // string
    local parents = { [cfg[k].next]: k for k in keys if k != tail };  // Map<string, string>
    local f(curr) = if std.objectHas(parents, curr) then f(parents[curr]) + [curr] else [curr];
    local order = f(tail);
    { [k]: cfg[k] for k in order }
  ,

  abc: self.linkedList({
    a: { next:: 'b' },
    b: { next:: 'c' },
    c: { next:: null },
  }),
}
