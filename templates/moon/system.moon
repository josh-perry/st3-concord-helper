System = require("{systems_path}")

{component_requires}

system = System({component_list})

system.{system_callback} = =>
  for i = 1, @pool.size do
    e = @pool\get(i)

return system